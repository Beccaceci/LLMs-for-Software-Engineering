import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".agents/skills/laboratory-study-guide-integrator/scripts"))
import cell_coverage


class CellCoverageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.nb = self.root / "lab01" / "text.ipynb"
        self.nb.parent.mkdir()
        self.source = "x = 2\nprint(x)"
        notebook = {
            "cells": [
                {"cell_type": "markdown", "source": ["# Exercise 1\n"]},
                {"cell_type": "code", "source": self.source.splitlines(True), "execution_count": 1,
                 "outputs": [{"output_type": "stream", "name": "stdout", "text": ["2\n"]}]},
            ]
        }
        self.nb.write_text(json.dumps(notebook))
        self.outdir = self.root / "artifacts"
        self.inv = cell_coverage.export([self.nb], self.root, self.outdir)
        self.inv_path = self.root / "inventory.json"
        self.inv_path.write_text(json.dumps(self.inv))
        cell = self.inv["cells"][0]
        self.coverage_path = self.root / "coverage.json"
        self.coverage = {"cells": [{
            "key": cell["key"], "source_sha256": cell["source_sha256"],
            "exercise_chapter": "Exercise 1", "section": "Dataset",
            "source_artifact": cell["exported_source"], "output_anchor": "res:lab01-ex1-cell1",
            "execution_evidence": "execution_count",
            "output_disposition": "printed-result", "figures": [],
            "outputs": [{
                "index": output["index"], "source_sha256": cell["source_sha256"],
                "payload_sha256": output["payload_sha256"],
                "presentation_artifact": cell["exported_outputs"][output["index"]]["presentation_artifact"],
            } for output in cell["outputs"]],
        }]}
        self.write_coverage()
        self.tex = self.root / "solution.tex"
        self.write_tex()

    def tearDown(self):
        self.tmp.cleanup()

    def write_coverage(self):
        self.coverage_path.write_text(json.dumps(self.coverage))

    def write_tex(self):
        cell = self.inv["cells"][0]
        outputs = ""
        for output in cell.get("exported_outputs", []):
            artifact = output["presentation_artifact"] or "-"
            outputs += (
                f"% coverage-output: {cell['notebook']} cell={cell['cell_index']} output={output['index']} "
                f"source_sha256={cell['source_sha256']} payload_sha256={output['payload_sha256']} artifact={artifact}\n"
            )
            if output["presentation_artifact"]:
                outputs += f"\\lstinputlisting{{{output['presentation_artifact']}}}\n"
        self.tex.write_text(
            f"% coverage-cell: {cell['notebook']} cell={cell['cell_index']} source_sha256={cell['source_sha256']}\n"
            "The computation is documented and its result is retained.\n"
            "\\begin{lstlisting}[language=Python]\n"
            f"{self.source}\n"
            "\\end{lstlisting}\n"
            "\\label{res:lab01-ex1-cell1}\n"
            f"{outputs}"
        )

    def validate(self):
        return cell_coverage.validate(self.inv_path, self.coverage_path, [self.tex], self.root)

    def test_complete_code_snippet_passes_without_visible_cell_label(self):
        self.assertEqual([], self.validate())

    def test_missing_cell_is_reported(self):
        self.coverage["cells"] = []
        self.write_coverage()
        self.assertTrue(any("Unmapped code cell" in e for e in self.validate()))

    def test_changed_notebook_hash_is_reported(self):
        self.nb.write_text(self.nb.read_text().replace("x = 2", "x = 3"))
        self.inv_path.write_text(json.dumps(cell_coverage.inventory([self.nb], self.root)))
        self.assertTrue(any("Stale source hash" in e for e in self.validate()))

    def test_missing_output_anchor_is_reported(self):
        self.coverage["cells"][0]["output_anchor"] = ""
        self.write_coverage()
        self.assertTrue(any("lacks an anchor" in e for e in self.validate()))

    def test_snippet_that_omits_source_is_reported(self):
        self.tex.write_text(self.tex.read_text().replace("print(x)", ""))
        self.assertTrue(any("Rendered code snippet differs" in e for e in self.validate()))

    def test_changed_internal_source_artifact_is_reported(self):
        artifact = self.root / self.coverage["cells"][0]["source_artifact"]
        artifact.write_text("x = 2\n")
        self.assertTrue(any("Internal source artifact differs" in e for e in self.validate()))

    def test_missing_figure_is_reported(self):
        self.coverage["cells"][0]["figures"] = ["artifacts/missing.png"]
        self.write_coverage()
        self.assertTrue(any("Missing output figure" in e for e in self.validate()))

    def test_notebook_plot_without_figure_destination_is_reported(self):
        self.inv["cells"][0]["exported_figures"] = ["artifacts/plot.png"]
        self.inv_path.write_text(json.dumps(self.inv))
        self.coverage["cells"][0]["figures"] = []
        self.write_coverage()
        self.assertTrue(any("image output has no included figure destination" in e for e in self.validate()))

    def test_stale_cell_reference_is_reported(self):
        self.coverage["cells"][0]["key"] = "lab01/text.ipynb::cell-0099"
        self.write_coverage()
        self.assertTrue(any("stale notebook cell" in e for e in self.validate()))

    def test_missing_individual_output_include_is_reported(self):
        self.tex.write_text(self.tex.read_text().replace("\\lstinputlisting", "\\missinglisting"))
        self.assertTrue(any("PDF source omits output artifact" in e for e in self.validate()))

    def test_missing_output_coverage_mapping_is_reported(self):
        self.coverage["cells"][0]["outputs"] = []
        self.write_coverage()
        self.assertTrue(any("lacks a coverage destination" in e for e in self.validate()))

    def test_manifest_reads_optional_section_titles_and_subsections(self):
        cell = self.inv["cells"][0]
        self.tex.write_text(
            r"\section[Exercise 1]{Exercise 1: Quantization}" + "\n"
            r"\subsection{Absmax quantization}" + "\n"
            f"% coverage-cell: {cell['notebook']} cell={cell['cell_index']} "
            f"source_sha256={cell['source_sha256']}\n"
        )
        manifest = cell_coverage.build_manifest(self.inv_path, [self.tex])
        entry = manifest["cells"][0]
        self.assertEqual("Exercise 1: Quantization", entry["exercise_chapter"])
        self.assertEqual("Exercise 1: Quantization", entry["exercise_name"])
        self.assertEqual("Absmax quantization", entry["section"])

    def test_rich_html_output_exports_table_values_and_raw_html(self):
        nb = self.root / "lab01" / "rich.ipynb"
        html = "<table><tr><th>Step</th><th>Loss</th></tr><tr><td>10</td><td>3.14</td></tr></table>"
        notebook = {"cells": [{"cell_type": "code", "source": "display(result)", "execution_count": 1,
                              "outputs": [{"output_type": "display_data", "data": {
                                  "text/plain": "<IPython.core.display.HTML object>", "text/html": html
                              }}]}]}
        nb.write_text(json.dumps(notebook))
        result = cell_coverage.export([nb], self.root, self.outdir)
        output = result["cells"][0]["exported_outputs"][0]
        presentation = (self.root / output["presentation_artifact"]).read_text()
        raw_html = next(item for item in output["raw_payload_artifacts"] if item["path"].endswith(".html"))
        self.assertIn("Step", presentation)
        self.assertIn("3.14", presentation)
        self.assertNotIn("IPython.core.display.HTML object", presentation)
        self.assertEqual(html, (self.root / raw_html["path"]).read_text())

    def test_produced_file_must_be_mapped_and_listed(self):
        artifact = self.root / "lab01" / "answers.json"
        artifact.write_text('[{"answer": 4}]\n')
        cell = self.inv["cells"][0]
        payload_hash = cell_coverage.sha256(artifact.read_bytes())
        marker = (
            f"% coverage-artifact: {cell['key']} source_sha256={cell['source_sha256']} "
            f"path=lab01/answers.json sha256={payload_hash}\n"
        )
        self.tex.write_text(self.tex.read_text() + marker + "\\lstinputlisting{answers.json}\n")
        self.coverage["cells"][0]["artifacts"] = [{
            "source_sha256": cell["source_sha256"], "path": "lab01/answers.json", "sha256": payload_hash,
        }]
        self.write_coverage()
        self.assertEqual([], self.validate())
        self.tex.write_text(self.tex.read_text().replace("\\lstinputlisting{answers.json}", ""))
        self.assertTrue(any("omits produced artifact" in e for e in self.validate()))

    def test_lab04_training_html_keeps_every_evaluation_row(self):
        source_notebook = Path(__file__).resolve().parents[2] / "lab04" / "text-01-clm.ipynb"
        source = json.loads(source_notebook.read_text(encoding="utf-8"))
        cell = source["cells"][15]
        notebook = self.root / "lab04" / "training.ipynb"
        notebook.parent.mkdir(parents=True, exist_ok=True)
        notebook.write_text(json.dumps({"cells": [cell]}), encoding="utf-8")
        result = cell_coverage.export([notebook], self.root, self.outdir)
        rendered = self.root / result["cells"][0]["exported_outputs"][0]["presentation_artifact"]
        table = rendered.read_text(encoding="utf-8")
        for step in range(10, 161, 10):
            self.assertRegex(table, rf"(?m)^{step}$")
        self.assertIn("3.177716", table)
        self.assertIn("3.131138", table)


if __name__ == "__main__":
    unittest.main()
