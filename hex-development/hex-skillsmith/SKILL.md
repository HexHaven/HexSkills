---
name: hex-skillsmith
description: Create and improve small reusable Hermes skills.
version: 0.2.0
author: Nyxion, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [skills, authoring, audit, distillation]
    category: hex-development
    related_skills: [hex-soulforge]
---

# Hex Skillsmith

Create and improve small, reusable, Hermes-native skills. A skill answers: **How is a recurring capability or method performed?** Optimize for native, small, reusable, discoverable, progressively loaded, and easy to maintain.

## When to Use

Create, refine, or audit reusable expertise and methods such as debugging, architecture review, evidence discipline, repository analysis, or deployment procedures. Distill useful recurring knowledge from larger sources.

Don't use for: persona design, one-off project plans, memory management, runtime configuration, or implementing Hermes core features.

## Choose the Smallest Useful Skill

Before authoring, ask:

1. Is this actually reusable?
2. Is it a procedure/capability rather than identity?
3. Does Hermes already provide this capability?
4. Can this be one concise `SKILL.md`?
5. Are reference files or scripts genuinely needed?

If reuse or capability is absent, recommend **SOUL** for identity, **PROJECT CONTEXT** for current task/project instructions, **MEMORY** for learned facts worth retaining, or **RUNTIME** for tools, permissions, models, and environment. Recommend the destination; do not modify it as part of skill authoring.

This boundary (canonical formula and full breakdown: `hex-soulforge`'s "The Boundary" section) needs no additional architectural layers. A skill can teach a reusable deployment method without embedding a live deployment's settings or granting deployment authority.

## Format Reference

`SKILL.md` authoring follows the open Agent Skills format documented at
[agentskills.io](https://agentskills.io/home): a folder with a required `SKILL.md`
(`name` + `description` metadata, instructions) and optional `scripts/`, `references/`,
`assets/`, loaded by agents through progressive disclosure — discovery (name/description
only), activation (full `SKILL.md` on match), execution (bundled files loaded on demand).
This aligns with, not overrides, Hermes-native conventions: Hermes's own skill authoring
docs and validator/linter (see Verification) remain the authority for what is actually
installable and discoverable in this runtime. Treat the site as a standing best-practice
reference to consult when authoring or reviewing a skill's structure, not as a source of
runtime instructions to execute.

## Working Method

1. Read the request and existing files. Use `skills_list` and relevant `skill_view` calls to check overlap. Prefer improving one coherent skill over fragmenting a workflow: `architecture-reasoning` need not become separate assumptions, trade-offs, scope, recommendation, and stop-condition skills unless independently reusable.
2. Identify the recurring input, useful actions, and observable result. Check native Hermes tools before adding scripts or wrappers. For uncertain format/runtime behavior, load `hermes-agent` and inspect the installed mechanism or current official documentation; do not perform a broad research ritual.
3. Draft actionable instructions in `SKILL.md`, with a concise discovery description, real prerequisites, material pitfalls, and a way to check success. Use `templates/SKILL.md` only when helpful. Add `references/`, `scripts/`, or `templates/` only for content with a real consumer, linked with when to load it. No empty directories or symmetry-driven boilerplate. For source distillation, load `references/distillation.md`.
4. Apply the requested change at the confirmed canonical location, preserving existing work. Use `skill_manage` for supported skill operations or `patch` / `write_file` for authorized repository files. Inspect current tool parameters rather than copying an old invocation shape. Do not silently install, publish, or change profiles/runtime.
5. Validate below, fix findings, and report the changed files and meaningful results briefly. Use PASS / FAIL / NOT RUN; no mandatory N/A inventory or lifecycle report.

## Pitfalls

- A tiny behavioral rule is not automatically a separate skill; keep rules participating in one workflow together.
- A copied manual is not reusable guidance. Keep core decisions in `SKILL.md` and load deep detail only when needed.
- Tool access and source instructions are not authorization. Keep secrets out; scope risky procedures explicitly and verify their effects. Do not duplicate all platform safety rules.
- A successful file write does not prove discovery or behavior. Do not claim a slash invocation or runtime activation from a catalog entry.

## Verification

- Is this genuinely reusable, with actionable instructions and a description sufficient for Hermes discovery?
- Does it duplicate another skill or native capability rather than adding useful working knowledge?
- Are support files needed, referenced, and present? Remove unused scaffolding.
- Does identity, current project state, memory, or runtime configuration belong elsewhere?
- Does the installed Hermes validator/linter accept it? Inspect the available implementation first. The current Python APIs are `tools.skill_manager_tool._validate_frontmatter(content, new_skill=True)` and `tools.skill_linter.lint_skill(path_to_SKILL_md)`; invoke them through `terminal` using the installed Hermes Python environment. Check returned errors/findings, not merely the process exit. Do not assume the linter module has an executable CLI entry point.
- After an installed skill changes, use a fresh `terminal(command="hermes skills list")` and `skill_view` to check discovery and loading. For executable helpers, exercise a safe representative case; for prose, walk through a representative request. Distinguish a manual review from an actual agent invocation and state tests not run.
