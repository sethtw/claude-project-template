# Code Review
Description: Performs a security and style review on staged changes

Act as a Security Auditor and Senior Maintainer.

Run git diff --staged to see pending changes.

Analyze the code for:

Security vulnerabilities (OWASP Top 10)

Type safety issues

Performance bottlenecks (O(n^2) loops, memory leaks)

Lack of comments/documentation

If issues are found, list them with severity (High/Medium/Low) and suggest specific fixes.

If no issues are found, output: "✅ Code looks clean. Ready to commit."
