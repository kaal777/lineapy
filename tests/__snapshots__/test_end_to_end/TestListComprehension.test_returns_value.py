import datetime
from lineapy.data.types import *
from lineapy.utils import get_new_id

session = SessionContext(
    id=get_new_id(),
    environment_type=SessionType.SCRIPT,
    creation_time=datetime.datetime(1, 1, 1, 0, 0),
    file_name="[source file path]",
    code="x = [i + 1 for i in range(3)]",
    working_directory="dummy_linea_repo/",
    libraries=[],
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
        end_col_offset=29,
        arguments=[
            ArgumentNode(
                id=get_new_id(),
                session_id=session.id,
                positional_order=0,
                value_node_id=CallNode(
                    id=get_new_id(),
                    session_id=session.id,
                    lineno=1,
                    col_offset=4,
                    end_lineno=1,
                    end_col_offset=29,
                    arguments=[
                        ArgumentNode(
                            id=get_new_id(),
                            session_id=session.id,
                            keyword="range",
                            value_node_id=LookupNode(
                                id=get_new_id(),
                                session_id=session.id,
                                name="range",
                            ).id,
                        ).id,
                        ArgumentNode(
                            id=get_new_id(),
                            session_id=session.id,
                            positional_order=0,
                            value_node_id=LiteralNode(
                                id=get_new_id(),
                                session_id=session.id,
                                value="[i + 1 for i in range(3)]",
                            ).id,
                        ).id,
                        ArgumentNode(
                            id=get_new_id(),
                            session_id=session.id,
                            positional_order=1,
                            value_node_id=LiteralNode(
                                id=get_new_id(),
                                session_id=session.id,
                                value=1,
                            ).id,
                        ).id,
                    ],
                    function_id=LookupNode(
                        id=get_new_id(),
                        session_id=session.id,
                        name="__exec__",
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
                    value=0,
                ).id,
            ).id,
        ],
        function_id=LookupNode(
            id=get_new_id(),
            session_id=session.id,
            name="getitem",
        ).id,
    ).id,
    assigned_variable_name="x",
)