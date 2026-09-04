# Nyx Development Skills

Hermes-native, user-local procedures for moving from project idea to verified bounded implementation, and for creating additional Hermes skills.

## Skills

| Skill | Owns | Workflow |
|---|---|---|
| `nyx-seed` | Project discovery, concise specification, readiness | `IDEA → DISCOVER → SHAPE → SPECIFY → READINESS CHECK → HANDOFF` |
| `nyx-build` | Authorized bounded implementation and loop closure | `PLAN → APPLY → QUALIFY → UNIFY` |
| `nyx-skillsmith` | Hermes skill discovery, scaffold, distillation, audit | `DISCOVER → SPECIFY → SCAFFOLD → DISTILL → AUDIT → VERIFY` |

Project flow:

```text
Idea → nyx-seed → project specification → nyx-build → closed milestone
```

Skill-authoring flow is separate and owned entirely by `nyx-skillsmith`; there is no circular dependency.

## Inspiration and provenance

Concepts were reviewed from:

- [ChristopherKahler/seed](https://github.com/ChristopherKahler/seed)
- [ChristopherKahler/paul](https://github.com/ChristopherKahler/paul)
- [ChristopherKahler/skillsmith](https://github.com/ChristopherKahler/skillsmith)

The Nyx files are independently rewritten for Hermes. No source files, substantial source wording, installers, branded footers, Claude-specific metadata, or runtime command conventions were copied. PAUL includes an MIT license file. The inspected SEED and Skillsmith commits declare MIT in package metadata, but no `LICENSE` file was present. See `REFERENCE-NOTES.md` for commits, evidence, and the full `ADOPT`/`ADAPT`/`REJECT`/`DEFER` table.

## Location and activation

Installed for the active default profile at:

```text
~/.hermes/skills/nyx-development/
```

Hermes discovers each nested `SKILL.md` automatically. On Hermes Agent `v0.20.6`, use a fresh process for discovery:

```bash
hermes skills list
```

Inside an existing session, `/reload-skills` requests a re-scan. A new session is the conservative activation boundary. Skills are invoked as `/nyx-seed`, `/nyx-build`, and `/nyx-skillsmith`; do not claim slash activation until an invocation is observed.

## Safe updates

1. Confirm the active profile and exact skill path.
2. Read current Hermes skill docs, validator/linter behavior, and the existing skill before editing.
3. Preserve the 60-character description budget and progressive-disclosure structure.
4. Use targeted `skill_manage` patches for small changes; obtain explicit authorization for rewrites or new files.
5. Re-run static validation, `hermes skills list`, and a safe behavioral dry run.
6. Do not modify Hermes core, bundled skills, plugins, MCP configuration, or remote systems as part of maintenance.

## Deferred

BASE integration is **DEFERRED**. These skills contain no BASE dependency, CLI call, hook, graph registration, installer, or runtime assumption. A future separately authorized `nyx-context` evaluation may assess it.
