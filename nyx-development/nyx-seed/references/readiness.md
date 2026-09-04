# Readiness Gate

## States

| State | Meaning | Exit condition |
|---|---|---|
| `IDEA` | Intent exists but problem, user, or outcome is still vague. | A concrete problem and desired outcome are stated. |
| `DISCOVERY` | Material facts and decisions are being gathered. | High-impact unknowns are resolved or explicitly bounded. |
| `SPECIFIED` | Goals, non-goals, requirements, constraints, and acceptance criteria are documented. | Architecture and first milestone can be planned. |
| `PLANNED` | A bounded first milestone and validation approach exist. | Every READY condition below passes. |
| `READY` | The first task can be implemented without inventing high-impact facts. | Separate execution authorization is obtained. |

Report exactly one current state. A project does not advance because time was spent on it; it advances when the exit condition is evidenced.

## READY conditions

All must pass:

- **Goal:** one clear outcome and intended user or operator.
- **Scope:** bounded requirements and named non-goals.
- **Acceptance:** observable behavior and failure expectations.
- **Architecture:** chosen, observed, or explicitly proposed with accepted assumptions.
- **Dependencies:** first-task dependencies are available or have a safe acquisition plan.
- **Security/privacy:** no unresolved trust, exposure, credential, or data blocker for the first task.
- **Operations:** deployment, migration, billing, and rollback questions that affect the first task are resolved.
- **Task boundary:** a small first milestone with expected files and validation exists.

## Assessment format

```markdown
## Readiness

**State:** READY | PLANNED | SPECIFIED | DISCOVERY | IDEA

| Condition | Result | Evidence or blocker |
|---|---|---|
| Goal | PASS | ... |
| Scope | PASS | ... |
| Acceptance | FAIL | `UNKNOWN` — ... |
```

Use `PASS`, `FAIL`, or `NOT APPLICABLE` per condition. `READY` requires no `FAIL`.

## Authorization boundary

`READY` means information is sufficient. It does not authorize:

- repository edits or file creation beyond the approved specification;
- commit, push, branch changes, reset, clean, or restore;
- deployment or service restart;
- credentials, spending, external messages, or remote mutation;
- destructive or security-reducing action.

The handoff must name the next proposed action and wait for its authorization.
