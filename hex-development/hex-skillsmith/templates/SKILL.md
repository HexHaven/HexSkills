---
name: <skill-name>
description: <Trigger-complete sentence, at most 60 characters.>
version: 0.1.0
author: <Human Contributor>, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [<domain>, <capability>]
    category: <category>
    related_skills: []
---

# <Skill Title>

<One or two sentences: capability, ownership, and what it does not own.>

## When to Use

- <Concrete trigger.>
- <Concrete trigger.>

Don't use for: <counter-trigger or adjacent owner>.

## Prerequisites

- <Only real requirements; omit this section if none.>

## Procedure

1. **<Stage>** — <specific action using Hermes tools>. Done when <observable completion criterion>.
2. **<Stage>** — <specific action>. Done when <observable completion criterion>.
3. **<Stage>** — <verify actual state>. Done when <evidence requirement>.

## Safety Boundaries

- Read-only discovery precedes mutation.
- <Exact authorization and scope limits.>
- Use `<TOKEN>`, `<PASSWORD>`, `<HOST>`, and `<IP_ADDRESS>` in examples; never include secrets.

## References

- `references/<topic>.md` — <load condition and purpose>.
- `templates/<artifact>.md` — <output use>.

Remove this section and unused directories when no support files are needed.

## Pitfalls

- <Specific failure mode and correction.>
- <Specific scope or verification trap.>

## Verification

- [ ] <Structural check.>
- [ ] <Behavioral check with observed evidence.>
- [ ] <Safety and authorization check.>
