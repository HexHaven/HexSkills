# HexSkills

HexHaven's skill library for [Hermes](https://hermes-agent.nousresearch.com/) agents — reusable, on-demand knowledge documents (procedures, references, templates, scripts) that agents load progressively rather than carrying in every context.

This repo is **not** a copy of any single Hermes profile's local skills. It is the authoritative, git-tracked source for skills we've built ourselves (as opposed to skills bundled with Hermes or installed from third-party hubs), meant to be shared across multiple Hermes profiles/machines without duplication.

## Structure

Skills are grouped into category directories, mirroring the layout Hermes itself uses under `~/.hermes/skills/`:

```
HexSkills/
├── skills.sh.json         # skills.sh-compatible category groupings (for hub browsing)
├── <category>/
│   ├── <skill-name>/
│   │   ├── SKILL.md       # required — main instructions
│   │   ├── references/    # optional — supporting docs loaded on demand
│   │   ├── templates/     # optional — output scaffolding
│   │   ├── scripts/       # optional — helper scripts
│   │   └── assets/        # optional — supplementary files
│   └── ...
└── README.md
```

### Current categories

| Category | Description |
| --- | --- |
| [`hex-development`](./hex-development/) | General-purpose Hermes agent workflow skills: project idea → spec → implementation loop (`hex-seed`/`hex-build`), session recap (`hex-recap`), skill authoring (`hex-skillsmith`), agent Soul authoring (`hex-soulforge`), and Niri compositor configuration. |

New categories are added organically as skills are authored — no placeholder categories are pre-created.

## Using this hub with Hermes

### Option A — external skill directory (read/write, for profiles you actively develop on)

Point a Hermes profile at this repo so its skills load alongside the profile's local ones. Add under `skills.external_dirs` in that profile's `config.yaml`:

```yaml
skills:
  external_dirs:
    - /path/to/HexSkills   # wherever you cloned this repo
```

Or via CLI:

```bash
hermes -p <profile> config set skills.external_dirs '["/path/to/HexSkills"]'
```

Skills under an external dir are fully integrated: they appear in the skill index, `skills_list`, `skill_view`, and as `/skill-name` slash commands. If a same-named skill exists both locally and here, the local one wins.

**Note:** external dirs are not a write-protection boundary. If this checkout is writable, `skill_manage` (patch/edit/write_file/etc.) can modify files here directly — commit and push deliberately to keep the shared history clean.

### Option B — install as a GitHub skill tap (read-only, per-skill install)

Once pushed to `github.com/HexHaven/HexSkills`, this repo is installable as a direct GitHub tap:

```bash
hermes skills tap add HexHaven/HexSkills
hermes skills browse --source github        # or hermes skills search <query>
hermes skills install HexHaven/HexSkills/hex-development/hex-build
```

The `skills.sh.json` file at the repo root defines category groupings (`groupings`) so installs show real category labels instead of tag-derived guesses, both in the Hermes dashboard's Browse-hub view and on skills.sh-compatible tooling.

## Conventions

- One skill = one directory with a `SKILL.md` (frontmatter + procedure, following the [house authoring standard](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/#skillmd-format)).
- Keep `SKILL.md` lean; put long-form material in `references/`, output scaffolding in `templates/`, and runnable helpers in `scripts/`.
- Skills sourced from Hermes bundles, official/optional catalogs, or third-party hubs do **not** belong here — this repo is exclusively for skills authored by us.
- Commits are DCO signed-off (`-s`) and SSH-signed (`-S`).
