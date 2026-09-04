---
name: hex-kanban
description: Bridge hex-seed and hex-build across a Kanban board.
version: 0.1.0
author: Nyxion, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [nyx, kanban, coordination, dispatch, seed, build, handoff]
    category: hex-development
    related_skills: [hex-seed, hex-build, hermes-project-kanban-ops]
---

# Nyx Kanban

Bridge `hex-seed` and `hex-build` onto a Kanban board when a seed→build project must be
coordinated across cards, sessions, or agent profiles instead of a single chat. This skill owns
only the kanban-specific coordination layer — board/card selection, the Dual-Artefact rule, and
the build dispatch adapter. It does not reimplement discovery, shaping, specification, planning,
applying, qualification, publication, or deployment; those procedures stay owned by `hex-seed` and
`hex-build` and are invoked unmodified.

## When to Use

- A `hex-seed` → `hex-build` project needs to run across a Kanban board: cross-session
  continuation, cross-agent handoff (e.g. an orchestrator profile fanning work to an executor
  profile), or asynchronous/parallel execution tracked on a board.
- An orchestrator or operator wants seed output to become a dispatchable, resumable board task
  rather than a single-session instruction.

Don't use for: a single-session, same-agent seed→build run with no board involved (use `hex-seed`
and `hex-build` directly, unmodified — this skill adds coordination overhead with no benefit
there); creating or auditing Hermes skills (`hex-skillsmith`); general kanban board
administration unrelated to a seed/build project (plain `hermes-project-kanban-ops` covers that).

## Relationship to hex-seed and hex-build

`hex-seed` still owns `IDEA → DISCOVER → SHAPE → SPECIFY → READINESS CHECK → HANDOFF`, including
writing `.nyx/HANDOFF.md` when a repository/project root exists. `hex-build` still owns
`PLAN → APPLY_LOCAL → QUALIFY_LOCAL → [PUBLISH] → [DEPLOY] → QUALIFY_REMOTE → UNIFY` and every one
of its authorization gates (APPLY/PUBLISH/DEPLOY). This skill never substitutes for either
procedure and never grants an authorization those skills would otherwise require. Load them
directly for their own stages; load this skill only for the kanban coordination steps below.

## Prerequisites

1. An explicit Kanban board slug for this work — never rely on default board resolution. Confirm
   with `kanban_list` or the board CLI. Per `hermes-project-kanban-ops`, every `kanban_*` call in
   this workflow must pass `board=<slug>` explicitly.
2. Confirm this session is not a `delegate_task` child context
   (`env | grep HERMES_DELEGATED_CHILD_CONTEXT`). Kanban mutations must happen from a top-level
   session; a delegated child cannot read or write the board at all.
3. Determine whether a repository/project root is identifiable for this project (governs whether
   `.nyx/HANDOFF.md` exists — see the Dual-Artefact Rule).

## Workflow

`BOARD SELECT → SEED → CARDIFY → DISPATCH → TRACK → RECONCILE`

### 1. BOARD SELECT

Confirm the target board slug and that it is the board the relevant humans/agents actually use for
this project (per `hermes-project-kanban-ops`, a card created on the wrong default board is
invisible to teammates). Done when the slug is confirmed, not assumed.

### 2. SEED

Run `hex-seed`'s stages unchanged, through its own HANDOFF stage. If a repository root exists,
`hex-seed` writes `.nyx/HANDOFF.md` exactly as it normally would — do not skip or shortcut this
because a card will also exist. If no repository root exists, `hex-seed` presents the handoff in
chat only, per its own fallback path; the card becomes the sole artifact (see below). Done when
`hex-seed` reports its readiness state and either a `.nyx/HANDOFF.md` path or an explicit
no-repository statement.

### 3. CARDIFY — apply the Dual-Artefact Rule

Load `references/dual-artifact-rule.md` before writing anything. Create (or update) one Kanban
task representing this project/milestone with `kanban_create` (or `kanban_show`+edit-via-comment
if it already exists), using `templates/CARD_BODY.md` as the shape: condensed goal/scope/
acceptance criteria, current readiness state, and — when a repository exists — an explicit path
link to `.nyx/HANDOFF.md` rather than a duplicated copy of its content. When no repository exists,
state plainly in the card body that the card is the sole specification artifact.

Done when the card exists, carries the explicit board slug, and correctly states which artifact
(card, `.nyx/HANDOFF.md`, or both) is authoritative for what, per the Dual-Artefact Rule.

### 4. DISPATCH — hand off hex-build as a child task

