# Public Customer Report Examples

This directory contains public example report packs for `project-readiness-auditor`.

Public examples are intentionally curated. They are not every report ever generated under
`reports/customer/`; they are the allowlisted packs that pass the strict public example
gate.

## Official Examples

| Report pack | What it demonstrates |
|---|---|
| [`recommender-systems-from-zero`](recommender-systems-from-zero/) | L2 educational ML/codebase audit with tests, imports, AST checks, and notebook metadata evidence. |
| [`hiking-route-recommender-demo`](hiking-route-recommender-demo/) | Current strict report format for a docs-vs-code static rerun with explicit validation basis and corrected bug-audit semantics. |
| [`mt5-research`](mt5-research/) | Path-redacted high-risk automation/trading research audit for a private MT5 research system. |

## Quality Bar

Each public report pack should include:

- `index.md`
- `code-only-project-readiness-YYYY-MM-DD.md`
- `project-readiness-YYYY-MM-DD.md`
- `bug-audit-YYYY-MM-DD.md`

Each report should state its validation basis, list exact commands or explicitly state that
no shell commands were run, separate missing evidence from bug candidates, and keep
readiness claims below the evidence collected.

## Validation

Run the official public example gate from the repository root:

```bash
python3 project-readiness-auditor/scripts/validate_skill.py project-readiness-auditor --strict-report-quality --public-report-examples --report-quality-summary
```

Expected result:

```text
QUALITY SUMMARY: no customer report-pack failures
RESULT: PASS L0
```
