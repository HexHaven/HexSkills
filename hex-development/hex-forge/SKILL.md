---
name: hex-forge
description: Turn an idea into a project root and a build blueprint.
version: 0.3.0
author: Nyxion, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [nyx, development, discovery, specification, blueprint, planning, recap, lifecycle]
    category: hex-development
    related_skills: [hex-build, hex-skillsmith, hex-soulforge]
---

# Hex Forge

The planning half of the hex lifecycle. Takes an idea through discovery and
specification, adapts or creates the project root, and cuts the work into a
**blueprint** (`.nyx/BLUEPRINT.md`) of missions and slices. `hex-build` works that
blueprint off slice by slice. hex-forge owns the intent; hex-build owns the execution.

**The blueprint is the contract between the two skills.** Its format and ownership rules
live in `references/blueprint.md`. hex-forge writes intent (missions, slices, intent lines,
order); hex-build writes only slice status, `Parked` and `Decisions`.

**Durable rule:** authority over every repository write, APPLY, PUBLISH and DEPLOY
belongs to the operator in every case. Autonomy applies to how phases connect, never to
who approves a mutation.

## When to Use

- A project idea needs shaping into a specification, a project root and a build plan.
- The blueprint needs changing: new or dropped slices, reordered work, a changed intent
  line, or an escalation from hex-build (Intent/Specification divergence).
- "recap", "where are we", "handoff", "continue in new session" on a hex project
  (shared with hex-build, see RECAP below).

Don't use for: implementing a slice (`hex-build`), creating or auditing Hermes skills
(`hex-skillsmith`), forging agent identity (`hex-soulforge`).

## Lifecycle

```text
hex-forge:  IDEA → DISCOVER → SHAPE → SPECIFY → ROOT → BLUEPRINT
                                                          │ open slice
hex-build:  PLAN → READINESS → APPLY → QUALIFY → [PUBLISH] → [DEPLOY] → UNIFY
                ▲                                                      │
                └──────────── next open slice ─────────────────────────┘
            intent/spec change ─────────────→ back to hex-forge (BLUEPRINT)
```

States hex-forge reports: `IDEA → DISCOVERY → SPECIFIED`, then the blueprint status.
`PLANNED` and `READY` belong to a slice and are assessed by hex-build.

Discovery, specification, root and blueprint form one continuous flow. Do not stop for a
ceremonial handoff or ask the operator to repeat the idea.

## Procedure

### Phase 1: IDEA → SPECIFY

Load `references/discovery.md` (question gate, project typing) and
`references/fact-model.md` (six evidence labels: `USER-STATED`, `OBSERVED`, `ASSUMED`,
`PROPOSED`, `UNKNOWN`, `CONTRADICTORY`, no others). Restate intent, inspect read-only
before asking, shape goals, non-goals and flows. Write `docs/PROJECT.md` (via
`templates/PROJECT.md`) only when a repository specification is useful and its write is
authorized; otherwise present the specification in chat. Do not implement, commit, push
or deploy.

### Phase 2: ROOT

Load `references/blueprint.md`. Find the repository or workspace that already owns the
work and adapt it, or propose exactly one new root, checked against the host's home and
workspace policy. Create it only after the operator approves the exact path. The scaffold
holds specification records only (`docs/PROJECT.md`, `.nyx/BLUEPRINT.md`, optionally
`.nyx/HANDOFF.md`); code, dependencies and CI are slice work for hex-build.

### Phase 3: BLUEPRINT

Cut the specification into missions and slices in `.nyx/BLUEPRINT.md` (via
`templates/BLUEPRINT.md`), or in chat when writing is not authorized. Every level has one
intent line saying why; every slice has an observable `Done when`. Detail only the near
missions. Present the blueprint, then hand the next open slice to `hex-build` in the same
conversation. No re-statement is needed, because the blueprint carries the intent.

### Changing the blueprint

When hex-build escalates, or the operator changes direction: propose the concrete change
(slices added, dropped or reordered, intent lines changed) with its reason, wait for the
operator's decision, then update the blueprint. Mark dropped slices `[-]`; never renumber.

## RECAP (shared with hex-build)

Read-only. Never advances a phase or mutates anything. Load `references/recap.md`. Both
skills use this one reference: hex-forge answers project-level questions, hex-build answers
mid-slice ones. Either way the report leads with the Refocus block and blueprint progress.
It produces a compact **RECAP** (under 500 words) or a paste-ready **HANDOFF** (500–1200
words, via `templates/SESSION-HANDOFF.md`) depending on phrasing.

## Shared References

hex-build loads these from this skill (`skill_view(name="hex-forge", file_path=...)`):

- `references/blueprint.md`: root, blueprint format, ownership split, working it off.
- `references/refocus.md`: trace a step to its intent; reminder block; park vs. stop.
- `references/readiness.md`: state definitions and the READY gate.
- `references/handoff.md`: optional `.nyx/HANDOFF.md` contract.
- `references/recap.md`: RECAP/HANDOFF rendering.
- `references/fact-model.md`: evidence labels.

Own references: `references/discovery.md`. Templates: `templates/PROJECT.md`,
`templates/BLUEPRINT.md`, `templates/PROJECT-HANDOFF.md`, `templates/SESSION-HANDOFF.md`.

## Safety

- Read-only discovery precedes any write.
- Every repository write (root, scaffold, blueprint, handoff) needs explicit authorization
  of that write; discussing the idea is not permission. Remotes, branches and signing stay
  untouched unless separately authorized.
- Never place tokens, passwords, private keys or credentials in a specification,
  blueprint or handoff; use `<TOKEN>`, `<PASSWORD>`, `<HOST>`, `<IP_ADDRESS>`.

## Pitfalls

- Creating a new project root when an existing repository already owns the work.
- Scaffolding code, dependencies or CI; that is hex-build's slice work under APPLY.
- Planning every future mission in detail; slice only what is near.
- Intent lines that say how instead of why; Refocus has nothing to return then.
- Slices without an observable `Done when`, or slices too big for one reviewed change.
- Letting hex-build change intent lines or slice order by itself.
- Turning discovery into a long questionnaire instead of inspecting first.
- Producing a RECAP/HANDOFF that advances or mutates state.

## Verification

- [ ] Every material claim carries a fact label or a direct source.
- [ ] The root was adapted, or approved by exact path; the scaffold holds only spec records.
- [ ] Every mission and slice has a one-line intent; every slice has a `Done when`.
- [ ] Blueprint changes after the first draft were proposed and decided by the operator.
- [ ] No implementation, commit, push or deployment happened in hex-forge.
