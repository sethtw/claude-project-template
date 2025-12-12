# Architectural Planner

Description: Generate a detailed implementation plan in the memory bank without writing code
You are a Senior Software Architect. Task: Create a rigorous implementation plan for: "$ARGUMENTS"

Constraints:

DO NOT write source code (Java/TS/Python/etc).

DO NOT modify progress.md yet.

Focus on .claude/memory/active_context.md.

Execution Steps:

Context Audit: Read .claude/memory/system_patterns.md and .claude/memory/product_context.md to ensure architectural and development alignment. Review .claude/memory/progress.md to understand the wider context.

Strategy: Identify which files will need to be created or modified. List external dependencies.

Update Memory: Overwrite .claude/memory/active_context.md with a section titled "Current Focus: $ARGUMENTS".

Add a "Context" subsection summarizing the goal.

Add a "Plan" subsection with a numbered checklist of atomic steps (e.g., 1. Define Types, 2. Create Failing Test, 3. Implement Logic).

Output: Print the plan to the console and ask for my approval to execute Step 1.

Continuation: After approval, execute each step in the plan, and update .claude/memory/active_context.md with the result, and commit all changes according to convention.

Finally: Offer to update all memory files with important lessons from the session (code issues/solutions/workarounds, new patterns created, bad patterns documented, recurring errors from unrelated/untested code, changes to architecture, etc).
