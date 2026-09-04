# Hermes Skill Specification

**Observed installation:** Hermes Agent `v0.20.6 (2026.8.27)`, upstream `a24c12d1`. Recheck current installed source and official documentation before framework-sensitive changes; installed behavior is authoritative for the active runtime.

## Locations and discovery

- Active profile root: `$HERMES_HOME`; default profile normally resolves to `~/.hermes`.
- User-local skills: `$HERMES_HOME/skills/<optional-category>/<skill-name>/SKILL.md`.
- Hermes recursively discovers skill roots and excludes support directories beneath a discovered root.
- Local skills take precedence over configured external directories with the same name; trusted project-local skills have higher precedence within their repository.
- Current source of truth: `$HERMES_HOME/hermes-agent/agent/skill_utils.py` and `$HERMES_HOME/hermes-agent/tools/skill_manager_tool.py` when Hermes is git-installed.

## Required `SKILL.md` structure

The installed validator requires:

- YAML frontmatter beginning with `---` at byte 0;
- a YAML mapping containing non-empty `name` and `description`;
- a closing `---` fence;
- a non-empty body;
- content no larger than the installed limit (currently 100,000 characters for agent writes).

New skill names must be at most 64 characters and use lowercase letters, digits, dots, underscores, or hyphens, starting with a letter or digit. The installed linter uses the stricter common form `[a-z0-9][a-z0-9_-]*`; prefer lowercase kebab-case. The frontmatter `name` must equal the containing directory name.

New agent-created descriptions must be one trigger-complete sentence of at most 60 characters. End with a period and avoid marketing adjectives.

## Current conventional frontmatter

```yaml
---
name: example-skill
description: Perform one narrow repeatable capability safely.
version: 0.1.0
author: Human Contributor, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [domain, capability]
    category: category-name
    related_skills: []
---
```

`name` and `description` are hard requirements. Current local authoring conventions also expect `version`, `author`, `license`, `platforms`, and `metadata.hermes.tags`. Use semantic versions; new skills normally start at `0.1.0`.

## Platforms

Documented values are `linux`, `macos`, and `windows`. Omit `platforms` to load on all platforms, or list only platforms actually supported by the prose and scripts. Installed lint also accepts legacy `darwin`, but new skills should use `macos`.

## Optional Hermes metadata

Under `metadata.hermes`:

- `tags`: short discovery terms.
- `category`: catalog/category label; directory category remains the observed CLI grouping source.
- `related_skills`: existing related skills only; use `[]` when no relationship is needed.
- `requires_toolsets`: hide unless every named toolset is active.
- `requires_tools`: hide unless every named tool is available.
- `fallback_for_toolsets`: hide when a listed toolset is available.
- `fallback_for_tools`: hide when a listed tool is available.
- `config`: non-secret settings stored under `skills.config`.
- `blueprint`: optional automation suggestion metadata; installation does not itself schedule the job.

Do not add conditional gates merely because a procedure sometimes uses a tool; gates affect discovery. Add them only when the skill cannot function without the capability.

Top-level optional requirement declarations include:

- `required_environment_variables` for secrets securely configured outside prompts;
- `required_credential_files` for credential files relative to `$HERMES_HOME`.

Never embed their values in a skill.

## Body and progressive disclosure

Recommended body:

1. identity/purpose;
2. `## When to Use` including counter-triggers;
3. prerequisites or authority checks when needed;
4. actionable numbered procedure with completion criteria;
5. safety boundaries;
6. pointers to support files;
7. `## Pitfalls`;
8. `## Verification`.

Use native Hermes tool names such as `read_file`, `search_files`, `write_file`, `patch`, `terminal`, `web_search`, and `skill_view`. Do not direct the agent to wrapped shell utilities when native tools exist.

## Support files

Supported progressive-disclosure directories:

- `references/` — deep methodology, APIs, decision rules, provenance.
- `templates/` — reusable output shapes.
- `scripts/` — necessary deterministic helpers; prefer standard library and narrow scope.
- `assets/` — supplementary non-procedural files.

Current documentation also recognizes `examples/` for installed bundles, but `skill_manage` write operations are currently limited to `references`, `templates`, `scripts`, and `assets`. Use only directories the chosen creation path supports.

Every support file must have a consumer in `SKILL.md` or another referenced file. Support directories may contain a template named `SKILL.md`; discovery excludes them after finding the parent skill root.

## Creation and activation

- Create user-local skills with `skill_manage(action="create", name=..., category=..., content=...)`.
- Add support files with `skill_manage(action="write_file", ...)`.
- Confirm before creation or deletion; stop on an existing name.
- Installed skills are available as `/<skill-name>` slash commands on compatible, enabled surfaces.
- Multiple leading skill commands can be stacked (currently up to five).
- The current conversation's skill index may be cached. `/reload-skills` re-scans; a new session is the conservative activation boundary.
- A successful write does not prove discovery or slash invocation.

## Verification

1. Parse frontmatter with the installed validator or equivalent YAML parser.
2. Run the installed linter when available:
   `terminal(command="python -m tools.skill_linter <skill-directory>", workdir="$HERMES_HOME/hermes-agent")`.
3. Run `terminal(command="hermes skills list")` in a fresh process and confirm exact name, category, enabled status, and platform compatibility.
4. Load with `skill_view` or start a fresh session with the skill preloaded.
5. Perform a safe representative dry run and record structure, discovery, activation, and behavior separately.

## Common pitfalls

- Description routing signal appears only after character 60.
- Frontmatter name and directory differ.
- Platform gate is copied rather than audited.
- A support link is dangling or an empty directory has no consumer.
- A foreign agent's metadata or command syntax is copied into Hermes.
- A dry run proves generated prose but not actual discovery or activation.
- Documentation examples are treated as stricter than the installed validator/linter without checking both.
