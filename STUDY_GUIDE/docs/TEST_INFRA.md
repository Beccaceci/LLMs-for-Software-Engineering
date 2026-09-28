# Test Infrastructure and E2E Quality Assurance Architecture

## 1. Executive Summary & Testing Philosophy

This document defines the End-to-End (E2E) testing framework, testing philosophy, and verification matrix for the publication-grade LaTeX study guide and custom Antigravity skill developed for the Master's degree course *"Large Language Models for Software Engineering"* at Politecnico di Torino (taught by Prof. Flavio Giobergia and Prof. Riccardo Coppola).

### Core Testing Invariants
1. **Opaque-Box Verification**: The test suite evaluates deliverables strictly through external interfaces, contract compliance, structural assertions, syntax parsers, and live compilation runs without relying on internal mock facades.
2. **Pedagogical & Mathematical Completeness**: Every concept, formula, table, callout box, and citation demanded by the course syllabus and reference materials (`ORIGINAL_REQUEST.md`, `PROJECT.md`, `SLIDES/`) is systematically validated.
3. **No Facade / No Mock Testing**: Tests do not use superficial return-true stubs. They parse real `.tex` files, validate real BibTeX entries, parse real YAML frontmatter via `yaml.safe_load`, invoke real compiler binaries (`latexmk`, `pdflatex`, `bibtex`), and inspect real compiled PDF objects via `pypdf`.
4. **Progressive Testability & Graceful Diagnostics**: Tests provide precise diagnostic messages upon assertion failure, identifying exact line numbers, missing tokens, unclosed environments, or compile exit codes to facilitate immediate remediation.

---

## 2. Test Suite Architecture

```
/Users/nicolabeccaceci/Desktop/LLMs/
├── TEST_INFRA.md                          # Testing philosophy, architecture, and feature matrix
├── TEST_READY.md                          # Test suite execution instructions and coverage status
├── tests/
│   ├── test_study_guide_e2e.py            # Comprehensive 4-Tier test suite (Pytest + Unittest)
│   └── run_all_tests.sh                   # Unified test runner with colorized summary output
```

The test runner `tests/test_study_guide_e2e.py` is written in standard Python 3 utilizing `unittest.TestCase` conventions, making it fully compatible with both:
- `pytest -v tests/test_study_guide_e2e.py`
- `python3 -m unittest discover -s tests -v`
- `./tests/run_all_tests.sh`

---

## 3. Four-Tier Testing Methodology

The test suite is structured into four distinct verification tiers:

```
+-------------------------------------------------------------------------------+
| Tier 4: Real-World Scenarios                                                  |
| - Full PDF compilation (latexmk -pdf) -> Exit code 0                          |
| - PDF page count (>30 pages) & bookmark validation via pypdf                  |
| - Standalone subfile chapter compilation                                      |
| - Build clean target and idempotent artifact cleanup                          |
+---------------------------------------+---------------------------------------+
                                        ^
+---------------------------------------+---------------------------------------+
| Tier 3: Cross-Feature Combinations                                            |
| - Citation Cross-Validation: Every \cite / \citep in chapters -> references.bib|
| - Subfile Standalone Compatibility: Chapters correctly import ../../main.tex  |
| - Macro Environment Consistency: Chapters use declared tcolorbox macros       |
| - Automated Coverage Script execution against real chapter content            |
+---------------------------------------+---------------------------------------+
                                        ^
+---------------------------------------+---------------------------------------+
| Tier 2: Boundary & Corner Cases                                               |
| - LaTeX Escaping: Proper escaping of %, _, &, # outside math/listings         |
| - Delimiter Balancing: Exact match for \begin{...} and \end{...}              |
| - Label Uniqueness: No duplicated \label{...} across entire codebase           |
| - BibTeX Syntax Integrity: Required fields (author, title, year), balanced {} |
| - Skill Frontmatter Boundaries: Strict YAML parsing, description length > 50   |
+---------------------------------------+---------------------------------------+
                                        ^
+---------------------------------------+---------------------------------------+
| Tier 1: Feature Coverage (>=5 test cases per feature)                         |
| - Project Deliverables & Layout: main.tex, Makefile, .latexmkrc, frontmatter  |
| - Macros & Math Foundation: macros.sty, standard notation, math operators     |
| - Specialized Callout Boxes: examinsight, intuition, deepdive, def, thm       |
| - Master Bibliography: 12+ seminal papers cited in course syllabus            |
| - Chapter Hierarchy: 16 chapters partitioned across Part 1 and Part 2         |
| - Antigravity Skill: SKILL.md, 5 reference guides, verify_coverage.py script  |
+-------------------------------------------------------------------------------+
```

---

## 4. Feature Inventory & Test Coverage Matrix

Every feature defined in `PROJECT.md § Feature Inventory` is mapped to explicit test cases:

