# Dual-Artefact Rule

`hex-kanban` deliberately keeps two artefacts rather than merging them into one. Merging them
either loses the board's live coordination state or turns the card into an unbounded duplicate of
the repository specification. Instead, each artefact has exactly one job.

## Source-of-truth table

| Artefact | Role | Owner | Updated by |
|---|---|---|---|
| Kanban card (body + comments) | Workflow/coordination source of truth — current dispatch state, who is working what, live status | `hex-kanban` | `hex-kanban`, at each stage transition (CARDIFY, DISPATCH, RECONCILE) |
| `.nyx/HANDOFF.md` | Durable repository specification — survives the board, is Git-versioned, is the technical source of truth for goal/scope/acceptance criteria | `hex-seed` / `hex-build` (unchanged) | `hex-seed` (SPECIFY/HANDOFF stage), `hex-build` (`## Build Result` at UNIFY) |

## Conflict rule

When the two disagree:

- For **specification content** — goal, scope, non-goals, acceptance criteria, architecture
  constraints — `.nyx/HANDOFF.md` wins. It is the durable, reviewable, Git-tracked artefact;
  the card must not silently override it. If the card's summary has drifted from the file, treat
  the card summary as stale and refresh it from the file rather than editing the file to match the
  card.
- For **current dispatch/execution status** — which stage is active, who owns the next action,
  whether a child task is blocked — the card wins. The board is live; `.nyx/HANDOFF.md` is only
  updated at discrete checkpoints (HANDOFF write, Build Result append) and does not track
  real-time execution state.
- A disagreement on specification content that the card claims to have superseded (e.g. a comment
  asserting new scope not reflected in `.nyx/HANDOFF.md`) is `CONTRADICTORY`, not silently
  resolvable — surface it and route back through `hex-seed`'s HANDOFF stage for an explicit
  amendment, rather than picking a side ad hoc.

## No-repository case

When no repository/project root is identifiable, `hex-seed` cannot write `.nyx/HANDOFF.md` (see
its own fallback path). In that case the Kanban card is the **sole** specification artefact and
must say so explicitly in its body — do not imply a `.nyx/HANDOFF.md` exists when it does not, and
do not fabricate a path.

## What the card should contain (and what it should not)

The card body carries a **condensed** summary sufficient for a dispatched assignee or observer to
orient without reading the full file: goal (1–2 sentences), scope/non-goals (bullet list),
acceptance criteria (bullet list), current readiness state, and the explicit `.nyx/HANDOFF.md`
path (or the no-repository statement). It should not contain the full Established Facts,
Architecture/Constraints prose, or Validation detail already captured in the file — link, don't
copy. See `templates/CARD_BODY.md` for the exact shape.
