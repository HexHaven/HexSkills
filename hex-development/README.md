# Hex Development Skills

Hermes-native, general-purpose procedures for moving from project idea to verified bounded implementation, recovering session context, and creating additional Hermes skills.

## Skills

| Skill | Owns | Workflow |
|---|---|---|
| `hex-seed` | Project discovery, concise specification, readiness | `IDEA → DISCOVER → SHAPE → SPECIFY → READINESS CHECK → HANDOFF` |
| `hex-build` | Authorized bounded implementation and loop closure | `PLAN → APPLY → QUALIFY → UNIFY` |
| `hex-recap` | Compact, evidence-backed session recap/handoff | read-only report of `hex-seed`/`hex-build` state |
| `hex-skillsmith` | Hermes skill discovery, scaffold, distillation, audit | `DISCOVER → SPECIFY → SCAFFOLD → DISTILL → AUDIT → VERIFY` |
| `hex-soulforge` | Forging and refining compact agent Souls in the `SOUL.md` shape | soul draft → distill → validate |
| `hexhaven-gitops` | Aurelius, the trigger-driven autonomous HexHaven Git executor | `inspect → understand intent → change → validate → self-review → sign commit → push → verify → report` |
| `aurelius-repo-identity` | Binding one named HexHaven repo to Aurelius' signing identity | verify repo → set identity → confirm signature |
| `delegated-execution-discipline` | Handing part of a task to a sub-agent or harness | scope → delegate → verify the claim |
| `multi-agent-coordination` | Routing work across specialist agents, escalating decisions | classify → route → escalate |
| `niri-configuration` | Changing Niri compositor config, tracing source to runtime | config edit → validate → reload → verify |

Project flow:

```text
Idea → hex-seed → project specification → hex-build → closed milestone
```

Skill-authoring flow is separate and owned entirely by `hex-skillsmith`; there is no circular dependency.

## Inspiration and provenance

Concepts were reviewed from:

- [ChristopherKahler/seed](https://github.com/ChristopherKahler/seed)
- [ChristopherKahler/paul](https://github.com/ChristopherKahler/paul)
- [ChristopherKahler/skillsmith](https://github.com/ChristopherKahler/skillsmith)
- [soul.md](https://soul.md/) and [Stefz29/SOUL-Hermes](https://github.com/Stefz29/SOUL-Hermes#suggested-soulmd-shape) — the `SOUL.md` idea and section shape that `hex-soulforge` follows

The Nyx files are independently rewritten for Hermes. No source files, substantial source wording, installers, branded footers, Claude-specific metadata, or runtime command conventions were copied. PAUL includes an MIT license file. The inspected SEED and Skillsmith commits declare MIT in package metadata, but no `LICENSE` file was present.

## Location and activation

Install via a Hermes external skill directory or GitHub tap — see the [HexSkills repo README](../README.md) for both paths.

## Safe updates

1. Confirm the active profile and exact skill path.
2. Read current Hermes skill docs, validator/linter behavior, and the existing skill before editing.
3. Preserve the 60-character description budget and progressive-disclosure structure.
4. Use targeted `skill_manage` patches for small changes; obtain explicit authorization for rewrites or new files.
5. Re-run static validation, `hermes skills list`, and a safe behavioral dry run.
6. Do not modify Hermes core, bundled skills, plugins, MCP configuration, or remote systems as part of maintenance.

## Deferred

BASE integration is **DEFERRED**. These skills contain no BASE dependency, CLI call, hook, graph registration, installer, or runtime assumption. A future separately authorized `hex-context` evaluation may assess it.
