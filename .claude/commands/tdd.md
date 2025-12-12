# Description: Enforces strict Red-Green-Refactor cycle

You are a TDD Architect. Follow this strict cycle for the feature: "$ARGUMENTS"

Red (Test): Create a robust test file for "$ARGUMENTS". It must fail. Run the test to confirm failure.

Green (Implementation): Write the minimal code required to pass the test. Do not over-engineer. Run the test to confirm it passes.

Refactor (Optimize): Review the code for readability and performance. Refactor if necessary. Ensure tests still pass.

Done: Update .claude/memory/active_context.md with the result.