| # | Feature Name | Mapped Milestone | Test Class & Method in `test_study_guide_e2e.py` | Tier |
|---|--------------|------------------|--------------------------------------------------|------|
| 1 | TeX Book Layout & Typography | M1 | `TestTier1FeatureCoverage.test_feature1_main_tex_*` (5 tests) | 1 |
| 2 | Macro & Math Foundation | M1 | `TestTier1FeatureCoverage.test_feature2_macros_sty_*` (5 tests) | 1 |
| 3 | Specialized Callout Boxes | M1 | `TestTier1FeatureCoverage.test_feature3_callout_boxes_*` (5 tests) | 1 |
| 4 | Build Engine & Automation | M1 | `TestTier1FeatureCoverage.test_feature4_build_automation_*` (5 tests) | 1 |
| 5 | Master Bibliography | M1 | `TestTier1FeatureCoverage.test_feature5_references_bib_*` (5 tests) | 1 |
| 6 | Directory & Chapter Scaffolding | M1 | `TestTier1FeatureCoverage.test_feature6_chapter_scaffolding_*` (5 tests) | 1 |
| 7 | Antigravity Skill Frontmatter | M2 | `TestTier1FeatureCoverage.test_feature7_skill_frontmatter_*` (5 tests) | 1 |
| 8 | Pre-Ingestion Research Protocol | M2 | `TestTier1FeatureCoverage.test_feature8_research_protocol_*` (5 tests) | 1 |
| 9 | 4-Mode Integration Workflows | M2 | `TestTier1FeatureCoverage.test_feature9_integration_modes_*` (5 tests) | 1 |
| 10 | TikZ Diagram Guidelines | M2 | `TestTier1FeatureCoverage.test_feature10_tikz_guidelines_*` (5 tests) | 1 |
| 11 | Math Derivation Guidelines | M2 | `TestTier1FeatureCoverage.test_feature11_math_expansion_*` (5 tests) | 1 |
| 12 | Zero-Omission Audit Matrix | M2 | `TestTier1FeatureCoverage.test_feature12_zero_omission_checklist_*` (5 tests) | 1 |
| 13 | Coverage Verification Script | M2 | `TestTier1FeatureCoverage.test_feature13_verify_coverage_script_*` (5 tests) | 1 |
| 14-29 | Slide Content Decks 01-04 (LMs, DL, Embeddings, RNNs) | M3 | `TestTier1FeatureCoverage.test_feature14_to_29_slide_content_*` | 1 |
| 30 | Syllabus Scaffolding (Chapters 05-16) | M3 | `TestTier1FeatureCoverage.test_feature30_syllabus_scaffolding_*` | 1 |
| 31 | Full LaTeX Compilation & PDF Output | M4 | `TestTier4RealWorldScenarios.test_full_pdf_compilation_*` | 4 |
| 32 | E2E Requirement & Skill Verification | M4 | `TestTier2BoundaryAndCornerCases`, `TestTier3CrossFeatureCombinations` | 2, 3 |

---

## 5. Detailed Test Specifications by Tier

### Tier 1: Feature Coverage (Minimum 5 tests per feature)
- **Feature 1 (Layout & Typography)**: Validates `main.tex` presence, `\documentclass[...]{book}`, font loading (`newpxtext`, `newpxmath`, `sourcecodepro`), geometry margins (`25mm`), and document structure divisions (`\frontmatter`, `\mainmatter`, `\backmatter`).
- **Feature 2 (Macros & Math Notation)**: Validates `style/macros.sty` presence, mathematical operators (`\softmax`, `\sigmoid`, `\relu`, `\gelu`), expectation and norm macros (`\E`, `\norm`, `\Loss`), vector/matrix formatting (`\vx`, `\mW`), and SE metrics (`\PassAtK`, `\CodeBLEU`).
- **Feature 3 (Specialized Callout Boxes)**: Validates definitions of `examinsight`, `intuition`, `deepdive`, `definition`, and `theorem`, complete with fontawesome icons, breakable properties, and PoliTo color palette.
- **Feature 4 (Build Engine)**: Validates `Makefile` and `.latexmkrc` targets (`all`, `pdf`, `clean`, `pdflatex`), latexmk configuration parameters (`$pdf_mode = 1`), and executable `scripts/compile.sh`.
- **Feature 5 (Master Bibliography)**: Validates `references.bib` existence, valid BibTeX syntax, minimum count >= 12 seminal references, presence of seminal authors (Shannon, Bengio, Mikolov, Hochreiter, Cho, Vaswani), and required BibTeX fields.
- **Feature 6 (Directory & Chapter Scaffolding)**: Validates presence of `frontmatter/` (3 files), all 8 chapters in `chapters/part1_foundations/`, and all 8 chapters in `chapters/part2_llm4se/`.
- **Feature 7 (Skill Frontmatter)**: Validates `SKILL.md` presence, YAML frontmatter tags (`---`), `name: lecture-study-guide-integrator`, description length >= 50 characters, and progressive disclosure architecture.
- **Features 8-12 (Reference Docs)**: Validates existence and structural sections for `01_research_protocol.md` (5 authority vectors), `02_integration_modes.md` (4 modes), `03_tikz_guidelines.md` (PoliTo color palette), `04_math_expansion.md` (tensor dimensions), and `05_zero_omission_checklist.md` (audit matrix).
- **Feature 13 (Coverage Script)**: Validates `scripts/verify_coverage.py` existence, python compilation check, executable flags, CLI help output, and audit logic.

