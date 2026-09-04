# APPLY Stage

## Entry conditions

- The current plan or named subset has explicit authorization.
- The plan still matches current repository state.
- Required dependencies and recovery steps are available.

## Execution discipline

1. Reconfirm the target file before each edit and preserve repository conventions.
2. Make the smallest coherent change that can satisfy the current acceptance criteria.
3. Use `patch` for targeted edits and `write_file` for intentional complete-file creation or replacement.
4. Keep unrelated modifications, formatting, generated files, and refactors out of the diff.
5. Record unexpected discoveries, decisions, and deviations as they occur.
6. After each coherent slice, inspect the resulting diff/state before widening work.

## Divergence gate

Stop when any of these occurs:

- an expected file, API, dependency, or invariant does not exist;
- implementation requires touching an excluded or unrelated area;
- the security, data, deployment, credential, billing, or rollback model changes;
- acceptance criteria cannot be met as written;
- repository state changed concurrently or ownership is unclear.

Classify before continuing:

| Class | Meaning | Response |
|---|---|---|
| Intent | The requested outcome is wrong or changed. | Return to task definition and obtain a new decision. |
| Specification | Acceptance or plan omitted/misstated required behavior. | Revise the plan and approval boundary. |
| Implementation | The plan is sound but the change is incorrect. | Correct inside approved scope, then qualify. |
| Environment | Tooling, permissions, dependency, or runtime blocks proof. | Report evidence and recovery options; do not fake progress. |

## Mutation boundaries

- No commit, push, branch switch, reset, clean, restore, deploy, restart, migration, or external write unless separately authorized.
- Never discard unrelated work.
- Never expose secrets in command arguments, logs, files, or summaries.
- Never bypass TLS, host verification, authorization, approvals, or security controls.
- For an authorized external write, read back the exact target before claiming success.

## Exit condition

APPLY ends when the approved change is implemented, or when it is honestly `BLOCKED` or `CANCELLED`. Execution then moves to QUALIFY; even a blocked/cancelled execution must proceed to UNIFY for closure.
