# RECAP / HANDOFF Mode

Read-only reporting over current or past `hex-forge` state. Never advances IDEA…UNIFY,
never shapes a spec, never mutates anything.

## Mode selection

| Mode | Trigger phrasing | Target reader | Length |
|---|---|---|---|
| **RECAP** | "recap", "summarize current state", "compact context" | The operator | under 500 words |
| **HANDOFF** | "handoff", "continue in new session", explicit paste-ready request | A fresh Hermes session | 500-1200 words |

If ambiguous, produce RECAP and offer HANDOFF.

## Procedure

1. **Identify scope** — determine which hex-forge phase (IDEA…READINESS or
   PLAN…UNIFY) is active from the current conversation and `.nyx/HANDOFF.md`. If
   neither, say so plainly and fall back to a generic session recap.
2. **Inspect repository evidence (read-only)** — using whatever terminal/shell tool
   the current runtime exposes, run and record actual output, never assume:
   ```bash
   git status --short && git branch --show-current && git log -1 --oneline && git remote -v
   ```
   Then read any of the following that exist: `AGENTS.md`, `docs/PROJECT.md`,
   `docs/ARCHITECTURE.md`, `docs/CAPABILITIES.md`, `.nyx/HANDOFF.md`, current ADRs
   under `docs/adr/` or similar. Skip files that don't exist rather than guessing
   their content; use a file-search capability if one is available and the ADR
   location is unclear.
3. **Reconcile evidence against conversational claims** — repository state overrides a
   stale conversational claim. Flag contradictions explicitly. Every fact used gets a
   label: `USER-STATED`, `OBSERVED`, `ASSUMED`, `PROPOSED`, `UNKNOWN`, `CONTRADICTORY`.
4. **Assemble machine-readable fields** for implemented/verified work:
   ```
   changed_files: [...]
   verification: [...]      # commands actually run + PASS/FAIL/BLOCKED/NOT RUN, never invented
   blocked_reason: null | "..."
   residual_risk: [...]
   ```
5. **Render**:
   - RECAP — compact prose, no fixed headers required, under 500 words.
   - HANDOFF — `templates/SESSION-HANDOFF.md` as the section skeleton, verbatim; fill
     only sections with real content, write "None observed." rather than inventing
     filler. 500-1200 words.
6. **State phase continuation** explicitly — the single next concrete action, one sentence.

## Safety Boundaries

- Read-only throughout — no commit, push, deploy, file edit, or remote mutation, even
  when the underlying phase is APPLY.
- Never place tokens, passwords, private keys, cookies, connection strings, or secrets
  in the output; use placeholders if unavoidable.
- Never invent a PASS result, a file that wasn't actually observed, or a decision the
  operator didn't state.

## Pitfalls

- Trusting an earlier assistant claim over what `git status`/`read_file` actually show now.
- Producing a HANDOFF that's a compressed transcript instead of a decision-and-state summary.
- Skipping the repository check because the conversation "already covered it."
- Reporting `verification: [...]` entries that were only planned, not actually run.
