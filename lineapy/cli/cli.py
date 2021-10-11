import logging
import pathlib
from typing import cast

import click
import rich
import rich.syntax
import rich.tree

from lineapy.constants import ExecutionMode
from lineapy.data.graph import Graph
from lineapy.data.types import LineaID, SessionType
from lineapy.db.relational.db import RelationalLineaDB
from lineapy.graph_reader.program_slice import get_program_slice
from lineapy.instrumentation.tracer import Tracer
from lineapy.logging import configure_logging
from lineapy.transformer.node_transformer import transform

"""
We are using click because our package will likely already have a dependency on
  flask and it's fairly well-starred.
"""

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--mode",
    default="memory",
    help="Either `memory`, `dev`, `test`, or `prod` mode",
)
@click.option(
    "--slice",
    default=None,
    help="Print the sliced code that this artifact depends on",
)
@click.option(
    "--print-source", help="Whether to print the source code", is_flag=True
)
@click.option(
    "--print-graph",
    help="Whether to print the generated graph code",
    is_flag=True,
)
@click.option(
    "--verbose",
    help="Print out logging for graph creation and execution",
    is_flag=True,
)
@click.argument(
    "file_name",
    type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path),
)
def linea_cli(
    file_name: pathlib.Path, mode, slice, print_source, print_graph, verbose
):
    configure_logging("INFO" if verbose else "WARNING")
    tree = rich.tree.Tree(f"📄 {file_name}")

    execution_mode = ExecutionMode.__getitem__(str.upper(mode))
    db = RelationalLineaDB.from_environment(execution_mode)
    code = file_name.read_text()

    if print_source:
        tree.add(
            rich.console.Group(
                "Source code", rich.syntax.Syntax(code, "python")
            )
        )
    tracer = Tracer(db, SessionType.SCRIPT)
    transform(code, file_name, tracer)

    db = tracer.db
    nodes = db.get_all_nodes()
    context = tracer.session_context
    graph = Graph(nodes, context)

    if slice:
        artifact = db.get_artifact_by_name(slice)
        sliced_code = get_program_slice(graph, [cast(LineaID, artifact.id)])
        tree.add(
            rich.console.Group(
                f"Slice of {repr(slice)}",
                rich.syntax.Syntax(sliced_code, "python"),
            )
        )

    db.close()
    if print_graph:
        graph_code = graph.print(
            include_source_location=False,
            include_id_field=False,
            include_session=False,
            include_imports=False,
        )
        tree.add(
            rich.console.Group(
                "፨ Graph", rich.syntax.Syntax(graph_code, "python")
            )
        )

    console = rich.console.Console()
    console.print(tree)


if __name__ == "__main__":
    linea_cli()
