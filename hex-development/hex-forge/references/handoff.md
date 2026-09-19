# `.nyx/HANDOFF.md` Contract

Canonical schema for the repository-local project handoff. hex-forge owns writing it
(READINESS), validating it against fresh evidence (PLAN), and closing it (UNIFY) — all
within the same skill, so there is no cross-skill authority split to document.

## Purpose and scope

`.nyx/HANDOFF.md` lets a project survive across fresh Hermes sessions without the
operator re-pasting the conversation. It is a workflow artifact, not project
documentation and not implementation. Use it only with an identifiable
repository/project root; otherwise present the handoff in chat only and say so plainly.
Never force `.nyx/` into a directory that is not the project's own root.

## Files

- `.nyx/HANDOFF.md` — the single canonical active or most-recently-closed handoff.
- `.nyx/history/<ISO-8601-timestamp>-<slug-topic>.md` — archived handoffs, created only
  when a real handoff is actually being archived.

## Frontmatter schema

```yaml
---
version: 1
status: ACTIVE
source: hex-forge
created_at: <ISO-8601>
project_root: <absolute-or-repo-identified-path>
branch: <branch-or-NONE>
head: <commit-or-NONE>
working_tree: clean|dirty|unknown
readiness: IDEA|DISCOVERY|SPECIFIED|PLANNED|READY
topic: <short topic>
---
```

Frontmatter fields are not uniformly one evidence label. `branch`, `head`,
`working_tree`, and `project_root` are `OBSERVED` — read fresh from the repository
at write time, never carried over from earlier in the conversation. `created_at` is
a mechanically generated timestamp, not a claim needing a fact label. `topic`
reflects the operator's or session's own naming of the work (typically
`USER-STATED`, occasionally `PROPOSED` if the skill suggested a slug the operator
accepted). `readiness` and `status` are workflow-state classifications governed by
their own defined vocabularies (`references/readiness.md`, `references/unify.md`),
not entries in the six-label fact model — do not force them into
`USER-STATED`/`OBSERVED`/etc.

## Body sections

```markdown
# Nyx Handoff

## Goal
## Scope
## Non-Goals
## Established Facts   (USER-STATED | OBSERVED | ASSUMED | PROPOSED | UNKNOWN | CONTRADICTORY only)
## Decisions
## Architecture / Constraints
## Expected Files
## Acceptance Criteria
## Validation
## Safety Boundaries
## Unknowns / Blockers

## Build Instruction
PLAN first. STOP for operator approval before APPLY.
```

Keep it compact. No raw conversation dumps, environment variables, secrets, tokens,
credentials, private keys, or giant logs. Link to `docs/PROJECT.md` rather than
duplicating it. APPLY appends `## Build Plan Amendments` (operator-approved refinements
only); UNIFY appends `## Build Result` (below). Neither rewrites the original
Goal/Scope/Non-Goals/Acceptance Criteria.

## Deployment addition

A deployment-capable PLAN/APPLY may append this section without rewriting the original
Goal/Scope/Non-Goals/Acceptance Criteria:

```markdown
## Deployment

mode: none|git-checkout|artifact|container|unknown
target: UNKNOWN
remote: UNKNOWN
branch: UNKNOWN
production_path: UNKNOWN
service: UNKNOWN
health_check: UNKNOWN
rollback: UNKNOWN
```

`mode` is PLAN classification; other fields are `OBSERVED`, `USER-STATED`, or `UNKNOWN`.
Resolve required high-impact fields before proposing DEPLOY approval; never infer a
procedure from this section. A task is not deployment-ready while required high-impact
deployment fields are unresolved.

## Status lifecycle

| Status | Set during | Meaning |
|---|---|---|
| `ACTIVE` | READINESS/HANDOFF | Ready to continue into PLAN, same or fresh session. |
| `PLANNED` | PLAN | Produced and validated against repo evidence; awaiting APPLY. |
| `IN_PROGRESS` | APPLY | Operator approved; APPLY has started. |
| `PASS`/`FAIL`/`BLOCKED`/`CANCELLED` | UNIFY | Closure state — see `references/unify.md`. |
| `SUPERSEDED` | READINESS (next run) | Set only when explicitly archiving a still-relevant-but-replaced handoff. |

`SUPERSEDED` is set only during a new READINESS write, never during UNIFY.

## Conflict check (performed before writing a new ACTIVE handoff)

1. Read current `.nyx/HANDOFF.md` frontmatter `status`, if the file exists.
2. `ACTIVE`, `PLANNED`, or `IN_PROGRESS` → **STOP**. Report topic, status, age; ask
   whether to archive before proceeding. Never overwrite silently.
3. `PASS`, `FAIL`, `BLOCKED`, `CANCELLED`, or `SUPERSEDED` → archive (below), then write
   the new `ACTIVE` handoff.

## Archiving convention

`.nyx/HANDOFF.md` always holds the latest handoff — active or most recently completed.
UNIFY does **not** move it to history; it only updates status and appends `## Build
Result`. Archiving happens immediately before writing a new `ACTIVE` handoff over a
completed one:

1. Copy the current `.nyx/HANDOFF.md` to
   `.nyx/history/<ISO-8601-timestamp>-<slug-topic>.md`.
2. Write the new handoff to `.nyx/HANDOFF.md`.

## Build Result section (appended at UNIFY)

```markdown
## Build Result

status: PASS|FAIL|BLOCKED|CANCELLED

### Implemented
### Changed Files
### Verification
### Deviations
### Residual Risk
### Next Recommended Action
```

No large logs. Evidence-backed statuses only — see `references/qualify.md` and
`references/unify.md`.

## Tracking policy

Normally **tracked** in Git: it records project intent and task specification, enables
reproducible continuation, and creates an auditable phase history. Do not force this if
it conflicts with an existing repository convention the operator states. Never `git
add`/commit/push automatically; normal operator Git policy applies. Never place secrets,
tokens, credentials, private keys, or raw environment dumps in `.nyx/`.

## Validation against repository evidence (performed at PLAN)

Compare handoff frontmatter/content to freshly observed evidence:

| Class | Meaning |
|---|---|
| `MATCH` | Agrees with fresh evidence. |
| `STALE` | Low-impact divergence; note in PLAN and continue. |
| `CONTRADICTORY` | High-impact divergence (security, architecture, credentials, exposure, data, acceptance, deployment target); **STOP** before PLAN. |
| `UNKNOWN` | Cannot currently be checked. |

## Readiness distinction

Distinguish project-wide readiness (the handoff's `readiness` field) from bounded-task
readiness (whether *this* first task can be safely implemented). A project at `PLANNED`
can still contain a task that is ready for implementation. Do not reject a safe bounded
task merely because unrelated future work remains `UNKNOWN`. Do not proceed when an
`UNKNOWN` materially affects this task's security, architecture, credentials, exposure,
data handling, or acceptance criteria.
