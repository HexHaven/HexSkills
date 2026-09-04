---
name: niri-configuration
description: "Use when changing Niri config. Trace source to runtime."
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [niri, wayland, compositor, kdl, org-babel, window-rules, hud, visual-debugging]
    category: hex-development
    related_skills: [hex-build]
---

# Niri Configuration

Operate Niri changes as a closed source-to-runtime loop. The maintained source may be a literate Org document while Niri consumes generated KDL files; never treat the generated file as the authoring source when it declares itself generated.

## When to use

- A Niri window rule appears not to match.
- A Wayland application has the wrong workspace, floating state, size, border, focus ring, or position.
- A screenshot shows a visual artifact and it is unclear whether the compositor or application rendered it.
- A literate Org configuration must be changed and applied safely.

## Source and runtime ownership

1. Identify the maintained source (`.org`, `.kdl`, or repository-native configuration) and the generated/runtime target.
2. Read repository instructions and inspect the current Git state before editing.
3. Query the live compositor with `niri msg windows` and preserve the reported `Window ID`, title, `App ID`, floating state, workspace ID, and geometry exactly. Niri app-id matching is case-sensitive in practice; do not normalize observed values.
4. Inspect all matching and later rules for precedence. A rule that looks correct in the source is not proof that it is active.
5. For literate Org sources, edit only the Org source and tangle through Emacs. Use an explicit batch invocation that loads both `org` and `ob`, prints the tangle result, and runs `org-babel-tangle-file`; a silent invocation may leave generated files stale without an obvious error.
6. Verify the intended block exists in the generated target (not merely that tangling returned), validate the actual config with `niri validate`, reload using `niri msg action load-config-file`, then query live state again.
7. For application-controlled recording via a compositor binding (for example `voxtype record toggle`), ensure the application's own global/evdev hotkey listener is disabled to avoid duplicate triggers. Document whether the binding is push-to-talk (press/release) or toggle (press once to start, again to stop).

## Visual artifact diagnosis

Separate the window frame from application content before changing rules:

- A compositor border or focus ring normally follows the full outer window rectangle.
- A CSS/input focus outline follows an inner control, often with its own rounded corners, and remains inset from the window edge.
- A panel background, shadow, or blur can make an edge appear to be a border; inspect the full perimeter and compare it with the live window geometry.
- If the Niri rule already contains `border { off; }`, `focus-ring { off; }`, and `draw-border-with-background false`, do not add redundant compositor rules without evidence. Report that the remaining artifact is likely application-rendered and move diagnosis to the application layer.

See `references/hud-visual-diagnostics.md` for the tested HUD case and evidence pattern.

## Rule design

Keep rules narrow and explicit:

```kdl
window-rule {
  match app-id="^hermes$" title="^Hermes HUD$"
  open-on-workspace "CLOUD"
  open-floating true
  default-column-width { fixed 620; }
  default-window-height { fixed 320; }
  border { off; }
  focus-ring { off; }
  draw-border-with-background false
}
```

Use the exact observed app-id and title. Anchor regular expressions with `^` and `$` when matching one application/window, unless multiple variants are an intentional requirement.

## Qualification checklist

Report each check with evidence:

- `PASS` — source contains the intended rule.
- `PASS` — generated KDL contains the intended rule.
- `PASS` — `niri validate` accepts the active configuration.
- `PASS` — reload command completes.
- `PASS` — `niri msg windows` shows the target with intended floating state, workspace, and geometry.
- `NOT RUN` — visual confirmation was not possible; do not claim pixel-level success.

A reload can update rule-managed geometry without proving that every visual property came from Niri. For screenshot-based claims, state whether the evidence covers the outer window frame or only application content.

## Safety and rollback

- Preserve unrelated working-tree changes; never reset or clean them.
- Do not manually edit generated KDL when the Org source is authoritative.
- Before tangling, capture the source diff and avoid broad refactors.
- Roll back by restoring only the changed source hunk, re-tangling, validating, and reloading.
- Do not commit, push, or alter unrelated generated artifacts without explicit authorization.

## Common pitfalls

- Matching `^Hermes$` when the live app-id is `hermes`.
- Treating a visible inner blue input outline as a Niri window border.
- Declaring success after editing only the Org source while the generated runtime file remains stale.
- Running a silent or incorrect tangle command and assuming it updated the target; load `ob`, print the tangle result, and inspect the generated block.
- Binding an application's toggle command in Niri while leaving its independent global hotkey listener enabled, causing duplicate start/stop events.
- Replacing or discarding unrelated changes in a literate configuration repository.
