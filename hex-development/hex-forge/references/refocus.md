# Refocus

Brings the bigger picture back to the agent holding the local details. It prevents scope
inflation: a chain of individually reasonable steps (doghouse → light → power →
generator) that no longer serves the intent anyone asked for.

## Triggers

- **APPLY:** the next step adds something no acceptance criterion of the active slice
  requires, such as a new dependency, a component, a file outside Expected Files, or
  "while I'm at it".
- **Delegation:** before handing a sub-step to a sub-agent, include the block in its context.
- **Resume:** after a context compaction or in a fresh session (RECAP "compact context").
- **On request:** the operator says "refocus".

## Procedure

1. **Start where the work is.** Name the concrete step about to be taken.
2. **Trace to the root.** Read the intent lines from `.nyx/BLUEPRINT.md`: the active slice,
   its mission, then the project. Without a blueprint, fall back to the plan's Intent,
   the handoff's Goal, and the Vision in `docs/PROJECT.md`. Write `UNKNOWN` for a
   missing level. Never invent one.
3. **Compose the reminder.** Use the block below, quoted from the files with no new content:

   ```text
   Derived intent
   - Slice   <id>: <intent line>
   - Mission <id>: <intent line>
   - Project:      <intent line>
   Current step: <the step from 1>
   Does this step still serve the slice intent?
   ```

4. **The agent holding the details decides.** The block returns the purpose; it never
   pre-decides the answer.
   - The step serves the intent: continue.
   - The step is useful but does not serve the intent: add it to `Parked` in the
     blueprint (or report it in chat) and continue without it.
   - The step would change intent, scope or acceptance: stop and use the APPLY
     divergence gate (Intent/Specification class in hex-build `references/apply.md`).
     The change goes back to hex-forge and the operator's decision.

## Rules

- An approval from an agent that lacks the details is not an approval. Bring the intent
  down to the details; do not send the decision up to missing context.
- Keep the block under about eight lines. It is a reminder, not a transcript.
- Refocus is read-only. Only a `Parked` entry may be written, and only when the
  blueprint is in the authorized scope.

## Limitation

Automatic injection after a compaction is not wired. Hermes offers hooks for it
(`session:compress`, `pre_llm_call`), but using them needs a plugin. Until then, Refocus
runs through the triggers above.