### Tier 2: Boundary & Corner Cases (Minimum 5 tests per feature)
- **LaTeX Escaping & Syntax Boundaries**:
  - `test_unescaped_percent_in_prose`: Verifies `%` is escaped as `\%` when used as a literal character in text rather than initiating an unclosed comment.
  - `test_unescaped_underscore_in_text`: Verifies `_` is not used in text mode outside `\texttt{...}`, `\lstinline{...}`, or math mode (`$ ... $`).
  - `test_unescaped_ampersand`: Verifies `&` is escaped as `\&` when not used as table/alignment separator.
  - `test_balanced_latex_environments`: Verifies every `\begin{XYZ}` has a corresponding `\end{XYZ}` across all `.tex` files.
  - `test_label_uniqueness`: Verifies zero duplicate `\label{...}` entries across the entire project.
  - `test_bibtex_key_validity_and_uniqueness`: Verifies all BibTeX keys follow alphanumeric identifier conventions with zero duplicates.
- **Skill Frontmatter & Markdown Boundaries**:
  - `test_strict_yaml_parsing`: Verifies YAML frontmatter parses strictly via `yaml.safe_load`.
  - `test_progressive_disclosure_links`: Extracts all markdown links (`[text](references/...)`) from `SKILL.md` and verifies target files exist.
  - `test_empty_or_whitespace_skill_fields`: Verifies `name` and `description` contain non-whitespace, non-dummy values.
  - `test_invalid_yaml_rejection`: Injects malformed YAML into an in-memory parser to verify parser rejection semantics.

### Tier 3: Cross-Feature Combinations
- **Citation Cross-Validation**: Extracts all `\cite{...}`, `\citep{...}`, and `\citet{...}` instances in all chapters and cross-checks them against keys in `references.bib`.
- **Subfile Standalone Contract**: Verifies every chapter file begins with `\documentclass[../../main.tex]{subfiles}` and can locate the root document relative to its location.
- **Callout Box Environment Consistency**: Verifies every chapter calling `\begin{examinsight}`, `\begin{intuition}`, etc., has `style/macros.sty` loaded via root or subfile preamble.
- **Coverage Script Integration**: Executes `verify_coverage.py` against sample slide data and verifies that missing topics trigger non-zero exit codes while full coverage yields exit code 0.

### Tier 4: Real-World Scenarios
- **Full PDF Compilation**: Runs `latexmk -pdf -interaction=nonstopmode main.tex` (or `make pdf`), verifying exit code 0 and non-empty output `main.pdf`.
- **PDF Structural Quality Check**: Uses `pypdf` to inspect `main.pdf`:
  - Page count verification (confirms non-trivial volume).
  - Bookmark / Outline verification (confirms Table of Contents entries for Part I, Part II, and chapters exist in the PDF tree).
  - Metadata verification (Title and Author are properly embedded).
- **Standalone Chapter Compilation**: Compiles a single chapter (e.g. `chapters/part1_foundations/01_language_models_intro.tex`) in isolation to verify modular subfile capability.
- **Build Target Cleanliness**: Runs `make clean` and verifies auxiliary files are pruned while primary source files remain intact.

---

## 6. Execution Instructions

### Prerequisites
- Python 3.10+
- `pytest` (`pip install pytest`)
- `pyyaml` (`pip install pyyaml`)
- `pypdf` (`pip install pypdf`)
- TeX Live 2026 (`latexmk`, `pdflatex`, `bibtex`)

### Running the Test Suite
```bash
# Method 1: Using pytest
pytest -v tests/test_study_guide_e2e.py

# Method 2: Using python unittest runner
python3 -m unittest discover -s tests -v

# Method 3: Using the unified shell runner
chmod +x tests/run_all_tests.sh
./tests/run_all_tests.sh
```

---

## 7. Quality Gates & Acceptance Thresholds

| Quality Gate | Minimum Acceptable Threshold | Enforcement Mechanism |
|---|---|---|
| Tier 1 Feature Tests | 100% Pass | `pytest tests/test_study_guide_e2e.py -k TestTier1` |
| Tier 2 Boundary Tests | 100% Pass (0 unescaped chars, 0 duplicate labels) | `pytest tests/test_study_guide_e2e.py -k TestTier2` |
| Tier 3 Cross-Feature Tests | 100% Citation Resolution (0 broken references) | `pytest tests/test_study_guide_e2e.py -k TestTier3` |
| Tier 4 Real-World Tests | Exit Code 0, Valid `main.pdf` generated | `pytest tests/test_study_guide_e2e.py -k TestTier4` |
| Zero Omission Check | 100% Concept Coverage against Slide Inventory | `verify_coverage.py` |
