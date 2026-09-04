# HUD visual diagnostics

## Reproduction pattern

A live Niri window can report:

```text
Title: "Hermes HUD"
App ID: "hermes"
Is floating: yes
```

A rule using `match app-id="^Hermes$"` does not match that lowercase app-id. Correct the maintained literate source, tangle it, validate, reload, and query `niri msg windows` again.

## Border diagnosis

A valid targeted rule can include:

```kdl
border { off; }
focus-ring { off; }
draw-border-with-background false
```

In the observed HUD screenshot, the thin blue outline followed the rounded inner composer/input control rather than the full 620×320 outer HUD rectangle. The outer translucent window had no matching perimeter outline. That geometry indicates an application-level CSS/input focus outline, not a Niri compositor border. Do not keep adding Niri border settings when the compositor settings are already explicit and the visual artifact is inset around a control.

## Proof pattern

1. `niri validate` → `config is valid`.
2. `niri msg action load-config-file` reloads the active config.
3. `niri msg windows` confirms the target remains floating and reports the expected dimensions/position.
4. Treat pixel-level disappearance of an inner control outline as unverified unless a fresh screenshot or application-layer inspection confirms it.
