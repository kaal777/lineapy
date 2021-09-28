import datetime
from lineapy.data.types import *
from lineapy.utils import get_new_id

session = SessionContext(
    id=get_new_id(),
    environment_type=SessionType.SCRIPT,
    creation_time=datetime.datetime(1, 1, 1, 0, 0),
    file_name="[source file path]",
    code='bs = [1,2]\nif len(bs) > 4:\n    print("True")\nelse:\n    bs.append(3)\n    print("False")\n',
    working_directory="dummy_linea_repo/",
    libraries=[],
)
call_2 = CallNode(
    id=get_new_id(),
    session_id=session.id,
    lineno=3,
    col_offset=4,
    end_lineno=3,
    end_col_offset=17,
    arguments=[
        ArgumentNode(
            id=get_new_id(),
            session_id=session.id,
            positional_order=0,
            value_node_id=LiteralNode(
                id=get_new_id(),
                session_id=session.id,
                lineno=3,
                col_offset=10,
                end_lineno=3,
                end_col_offset=16,
                value="True",
            ).id,
        ).id
    ],
    function_id=LookupNode(
        id=get_new_id(),
        session_id=session.id,
        name="print",
    ).id,
)
call_3 = CallNode(
    id=get_new_id(),
    session_id=session.id,
    lineno=6,
    col_offset=4,
    end_lineno=6,
    end_col_offset=18,
    arguments=[
        ArgumentNode(
            id=get_new_id(),
            session_id=session.id,
            positional_order=0,
            value_node_id=LiteralNode(
                id=get_new_id(),
                session_id=session.id,
                lineno=6,
                col_offset=10,
                end_lineno=6,
                end_col_offset=17,
                value="False",
            ).id,
        ).id
    ],
    function_id=LookupNode(
        id=get_new_id(),
        session_id=session.id,
        name="print",
    ).id,
)
variable_1 = VariableNode(
    id=get_new_id(),
    session_id=session.id,
    source_node_id=CallNode(
        id=get_new_id(),
        session_id=session.id,
        lineno=1,
        col_offset=0,
        end_lineno=1,
        end_col_offset=10,
        arguments=[
            ArgumentNode(
                id=get_new_id(),
                session_id=session.id,
                positional_order=0,
                value_node_id=LiteralNode(
                    id=get_new_id(),
                    session_id=session.id,
                    lineno=1,
                    col_offset=6,
                    end_lineno=1,
                    end_col_offset=7,
                    value=1,
                ).id,
            ).id,
            ArgumentNode(
                id=get_new_id(),
                session_id=session.id,
                positional_order=1,
                value_node_id=LiteralNode(
                    id=get_new_id(),
                    session_id=session.id,
                    lineno=1,
                    col_offset=8,
                    end_lineno=1,
                    end_col_offset=9,
                    value=2,
                ).id,
            ).id,
        ],
        function_id=LookupNode(
            id=get_new_id(),
            session_id=session.id,
            name="__build_list__",
        ).id,
    ).id,
    assigned_variable_name="bs",
)
call_6 = CallNode(
    id=get_new_id(),
    session_id=session.id,
    lineno=5,
    col_offset=4,
    end_lineno=5,
    end_col_offset=16,
    arguments=[
        ArgumentNode(
            id=get_new_id(),
            session_id=session.id,
            positional_order=0,
            value_node_id=LiteralNode(
                id=get_new_id(),
                session_id=session.id,
                lineno=5,
                col_offset=14,
                end_lineno=5,
                end_col_offset=15,
                value=3,
            ).id,
        ).id
    ],
    function_id=CallNode(
        id=get_new_id(),
        session_id=session.id,
        lineno=5,
        col_offset=4,
        end_lineno=5,
        end_col_offset=13,
        arguments=[
            ArgumentNode(
                id=get_new_id(),
                session_id=session.id,
                positional_order=0,
                value_node_id=variable_1.id,
            ).id,
            ArgumentNode(
                id=get_new_id(),
                session_id=session.id,
                positional_order=1,
                value_node_id=LiteralNode(
                    id=get_new_id(),
                    session_id=session.id,
                    value="append",
                ).id,
            ).id,
        ],
        function_id=LookupNode(
            id=get_new_id(),
            session_id=session.id,
            name="getattr",
        ).id,
    ).id,
)
call_7 = CallNode(
    id=get_new_id(),
    session_id=session.id,
    lineno=2,
    col_offset=3,
    end_lineno=2,
    end_col_offset=14,
    arguments=[
        ArgumentNode(
            id=get_new_id(),
            session_id=session.id,
            positional_order=0,
            value_node_id=CallNode(
                id=get_new_id(),
                session_id=session.id,
                lineno=2,
                col_offset=3,
                end_lineno=2,
                end_col_offset=10,
                arguments=[
                    ArgumentNode(
                        id=get_new_id(),
                        session_id=session.id,
                        positional_order=0,
                        value_node_id=variable_1.id,
                    ).id
                ],
                function_id=LookupNode(
                    id=get_new_id(),
                    session_id=session.id,
                    name="len",
                ).id,
            ).id,
        ).id,
        ArgumentNode(
            id=get_new_id(),
            session_id=session.id,
            positional_order=1,
            value_node_id=LiteralNode(
                id=get_new_id(),
                session_id=session.id,
                lineno=2,
                col_offset=13,
                end_lineno=2,
                end_col_offset=14,
                value=4,
            ).id,
        ).id,
    ],
    function_id=LookupNode(
        id=get_new_id(),
        session_id=session.id,
        name="gt",
    ).id,
)