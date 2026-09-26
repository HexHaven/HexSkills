# `.nyx/HANDOFF.md` Contract

Canonical schema for an optional repository-local project handoff. With repository
write authorization, hex-forge creates it and keeps its intent sections; hex-build
validates it against fresh evidence at PLAN, updates status, and appends the Build
Result at UNIFY. Both follow this one contract.

## Purpose and scope

`.nyx/HANDOFF.md` lets a project survive across fresh Hermes sessions without the
operator re-pasting the conversation. It is a workflow artifact, not project
documentation and not implementation. Use it only with an identifiable
repository/project root; otherwise present the handoff in chat only and say so plainly.
Never force `.nyx/` into a directory that is not the project's own root. Do not
create this file just to advance a phase: first confirm the repository convention
and obtain authorization for the record. If absent or not authorized, retain state
in conversation and present a paste-ready handoff when requested. Once authorized,
routine updates within the agreed scope need no new approval; replacing a different
active handoff still requires the conflict decision below.

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
their own defined vocabularies (`references/readiness.md`, hex-build `references/unify.md`),
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
If the bounded task is not yet planned, PLAN first. STOP for operator approval before APPLY.
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
| `ACTIVE` | SPECIFY/HANDOFF | Specification captured; continue to PLAN or resume the current phase. |
| `PLANNED` | PLAN/READINESS | First-task plan checked against repo evidence; await APPLY only if readiness is `READY`. |
| `IN_PROGRESS` | APPLY | Operator approved; APPLY has started. |
| `PASS`/`FAIL`/`BLOCKED`/`CANCELLED` | UNIFY | Closure state — see hex-build `references/unify.md`. |
| `SUPERSEDED` | Next authorized handoff | Set only when explicitly archiving a still-relevant-but-replaced handoff. |

`SUPERSEDED` is set only when replacing a handoff, never during UNIFY.

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

No large logs. Evidence-backed statuses only — see hex-build `references/qualify.md`
and `references/unify.md`.

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

The handoff's `readiness` field describes the bounded first task, not the entire
project. A project can have unrelated future unknowns while that task is `READY`.
Do not reject the task merely because later work remains `UNKNOWN`. Do not proceed when an
`UNKNOWN` materially affects this task's security, architecture, credentials, exposure,
data handling, or acceptance criteria.
