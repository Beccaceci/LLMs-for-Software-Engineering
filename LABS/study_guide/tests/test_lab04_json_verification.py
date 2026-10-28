import ast
import contextlib
import io
import json
import unittest
from pathlib import Path


NOTEBOOK = Path(__file__).resolve().parents[2] / "lab04" / "text-02-llms.ipynb"


def load_notebook_verifier():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    source = "".join(notebook["cells"][37]["source"])
    tree = ast.parse(source)
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "verify_answer")
    namespace = {"json": json}
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(NOTEBOOK), "exec"), namespace)
    return namespace["verify_answer"]


class Lab04JSONVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verify_answer = staticmethod(load_notebook_verifier())

    def verify(self, content, num_1=26, num_2=760):
        entry = {
            "num_1": num_1,
            "num_2": num_2,
            "model_answer": [{"role": "assistant", "content": content}],
        }
        with contextlib.redirect_stdout(io.StringIO()):
            return self.verify_answer(entry)

    def test_correct_json_and_sum_pass(self):
        self.assertTrue(self.verify('{"num_1": 26, "num_2": 760, "answer": 786}'))

    def test_incorrect_sum_fails(self):
        self.assertFalse(self.verify('{"num_1": 26, "num_2": 760, "answer": 785}'))

    def test_malformed_json_fails_cleanly(self):
        self.assertFalse(self.verify('{"num_1": 26, "num_2": 760,'))

    def test_missing_assistant_message_fails_cleanly(self):
        entry = {"num_1": 26, "num_2": 760, "model_answer": [{"role": "user", "content": "question"}]}
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(self.verify_answer(entry))

    def test_missing_json_field_fails_cleanly(self):
        self.assertFalse(self.verify('{"num_1": 26, "num_2": 760}'))


if __name__ == "__main__":
    unittest.main()
