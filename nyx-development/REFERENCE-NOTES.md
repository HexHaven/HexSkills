# Nyx Development Skill Forge — Reference Notes

## Research scope

These notes record concept extraction for three independently written Hermes-native, user-local skills. The source repositories were inspected read-only at:

| Source | Commit | Research checkout |
|---|---|---|
| SEED | `1183a1e43df06171a4d91719f28e22ff0b28e3f4` | `/home/nyxion/Forge/References/nyx-skill-forge-20260828/seed` |
| PAUL | `f8552c72d0e69309a0cb61b5de5c85a06838ddcb` | `/home/nyxion/Forge/References/nyx-skill-forge-20260828/paul` |
| Skillsmith | `7a9ff943ae8905cdbaf858436f8da961ebc2ebfe` | `/home/nyxion/Forge/References/nyx-skill-forge-20260828/skillsmith` |

The checkouts retain their original `origin` remotes and were not modified.

## Licensing and provenance

| Repository | Observed license evidence | What may be reused | Nyx implementation decision |
|---|---|---|---|
| SEED | `package.json` declares `MIT`; `README.md` labels the project MIT, but no `LICENSE` file was present in the inspected commit. | General ideas and independently expressed behavior. Exact source text or substantial code is not needed. Because the repository lacks the referenced license text at this commit, avoid copying source wording or code. | Extract concepts only; independently rewrite all operational guidance, labels, templates, and structure for Hermes. |
| PAUL | `LICENSE` contains the MIT License, copyright 2026 Chris Kahler; `package.json` also declares `MIT`. | MIT permits use, modification, and distribution subject to retaining its notice in copies or substantial portions. | No source text or code is copied. Concepts are independently specified, so no third-party license text is embedded in the Nyx skills. |
| Skillsmith | `package.json` declares `MIT`; no `LICENSE` file was present in the inspected commit. | General ideas and independently expressed behavior. Avoid copying exact source text or code without a present license grant file. | Extract concepts only; independently rewrite for the installed Hermes skill format. |

**Actual reuse:** repository names and factual provenance, short names of general workflow concepts, and high-level ideas. **Not reused:** source files, XML task syntax, installers, command routing, templates, branded footers, marketing copy, provenance markers, or substantial source wording.

## Hermes authority and observed version differences

Hermes Agent `v0.20.6 (2026.8.27)`, upstream commit `a24c12d1`, was inspected before authoring. The active profile resolves `HERMES_HOME=/home/nyxion/.hermes`; user-local skills are discovered recursively below `$HERMES_HOME/skills/`.

Observed installed behavior:

- `SKILL.md` must start at byte 0 with YAML frontmatter, include `name` and `description`, close the frontmatter, and contain a non-empty body.
- New agent-created descriptions are limited to 60 characters by `tools/skill_manager_tool.py`; the prompt index truncates longer descriptions.
- Current conventions also expect `version`, `author`, `license`, `platforms`, and `metadata.hermes.tags`; `metadata.hermes.category` is supported by current documentation.
- Valid platform gates are `linux`, `macos`, and `windows`; installed lint code also accepts legacy `darwin`.
- Supporting files may live under `references/`, `templates/`, `scripts/`, and `assets/`. The skill discovery walker excludes those support directories once a root `SKILL.md` is found.
- `metadata.hermes.requires_toolsets` and `requires_tools` hide a skill if requirements are unavailable. `fallback_for_toolsets` and `fallback_for_tools` provide inverse gating. None are necessary for these procedural skills.
- Every installed skill is available as `/<skill-name>` on supported surfaces. Multiple leading skill commands can be stacked. `/reload-skills` re-scans the directory; a new session is the conservative activation boundary because the current session index may be cached.
- User-local category layout is supported: `~/.hermes/skills/<category>/<name>/SKILL.md`.
- The installed authoring skill recommends a trigger-complete description of at most 60 characters, progressive disclosure, native Hermes tool names instead of wrapped shell utilities, explicit pitfalls, and evidence-based verification.

Version-specific caution: current website guidance and installed source agree on the core format and 60-character description budget. Some examples in general documentation omit `author` or `license`, while the installed authoring standard and linter expect them. These Nyx skills use the stricter installed convention. Hermes is 189 commits behind current upstream at inspection time, so `references/hermes-skill-spec.md` must be rechecked before future framework-sensitive edits.

## Concept extraction

