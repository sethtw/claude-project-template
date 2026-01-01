#!/bin/bash
# Claude Code Project Startup Script
# Output is automatically added as context to the session

echo ""
echo "=============================================="
echo "  PROJECT COMMANDS"
echo "=============================================="
echo ""
echo "  SETUP & ANALYSIS"
echo "    /initialize  - First run: full codebase scan"
echo "    /analyze     - Analyze codebase patterns"
echo "    /context     - Show current memory state"
echo ""
echo "  DEVELOPMENT"
echo "    /architect   - Plan implementation (Opus)"
echo "    /implement   - Cost-optimized staged execution"
echo "    /tdd         - Test-driven development"
echo "    /refactor    - Multi-file refactoring"
echo ""
echo "  REVIEW"
echo "    /review      - Quick staged changes review"
echo "    /code-review - Full codebase review"
echo ""
echo "  OTHER"
echo "    /test-gen    - Generate tests for module"
echo "    /migrate     - Framework/version migration"
echo ""
echo "=============================================="

# Show git status if in a git repo
if git rev-parse --git-dir > /dev/null 2>&1; then
  echo ""
  echo "  Git: $(git branch --show-current 2>/dev/null || echo 'detached')"
  CHANGES=$(git status --porcelain 2>/dev/null | wc -l)
  if [ "$CHANGES" -gt 0 ]; then
    echo "  Changes: $CHANGES uncommitted files"
  else
    echo "  Changes: Clean"
  fi
fi

echo ""

exit 0
