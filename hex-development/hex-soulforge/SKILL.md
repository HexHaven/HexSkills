---
name: hex-soulforge
description: Forge and refine compact agent Souls.
version: 0.4.0
author: Nyxion, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [soul, identity, character, naming, audit]
    category: hex-development
    related_skills: [hex-skillsmith]
---

# Hex Soulforge

Forge and refine compact Souls that describe who an agent is. **Identity rather than capabilities.**

A Soul is written down so identity survives sessions that carry no memory (soul.md). Its shape follows the `SOUL.md` convention: identity, tone, convictions, uncertainty, pushback, hard stops, user relationship, correction style, optional voice, boundaries, drift checks.

## When to Use

- Create or refine an agent's identity, character, values, intellectual temperament, user relationship, professional stance, or meaningful boundaries.
- Choose a fitting name or audit a Soul for identity drift and misplaced content.
- Decide whether a proposed specialist represents a different identity or just different skills/context.

Don't use for: implementing skills, project instructions, memory management, runtime configuration, or profile deployment.

## The Boundary

`Agent = Soul + Skills + Context + Memory + Runtime`

SOUL is who the agent is; Skills are reusable expertise and working methods; Context is what applies to the current project/task; Memory is what should persist across sessions; Runtime is tools, permissions, models, and environment. These are distinctions, not new infrastructure to build.

For each passage ask: **Would this still describe the agent if its project, tools, skills, model, and runtime changed tomorrow?** If yes, it may belong in SOUL. If no, recommend a destination without managing it:

- **SKILL** — reusable expertise, procedures, and working methods.
- **PROJECT CONTEXT** — current goals, project facts, and task-specific rules.
- **MEMORY** — learned facts worth retaining across sessions, not defining identity.
- **RUNTIME** — tools, permissions, models, environment, and deployment settings.
- **DROP** — repetition, empty virtues, obsolete material, or filler.

## Working Method

1. Read the brief and complete existing Soul using `read_file`; use `search_files` to locate its canonical source if needed. Identify what makes this mind distinctive. Ask only about gaps that materially change the identity.
2. Draft or refine in natural-language Markdown following `templates/SOUL.md`. Keep the section names so Souls stay portable across agents; omit sections that would only carry filler and remove placeholders. Prefer a few consequential principles over a capability list or a line quota.
3. Keep every section behavior-predictive. Convictions read as tradeoffs (`X over Y: so I do Z`), tone as the temperature the user feels, pushback as pattern plus in-character response. Cut or rewrite anything that would not change how the agent acts under pressure.
4. Size to purpose: roughly 80–200 lines for a standard Soul, 200–350 when register and cadence are part of the character (use the optional Voice section with an anti-register list and short examples), 80–120 for a minimal voice.
5. Audit against the checks below. Preserve distinctive judgment rather than replacing it with generic helpfulness. For naming, explain the fit and check available names for collisions when relevant; do not rename a profile.
6. Deliver the requested Soul or concise audit findings. For misplaced content, identify the passage and recommended destination. Write only an authorized canonical target; a draft is not profile activation. Do not require a long report for a small edit.

## Specialists

`Specialist = professional identity + suitable skills + relevant context`

- Same identity + different capability → same profile + another skill.
- Same identity + different project → same profile + different context.
- Genuinely different identity → consider another profile.

Compare actual identities, not titles or shared tools. Preserve meaningful differences in perspective and user relationship; never infer permission to collapse runtime isolation. If recommending specific skills, inspect them with `skills_list` / `skill_view`. Keep recommendations outside the Soul. No specialist contracts, ownership matrices, automatic skill creation, or profile merging.

## Pitfalls

- A decorative name and generic virtues do not describe a recognizable mind. Express preferences that affect judgment, including how it handles uncertainty, disagreement, complexity, and failure.
- A durable instinct may belong in SOUL; the step-by-step method for applying it belongs in a skill. Do not paste this authoring workflow into the Soul.
- Identity grants neither capability nor authority. Keep only identity-defining boundaries, not duplicated platform safeguards or prose permission systems. A Soul does not override system, safety, or project instructions; when personality and a higher rule conflict, the rule wins and the agent stays in character while complying.
- Adopting the section shape is not the work. Filled-in headings that read well but predict nothing are still a generic assistant.

## Verification

- Is the identity recognizable, even with its name removed?
- Does it describe a mind rather than a capability list?
- Is project/tool/runtime material leaking into the Soul? Have misplaced procedures and memory facts also been identified?
- Is it compact enough to remain readable, with no filler or forced sections, and within the length target for its type?
- Could a reader predict how this agent handles a new situation, a wrong premise, and high stakes?
- Does it avoid generic-assistant drift while retaining its defining character and boundaries?

Fix defects or report them briefly. A textual review is not proof of live behavior; report any unperformed behavioral test as NOT RUN. Soulforge recommends moves to other layers but does not implement them.
