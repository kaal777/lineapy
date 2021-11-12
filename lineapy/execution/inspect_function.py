from __future__ import annotations

import operator
import sys
import types
from dataclasses import dataclass
from typing import Callable, Iterable, Union

import joblib

from lineapy.lineabuiltins import ExternalState, db, file_system, l_list


def inspect_function(
    function: Callable,
    args: list[object],
    kwargs: dict[str, object],
    result: object,
) -> InspectFunctionSideEffects:
    """
    Inspects a function and returns how calling it mutates the args/result and
    creates view relationships between them.
    """
    if function == open:
        yield ImplicitDependencyValue(file_system)
        return

    if function == joblib.dump:
        yield MutatedValue(file_system)
        return
    if imported_module("pandas"):
        import pandas

        if (
            isinstance(function, types.MethodType)
            and function.__name__ == "to_sql"
            and isinstance(function.__self__, pandas.DataFrame)
        ):
            yield MutatedValue(db)
            return

        if (
            isinstance(function, types.FunctionType)
            and function.__name__ == "read_sql"
            and function.__module__ == "pandas.io.sql"
        ):
            yield ImplicitDependencyValue(db)
            return

        if (
            isinstance(function, types.MethodType)
            and function.__name__ == "to_csv"
            and isinstance(function.__self__, pandas.DataFrame)
        ):
            yield MutatedValue(file_system)
            return

        if (
            isinstance(function, types.FunctionType)
            and function.__name__ == "read_csv"
            and function.__module__ == "pandas.io.parsers.readers"
        ):
            yield ImplicitDependencyValue(file_system)
            return

    if imported_module("PIL.Image"):
        from PIL.Image import Image

        if (
            isinstance(function, types.MethodType)
            and function.__name__ == "save"
            and isinstance(function.__self__, Image)
        ):
            yield MutatedValue(file_system)
            return
        if (
            isinstance(function, types.FunctionType)
            and (function.__name__ == "open")
            and (function.__module__ == "PIL.Image")
        ):
            yield ImplicitDependencyValue(file_system)
            return

    if function == setattr:
        # setattr(o, attr, value)
        yield MutatedValue(PositionalArg(0))
        if is_mutable(args[2]):
            yield ViewOfValues(PositionalArg(2), PositionalArg(0))
        return
    if function == getattr:
        # getattr(o, attr)
        if is_mutable(args[0]) and is_mutable(result):
            yield ViewOfValues(PositionalArg(0), Result())
    # TODO: We should probably not use use setitem, but instead get particular
    # __setitem__ for class so we can differentiate based on type more easily?
    if function == operator.setitem:
        # setitem(dict, key, value)
        yield MutatedValue(PositionalArg(0))
        if is_mutable(args[2]):
            yield ViewOfValues(PositionalArg(2), PositionalArg(0))
        return

    if function == operator.getitem:
        # getitem(dict, key)
        # If both are mutable, they are now views of one another!
        if is_mutable(args[0]) and is_mutable(result):
            yield ViewOfValues(PositionalArg(0), Result())
            return
    if function == operator.delitem:
        # delitem(dict, key)
        yield MutatedValue(PositionalArg(0))
        return
    if function == l_list:
        # l_build_list(x1, x2, ...)
        yield ViewOfValues(
            Result(),
            *(PositionalArg(i) for i, a in enumerate(args) if is_mutable(a)),
        )
        return
    if (
        isinstance(function, types.BuiltinMethodType)
        and function.__name__ == "append"
        and isinstance(function.__self__, list)
    ):
        # list.append(value)
        yield MutatedValue(BoundSelfOfFunction())
        if is_mutable(args[0]):
            yield ViewOfValues(BoundSelfOfFunction(), PositionalArg(0))
        return

    if imported_module("sklearn"):
        from sklearn.base import BaseEstimator

        if (
            isinstance(function, types.MethodType)
            and function.__name__ == "fit"
            and isinstance(function.__self__, BaseEstimator)
        ):
            # In res = clf.fit(x, y)
            # cff is mutated, and we say that the res and the clf
            # are views of each other, since mutating one will mutate the other
            # since they are the same object.
            yield MutatedValue(BoundSelfOfFunction())
            yield ViewOfValues(BoundSelfOfFunction(), Result())
            return
    # Note: Future functions might require normalizing the args/kwargs with
    # inspect.signature.bind(args, kwargs) first
    return []


def imported_module(name: str) -> bool:
    """
    Returns true if we have imported this module before.
    """
    return name in sys.modules


def is_mutable(obj: object) -> bool:
    """
    Returns true if the object is mutable.
    """

    # Assume all hashable objects are immutable
    try:
        hash(obj)
    except Exception:
        return True
    return False


@dataclass
class ViewOfValues:
    """
    A set of values which all potentially refer to shared pointers
    So that if one is mutated, the rest might be as well.
    """

    # They are unique, like a set, but ordered for deterministc behaviour
    pointers: list[ValuePointer]

    def __init__(self, *xs: ValuePointer) -> None:
        self.pointers = list(xs)


@dataclass(frozen=True)
class MutatedValue:
    """
    A value that is mutated when the function is called
    """

    pointer: ValuePointer


@dataclass(frozen=True)
class ImplicitDependencyValue:
    pointer: ValuePointer


InspectFunctionSideEffect = Union[
    ViewOfValues, MutatedValue, ImplicitDependencyValue
]
InspectFunctionSideEffects = Iterable[InspectFunctionSideEffect]


@dataclass(frozen=True)
class PositionalArg:
    index: int


@dataclass(frozen=True)
class KeywordArg:
    name: str


@dataclass(frozen=True)
class BoundSelfOfFunction:
    """
    If the function is a bound method, this refers to the instance that was
    bound of the method.
    """

    pass


@dataclass(frozen=True)
class Result:
    """
    The result of a function call, used to describe a View.
    """

    pass


# A value representing a pointer to some value related to a function call
ValuePointer = Union[
    PositionalArg,
    KeywordArg,
    Result,
    BoundSelfOfFunction,
    ExternalState,
]