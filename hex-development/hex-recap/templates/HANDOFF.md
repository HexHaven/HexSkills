# Nyx Handoff

## Project
- repository: <path or name, or "none observed">
- branch: <OBSERVED branch name>
- HEAD: <OBSERVED short SHA + subject>
- working-tree state: <clean / dirty + `git status --short` summary>

## Active workflow
- active hex-seed / hex-build topic: <name or "none">
- current phase: <IDEA|DISCOVER|SHAPE|SPECIFY|READINESS|HANDOFF for hex-seed, or PLAN|APPLY|QUALIFY|UNIFY for hex-build>
- readiness/closure state: <hex-seed readiness state, or hex-build PASS/FAIL/BLOCKED/CANCELLED/open>

## Established facts
Only evidence-backed or explicit USER-STATED facts, each labeled.
- <fact> — USER-STATED | OBSERVED

## Decisions
Only decisions that affect future work.
- <decision and why>

## Implemented
What actually exists now (OBSERVED), not what was planned.
- <file/feature — evidence>

## Verification
Commands/results actually observed this session. Never invented.
- <command> → PASS | FAIL | BLOCKED | NOT RUN

## Unresolved
Only material blockers or UNKNOWN items.
- <item> — UNKNOWN | CONTRADICTORY

## Constraints / Non-goals
Safety and scope boundaries that still apply.
- <constraint>

## Next action
One concrete next action.

## Continuation prompt
A concise paste-ready prompt for the next fresh Hermes session.

```
<paste-ready prompt>
```

<!-- Optional machine-readable block when engineering work is in scope -->
<!--
changed_files: []
verification: []
blocked_reason: null
residual_risk: []
-->