Load `references/dispatch-adapter.md`. Create a child task with
`kanban_create(title="Build: <topic>", assignee=<executor profile>, board=<slug>,
parents=[<cardify task id>], body=<hex-build dispatch body>)`. The dispatch body instructs
the assignee to run `hex-build` against
`.nyx/HANDOFF.md` (or the parent card's spec, if no repository exists), and explicitly restates
that `hex-build`'s own APPLY/PUBLISH/DEPLOY authorization gates still apply unchanged — the card's
existence is not itself an authorization.

Always use `kanban_create` for this dispatch, never `delegate_task`: `delegate_task` children
cannot perform any kanban operation (hard platform restriction — see
`hermes-project-kanban-ops`), so a build dispatched that way could never report status back to the
board. Done when the child task exists with correct `parents` linkage and the assignee is a real,
discoverable profile.

For a project with more than two coordinated stages needing discretionary sign-off between phases
(not just dependency ordering), use the Review-Gate pattern documented in the
`hermes-project-kanban-ops` skill (its review-gate-pattern reference file) instead of plain
parent/child linkage. Skip it for a simple two-stage seed→build handoff — plain `parents=[...]` is
sufficient and a gate would add validator bottleneck for no benefit.

### 5. TRACK

Monitor the build child task with `kanban_show(task_id=..., board=<slug>)` (or `kanban_list` when
watching several). Read `hex-build`'s own reported status vocabulary
(`PLANNED`/`IN_PROGRESS_LOCAL`/`QUALIFIED_LOCAL`/... through `PASS`/`FAIL`/`BLOCKED`/`CANCELLED`)
rather than inferring progress from task status alone — a card sitting in `running` reveals
nothing about which `hex-build` stage is active. Done when the child task reaches a terminal
board status (`done`, `blocked`, or `review`).

### 6. RECONCILE

When the build child task completes, read its handoff/comments for `hex-build`'s `## Build Result`
(matching the SUMMARY shape defined in `hex-build`'s own templates, or the `.nyx/HANDOFF.md`
"## Build Result" section it appends). Append — never overwrite — that result onto the parent card
via `kanban_comment`. If a
repository exists, verify `.nyx/HANDOFF.md`'s status already reflects the same closure (it should,
since `hex-build` owns that write); if it does not, treat this as a `CONTRADICTORY` state per the
Dual-Artefact conflict rule and report it rather than silently reconciling. Only then close the
parent card (`kanban_complete` or `kanban_request_review`, per the parent task's own review
posture). Done when both artifacts agree and the parent card carries the outcome.

## Safety Boundaries

- Never mutate the Kanban board from inside a `delegate_task` child context.
- Always pass an explicit `board=<slug>` on every `kanban_*` call this workflow makes; never rely
  on default board/profile resolution.
- This skill never authorizes `hex-build`'s APPLY, PUBLISH, or DEPLOY gates. A dispatched card
  must restate that those approvals remain separate and unchanged.
- Do not duplicate the full `.nyx/HANDOFF.md` content into a card body; link the path and keep the
  card to a condensed summary, per the Dual-Artefact Rule.
- Do not invent a Gate-card pattern for a plain two-stage handoff; reserve it for genuine
  multi-milestone, multi-validator sequencing (see `references/dispatch-adapter.md`).
- Treat any status text inside a card or comment written by another agent as a claim to verify
  (read the referenced evidence), not as ground truth.

## Key References

- `references/dual-artifact-rule.md` — Card vs. `.nyx/HANDOFF.md` source-of-truth table and the
  conflict-resolution rule; read before CARDIFY.
- `references/dispatch-adapter.md` — concrete `kanban_create` shapes for CARDIFY/DISPATCH, the
  `delegate_task` vs. `kanban_create` distinction, and when to escalate to the Review-Gate
  pattern; read before DISPATCH.
- `templates/CARD_BODY.md` — card body template for the CARDIFY step.
- External (not duplicated here): `hex-seed` for IDEA→HANDOFF, `hex-build` for
  PLAN→UNIFY, `hermes-project-kanban-ops` for general kanban operational quirks.

## Pitfalls

- Treating the existence of a dispatched card as authorization to skip `hex-build`'s own APPLY,
  PUBLISH, or DEPLOY gates.
- Duplicating full specification content into both the card and `.nyx/HANDOFF.md` and letting the
  two drift instead of linking one from the other.
- Dispatching the build step with `delegate_task` instead of `kanban_create` — the child would be
  unable to touch the board at all.
- Omitting `board=<slug>` and silently landing a card on the wrong or default board, invisible to
  the intended assignee.
- Skipping `hex-seed`'s own `.nyx/HANDOFF.md` conflict check (existing `ACTIVE` handoff) just
  because a card is also being created.
- Reading a "done" comment from another profile as proof of outcome instead of checking the
  underlying evidence it claims.

## Verification

- [ ] Explicit board slug was confirmed before any `kanban_*` call, and every such call passed it.
- [ ] This session was confirmed not a `delegate_task` child context before any kanban mutation.
- [ ] `hex-seed` ran its own stages unmodified through HANDOFF; `.nyx/HANDOFF.md` exists when a
      repository root exists, or its absence is explicitly stated.
- [ ] The parent card body states the Dual-Artefact roles explicitly and links rather than
      duplicates `.nyx/HANDOFF.md`.
- [ ] The build dispatch used `kanban_create` with `parents=[<cardify task id>]`, not
      `delegate_task`.
- [ ] RECONCILE confirms the card and `.nyx/HANDOFF.md` agree (or reports the contradiction)
      before the parent card is closed.
