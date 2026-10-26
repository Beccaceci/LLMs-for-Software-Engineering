import json
import re
from pathlib import Path

GUIDE = Path('STUDY_GUIDE/main.tex')
BASELINE = Path('STUDY_GUIDE/scratch/rewrite_baseline.json')

manifest = json.loads(BASELINE.read_text(encoding='utf-8'))

for row in manifest['chapters']:
    source = (GUIDE.parent.parent / row['path']).read_text(encoding='utf-8')
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
    row['structure'] = structure
    row['labels'] = labels
    row['citations'] = citations
    for artifact, count in counts.items():
        row[artifact] = count

BASELINE.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print("Successfully synchronized rewrite_baseline.json")
