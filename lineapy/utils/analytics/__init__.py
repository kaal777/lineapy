from functools import wraps
from typing import Callable, TypeVar, cast

from lineapy.data.types import LineaID
from lineapy.db.db import RelationalLineaDB
from lineapy.instrumentation.annotation_spec import ExternalState
from lineapy.utils.analytics.event_schemas import (
    ExceptionEvent,
    GetParam,
    LibInfo,
    LibInfoEvent,
    LineapyAPIEvent,
    SaveParam,
    ToPipelineParam,
)
from lineapy.utils.analytics.usage_tracking import do_not_track, track

C = TypeVar("C", bound=Callable)


def allow_do_not_track(fn: C) -> C:
    @wraps(fn)
    def decorator(*args, **kwargs):
        if do_not_track():
            return
        return fn(*args, **kwargs)

    return cast(C, decorator)


# checking earlier to avoid doing extra DB query work
@allow_do_not_track
def send_lib_info_from_db(db: RelationalLineaDB, session_id: LineaID):
    import_nodes = db.get_libraries_for_session(session_id)
    libs = [LibInfo(str(n.name), str(n.version)) for n in import_nodes]
    track(LibInfoEvent(libs))


def side_effect_to_str(reference: object):
    if isinstance(reference, ExternalState):
        return reference.external_state
    return ""


__all__ = [
    "track",
    "ExceptionEvent",
    "allow_do_not_track",
    "LineapyAPIEvent",
    "ToPipelineParam",
    "GetParam",
    "SaveParam",
    "side_effect_to_str",
]
