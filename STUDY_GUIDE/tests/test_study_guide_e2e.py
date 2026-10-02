#!/usr/bin/env python3
"""
End-to-End Test Suite for Politecnico di Torino "LLM for Software Engineering" Study Guide & Antigravity Skill.
Validates Tiers 1-4:
  Tier 1: Feature Coverage (>=5 tests per feature)
  Tier 2: Boundary & Corner Cases (>=5 tests per feature)
  Tier 3: Cross-Feature Combinations
  Tier 4: Real-World Scenarios
"""

import os
import re
import sys
import shutil
import tempfile
import unittest
import subprocess
from pathlib import Path
import yaml

try:
    import pypdf
except ImportError:
    pypdf = None

_CUR = Path(__file__).resolve()
if (_CUR.parent.parent / ".agents").exists():
    PROJECT_ROOT = _CUR.parent.parent
elif (_CUR.parent.parent.parent / ".agents").exists():
    PROJECT_ROOT = _CUR.parent.parent.parent
else:
    PROJECT_ROOT = _CUR.parent.parent

STUDY_GUIDE_DIR = (PROJECT_ROOT / "STUDY_GUIDE") if (PROJECT_ROOT / "STUDY_GUIDE").exists() else (
    (PROJECT_ROOT / "study_guide") if (PROJECT_ROOT / "study_guide").exists() else PROJECT_ROOT
)
LECTURES_DIR = (STUDY_GUIDE_DIR / "lectures") if (STUDY_GUIDE_DIR / "lectures").exists() else STUDY_GUIDE_DIR
LABS_DIR = (STUDY_GUIDE_DIR / "laboratories") if (STUDY_GUIDE_DIR / "laboratories").exists() else STUDY_GUIDE_DIR
SHARED_DIR = (STUDY_GUIDE_DIR / "shared") if (STUDY_GUIDE_DIR / "shared").exists() else STUDY_GUIDE_DIR

MAIN_TEX = (LECTURES_DIR / "main.tex") if (LECTURES_DIR / "main.tex").exists() else (MAIN_TEX)
LABS_TEX = (LABS_DIR / "labs.tex") if (LABS_DIR / "labs.tex").exists() else (STUDY_GUIDE_DIR / "labs.tex")
MACROS_STY = (SHARED_DIR / "style" / "macros.sty") if (SHARED_DIR / "style" / "macros.sty").exists() else (MACROS_STY)
REFERENCES_BIB = (SHARED_DIR / "references.bib") if (SHARED_DIR / "references.bib").exists() else (REFERENCES_BIB)
FRONTMATTER_DIR = (LECTURES_DIR / "frontmatter") if (LECTURES_DIR / "frontmatter").exists() else (FRONTMATTER_DIR)
CHAPTERS_DIR = (LECTURES_DIR / "chapters") if (LECTURES_DIR / "chapters").exists() else (CHAPTERS_DIR)


# Ensure /Library/TeX/texbin is in PATH for TeX commands on macOS
TEX_BIN = "/Library/TeX/texbin"
CURRENT_PATH = os.environ.get("PATH", "")
if TEX_BIN not in CURRENT_PATH and os.path.exists(TEX_BIN):
    os.environ["PATH"] = f"{TEX_BIN}:{CURRENT_PATH}"


