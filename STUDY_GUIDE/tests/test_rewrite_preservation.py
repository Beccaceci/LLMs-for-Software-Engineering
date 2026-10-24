"""Preservation checks for the complete editorial rewrite baseline."""

import json
import re
from pathlib import Path


GUIDE = Path(__file__).resolve().parents[1]
BASELINE = GUIDE / "scratch" / "rewrite_baseline.json"


def test_active_chapter_structure_and_protected_artifacts_are_preserved():
    manifest = json.loads(BASELINE.read_text(encoding="utf-8"))
    assert len(manifest["chapters"]) == 7

    for row in manifest["chapters"]:
        source = (GUIDE.parent / row["path"]).read_text(encoding="utf-8")
        structure = re.findall(
            r"^\\(?:chapter|section|subsection|subsubsection|paragraph)\*?\{.*$",
            source,
            re.MULTILINE,
        )
        labels = re.findall(r"\\label\{[^}]+\}", source)
        citations = sorted(
            set(re.findall(r"\\cite[a-zA-Z*]*\{([^}]+)\}", source))
        )
        counts = {
            "equations": len(
                re.findall(
                    r"\\begin\{(?:equation\*?|align\*?|gather\*?|multline\*?)\}",
                    source,
                )
            ),
            "tables": len(re.findall(r"\\begin\{table\*?\}", source)),
            "figures": len(re.findall(r"\\begin\{figure\*?\}", source)),
            "listings": len(re.findall(r"\\begin\{lstlisting\}", source)),
        }

        assert structure == row["structure"], f"Heading hierarchy changed: {row['path']}"
        assert labels == row["labels"], f"Labels changed: {row['path']}"
        assert citations == row["citations"], f"Citation keys changed: {row['path']}"
        for artifact, count in counts.items():
            assert count == row[artifact], f"{artifact} count changed: {row['path']}"

    for row in manifest["frontmatter"]:
        source = (GUIDE.parent / row["path"]).read_text(encoding="utf-8")
        structure = re.findall(
            r"^\\(?:chapter|section|subsection|subsubsection)\*?\{.*$",
            source,
            re.MULTILINE,
        )
        labels = re.findall(r"\\label\{[^}]+\}", source)
        citations = sorted(
            set(re.findall(r"\\cite[a-zA-Z*]*\{([^}]+)\}", source))
        )
        assert structure == row["structure"], f"Frontmatter hierarchy changed: {row['path']}"
        assert labels == row["labels"], f"Frontmatter labels changed: {row['path']}"
        assert citations == row["citations"], f"Frontmatter citations changed: {row['path']}"
