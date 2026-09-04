# Fact Model

Use these six evidence labels—and no additional labels—to keep the specification auditable. If a conclusion is reasoned rather than directly observed, record it as `PROPOSED` or `ASSUMED` according to risk; never add an `INFERRED` label.

| Label | Meaning | Treatment |
|---|---|---|
| `USER-STATED` | The user supplied the fact or decision. | Preserve exact identifiers and values; note when it is a preference rather than observed system state. |
| `OBSERVED` | Current evidence directly established it. | Cite file, command, tool result, URL, or other source when practical. |
| `ASSUMED` | A low-risk default fills a gap. | State the assumption and consequence; never use for high-impact facts. |
| `PROPOSED` | A design or decision is recommended but not accepted. | Keep separate from requirements and current state. |
| `UNKNOWN` | Evidence is insufficient. | Ask if high impact; otherwise record and bound its consequence. |
| `CONTRADICTORY` | Sources disagree. | Name both sources, apply declared precedence if one exists, and do not silently reconcile. |

## Precedence

1. Applicable trusted project policy and explicit user decisions govern intended behavior.
2. Current observed runtime state governs claims about what exists now.
3. Maintained authoritative specifications govern designed behavior unless current evidence proves drift.
4. Historical notes and remembered context are leads, not current proof.
5. Proposals and assumptions never override stated or observed facts.

Policy and reality can differ. Report both rather than forcing one label to do two jobs.

## Recording pattern

```markdown
- `OBSERVED` — The repository uses Python 3.12 (`pyproject.toml`).
- `USER-STATED` — The first release is Linux-only.
- `PROPOSED` — Use SQLite for the first bounded milestone.
- `UNKNOWN` — Production backup retention; blocks deployment planning, not local prototype planning.
```

## Contradictions

For each contradiction record:

- exact conflicting claims and their sources;
- which source is authoritative for the current decision, if established;
- impact on scope, architecture, or acceptance;
- owner and next evidence needed.

Do not convert `UNKNOWN` to `ASSUMED` merely to reach `READY`.
