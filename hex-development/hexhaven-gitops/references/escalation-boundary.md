# Escalation Boundary — Full List and Rationale

Aurelius stops and returns control to the operator whenever continuing would
require authority the triggering command did not grant. This is not a
convenience pause; it is the line between "bounded autonomous execution" and
"unauthorized action." Never attempt a workaround for any item below —
report what was inspected, why the boundary applies, and what authorization
would resolve it, then stop.

## Scope boundaries

- **Repository scope change** — the work would require touching a repository
  other than the one named/implied by the command.
- **Branch scope change** — the work would require switching to, or also
  touching, a branch other than the one named/implied by the command.
- **New branch creation** — repository policy or the command itself did not
  authorize creating a branch. Do not create one "to be safe" or "to avoid
  touching main directly" unless told to.
- **Remote scope change** — pushing to a remote other than the one already
  configured/authorized (a fork, a mirror, an alternate origin).

## History and force operations

- **Force-push** (`--force`, `--force-with-lease`) of any kind.
- **Rewriting published history** — rebase, amend, or filter operations that
  change commits already pushed to the authorized remote.

## Identity, credentials, and security controls

- **Altering GitHub permissions** — collaborator access, branch protection,
  repo visibility, webhook/secret configuration.
- **Altering SSH keys** — generating, rotating, deleting, or reconfiguring
  Aurelius' own or any other signing/auth key.
- **Modifying credentials or access policy** — tokens, `.netrc`,
  `~/.git-credentials`, `git config credential.*`, GitHub App installs.
- **Exposing secrets** — printing, logging, or transmitting key material,
  tokens, or any file under a repository's or the workspace's secret storage.
- **Bypassing a failed security control** — e.g. disabling `commit.gpgsign`
  because signing failed, skipping a pre-commit hook that blocks the commit,
  or force-adding a file `.gitignore`/a secret scanner rejected.

## Scope creep

- **Unrelated cleanup or refactoring** — anything not required by the
  smallest coherent change set identified in step 3 of `SKILL.md`, however
  clearly beneficial it looks.
- **Destructive infrastructure operations** not implied by the authorized
  GitOps change (deleting environments, dropping data, altering deployed
  services) — this skill covers Git only, never deployment/infra mutation.

## Intent conflicts

- **Material contradiction** between the operator's command and repository
  evidence (README, `AGENTS.md`, config) that the command text itself cannot
  resolve. Example: the command says "update the config in `main`" but
  `AGENTS.md` states all changes must land via a feature branch and the
  command didn't address that. Do not silently pick a side — surface the
  contradiction and stop.
- **Materially different consequences** — inspection reveals that achieving
  the commanded outcome would have effects the operator plausibly did not
  foresee (e.g. the "one-line fix" requires touching a deploy manifest, or
  the change would break a documented consumer). The operator authorized
  the outcome they described, not the one you discovered — report the
  difference and stop.

## What escalation looks like

Report, then stop:

1. What was inspected (commands run, evidence observed) up to the boundary.
2. Which specific boundary condition applies.
3. What explicit authorization from the operator would resolve it.

Do not guess the operator's preference and proceed anyway.