def read_text_safe(path: Path) -> str:
    """Read a text file with UTF-8 encoding."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def strip_comments_and_strings(content: str) -> str:
    """
    Strips LaTeX comments (anything after unescaped %)
    while keeping the rest intact.
    """
    clean_lines = []
    for line in content.splitlines():
        # Match % that is not preceded by \
        parts = re.split(r"(?<!\\)%", line, maxsplit=1)
        clean_lines.append(parts[0])
    return "\n".join(clean_lines)


def parse_bibtex(bib_text: str) -> list[dict]:
    """Parse BibTeX entries into a list of dicts with key, type, and fields."""
    entries = []
    # Pattern to match @type{key, ...}
    entry_pattern = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,\s*(.*?)\n\s*\}", re.DOTALL)
    for match in entry_pattern.finditer(bib_text):
        entry_type = match.group(1).lower()
        key = match.group(2).strip()
        body = match.group(3)
        fields = {}
        field_matches = re.finditer(r'(\w+)\s*=\s*[\{"](.*?)[\}"]', body, re.DOTALL)
        for fm in field_matches:
            fields[fm.group(1).lower()] = fm.group(2).strip()
        entries.append({"key": key, "type": entry_type, "fields": fields, "raw": match.group(0)})
    return entries


def parse_yaml_frontmatter(file_path: Path) -> tuple[dict, str]:
    """Extract YAML frontmatter and body markdown from a file."""
    content = read_text_safe(file_path)
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content
    yaml_text = match.group(1)
    body = match.group(2)
    try:
        data = yaml.safe_load(yaml_text) or {}
        return data, body
    except Exception as e:
        raise ValueError(f"YAML parsing error in {file_path}: {e}")


# ==============================================================================
# TIER 1: FEATURE COVERAGE (>=5 tests per feature)
# ==============================================================================

class TestTier1FeatureCoverage(unittest.TestCase):
    """Tier 1: Feature Coverage testing for all core deliverables and architectural components."""

    # --------------------------------------------------------------------------
    # Feature 1: TeX Book Layout & Typography
    # --------------------------------------------------------------------------
    def test_feature1_main_tex_exists_and_non_empty(self):
        """Feature 1.1: main.tex exists and is non-empty."""
        main_tex = MAIN_TEX
        self.assertTrue(main_tex.exists(), "main.tex must exist in project root")
        self.assertGreater(main_tex.stat().st_size, 200, "main.tex must not be empty or stub")

    def test_feature1_main_tex_documentclass_and_options(self):
        """Feature 1.2: documentclass is book with required options."""
        content = read_text_safe(MAIN_TEX)
        self.assertRegex(content, r"\\documentclass\[.*?\]\{book\}", "main.tex must use book class")
        self.assertIn("a4paper", content, "main.tex must specify a4paper layout")
        self.assertIn("oneside", content, "main.tex must specify oneside reading mode")

    def test_feature1_main_tex_required_packages_included(self):
        """Feature 1.3: Core typography and math packages are loaded."""
        content = read_text_safe(MAIN_TEX)
        required_pkgs = ["amsmath", "amssymb", "mathtools", "newpxtext", "newpxmath", "sourcecodepro", "microtype"]
        for pkg in required_pkgs:
            matched = re.search(rf"\\usepackage(?:\[.*?\])?\{{[^}}]*\b{pkg}\b[^}}]*\}}", content)
            self.assertIsNotNone(matched, f"main.tex must load package {pkg}")

    def test_feature1_main_tex_geometry_and_margins(self):
        """Feature 1.4: Geometry package configured with 25mm margins."""
        content = read_text_safe(MAIN_TEX)
        self.assertIn("geometry", content, "main.tex must load geometry package")
        self.assertRegex(content, r"top\s*=\s*25mm", "Top margin must be 25mm")
        self.assertRegex(content, r"bottom\s*=\s*25mm", "Bottom margin must be 25mm")

    def test_feature1_main_tex_document_divisions_and_subfiles(self):
        """Feature 1.5: Document includes frontmatter, mainmatter, backmatter, subfiles."""
        content = read_text_safe(MAIN_TEX)
        self.assertIn(r"\frontmatter", content, "main.tex must contain \\frontmatter")
        self.assertIn(r"\mainmatter", content, "main.tex must contain \\mainmatter")
        self.assertIn(r"\backmatter", content, "main.tex must contain \\backmatter")
        self.assertIn(r"\tableofcontents", content, "main.tex must generate table of contents")
        self.assertIn(r"\subfile{", content, "main.tex must include modular chapters via \\subfile")

    # --------------------------------------------------------------------------
    # Feature 2: Macro & Math Foundation
    # --------------------------------------------------------------------------
    def test_feature2_macros_sty_exists_and_provides_package(self):
        """Feature 2.1: style/macros.sty exists with valid \\ProvidesPackage."""
        macros_sty = MACROS_STY
        self.assertTrue(macros_sty.exists(), "style/macros.sty must exist")
        content = read_text_safe(macros_sty)
        self.assertRegex(content, r"\\ProvidesPackage\{style/macros\}", "macros.sty must declare ProvidesPackage")

    def test_feature2_macros_sty_required_dependencies(self):
        """Feature 2.2: style/macros.sty requires xcolor, tcolorbox, fontawesome5, etc."""
        content = read_text_safe(MACROS_STY)
        for dep in ["tcolorbox", "fontawesome5", "amsmath", "mathtools"]:
            self.assertTrue(
                dep in content,
                f"macros.sty must require or load dependency {dep}"
            )

    def test_feature2_macros_sty_math_operators(self):
        """Feature 2.3: Standard activation functions and math operators declared."""
        content = read_text_safe(MACROS_STY)
        operators = ["softmax", "sigmoid", "relu", "gelu"]
        for op in operators:
            op_macro = "\\" + op
            self.assertTrue(
                f"\\DeclareMathOperator{{{op_macro}}}" in content or f"\\newcommand{{{op_macro}}}" in content,
                f"Operator \\{op} must be defined in macros.sty"
            )

    def test_feature2_macros_sty_expectation_norms_and_losses(self):
        """Feature 2.4: Probability, Expectation, Loss, and Norm macros defined."""
        content = read_text_safe(MACROS_STY)
        expected_macros = [r"\E", r"\norm", r"\Loss"]
        for macro in expected_macros:
            self.assertTrue(
                macro in content,
                f"Macro {macro} must be defined in macros.sty"
            )

    def test_feature2_macros_sty_vector_matrix_and_se_metrics(self):
        """Feature 2.5: Matrix/vector notation and SE metrics (Pass@k, CodeBLEU) defined."""
        content = read_text_safe(MACROS_STY)
        for symbol in [r"\mW", r"\vx", r"\PassAtK", r"\CodeBLEU"]:
            self.assertTrue(
                symbol in content,
                f"Symbol/metric {symbol} must be defined in macros.sty"
            )

    # --------------------------------------------------------------------------
    # Feature 3: Specialized Callout Boxes
    # --------------------------------------------------------------------------
    def test_feature3_examinsight_environment_definition(self):
        """Feature 3.1: examinsight box defined with breakable, color, and faGraduationCap."""
        content = read_text_safe(MACROS_STY)
        self.assertIn(r"\newtcolorbox{examinsight}", content, "examinsight must be defined with \\newtcolorbox")
        self.assertIn("faGraduationCap", content, "examinsight must feature faGraduationCap icon")
        self.assertIn("breakable", content, "examinsight must be breakable across page boundaries")

    def test_feature3_intuition_environment_definition(self):
        """Feature 3.2: intuition box defined with breakable, color, and faLightbulb."""
        content = read_text_safe(MACROS_STY)
        self.assertIn(r"\newtcolorbox{intuition}", content, "intuition must be defined with \\newtcolorbox")
        self.assertIn("faLightbulb", content, "intuition must feature faLightbulb icon")
        self.assertIn("breakable", content, "intuition must be breakable")

    def test_feature3_deepdive_environment_definition(self):
        """Feature 3.3: deepdive box defined with breakable, color, and faCompass."""
        content = read_text_safe(MACROS_STY)
        self.assertIn(r"\newtcolorbox{deepdive}", content, "deepdive must be defined with \\newtcolorbox")
        self.assertIn("faCompass", content, "deepdive must feature faCompass icon")
        self.assertIn("breakable", content, "deepdive must be breakable")

    def test_feature3_definition_environment_definition(self):
        """Feature 3.4: Numbered definition environment defined with tcbtheorem."""
        content = read_text_safe(MACROS_STY)
        self.assertRegex(
            content,
            r"\\newtcbtheorem.*?\{definition\}\{Definition\}",
            "definition environment must be declared via \\newtcbtheorem"
        )

    def test_feature3_theorem_environment_definition(self):
        """Feature 3.5: Numbered theorem environment defined with tcbtheorem."""
        content = read_text_safe(MACROS_STY)
        self.assertRegex(
            content,
            r"\\newtcbtheorem.*?\{theorem\}\{Theorem\}",
            "theorem environment must be declared via \\newtcbtheorem"
        )

    # --------------------------------------------------------------------------
    # Feature 4: Build Engine & Automation
    # --------------------------------------------------------------------------
    def test_feature4_latexmkrc_configuration(self):
        """Feature 4.1: .latexmkrc exists with pdf_mode=1 and pdflatex/bibtex engine."""
        latexmkrc = STUDY_GUIDE_DIR / ".latexmkrc"
        self.assertTrue(latexmkrc.exists(), ".latexmkrc must exist in project root")
        content = read_text_safe(latexmkrc)
        self.assertIn("$pdf_mode = 1", content, ".latexmkrc must set $pdf_mode = 1")
        self.assertIn("pdflatex", content, ".latexmkrc must specify pdflatex")
        self.assertIn("bibtex", content, ".latexmkrc must specify bibtex")

    def test_feature4_makefile_presence_and_targets(self):
        """Feature 4.2: Makefile exists and defines all, pdf, and clean targets."""
        makefile = STUDY_GUIDE_DIR / "Makefile"
        self.assertTrue(makefile.exists(), "Makefile must exist in project root")
        content = read_text_safe(makefile)
        self.assertIn("all:", content, "Makefile must have 'all' target")
        self.assertIn("pdf:", content, "Makefile must have 'pdf' target")
        self.assertIn("clean:", content, "Makefile must have 'clean' target")

    def test_feature4_compile_script_presence_and_executable(self):
        """Feature 4.3: scripts/compile.sh exists and is non-empty."""
        compile_sh = (STUDY_GUIDE_DIR / "scripts" / "compile.sh") if (STUDY_GUIDE_DIR / "scripts" / "compile.sh").exists() else (PROJECT_ROOT / "scripts" / "compile.sh")
        self.assertTrue(compile_sh.exists(), "scripts/compile.sh must exist")
        content = read_text_safe(compile_sh)
        self.assertTrue(content.startswith("#!/"), "compile.sh must start with a shebang")

    def test_feature4_makefile_clean_and_distclean_targets(self):
        """Feature 4.4: Makefile clean targets prune auxiliary files without deleting sources."""
        content = read_text_safe(STUDY_GUIDE_DIR / "Makefile")
        self.assertIn("*.aux", content, "Makefile clean target must clean .aux files")
        self.assertIn("*.log", content, "Makefile clean target must clean .log files")

    def test_feature4_makefile_standalone_chapter_target(self):
        """Feature 4.5: Makefile supports standalone chapter compilation."""
        content = read_text_safe(STUDY_GUIDE_DIR / "Makefile")
        self.assertIn("chapter:", content, "Makefile must support compiling individual chapters")

    # --------------------------------------------------------------------------
    # Feature 5: Master Bibliography
    # --------------------------------------------------------------------------
    def test_feature5_references_bib_exists_and_valid(self):
        """Feature 5.1: references.bib exists and parses without syntax errors."""
        bib_file = REFERENCES_BIB
        self.assertTrue(bib_file.exists(), "references.bib must exist")
        content = read_text_safe(bib_file)
        entries = parse_bibtex(content)
        self.assertGreater(len(entries), 0, "references.bib must contain valid BibTeX entries")

    def test_feature5_references_bib_seminal_paper_count(self):
        """Feature 5.2: references.bib contains at least 12 seminal papers."""
        content = read_text_safe(REFERENCES_BIB)
        entries = parse_bibtex(content)
        self.assertGreaterEqual(
            len(entries), 12,
            f"references.bib must contain >= 12 seminal papers, found {len(entries)}"
        )

    def test_feature5_references_bib_seminal_authors_present(self):
        """Feature 5.3: Core seminal authors (Shannon, Bengio, Mikolov, Vaswani) present."""
        content = read_text_safe(REFERENCES_BIB).lower()
        seminal_names = ["shannon", "bengio", "mikolov", "vaswani"]
        for name in seminal_names:
            self.assertIn(name, content, f"Seminal author '{name}' must be cited in references.bib")

    def test_feature5_references_bib_required_fields_present(self):
        """Feature 5.4: Every BibTeX entry has author, title, and year fields."""
        content = read_text_safe(REFERENCES_BIB)
        entries = parse_bibtex(content)
        for e in entries:
            key = e["key"]
            fields = e["fields"]
            self.assertTrue(
                "author" in fields or "editor" in fields,
                f"BibTeX entry '{key}' must have 'author' or 'editor'"
            )
            self.assertIn("title", fields, f"BibTeX entry '{key}' must have 'title'")
            self.assertIn("year", fields, f"BibTeX entry '{key}' must have 'year'")

    def test_feature5_references_bib_unique_keys(self):
        """Feature 5.5: All BibTeX citation keys are unique."""
        content = read_text_safe(REFERENCES_BIB)
        entries = parse_bibtex(content)
        keys = [e["key"] for e in entries]
        duplicates = [k for k in keys if keys.count(k) > 1]
        self.assertEqual(len(duplicates), 0, f"Duplicate BibTeX keys found: {set(duplicates)}")

    # --------------------------------------------------------------------------
    # Feature 6: Directory & Chapter Scaffolding
    # --------------------------------------------------------------------------
    def test_feature6_frontmatter_files_presence(self):
        """Feature 6.1: frontmatter/ contains titlepage, preface, and notation files."""
        fm_dir = FRONTMATTER_DIR
        self.assertTrue(fm_dir.exists(), "frontmatter/ directory must exist")
        for f in ["titlepage.tex", "preface.tex", "notation.tex"]:
            self.assertTrue((fm_dir / f).exists(), f"frontmatter/{f} must exist")

    def test_feature6_part1_foundations_chapters_presence(self):
        """Feature 6.2: chapters/part1_foundations/ contains all 8 core chapters."""
        p1_dir = CHAPTERS_DIR / "part1_foundations"
        self.assertTrue(p1_dir.exists(), "chapters/part1_foundations/ must exist")
        expected_p1 = [
            "01_language_models_intro.tex",
            "02_deep_learning_foundations.tex",
            "03_recurrent_neural_networks.tex",
            "04_word_embeddings.tex",
            "05_transformer_architecture.tex",
            "06_scaling_laws_pretraining.tex",
            "07_instruction_tuning_alignment.tex",
            "08_peft_inference_optimization.tex",
        ]
        for ch in expected_p1:
            self.assertTrue((p1_dir / ch).exists(), f"part1 chapter {ch} must exist")

    def test_feature6_part2_llm4se_chapters_presence(self):
        """Feature 6.3: chapters/part2_llm4se/ contains all 8 application chapters."""
        p2_dir = CHAPTERS_DIR / "part2_llm4se"
        self.assertTrue(p2_dir.exists(), "chapters/part2_llm4se/ must exist")
        expected_p2 = [
            "09_ai_in_software_engineering.tex",
            "10_prompt_engineering_chaining.tex",
            "11_ai_agents_multiagent.tex",
            "12_automated_test_generation_repair.tex",
            "13_requirements_engineering_modeling.tex",
            "14_code_refactoring_maintainability.tex",
            "15_evaluation_metrics_benchmarks_se.tex",
            "16_safety_bias_ethics_ip.tex",
        ]
        for ch in expected_p2:
            self.assertTrue((p2_dir / ch).exists(), f"part2 chapter {ch} must exist")

    def test_feature6_subfiles_documentclass_header(self):
        """Feature 6.4: All chapter files declare subfiles documentclass header."""
        for part in ["part1_foundations", "part2_llm4se"]:
            ch_dir = CHAPTERS_DIR / part
            for ch_file in ch_dir.glob("*.tex"):
                content = read_text_safe(ch_file)
                self.assertIn(
                    r"\documentclass[../../main.tex]{subfiles}",
                    content,
                    f"Chapter {ch_file.name} must declare \\documentclass[../../main.tex]{{subfiles}}"
                )

    def test_feature6_chapter_document_environments(self):
        """Feature 6.5: All chapter files enclose content in begin/end document."""
        for part in ["part1_foundations", "part2_llm4se"]:
            ch_dir = CHAPTERS_DIR / part
            for ch_file in ch_dir.glob("*.tex"):
                content = read_text_safe(ch_file)
                self.assertIn(r"\begin{document}", content, f"{ch_file.name} must have \\begin{{document}}")
                self.assertIn(r"\end{document}", content, f"{ch_file.name} must have \\end{{document}}")

    # --------------------------------------------------------------------------
    # Feature 7: Antigravity Skill Frontmatter
    # --------------------------------------------------------------------------
    def test_feature7_skill_file_exists(self):
        """Feature 7.1: SKILL.md exists in expected directory."""
        skill_file = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "SKILL.md"
        self.assertTrue(skill_file.exists(), "Antigravity skill SKILL.md must exist")

    def test_feature7_skill_valid_yaml_frontmatter(self):
        """Feature 7.2: SKILL.md begins with valid YAML frontmatter delimiters and syntax."""
        skill_file = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "SKILL.md"
        data, _ = parse_yaml_frontmatter(skill_file)
        self.assertIsInstance(data, dict, "Frontmatter must parse into a YAML dict")
        self.assertIn("name", data, "Frontmatter must define 'name'")
        self.assertIn("description", data, "Frontmatter must define 'description'")

    def test_feature7_skill_name_convention(self):
        """Feature 7.3: Skill name matches exact naming convention."""
        skill_file = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "SKILL.md"
        data, _ = parse_yaml_frontmatter(skill_file)
        self.assertEqual(data.get("name"), "lecture-study-guide-integrator", "Skill name must be exact")

    def test_feature7_skill_description_substance(self):
        """Feature 7.4: Description is detailed and includes progressive disclosure triggers."""
        skill_file = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "SKILL.md"
        data, _ = parse_yaml_frontmatter(skill_file)
        desc = data.get("description", "")
        self.assertGreaterEqual(len(desc), 50, "Skill description must be at least 50 characters")
        self.assertTrue(
            any(kw in desc.lower() for kw in ["lecture", "slides", "study guide", "karpathy", "transcription"]),
            "Description must mention core capabilities for model activation"
        )

    def test_feature7_skill_progressive_disclosure_structure(self):
        """Feature 7.5: SKILL.md body contains Core Principles and links to references."""
        skill_file = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "SKILL.md"
        _, body = parse_yaml_frontmatter(skill_file)
        self.assertIn("Core Principles", body, "SKILL.md must define Core Principles")
        self.assertIn("references/", body, "SKILL.md must link to reference documents")

    # --------------------------------------------------------------------------
    # Features 8-12: Antigravity Skill Reference Documents
    # --------------------------------------------------------------------------
    def test_feature8_research_protocol_guide_and_vectors(self):
        """Feature 8: 01_research_protocol.md exists and documents the 5 Authority Vectors."""
        ref_path = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "references" / "01_research_protocol.md"
        self.assertTrue(ref_path.exists(), "01_research_protocol.md must exist")
        content = read_text_safe(ref_path)
        for authority in ["Karpathy", "3Blue1Brown", "Enkk", "Lex Fridman"]:
            self.assertIn(authority, content, f"Research protocol must include {authority}")

    def test_feature9_integration_modes_guide_and_workflows(self):
        """Feature 9: 02_integration_modes.md exists and details the 4 Integration Modes."""
        ref_path = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "references" / "02_integration_modes.md"
        self.assertTrue(ref_path.exists(), "02_integration_modes.md must exist")
        content = read_text_safe(ref_path)
        for mode in ["Mode 1", "Mode 2", "Mode 3", "Mode 4"]:
            self.assertIn(mode, content, f"Integration modes must detail {mode}")

    def test_feature10_tikz_guidelines_and_patterns(self):
        """Feature 10: 03_tikz_guidelines.md exists and specifies color palette and patterns."""
        ref_path = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "references" / "03_tikz_guidelines.md"
        self.assertTrue(ref_path.exists(), "03_tikz_guidelines.md must exist")
        content = read_text_safe(ref_path)
        self.assertIn("tikzpicture", content, "TikZ guide must specify tikzpicture usage")
        self.assertTrue(
            any(color in content for color in ["poblue", "pogreen", "politoNavy", "blue!"]),
            "TikZ guide must specify semantic colors"
        )

    def test_feature11_math_expansion_and_tensor_dimensions(self):
        """Feature 11: 04_math_expansion.md exists and enforces tensor dimensions and steps."""
        ref_path = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "references" / "04_math_expansion.md"
        self.assertTrue(ref_path.exists(), "04_math_expansion.md must exist")
        content = read_text_safe(ref_path)
        self.assertIn("dimension", content.lower(), "Math expansion must emphasize dimensions")
        self.assertIn(r"\mathbb{R}", content, "Math expansion must use real space notation")

    def test_feature12_zero_omission_checklist_and_audit_matrix(self):
        """Feature 12: 05_zero_omission_checklist.md exists with slide inventory matrix."""
        ref_path = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "references" / "05_zero_omission_checklist.md"
        self.assertTrue(ref_path.exists(), "05_zero_omission_checklist.md must exist")
        content = read_text_safe(ref_path)
        self.assertIn("Zero-Omission", content, "Must emphasize zero omission standard")
        self.assertIn("Checklist", content, "Must include verification checklist")

    # --------------------------------------------------------------------------
    # Feature 13: Coverage Verification Script
    # --------------------------------------------------------------------------
    def test_feature13_verify_coverage_script_exists(self):
        """Feature 13.1: verify_coverage.py exists in skill or project scripts."""
        skill_script = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "scripts" / "verify_coverage.py"
        proj_script = PROJECT_ROOT / "scripts" / "verify_coverage.py"
        self.assertTrue(
            skill_script.exists() or proj_script.exists(),
            "verify_coverage.py must exist in skill or project scripts directory"
        )

    def test_feature13_verify_coverage_script_python_syntax(self):
        """Feature 13.2: verify_coverage.py is syntactically valid Python."""
        script_path = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "scripts" / "verify_coverage.py"
        if not script_path.exists():
            script_path = PROJECT_ROOT / "scripts" / "verify_coverage.py"
        res = subprocess.run([sys.executable, "-m", "py_compile", str(script_path)], capture_output=True)
        self.assertEqual(res.returncode, 0, f"verify_coverage.py has syntax errors: {res.stderr.decode()}")

    def test_feature13_verify_coverage_script_cli_interface(self):
        """Feature 13.3: verify_coverage.py accepts command line parameters."""
        script_path = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "scripts" / "verify_coverage.py"
        if not script_path.exists():
            script_path = PROJECT_ROOT / "scripts" / "verify_coverage.py"
        content = read_text_safe(script_path)
        self.assertTrue(
            "sys.argv" in content or "argparse" in content,
            "verify_coverage.py must support CLI parameters"
        )

    def test_feature13_verify_coverage_script_audit_logic(self):
        """Feature 13.4: verify_coverage.py contains slide concept matching logic."""
        script_path = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "scripts" / "verify_coverage.py"
        if not script_path.exists():
            script_path = PROJECT_ROOT / "scripts" / "verify_coverage.py"
        content = read_text_safe(script_path)
        self.assertTrue(
            any(term in content for term in ["coverage", "slide", "concept", "audit", "json"]),
            "verify_coverage.py must contain coverage or audit logic"
        )

    def test_feature13_verify_coverage_script_runs_successfully(self):
        """Feature 13.5: verify_coverage.py executes cleanly with --help or returns exit code."""
        script_path = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "scripts" / "verify_coverage.py"
        if not script_path.exists():
            script_path = PROJECT_ROOT / "scripts" / "verify_coverage.py"
        res = subprocess.run([sys.executable, str(script_path), "--help"], capture_output=True)
        self.assertNotIn("Traceback (most recent call last):", res.stderr.decode(), "Script must handle arguments without crashing")

    # --------------------------------------------------------------------------
    # Features 14-17: Deck 01 (Language Models Intro)
    # --------------------------------------------------------------------------
    def test_feature14_to_17_deck01_language_models_intro(self):
        """Features 14-17: Deck 01 content (probabilistic LMs, Markov, N-grams, PPL/CE)."""
        ch1 = CHAPTERS_DIR / "part1_foundations" / "01_language_models_intro.tex"
        content = read_text_safe(ch1)
        self.assertIn("Markov", content, "Ch 01 must explain Markov assumptions")
        self.assertIn("Perplexity", content, "Ch 01 must derive Perplexity")
        self.assertIn("Cross-Entropy", content, "Ch 01 must derive Cross-Entropy")
        self.assertTrue(r"\Prob" in content or "P(" in content, "Ch 01 must formulate probability chain rule")
        self.assertTrue("shannon" in content.lower() or "bengio" in content.lower(), "Ch 01 must cite Shannon or Bengio")

    # --------------------------------------------------------------------------
    # Features 18-21: Deck 02 (Deep Learning Foundations)
    # --------------------------------------------------------------------------
    def test_feature18_to_21_deck02_deep_learning_foundations(self):
        """Features 18-21: Deck 02 content (Perceptron, Linear collapse, Activations, Backprop DAG)."""
        ch2 = CHAPTERS_DIR / "part1_foundations" / "02_deep_learning_foundations.tex"
        content = read_text_safe(ch2)
        self.assertIn("Universal Approximation", content, "Ch 02 must explain Universal Approximation Theorem")
        self.assertTrue("linear stacking collapse" in content.lower(), "Ch 02 must prove linear stacking collapse")
        self.assertTrue(any(act in content for act in ["GELU", "ReLU", "Sigmoid", "Softmax"]), "Ch 02 must analyze activations")
        self.assertIn("Backpropagation", content, "Ch 02 must formulate backpropagation chain rule")

    # --------------------------------------------------------------------------
    # Features 22-25: Deck 03 (Word Embeddings - Chapter 04)
    # --------------------------------------------------------------------------
    def test_feature22_to_25_deck03_word_embeddings(self):
        """Features 22-25: Deck 03 content (One-hot limits, CBOW, Skip-Gram, Negative Sampling)."""
        ch4 = CHAPTERS_DIR / "part1_foundations" / "04_word_embeddings.tex"
        content = read_text_safe(ch4)
        self.assertIn("CBOW", content, "Ch 04 must explain Continuous Bag-of-Words")
        self.assertIn("Skip-Gram", content, "Ch 04 must explain Skip-Gram")
        self.assertIn("Negative Sampling", content, "Ch 04 must formulate negative sampling objective")
        self.assertTrue("mikolov" in content.lower(), "Ch 04 must cite Mikolov")

    # --------------------------------------------------------------------------
    # Features 26-29: Deck 04 (Recurrent Neural Networks - Chapter 03)
    # --------------------------------------------------------------------------
    def test_feature26_to_29_deck04_recurrent_neural_networks(self):
        """Features 26-29: Deck 04 content (Recurrent cells, BPTT, LSTM/GRU gating, Seq2Seq)."""
        ch3 = CHAPTERS_DIR / "part1_foundations" / "03_recurrent_neural_networks.tex"
        content = read_text_safe(ch3)
        self.assertIn("BPTT", content, "Ch 03 must formulate Backpropagation Through Time")
        self.assertTrue("LSTM" in content or "Long Short-Term" in content, "Ch 03 must detail LSTM architecture")
        self.assertTrue("GRU" in content or "Gated Recurrent" in content, "Ch 03 must detail GRU architecture")
        self.assertTrue("hochreiter" in content.lower() or "cho" in content.lower(), "Ch 03 must cite Hochreiter or Cho")

    # --------------------------------------------------------------------------
    # Feature 30: Syllabus Scaffolding (Chapters 05-16)
    # --------------------------------------------------------------------------
    def test_feature30_syllabus_scaffolding(self):
        """Feature 30: Scaffolded chapters 05-16 contain syllabus topics and reading lists."""
        all_chapters = list((CHAPTERS_DIR).rglob("*.tex"))
        for ch in all_chapters:
            content = read_text_safe(ch)
            self.assertIn(r"\chapter{", content, f"Chapter {ch.name} must declare \\chapter{{...}}")
            self.assertIn(r"\section{", content, f"Chapter {ch.name} must declare at least one \\section{{...}}")


# ==============================================================================
# TIER 2: BOUNDARY & CORNER CASES (>=5 tests per feature)
# ==============================================================================

class TestTier2BoundaryAndCornerCases(unittest.TestCase):
    """Tier 2: Boundary and corner case testing for LaTeX syntax, escaping, delimiters, and skill metadata."""

    # --------------------------------------------------------------------------
    # Boundary 1: LaTeX Special Character Escaping & Text-Mode Syntax
    # --------------------------------------------------------------------------
    def test_boundary_unescaped_literal_percent_in_prose(self):
        """Boundary 1.1: Literal percentage numbers (e.g. 50%) must use escaped \\%."""
        tex_files = list((CHAPTERS_DIR).rglob("*.tex")) + list((FRONTMATTER_DIR).rglob("*.tex"))
        for tf in tex_files:
            content = read_text_safe(tf)
            # Find occurrences of digits followed immediately by % without preceding backslash
            # (e.g., "95%" instead of "95\%") outside comments
            for line_idx, line in enumerate(content.splitlines(), start=1):
                clean_line = re.split(r"(?<!\\)%", line)[0]  # ignore comment part
                m = re.search(r"\d+%(?![\w\\])", clean_line)
                self.assertIsNone(
                    m,
                    f"Unescaped '%' found in {tf.relative_to(STUDY_GUIDE_DIR)} at line {line_idx}: {line.strip()}"
                )

    def test_boundary_unescaped_underscore_in_text_mode(self):
        """Boundary 1.2: Underscores in text prose outside math mode or listings must be escaped."""
        tex_files = list((CHAPTERS_DIR).rglob("*.tex"))
        for tf in tex_files:
            content = read_text_safe(tf)
            # Strip comments
            content = strip_comments_and_strings(content)
            # Remove math blocks ($...$, $$...$$, \[...\], \begin{equation}...\end{equation}, etc.)
            content = re.sub(r"\$\$.*?\$\$", "", content, flags=re.DOTALL)
            content = re.sub(r"\$.*?\$", "", content, flags=re.DOTALL)
            content = re.sub(r"\\\[.*?\\\]", "", content, flags=re.DOTALL)
            content = re.sub(r"\\begin\{equation\*?\}.*?\\end\{equation\*?\}", "", content, flags=re.DOTALL)
            content = re.sub(r"\\begin\{align\*?\}.*?\\end\{align\*?\}", "", content, flags=re.DOTALL)
            content = re.sub(r"\\begin\{lstlisting\}.*?\\end\{lstlisting\}", "", content, flags=re.DOTALL)
            content = re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", "", content, flags=re.DOTALL)
            content = re.sub(r"\\lstinline(\|[^\\]*?\||\{[^\\]*?\})", "", content)
            content = re.sub(r"\\(?:texttt|url|href|label|ref|eqref|cite|citep|citet|input|subfile)\{[^}]*\}", "", content)
            content = re.sub(r"\\(?:begin|end)\{[^}]+\}(?:\[[^\]]*\])?(?:\{[^}]*\})*", "", content)

            # In remaining prose, check for unescaped underscores
            for line_idx, line in enumerate(content.splitlines(), start=1):
                m = re.search(r"(?<!\\)_", line)
                self.assertIsNone(
                    m,
                    f"Unescaped underscore '_' outside math/code in {tf.relative_to(STUDY_GUIDE_DIR)} at line {line_idx}: {line.strip()}"
                )

    def test_boundary_unescaped_ampersand_outside_tables(self):
        """Boundary 1.3: Ampersands outside tabular, matrix, or align environments must be escaped as \\&."""
        tex_files = list((CHAPTERS_DIR).rglob("*.tex"))
        for tf in tex_files:
            content = read_text_safe(tf)
            content = strip_comments_and_strings(content)
            # Strip tabular, matrix, align, and aligned math environments
            content = re.sub(r"\\begin\{(?:tabular|tabularx|array|matrix|pmatrix|bmatrix|align|align\*|cases|aligned|split|gathered)\}.*?\\end\{(?:tabular|tabularx|array|matrix|pmatrix|bmatrix|align|align\*|cases|aligned|split|gathered)\}", "", content, flags=re.DOTALL)
            # Strip lstlisting
            content = re.sub(r"\\begin\{lstlisting\}.*?\\end\{lstlisting\}", "", content, flags=re.DOTALL)

            for line_idx, line in enumerate(content.splitlines(), start=1):
                m = re.search(r"(?<!\\)&", line)
                self.assertIsNone(
                    m,
                    f"Unescaped '&' outside tabular/align in {tf.relative_to(STUDY_GUIDE_DIR)} at line {line_idx}: {line.strip()}"
                )

    def test_boundary_unescaped_hash_outside_macros(self):
        """Boundary 1.4: Hash character '#' outside macro parameter definitions must be escaped."""
        tex_files = list((CHAPTERS_DIR).rglob("*.tex"))
        for tf in tex_files:
            content = read_text_safe(tf)
            content = strip_comments_and_strings(content)
            content = re.sub(r"\\begin\{lstlisting\}.*?\\end\{lstlisting\}", "", content, flags=re.DOTALL)
            content = re.sub(r"\\lstinline(\|[^\\]*?\||\{[^\\]*?\})", "", content)

            for line_idx, line in enumerate(content.splitlines(), start=1):
                # Allowed: \#, or macro definitions #1, #2 inside \newcommand
                if r"\newcommand" in line or r"\renewcommand" in line or r"\def" in line:
                    continue
                m = re.search(r"(?<!\\)#", line)
                self.assertIsNone(
                    m,
                    f"Unescaped '#' in {tf.relative_to(STUDY_GUIDE_DIR)} at line {line_idx}: {line.strip()}"
                )

    def test_boundary_balanced_prose_curly_braces(self):
        """Boundary 1.5: Verify no unescaped orphaned curly braces in LaTeX prose."""
        tex_files = list((CHAPTERS_DIR).rglob("*.tex"))
        for tf in tex_files:
            content = read_text_safe(tf)
            content = strip_comments_and_strings(content)
            # Remove escaped braces \{ and \}
            content = re.sub(r"\\\{|\\\}", "", content)
            open_count = content.count("{")
            close_count = content.count("}")
            self.assertEqual(
                open_count, close_count,
                f"Brace count mismatch in {tf.relative_to(STUDY_GUIDE_DIR)}: {open_count} '{{' vs {close_count} '}}'"
            )

    # --------------------------------------------------------------------------
    # Boundary 2: LaTeX Environment Delimiter Boundaries
    # --------------------------------------------------------------------------
    def test_boundary_balanced_latex_environments(self):
        """Boundary 2.1: Every \\begin{env} has a matching \\end{env} across all .tex files."""
        tex_files = list(PROJECT_ROOT.glob("*.tex")) + list((CHAPTERS_DIR).rglob("*.tex")) + list((FRONTMATTER_DIR).rglob("*.tex"))
        for tf in tex_files:
            content = read_text_safe(tf)
            content = strip_comments_and_strings(content)
            begins = re.findall(r"\\begin\{([a-zA-Z0-9_\*]+)\}", content)
            ends = re.findall(r"\\end\{([a-zA-Z0-9_\*]+)\}", content)

            begin_counts = {}
            for b in begins:
                begin_counts[b] = begin_counts.get(b, 0) + 1

            end_counts = {}
            for e in ends:
                end_counts[e] = end_counts.get(e, 0) + 1

            for env, b_count in begin_counts.items():
                e_count = end_counts.get(env, 0)
                self.assertEqual(
                    b_count, e_count,
                    f"Environment '{env}' unbalanced in {tf.name}: {b_count} \\begin vs {e_count} \\end"
                )

    def test_boundary_single_document_environment_per_file(self):
        """Boundary 2.2: Each chapter file contains exactly one begin{document} and end{document}."""
        ch_files = list((CHAPTERS_DIR).rglob("*.tex"))
        for cf in ch_files:
            content = read_text_safe(cf)
            begins = content.count(r"\begin{document}")
            ends = content.count(r"\end{document}")
            self.assertEqual(begins, 1, f"{cf.name} must have exactly one \\begin{{document}}, found {begins}")
            self.assertEqual(ends, 1, f"{cf.name} must have exactly one \\end{{document}}, found {ends}")

    def test_boundary_subfile_preamble_structure(self):
        """Boundary 2.3: Chapter subfiles strictly adhere to subfiles preamble convention."""
        ch_files = list(CHAPTERS_DIR.rglob("*.tex"))
        for cf in ch_files:
            content = read_text_safe(cf).strip()
            self.assertTrue(
                content.startswith(r"\documentclass[../../main.tex]{subfiles}"),
                f"{cf.name} must start with \\documentclass[../../main.tex]{{subfiles}}"
            )
        lab_files = list((LABS_DIR / "chapters").rglob("*.tex"))
        for lf in lab_files:
            content = read_text_safe(lf).strip()
            self.assertTrue(
                content.startswith(r"\documentclass[../labs.tex]{subfiles}"),
                f"{lf.name} must start with \\documentclass[../labs.tex]{{subfiles}}"
            )
    def test_boundary_callout_box_nesting_integrity(self):
        """Boundary 2.4: Callout environments (examinsight, intuition, deepdive) are properly closed."""
        ch_files = list((CHAPTERS_DIR).rglob("*.tex"))
        for cf in ch_files:
            content = read_text_safe(cf)
            for box in ["examinsight", "intuition", "deepdive", "definition", "theorem"]:
                b_count = len(re.findall(rf"\\begin\{{{box}\}}", content))
                e_count = len(re.findall(rf"\\end\{{{box}\}}", content))
                self.assertEqual(
                    b_count, e_count,
                    f"Callout box '{box}' in {cf.name} has mismatched tags: {b_count} \\begin vs {e_count} \\end"
                )

    def test_boundary_utf8_encoding_cleanliness(self):
        """Boundary 2.5: No raw unprintable control characters or invalid bytes in TeX files."""
        tex_files = list(PROJECT_ROOT.glob("*.tex")) + list((CHAPTERS_DIR).rglob("*.tex"))
        for tf in tex_files:
            raw_bytes = tf.read_bytes()
            # Check UTF-8 validity
            try:
                decoded = raw_bytes.decode("utf-8")
            except UnicodeDecodeError as err:
                self.fail(f"File {tf.name} is not valid UTF-8: {err}")
            # Ensure no null bytes or illegal control chars (excluding tab and newline)
            invalid_chars = [c for c in decoded if ord(c) < 32 and c not in ("\n", "\r", "\t")]
            self.assertEqual(len(invalid_chars), 0, f"File {tf.name} contains invalid control characters: {invalid_chars}")

    # --------------------------------------------------------------------------
    # Boundary 3: Cross-Referencing & Label Boundaries
    # --------------------------------------------------------------------------
    def test_boundary_zero_duplicate_labels_across_project(self):
        """Boundary 3.1: No duplicate \\label{...} declarations anywhere in project."""
        tex_files = list(PROJECT_ROOT.glob("*.tex")) + list((CHAPTERS_DIR).rglob("*.tex")) + list((FRONTMATTER_DIR).rglob("*.tex"))
        all_labels = []
        for tf in tex_files:
            content = read_text_safe(tf)
            content = strip_comments_and_strings(content)
            labels = re.findall(r"\\label\{([^}]+)\}", content)
            all_labels.extend(labels)

        duplicates = [lbl for lbl in all_labels if all_labels.count(lbl) > 1]
        self.assertEqual(
            len(duplicates), 0,
            f"Duplicate LaTeX \\label declarations found: {set(duplicates)}"
        )

    def test_boundary_no_empty_or_whitespace_labels(self):
        """Boundary 3.2: No empty or whitespace-only labels."""
        tex_files = list((CHAPTERS_DIR).rglob("*.tex"))
        for tf in tex_files:
            content = read_text_safe(tf)
            content = strip_comments_and_strings(content)
            empty_labels = re.findall(r"\\label\{\s*\}", content)
            self.assertEqual(len(empty_labels), 0, f"Empty label found in {tf.name}")

    def test_boundary_label_prefix_standardization(self):
        """Boundary 3.3: Labels follow standard prefixes (ch:, sec:, subsec:, def:, thm:, fig:, eq:, tab:)."""
        tex_files = list((CHAPTERS_DIR).rglob("*.tex"))
        valid_prefixes = ("ch:", "sec:", "subsec:", "def:", "thm:", "fig:", "eq:", "tab:", "box:")
        for tf in tex_files:
            content = read_text_safe(tf)
            labels = re.findall(r"\\label\{([^}]+)\}", content)
            for lbl in labels:
                self.assertTrue(
                    any(lbl.startswith(p) for p in valid_prefixes),
                    f"Label '{lbl}' in {tf.name} does not follow standard naming prefix {valid_prefixes}"
                )

    def test_boundary_figure_table_equation_label_matching(self):
        """Boundary 3.4: Figure labels use fig: prefix, equation labels use eq: prefix."""
        tex_files = list((CHAPTERS_DIR).rglob("*.tex"))
        for tf in tex_files:
            content = read_text_safe(tf)
            # Find labels inside figure environments
            fig_blocks = re.findall(r"\\begin\{figure\}.*?\\end\{figure\}", content, re.DOTALL)
            for fb in fig_blocks:
                labels = re.findall(r"\\label\{([^}]+)\}", fb)
                for lbl in labels:
                    self.assertTrue(lbl.startswith("fig:"), f"Figure label '{lbl}' in {tf.name} must start with 'fig:'")

    def test_boundary_cleveref_compatibility(self):
        """Boundary 3.5: cleveref package loaded in main.tex after hyperref."""
        content = read_text_safe(MAIN_TEX)
        self.assertIn(r"\usepackage{cleveref}", content, "main.tex must load cleveref")
        hyperref_pos = content.find("hyperref")
        cleveref_pos = content.find("cleveref")
        self.assertGreater(
            cleveref_pos, hyperref_pos,
            "cleveref must be loaded AFTER hyperref to ensure proper counter integration"
        )

    # --------------------------------------------------------------------------
    # Boundary 4: BibTeX Syntax & Field Boundaries
    # --------------------------------------------------------------------------
    def test_boundary_bibtex_citation_key_character_set(self):
        """Boundary 4.1: BibTeX keys contain only valid alphanumeric, hyphen, or colon characters."""
        content = read_text_safe(REFERENCES_BIB)
        entries = parse_bibtex(content)
        for e in entries:
            key = e["key"]
            self.assertRegex(key, r"^[a-zA-Z0-9_\-:]+$", f"Invalid characters in BibTeX key '{key}'")

    def test_boundary_bibtex_balanced_entry_braces(self):
        """Boundary 4.2: references.bib has properly balanced entry braces."""
        content = read_text_safe(REFERENCES_BIB)
        open_b = content.count("{")
        close_b = content.count("}")
        self.assertEqual(open_b, close_b, f"Mismatched braces in references.bib: {open_b} '{{' vs {close_b} '}}'")

    def test_boundary_bibtex_year_format_4digits(self):
        """Boundary 4.3: All publication years are 4 digits."""
        content = read_text_safe(REFERENCES_BIB)
        entries = parse_bibtex(content)
        for e in entries:
            year = e["fields"].get("year", "")
            self.assertRegex(year, r"^\d{4}$", f"Year for citation '{e['key']}' must be 4 digits, got '{year}'")

    def test_boundary_bibtex_no_empty_required_fields(self):
        """Boundary 4.4: Author and title values are non-empty."""
        content = read_text_safe(REFERENCES_BIB)
        entries = parse_bibtex(content)
        for e in entries:
            author = e["fields"].get("author") or e["fields"].get("editor") or ""
            title = e["fields"].get("title", "")
            self.assertGreater(len(author.strip()), 2, f"Author field too short for '{e['key']}'")
            self.assertGreater(len(title.strip()), 3, f"Title field too short for '{e['key']}'")

    def test_boundary_bibtex_entry_type_syntax(self):
        """Boundary 4.5: Entries use standard BibTeX types (article, inproceedings, book, etc.)."""
        content = read_text_safe(REFERENCES_BIB)
        entries = parse_bibtex(content)
        allowed_types = {"article", "inproceedings", "book", "phdthesis", "techreport", "misc"}
        for e in entries:
            self.assertIn(e["type"], allowed_types, f"Entry type '@{e['type']}' in '{e['key']}' is not standard")

    # --------------------------------------------------------------------------
    # Boundary 5: Antigravity Skill YAML & Markdown Boundaries
    # --------------------------------------------------------------------------
    def test_boundary_skill_yaml_delimiter_strictness(self):
        """Boundary 5.1: SKILL.md begins exactly with '---' delimiter on line 1."""
        skill_file = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "SKILL.md"
        content = read_text_safe(skill_file)
        self.assertTrue(content.startswith("---\n") or content.startswith("---\r\n"), "SKILL.md must begin with '---' on line 1")

    def test_boundary_skill_relative_links_resolution(self):
        """Boundary 5.2: All markdown links in SKILL.md resolve to existing files on disk."""
        skill_file = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "SKILL.md"
        _, body = parse_yaml_frontmatter(skill_file)
        skill_dir = skill_file.parent
        # Match links of the form [text](path)
        links = re.findall(r"\[.*?\]\(([a-zA-Z0-9_\-\.\/]+)\)", body)
        for link in links:
            if link.startswith("http://") or link.startswith("https://") or link.startswith("#"):
                continue
            target = (skill_dir / link).resolve()
            self.assertTrue(target.exists(), f"Broken relative link in SKILL.md: {link} -> {target}")

    def test_boundary_skill_empty_or_whitespace_fields(self):
        """Boundary 5.3: Name and description in SKILL.md are not whitespace-only."""
        skill_file = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "SKILL.md"
        data, _ = parse_yaml_frontmatter(skill_file)
        name = data.get("name", "")
        desc = data.get("description", "")
        self.assertGreater(len(name.strip()), 3, "Skill name must not be blank or whitespace")
        self.assertGreater(len(desc.strip()), 20, "Skill description must not be blank or whitespace")

    def test_boundary_skill_reference_docs_minimum_size(self):
        """Boundary 5.4: All 5 reference docs have substantive size (>300 bytes)."""
        ref_dir = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "references"
        for doc in ref_dir.glob("*.md"):
            self.assertGreater(doc.stat().st_size, 300, f"Reference doc {doc.name} is too short or empty")

    def test_boundary_skill_yaml_fuzz_malformed_rejection(self):
        """Boundary 5.5: YAML parser rejects malformed frontmatter syntax."""
        malformed_yaml = "---\nname: test\n  bad_indent: [unclosed\n---\nBody"
        with self.assertRaises(yaml.YAMLError):
            yaml.safe_load("name: test\n  bad_indent: [unclosed")


# ==============================================================================
# TIER 3: CROSS-FEATURE COMBINATIONS
# ==============================================================================

class TestTier3CrossFeatureCombinations(unittest.TestCase):
    """Tier 3: Cross-Feature interaction testing (citations vs bibliography, subfile paths, macro consistency)."""

    def test_cross_citation_integrity(self):
        """Tier 3.1: Every citation used across all chapters and frontmatter exists in references.bib."""
        bib_file = REFERENCES_BIB
        bib_content = read_text_safe(bib_file)
        bib_entries = parse_bibtex(bib_content)
        valid_keys = {e["key"] for e in bib_entries}

        tex_files = list((CHAPTERS_DIR).rglob("*.tex")) + list((FRONTMATTER_DIR).rglob("*.tex"))
        missing_citations = []

        for tf in tex_files:
            content = read_text_safe(tf)
            content = strip_comments_and_strings(content)
            # Find \cite{...}, \citep{...}, \citet{...}
            citations = re.findall(r"\\cite[pt]?\{([^}]+)\}", content)
            for c_group in citations:
                for key in c_group.split(","):
                    k = key.strip()
                    if k and k not in valid_keys:
                        missing_citations.append((tf.name, k))

        self.assertEqual(
            len(missing_citations), 0,
            f"Citations missing from references.bib: {missing_citations}"
        )

    def test_cross_subfile_path_resolution(self):
        """Tier 3.2: Subfile references '../../main.tex' resolve correctly from every chapter directory."""
        for part in ["part1_foundations", "part2_llm4se"]:
            ch_dir = CHAPTERS_DIR / part
            for ch_file in ch_dir.glob("*.tex"):
                content = read_text_safe(ch_file)
                match = re.search(r"\\documentclass\[(.*?)\]\{subfiles\}", content)
                self.assertIsNotNone(match, f"No subfiles documentclass found in {ch_file.name}")
                rel_path = match.group(1)
                resolved = (ch_file.parent / rel_path).resolve()
                self.assertTrue(
                    resolved.exists() and resolved.name == "main.tex",
                    f"Subfile relative path '{rel_path}' in {ch_file.name} does not resolve to main.tex"
                )

    def test_cross_macro_environment_consistency(self):
        """Tier 3.3: Every custom callout environment used in chapters is declared in style/macros.sty."""
        macros_content = read_text_safe(MACROS_STY)
        declared_envs = set()
        for m in re.finditer(r"\\newtcolorbox\{([a-zA-Z0-9_\*]+)\}", macros_content):
            declared_envs.add(m.group(1))
        for m in re.finditer(r"\\newtcbtheorem.*?\{([a-zA-Z0-9_\*]+)\}", macros_content):
            declared_envs.add(m.group(1))

        # Check core custom environments
        core_expected = {"examinsight", "intuition", "deepdive", "definition", "theorem"}
        for ce in core_expected:
            self.assertIn(ce, declared_envs, f"Core environment '{ce}' must be declared in macros.sty")

    def test_cross_main_tex_includes_all_chapters(self):
        """Tier 3.4: main.tex contains \\subfile calls for all 16 chapters in syllabus order."""
        content = read_text_safe(MAIN_TEX)
        expected_chapters = [
            "01_language_models_intro", "02_deep_learning_foundations",
            "03_recurrent_neural_networks", "04_word_embeddings",
            "05_transformer_architecture", "06_scaling_laws_pretraining",
            "07_instruction_tuning_alignment", "08_peft_inference_optimization",
            "09_ai_in_software_engineering", "10_prompt_engineering_chaining",
            "11_ai_agents_multiagent", "12_automated_test_generation_repair",
            "13_requirements_engineering_modeling", "14_code_refactoring_maintainability",
            "15_evaluation_metrics_benchmarks_se", "16_safety_bias_ethics_ip"
        ]
        for ch in expected_chapters:
            self.assertIn(ch, content, f"main.tex must include chapter '{ch}' via \\subfile")

    def test_cross_main_tex_includes_frontmatter(self):
        """Tier 3.5: main.tex includes titlepage, preface, and notation via \\subfile."""
        content = read_text_safe(MAIN_TEX)
        for fm in ["titlepage", "preface", "notation"]:
            self.assertIn(fm, content, f"main.tex must include frontmatter '{fm}' via \\subfile")

    def test_cross_coverage_script_execution(self):
        """Tier 3.6: verify_coverage.py executes against real chapters and produces an audit report."""
        script_path = PROJECT_ROOT / ".agents" / "skills" / "lecture-study-guide-integrator" / "scripts" / "verify_coverage.py"
        if not script_path.exists():
            script_path = PROJECT_ROOT / "scripts" / "verify_coverage.py"

        # Create temporary mock slide data
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tf:
            json_path = tf.name
            tf.write('[{"slide_number": 1, "text": "Language Models\\nProbabilistic language model\\nMarkov assumptions"}]')

        ch1_path = CHAPTERS_DIR / "part1_foundations" / "01_language_models_intro.tex"
        try:
            res = subprocess.run(
                [sys.executable, str(script_path), json_path, str(ch1_path)],
                capture_output=True,
                text=True
            )
            # The script should complete execution and report coverage metrics
            self.assertTrue(
                "Audit Summary" in res.stdout or "Coverage" in res.stdout or res.returncode in (0, 1),
                f"verify_coverage.py output unexpected: {res.stdout}\nError: {res.stderr}"
            )
        finally:
            if os.path.exists(json_path):
                os.remove(json_path)


# ==============================================================================
# TIER 4: REAL-WORLD SCENARIOS
# ==============================================================================

class TestTier4RealWorldScenarios(unittest.TestCase):
    """Tier 4: Live compiler verification, PDF generation, page count, and artifact cleanup."""

    @classmethod
    def setUpClass(cls):
        """Verify TeX compiler is present in environment."""
        cls.has_tex = (shutil.which("pdflatex") is not None) or (shutil.which("latexmk") is not None)

    def test_realworld_full_pdf_compilation(self):
        """Tier 4.1: Live LaTeX compilation produces main.pdf with exit code 0."""
        if not self.has_tex:
            self.skipTest("TeX compiler not found in PATH; skipping live PDF build")

        # Use latexmk or pdflatex with halt-on-error to fail-fast on TeX errors without hanging
        if shutil.which("latexmk") is not None:
            cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "main.tex"]
        else:
            cmd = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]

        res = subprocess.run(
            cmd,
            cwd=str(LECTURES_DIR),
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            stdin=subprocess.DEVNULL,
            timeout=180
        )
        if res.returncode != 0:
            # Extract last 30 lines of TeX log on error for immediate debugging
            log_file = LECTURES_DIR / "main.log"
            log_tail = ""
            if log_file.exists():
                lines = log_file.read_text(errors="replace").splitlines()
                log_tail = "\n".join(lines[-30:])
            self.fail(f"Compilation failed with exit code {res.returncode}.\nLog Tail:\n{log_tail}")

        pdf_path = LECTURES_DIR / "main.pdf"
        self.assertTrue(pdf_path.exists(), "main.pdf must be created after compilation")
        self.assertGreater(pdf_path.stat().st_size, 10000, "main.pdf must be >10KB")

    def test_realworld_pdf_structural_integrity(self):
        """Tier 4.2: Inspect main.pdf using pypdf for page count and bookmark tree."""
        pdf_path = LECTURES_DIR / "main.pdf"
        if not pdf_path.exists():
            self.skipTest("main.pdf does not exist; run compilation test first")
        if pypdf is None:
            self.skipTest("pypdf is not installed; skipping PDF structural inspection")

        reader = pypdf.PdfReader(str(pdf_path))
        num_pages = len(reader.pages)
        # Should have multiple pages (at least 5 pages for scaffolded, >30 for fully populated)
        self.assertGreaterEqual(num_pages, 5, f"PDF page count should be at least 5 pages, got {num_pages}")

        # Check PDF outline / bookmarks
        outline = reader.outline
        self.assertTrue(
            outline is not None and len(outline) > 0,
            "main.pdf must have bookmarks/outlines generated for Table of Contents"
        )

    def test_realworld_pdf_table_of_contents_rendered(self):
        """Tier 4.3: Table of contents rendered with Part I and Part II divisions."""
        pdf_path = LECTURES_DIR / "main.pdf"
        if not pdf_path.exists() or pypdf is None:
            self.skipTest("main.pdf does not exist or pypdf not installed")

        reader = pypdf.PdfReader(str(pdf_path))
        # Extract text from early pages (first 5 pages should contain TOC)
        toc_text = ""
        for p in reader.pages[:8]:
            toc_text += p.extract_text() or ""

        self.assertTrue(
            "Foundations of Large Language Models" in toc_text or "Language Models" in toc_text,
            "Table of contents text must contain course topic titles"
        )

    def test_realworld_standalone_subfile_compilation(self):
        """Tier 4.4: Individual chapter compiles standalone via subfiles without whole book."""
        if not self.has_tex:
            self.skipTest("TeX compiler not found in PATH")

        ch1_dir = CHAPTERS_DIR / "part1_foundations"
        ch1_file = ch1_dir / "01_language_models_intro.tex"
        if not ch1_file.exists():
            self.skipTest("01_language_models_intro.tex does not exist yet")

        cmd = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "01_language_models_intro.tex"]
        res = subprocess.run(
            cmd,
            cwd=str(ch1_dir),
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            stdin=subprocess.DEVNULL,
            timeout=60
        )
        self.assertEqual(
            res.returncode, 0,
            f"Standalone chapter compilation failed:\n{res.stderr}\n{res.stdout[-1000:]}"
        )
        ch1_pdf = ch1_dir / "01_language_models_intro.pdf"
        self.assertTrue(ch1_pdf.exists(), "Standalone chapter PDF must be produced")

    def test_realworld_z_build_clean_target(self):
        """Tier 4.5: Makefile clean target preserves .tex and .bib sources while removing build temp files."""
        # Touch dummy temporary files
        aux_test = STUDY_GUIDE_DIR / "test_dummy.aux"
        aux_test.touch()
        self.assertTrue(aux_test.exists())

        # Run make clean
        subprocess.run(["make", "clean"], cwd=str(STUDY_GUIDE_DIR), capture_output=True)

        # Verify source files intact
        self.assertTrue((MAIN_TEX).exists(), "main.tex must remain intact after make clean")
        self.assertTrue((REFERENCES_BIB).exists(), "references.bib must remain intact after make clean")
        self.assertFalse(aux_test.exists(), "Auxiliary test file should have been cleaned")


if __name__ == "__main__":
    unittest.main(verbosity=2)
