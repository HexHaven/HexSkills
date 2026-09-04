---
name: hex-soulforge
description: Design, audit, and refine Hermes persona SOUL.md files.
version: 0.1.0
author: Nyxion, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [persona, soul, identity, authoring, audit]
    category: hex-development
    related_skills: [hex-skillsmith]
---

# Hex Soulforge

Design, audit, refine, and validate Hermes persona identity contracts (`SOUL.md`). Owns persona structure, tone, authority boundaries, and anti-drift rules for a role brief. It does not own domain/specialist truth, infrastructure state, deployment, or platform/gateway configuration.

## When to Use

- A new Hermes profile needs a SOUL.md generated from a role brief.
- An existing persona/SOUL needs audit for drift, contradiction, or authority creep.
- A persona needs targeted refinement (tone, proactivity, boundaries) without a full rewrite.
- Naming candidates are needed for a new persona.

Don't use for: infrastructure/platform config for a profile (routing, model assignment, tool grants — that is runtime configuration, not identity), repository `AGENTS.md` files, or general project specs.

## Prerequisites

- An operator-authorized role brief (who the persona is for, what it must never do, its relationship to the user and to other profiles). Do not invent authority the brief does not grant.
- Awareness of existing profile names and identities (`hermes -p <profile> config show` or `ls ~/.hermes/profiles/`) to avoid collisions.

## Procedure

1. **Extract the persona contract** — from the role brief, pull role summary, duties, exclusions, authority (may/may-not), tone, proactivity level, relationship model, and uncertainty behavior. Load `references/persona-model.md` for the dimension set. Done when every dimension is filled or explicitly marked N/A.
2. **Check collisions** — compare the proposed name and role against existing Hermes profiles and the platform/backend name itself (e.g. never name a persona "Hermes" on the Hermes platform). Done when no unresolved name or authority collision remains.
3. **Draft the SOUL** — use `templates/SOUL.md` as the section skeleton; fill only behaviorally meaningful sections (see `## Section Policy` in the template). Keep mutable infrastructure/project facts out of the SOUL. Done when a complete draft exists.
4. **Audit the draft** — run every check in `references/validation-checklist.md` against the draft. Done when each check has an observed PASS/FAIL, not an assumption.
5. **Write the canonical file** — confirm the exact persona name with the operator, then write the audited SOUL.md to `/home/nyxion/Forge/Resources/agents/Personas/<personaname>/SOUL.md`. If a file already exists there, back it up (e.g. `SOUL.md.bak-<timestamp>`) before overwriting, and confirm the overwrite with the operator first. Done when the canonical file is written and read back to confirm content matches the audited draft.
6. **Report** — summarize role brief source, name/collision checks, authority model, drift risks, canonical file path written, and what validation was and was not performed.

Mirroring the SOUL.md to a live profile (`~/.hermes/profiles/<profile-name>/SOUL.md`), checksum verification, and oneshot activation validation are a separate, later step owned outside this skill. Do not perform that mirror/activation step here — hand off the canonical artifact instead.

## Safety Boundaries

- Never grant a persona deploy/publish/push/approval authority the role brief did not explicitly state.
- Never collapse platform/backend identity (e.g. Hermes) into persona identity.
- Keep the user (or the declared final operator) as final approval authority unless the brief explicitly delegates that.
- No secrets, credentials, or live personal data in SOUL files.
- Read-only discovery (existing profiles, existing SOUL) precedes any overwrite; back up before overwriting an existing SOUL.

## References

- `references/persona-model.md` — the 8 persona dimensions, naming rules, and anti-patterns to check against.
- `references/validation-checklist.md` — required and recommended audit checks.
- `templates/SOUL.md` — section skeleton for a new SOUL.md.

## Pitfalls

- Persona-as-costume: strong voice, no operational rules (authority, escalation, exclusions left vague).
- Authority creep: proactivity language quietly implying autonomous execution rights.
- SOUL bloat: mutable project facts, infrastructure topology, or long runbooks stored in the persona file instead of profile config/skills.
- Writing the mirrored `~/.hermes/profiles/<name>/SOUL.md` copy yourself instead of leaving that mirror/activation step to the separate later workflow that owns it.
- Overwriting an existing canonical SOUL.md at `/home/nyxion/Forge/Resources/agents/Personas/<personaname>/SOUL.md` without a backup or without operator confirmation.
- Treating a successful canonical write as proof of activation; mirroring and oneshot validation are a separate, later step owned elsewhere.

## Verification

- [ ] Every persona dimension in `references/persona-model.md` was filled or explicitly marked N/A.
- [ ] Name/role checked against existing profiles and the platform name; no unresolved collision.
- [ ] Every check in `references/validation-checklist.md` has an observed result.
- [ ] Canonical SOUL.md written to `/home/nyxion/Forge/Resources/agents/Personas/<personaname>/SOUL.md` and read back to confirm it matches the audited draft; any pre-existing file was backed up first.
- [ ] No mirror write to `~/.hermes/profiles/<profile-name>/SOUL.md` and no activation/oneshot validation was performed here; that step was left to the separate downstream workflow.
