# Provenance-Aware Distillation

Distillation converts source material into a reusable capability, not a compressed copy of the source.

## 1. Define the target capability

State:

- what repeated task the skill should improve;
- who invokes it and with what inputs;
- what output or behavior proves success;
- what source topics are irrelevant to that capability.

Without this boundary, stop before extracting.

## 2. Inventory evidence and rights

For each source record exact URL/path, version or commit, license evidence, and files inspected. Distinguish:

- explicit license text;
- package or README license claims without a present license file;
- no license evidence;
- third-party material embedded in the source.

General ideas may be independently expressed. Copy text or code only when necessary, permitted, and accompanied by required notices. When in doubt, rewrite from behavior and avoid substantial source expression.

## 3. Separate layers

| Layer | Keep? | Destination |
|---|---|---|
| Stable decision rule | Yes | `SKILL.md` if central; otherwise reference |
| Repeatable procedure | Yes | `SKILL.md` or focused reference |
| Deep domain detail | If needed | `references/` |
| Reusable output shape | If needed | `templates/` |
| Deterministic parsing/validation | If prose is insufficient | `scripts/` |
| Product installer, branding, marketing | Usually no | Provenance note only if relevant |
| Foreign runtime command/metadata | No | Replace with observed Hermes behavior |
| Historical implementation detail | Only if it prevents a known pitfall | Reference |

## 4. Build a concept decision table

Use `ADOPT`, `ADAPT`, `REJECT`, or `DEFER`:

- `ADOPT`: concept fits Hermes unchanged at the behavioral level.
- `ADAPT`: useful concept needs Hermes tools, safety, or scope changes.
- `REJECT`: conflicts with ownership, safety, current syntax, or task scope.
- `DEFER`: potentially useful but requires a separate authorized evaluation.

Record a one-sentence Hermes adaptation for every adopted or adapted concept.

## 5. Rewrite from behavior

Draft without the source open when practical, using the decision table as the specification. Then compare for:

- accidental phrase copying;
- missing license notices for actual reuse;
- retained branding or provenance markers;
- foreign command names, paths, metadata, hooks, or installers;
- assumptions that are not true in the active Hermes version.

## 6. Apply progressive disclosure

Keep triggers, core workflow, safety, and verification in `SKILL.md`. Move details that are needed only during a stage into a named reference. Avoid arbitrary chunk counts; one independently useful topic per reference is enough.

## 7. Verify provenance

The final report must say:

- what was independently rewritten;
- what exact text/code, if any, was reused;
- applicable license and retained notices;
- rejected/deferred integrations;
- source versions inspected.

Do not describe a license claim as a verified license file when that file was absent.