| Source | Concept | Decision | Hermes adaptation |
|---|---|---|---|
| SEED | Raw idea to structured project | ADOPT | Convert vague intent into a concise repository-local project specification without implementing it. |
| SEED | Guided, collaborative discovery | ADAPT | Ask only architecture-, security-, data-, deployment-, billing-, credential-, and acceptance-critical questions; label low-risk assumptions instead of conducting a long interview. |
| SEED | Project typing changes rigor | ADAPT | Use lightweight types such as application, service/API, workflow/automation, utility, infrastructure/platform, and data/content; type selects relevant depth, not a separate runtime. |
| SEED | Type-specific question sets | ADAPT | Keep compact guidance in `references/discovery.md`; do not create a dynamic data engine or one folder per type. |
| SEED | Planning artifact | ADAPT | Prefer `docs/PROJECT.md` in an existing repository, using only relevant template sections. Do not create a separate project tree or initialize Git. |
| SEED | Quality/readiness gate | ADOPT | Use explicit states `IDEA`, `DISCOVERY`, `SPECIFIED`, `PLANNED`, `READY`; `READY` requires observable acceptance criteria and no high-impact blocker for the first bounded task. |
| SEED | Graduation and handoff | ADAPT | Hand off a specification plus first-task contract to execution. Graduation never implies commit, deployment, or remote authorization. |
| SEED | Session checkpoints | DEFER | Repository-local draft state may be useful later, but no persistent state engine is required for the initial skill. |
| SEED | Claude-specific `/seed` command tree and `$ARGUMENTS` | REJECT | Hermes automatically exposes the installed skill as `/nyx-seed`; internal workflow selection follows the user request and current context. |
| SEED | Automatic Git initialization and initial commit | REJECT | Project specification does not authorize repository creation, commit, or branch mutation. |
| SEED | PAUL-specific launch coupling | REJECT | Handoff is a generic task contract consumed by `nyx-build`; no external framework is required. |
| SEED | BASE v2 detection, graph registration, and promotion | DEFER | No BASE clone, calls, hooks, state, or knowledge graph integration. A future `nyx-context` evaluation may consider it separately. |
| SEED | Branded footer and ecosystem promotion | REJECT | Not legally or technically required; excluded from operational artifacts. |
| PAUL | PLAN → APPLY → UNIFY loop | ADAPT | Use `PLAN → APPLY → QUALIFY → UNIFY`, making verification an explicit stage rather than embedding all qualification inside APPLY. |
| PAUL | Every plan must close | ADOPT | After execution starts, UNIFY is mandatory even for `FAIL`, `BLOCKED`, or `CANCELLED`; no orphaned execution state. |
| PAUL | Bounded plans with acceptance criteria | ADOPT | Define intent, scope, dependencies, expected files, non-goals, acceptance criteria, validation, and recovery only to the depth the task needs. |
| PAUL | Approval between plan and execution | ADOPT | Stop after PLAN for operator review unless the user explicitly authorized immediate execution of that exact scope. Readiness is not authorization. |
| PAUL | Preserve context and boundaries | ADOPT | Read applicable `AGENTS.md`, specification documents, `git status --short`, and `git branch --show-current`; preserve unrelated work and name protected areas. |
| PAUL | Small execution units | ADOPT | Apply the smallest coherent change and keep diffs reviewable; do not opportunistically refactor. |
| PAUL | Qualification independent of implementation confidence | ADOPT | Re-read actual state and run fresh validation. Record only `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN`, with evidence. |
| PAUL | Reconcile planned vs actual | ADOPT | UNIFY records implemented and untouched scope, decisions, verification, deviations, unresolved work, and the next recommended bounded task. |
| PAUL | Intent/spec/code failure classification | ADAPT | If reality materially diverges, stop and decide whether intent, plan/spec, implementation, or environment is wrong before continuing. |
| PAUL | Mandatory `.paul/` state, manifests, ledgers, and roadmap engine | REJECT | Use existing repository conventions first. Optional `.nyx/plan.md`, `.nyx/state.md`, and `.nyx/history/` are lightweight aids, never a required engine. |
| PAUL | Claude command names, hooks, and `~/.claude` paths | REJECT | Use Hermes skills and native file/terminal tools only. |
| PAUL | Automatic commits and phase-transition commits | REJECT | Commit, push, branch switching, reset, clean, restore, and deployment require explicit authorization. |
| Skillsmith | Discover → specify → scaffold → audit → verify | ADOPT | Implement one Hermes skill with intent-based workflow selection: `DISCOVER → SPECIFY → SCAFFOLD → DISTILL → AUDIT → VERIFY`. |
| Skillsmith | Skill specification before scaffold | ADOPT | Capture trigger, exclusions, ownership, inputs, outputs, safety, tools, files, and verification before writing. |
| Skillsmith | Minimal directory scaffold | ADOPT | Create only `SKILL.md` unless references, scripts, templates, or assets have a concrete consumer. |
| Skillsmith | Syntax consistency and quality rules | ADAPT | Treat installed Hermes docs, source validator, linter, and well-formed local skills as authoritative instead of external XML conventions. |
| Skillsmith | Distill long sources into progressive disclosure | ADOPT | Separate concepts from implementation, stable rules from examples, and main procedure from deep references; preserve licensing/provenance. |
| Skillsmith | Compliance audit with specific findings | ADOPT | Validate frontmatter, name/path agreement, description budget, metadata, support links, safe tool usage, secrets, activation, and observed discovery. |
| Skillsmith | Templates and checklists | ADAPT | Use ordinary Markdown templates and concise quality references; no mandatory custom task/framework/context taxonomy. |
| Skillsmith | Claude `allowed-tools`, `AskUserQuestion`, XML entry points, and `@` routing | REJECT | Use Hermes YAML and `skill_view` progressive disclosure. Do not emit Claude-only metadata or runtime assumptions. |
| Skillsmith | Claude installer and `~/.claude` targets | REJECT | Create user-local skills with `skill_manage` under the active `$HERMES_HOME/skills/` category. |
| Skillsmith | Mandatory branded attribution footer | REJECT | Not required by observed repository license metadata and not technically relevant. Provenance belongs in concise reference notes when material is actually adapted. |
| Skillsmith | PAUL-managed build option | REJECT | `nyx-skillsmith` owns skill authoring directly; it does not install or require external orchestration. |
| Skillsmith | BASE integration | DEFER | Explicitly excluded from this task and any runtime behavior. |

## Nyx ownership and handoff boundaries

- `nyx-seed` owns project discovery, scope shaping, specification, and readiness classification. It never implements the project.
- `nyx-build` owns execution only after a bounded task is sufficiently specified and authorized. It closes every started execution loop through UNIFY.
- `nyx-skillsmith` owns Hermes-native skill discovery, specification, scaffolding, distillation, auditing, and installation-readiness verification.

The ownership graph is acyclic: project specification flows from `nyx-seed` to `nyx-build`; skill authoring is a separate branch owned by `nyx-skillsmith`. None of the skills requires BASE, PAUL, SEED, Skillsmith, Claude Code, a plugin, or a Hermes core change at runtime.
