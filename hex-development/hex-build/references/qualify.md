# QUALIFY Stage

Qualification asks whether observed behavior satisfies the plan. It is independent of implementation confidence and has separate local and remote evidence.

## Evidence rules

- Re-read current files or remote state; do not rely on remembered output.
- Run validation fresh and capture command/observation, exit result, and meaningful outcome.
- Compare results to acceptance criteria, not merely test availability.
- A running service proves only process state; failed, blocked, and omitted checks remain visible.

## Local qualification

After APPLY, use maintained repository commands for targeted test, lint/format, typecheck, focused build/integration, smoke flow, end-to-end behavior, and security review as risk requires. Before PUBLISH inspect:

```text
git diff --check
git diff --stat
git diff
```

Do not proceed to PUBLISH after a validation failure unless the operator explicitly accepts the known failure and residual risk.

## Remote qualification

Run only after an explicitly authorized deployment. Minimum requirement:

```text
DEPLOYED_SHA == LOCAL_COMMIT
```

Then use repository/service-specific checks documented in PLAN, such as service active state, local health endpoint, HTTPS endpoint, authentication, persistence, intended user-visible path, or logs for new errors. Do not fabricate a generic check set when configuration lacks it.

## Status model

| Status | Meaning | Required evidence |
|---|---|---|
| `PASS` | Check ran/was observed and met its criterion. | command/observation plus result |
| `FAIL` | Check ran and did not meet its criterion. | failure evidence and affected criterion |
| `BLOCKED` | Check could not run because of external impediment. | blocker, attempt, unblocking need |
| `NOT RUN` | Check was omitted or inapplicable. | reason and residual risk |

## Failure handling and exit

For `FAIL`, classify intent/specification/implementation/environment before correction. Re-enter APPLY only inside existing authorization; changed scope returns to PLAN. For remote failure, use the approved rollback only if its remote mutation scope was authorized. Every applicable criterion maps to observed evidence or explicit gap before UNIFY.