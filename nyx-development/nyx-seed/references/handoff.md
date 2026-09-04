# Repository-Local Handoff Contract

Canonical, authoritative schema for `.nyx/HANDOFF.md`. `nyx-build` and `nyx-recap` read this file rather than duplicating the full schema; they may keep a short validation-focused excerpt.

## Purpose and scope

`.nyx/HANDOFF.md` lets `nyx-seed` hand an implementation-ready specification directly to `nyx-build` across a fresh Hermes session, without the operator re-pasting the seed conversation. It is a workflow artifact, not project documentation and not implementation.

Use it only when `nyx-seed` is operating with an identifiable repository/project root. When no repository exists, present the handoff in chat only and say plainly that no repository-local handoff could be written. Never force `.nyx/` into a directory that is not the project's own root.

## Files

- `.nyx/HANDOFF.md` — the single canonical **active or most-recently-closed** handoff.
- `.nyx/history/<ISO-8601-timestamp>-<slug-topic>.md` — archived handoffs. Create entries only when a real handoff is actually being archived; never pre-create empty history scaffolding.

## Frontmatter schema

```yaml
---
version: 1
status: ACTIVE
source: nyx-seed
created_at: <ISO-8601>
project_root: <absolute-or-repo-identified-path>
branch: <branch-or-NONE>
head: <commit-or-NONE>
working_tree: clean|dirty|unknown
readiness: IDEA|DISCOVERY|SPECIFIED|PLANNED|READY
topic: <short topic>
---
```

All fields are OBSERVED at write time, not remembered from earlier in the conversation. `readiness` mirrors the state from `references/readiness.md` in `nyx-seed`.

## Body sections

```markdown
# Nyx Handoff

## Goal
## Scope
## Non-Goals
## Established Facts        (USER-STATED | OBSERVED | ASSUMED | PROPOSED | UNKNOWN | CONTRADICTORY only)
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

Keep it compact. Do not dump the full seed conversation, raw environment variables, secrets, tokens, credentials, private keys, giant logs, or implementation history that no longer affects the next task. Link to `docs/PROJECT.md` when one exists rather than duplicating it.

`nyx-build` appends a `## Build Plan Amendments` section during APPLY (only for operator-approved refinements) and a `## Build Result` section during UNIFY (see below). It never rewrites the original Goal/Scope/Non-Goals/Acceptance Criteria sections.

## Status lifecycle

| Status | Set by | Meaning |
|---|---|---|
| `ACTIVE` | nyx-seed HANDOFF | Ready for a fresh session to run `/nyx-build`. |
| `PLANNED` | nyx-build PLAN | PLAN produced and validated against repo evidence; awaiting operator approval. |
| `IN_PROGRESS` | nyx-build APPLY | Operator approved; APPLY has started. |
| `PASS` / `FAIL` / `BLOCKED` / `CANCELLED` | nyx-build UNIFY | Closure state, matching `references/unify.md` closure semantics. |
| `SUPERSEDED` | nyx-seed HANDOFF (next run) | Set only when explicitly archiving a still-relevant-but-replaced handoff instead of a normal closure. |

`nyx-build` never sets `SUPERSEDED`; only `nyx-seed` does, and only when archiving.

## Conflict check (performed by nyx-seed before writing)

1. Read current `.nyx/HANDOFF.md` frontmatter `status`, if the file exists.
2. `ACTIVE`, `PLANNED`, or `IN_PROGRESS` → **STOP**. Report topic, status, and age; ask the operator whether to archive it before proceeding. Never overwrite silently.
3. `PASS`, `FAIL`, `BLOCKED`, `CANCELLED`, or `SUPERSEDED` → archive it (below), then write the new `ACTIVE` handoff.

## Archiving convention (adopted: A)

`.nyx/HANDOFF.md` always holds the latest handoff — active or most recently completed. `nyx-build`'s UNIFY does **not** move it to history; it only updates status and appends `## Build Result`. Archiving happens in `nyx-seed`'s HANDOFF stage, immediately before writing a new `ACTIVE` handoff over a completed one:

1. Copy the current `.nyx/HANDOFF.md` to `.nyx/history/<ISO-8601-timestamp>-<slug-topic>.md` (lowercase, hyphenated, no spaces or secrets in the filename).
2. Write the new handoff to `.nyx/HANDOFF.md`.

Rationale: easy human inspection of "what's active now", no empty-state ambiguity, and the next seed run is a natural, safe archiving point.

## Build Result section (appended by nyx-build UNIFY)

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

No large logs. Evidence-backed statuses only — see `nyx-build`'s `references/qualify.md` and `references/unify.md`.

## Tracking policy

`.nyx/HANDOFF.md` and `.nyx/history/` are normally **tracked** in Git: they record project intent and task specification, enable reproducible continuation, are reviewable alongside the implementation, and create an auditable Seed → Build history. Do not force this if it conflicts with an existing repository convention the operator states. Never `git add`/commit/push automatically from either `nyx-seed` or `nyx-build`; normal operator Git policy still applies. Never place secrets, tokens, credentials, private keys, or raw environment dumps in `.nyx/`.

## Validation against repository evidence (performed by nyx-build)

Compare handoff frontmatter/content to freshly observed evidence (branch, HEAD, working-tree state, project_root, applicable `AGENTS.md`, referenced files, stated readiness). Classify each compared field:

| Class | Meaning |
|---|---|
| `MATCH` | Handoff and current evidence agree. |
| `STALE` | Diverges, but low-impact; note it in the PLAN and continue. |
| `CONTRADICTORY` | Diverges on something high-impact (security, architecture, credentials, public exposure, data handling, acceptance criteria); **STOP** before PLAN. |
| `UNKNOWN` | Cannot currently be checked. |

## Readiness distinction (performed by nyx-build)

Distinguish project-wide readiness (the handoff's `readiness` field) from bounded-task readiness (whether *this* first task can be safely implemented). A project at `PLANNED` can still contain a task that is `READY FOR IMPLEMENTATION`. Do not reject a safe bounded task merely because unrelated future work remains `UNKNOWN`. Do not proceed when an `UNKNOWN` materially affects this task's security, architecture, credentials, public exposure, data handling, or acceptance criteria.
