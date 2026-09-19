# UNIFY Stage

UNIFY closes the execution loop by reconciling approved plan with actual local, publication, and remote state. It is mandatory after APPLY begins, including `FAIL`, `BLOCKED`, and `CANCELLED` outcomes.

## Inputs and reconciliation

Use the approved contract/gates, current Git state, `LOCAL_COMMIT` when published, remote state when deployed, deviations, and local/remote qualification evidence. For every planned task and criterion record planned behavior/files, implemented behavior/files, observed status, authorization/deviation, and protected untouched work.

Use this shape:

```markdown
## Local implementation
- Changed files:
- Validation:
- Local SHA:

## Publication
- Commit:
- Remote:
- Branch:
- Pushed SHA:

## Deployment
- Target:
- Previous SHA:
- Deployed SHA:
- Service action:
- Remote checks:
```

If publication was not authorized, state `Publication: NOT RUN`. If deployment was not authorized, state `Deployment: NOT RUN`. Never imply publication means deployment.

## Closure states

| Closure | Meaning |
|---|---|
| `PASS` | Every required criterion for authorized scope has observed PASS evidence. |
| `FAIL` | Work ran but required criteria failed. |
| `BLOCKED` | Progress/proof cannot continue because of a named blocker. |
| `CANCELLED` | Authorized work stopped; implemented/recovery state is recorded. |

Code-only or publication-only scope can pass without deployment. A deployment-required scope cannot pass with required remote `BLOCKED`/`NOT RUN` checks.

## State and exit

Use repository-native artifacts first. If `.nyx/HANDOFF.md` is in scope, append `## Build Result`; never alter the handoff's original Goal/Scope/Non-Goals/Acceptance Criteria. Preserve `UNKNOWN` deployment facts and rollback state. Do not automatically commit, push, deploy, restart, close issues, or notify as part of UNIFY.