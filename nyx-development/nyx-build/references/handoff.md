# Handoff Validation (nyx-build side)

The authoritative `.nyx/HANDOFF.md` schema, lifecycle, archiving convention, and tracking policy remain in `nyx-seed`'s `references/handoff.md` (`skill_view(name="nyx-seed", file_path="references/handoff.md")`). `nyx-seed` owns task intent/specification and creates the handoff; this supplement defines only `nyx-build` validation and optional execution/deployment additions.

## Locate and validate

During PLAN, check for `.nyx/HANDOFF.md` at repository root. If absent, proceed from project docs, direct operator request, or chat-pasted handoff; never require or create it automatically.

Compare present fields to fresh evidence: project root, branch, HEAD, working tree, `AGENTS.md`, referenced docs/files, readiness, expected files, and supplied deployment facts.

| Class | Meaning | Action |
|---|---|---|
| `MATCH` | Agrees with fresh evidence. | Proceed. |
| `STALE` | Low-impact divergence. | Record in PLAN. |
| `CONTRADICTORY` | High-impact security, architecture, credential, exposure, data, acceptance, or deployment-target divergence. | **STOP** before PLAN. |
| `UNKNOWN` | Cannot be checked. | Keep visible; block if high-impact. |

## Deployment addition

A deployment-capable build may append this section without rewriting seed-owned content:

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

`mode` is PLAN classification; other fields are `OBSERVED`, `USER-STATED`, or `UNKNOWN`. Resolve required high-impact fields before proposing DEPLOY approval; never infer a procedure from this section.

## Status and ownership

Set frontmatter `status` to `PLANNED` on presented PLAN, `IN_PROGRESS` when authorized APPLY begins, and closure state on UNIFY. Never set `SUPERSEDED`.

Never rewrite original `Goal`, `Scope`, `Non-Goals`, or `Acceptance Criteria`; append only approved `## Build Plan Amendments` and later `## Build Result`. Never archive/delete the handoff or automatically stage/commit/push/deploy/restart.

## UNIFY closure

Append, do not replace, the existing `## Build Result` structure. Include separate local implementation, publication, deployment, verification, deviations, residual risk, and next action; retain evidence-backed statuses and SHA values without large logs.