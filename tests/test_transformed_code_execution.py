import logging
import os
from tempfile import NamedTemporaryFile

from lineapy import SessionType, ExecutionMode
from lineapy.constants import SQLALCHEMY_ECHO
from lineapy.transformer.transformer import Transformer

logging.basicConfig()


class TestTransformedCodeExecution:
    @staticmethod
    def _run_program(code):
        logging.getLogger("sqlalchemy").setLevel(logging.ERROR)
        execution_mode = ExecutionMode.MEMORY
        os.environ[SQLALCHEMY_ECHO] = "False"
        transformer = Transformer()
        with NamedTemporaryFile() as tmp:
            tmp.write(str.encode(code))
            tmp.flush()
            new_code = transformer.transform(
                code,
                session_type=SessionType.SCRIPT,
                session_name=tmp.name,
                execution_mode=execution_mode,
            )
            exec(new_code)

    def test_chained_ops(self):
        code = "b = 1 < 2 < 3\nassert b"
        self._run_program(code)

    def test_binop(self):
        code = "b = 1 + 2\nassert b == 3"
        self._run_program(code)
