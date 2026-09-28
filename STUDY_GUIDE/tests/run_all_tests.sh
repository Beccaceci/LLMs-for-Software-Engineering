#!/usr/bin/env bash
# ==============================================================================
# Unified End-to-End Test Runner for Politecnico di Torino LLM Study Guide
# ==============================================================================

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

# Add MacTeX bin to PATH if installed
if [ -d "/Library/TeX/texbin" ]; then
    export PATH="/Library/TeX/texbin:${PATH}"
fi

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${BLUE}${BOLD}==============================================================================${NC}"
echo -e "${BLUE}${BOLD}  LLM4SE Study Guide & Antigravity Skill: End-to-End Verification Runner      ${NC}"
echo -e "${BLUE}${BOLD}==============================================================================${NC}"
echo -e "Project Root: ${PROJECT_ROOT}"
echo -e "Python Path:  $(which python3)"
echo -e "TeX Engine:   $(which latexmk 2>/dev/null || which pdflatex 2>/dev/null || echo 'Not Found')"
echo ""

# Check python dependencies
echo -e "${BOLD}[1/4] Checking Test Environment Prerequisites...${NC}"
python3 -c "import yaml" 2>/dev/null || {
    echo -e "${RED}[ERROR] PyYAML not installed. Run: pip install pyyaml${NC}"
    exit 1
}
python3 -c "import pypdf" 2>/dev/null || {
    echo -e "${YELLOW}[WARNING] pypdf not installed. PDF structural inspections will be skipped.${NC}"
}
echo -e "${GREEN}[OK] Python prerequisites satisfied.${NC}"
echo ""

# Run test suite
echo -e "${BOLD}[2/4] Executing Comprehensive 4-Tier Test Suite...${NC}"

if command -v pytest >/dev/null 2>&1; then
    echo -e "${BLUE}Running via Pytest...${NC}"
    pytest -v tests/test_study_guide_e2e.py "$@"
    TEST_EXIT_CODE=$?
else
    echo -e "${BLUE}Pytest not found, running via standard unittest...${NC}"
    python3 -m unittest discover -s tests -p "test_*.py" -v
    TEST_EXIT_CODE=$?
fi

echo ""
echo -e "${BOLD}[3/4] Test Suite Execution Completed.${NC}"

if [ ${TEST_EXIT_CODE} -eq 0 ]; then
    echo -e "${GREEN}${BOLD}SUCCESS: All active E2E tests passed cleanly!${NC}"
else
    echo -e "${RED}${BOLD}FAILURE: One or more E2E test cases failed (exit code ${TEST_EXIT_CODE}).${NC}"
fi

echo -e "${BLUE}${BOLD}==============================================================================${NC}"
exit ${TEST_EXIT_CODE}
