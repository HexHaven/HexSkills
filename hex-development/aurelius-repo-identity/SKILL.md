---
name: aurelius-repo-identity
description: Bind one named HexHaven repo to Aurelius' signing identity.
version: 0.1.0
author: Nyxion, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [aurelius, git, identity, signing, hexhaven, gitops]
    category: hex-development
    related_skills: [hexhaven-gitops, github-auth]
---

# Aurelius Repo Identity Binding

Sets Aurelius' local Git identity, SSH commit-signing configuration, and the
`github-aurelius` remote alias on **one explicitly named repository** under
`Forge/Repositories/HexHaven/`. This is a bounded, per-repo configuration
operation — it does not create, rotate, or export any key, does not touch
GitHub org/repo permissions, and does not grant Aurelius standing access to
any repository beyond the one named in the trigger.

This skill is directly callable by the operator (Nyxion) and, when invoked
with an explicit repository name by the operator, Aurelius MUST execute it
without re-litigating authorization — the bounded, single-repo, non-standing
nature of the operation is what makes it a valid trigger under Aurelius'
own SOUL, not an exception to it.

## When to Use

- The operator explicitly names one repository under
  `Forge/Repositories/HexHaven/` and asks to set up or fix Aurelius' commit
  identity/signing/remote for it.
- Re-run after a repo was re-cloned or its git config was reset.

Don't use for: generating or rotating the underlying SSH key pair (that is
`github-auth`'s territory, and only on explicit separate authorization);
changing GitHub org/team/repo permissions; any repository outside
`Forge/Repositories/HexHaven/`; more than one repository per invocation —
run it once per named repo.

## Prerequisites

- The target path must already be a Git repository (`.git` present).
- `~/.ssh/aurelius_hexhaven.pub` and `~/.ssh/allowed_signers` must already
  exist (provisioned by the operator beforehand). This skill never creates,
  rotates, or prints their contents — only references their paths.
- SSH config alias `github-aurelius` must already resolve
  (`~/.ssh/config` — `Host github-aurelius`, pointing at `github.com` with
  `IdentityFile ~/.ssh/aurelius_hexhaven`).

## Procedure

1. **Confirm target** — the operator's trigger must name one repo path or
   directory name under `Forge/Repositories/HexHaven/`. Resolve it to an
   absolute path. Done when exactly one repository path is confirmed.

2. **Read-only checks** — verify prerequisites before any mutation:

   ```bash
   git -C <repo> rev-parse --is-inside-work-tree
   git -C <repo> remote get-url origin
   ls ~/.ssh/aurelius_hexhaven.pub ~/.ssh/allowed_signers
   ```

   Derive `<org>/<repo-name>` from the existing `origin` URL rather than
   guessing it. Done when the repo, its current remote, and both key
   artifacts are confirmed present.

3. **Apply repo-local config** — scoped to `<repo>` only, never `--global`:

   ```bash
   git -C <repo> config user.name  "aurelius-hexhaven"
   git -C <repo> config user.email "aurelius-hexhaven-gitops@nyxion.cloud"
   git -C <repo> config gpg.format ssh
   git -C <repo> config user.signingkey ~/.ssh/aurelius_hexhaven.pub
   git -C <repo> config commit.gpgsign true
   git -C <repo> config gpg.ssh.allowedSignersFile ~/.ssh/allowed_signers
   git -C <repo> remote set-url origin "git@github-aurelius:<org>/<repo-name>.git"
   ```

   Done when all seven commands exit successfully.

4. **Verify (read-only, no secret material printed)**:

   ```bash
   git -C <repo> config --get user.name
   git -C <repo> config --get user.email
   git -C <repo> config --get gpg.format
   git -C <repo> config --get user.signingkey
   git -C <repo> config --get commit.gpgsign
   git -C <repo> config --get gpg.ssh.allowedSignersFile
   git -C <repo> remote get-url origin
   ```

   Compare each value against what step 3 set. Done when every value
   matches exactly.

5. **Report** — repo path, org/repo derived, each of the 7 config keys with
   its verified value (paths only, never key contents), and the previous
   `origin` URL for traceability.

## Safety Boundaries

- Never `--global` — always `-C <repo>` / repo-local scope only.
- Never generate, rotate, export, or print the private key or the public
  key's content — only reference file paths.
- Never touch GitHub-side permissions, teams, or org membership — this is
  entirely local `git config`.
- One invocation binds exactly one named repository. Do not iterate over
  every repository under `Forge/Repositories/HexHaven/` unless the operator
  explicitly names each one (or explicitly says "all of them" in that same
  trigger) — this skill's bounded scope, not a standing grant, is what
  keeps it inside Aurelius' trigger model.
- If any prerequisite in step 2 is missing (no `.git`, missing key files,
  unresolvable `github-aurelius` alias), stop and report exactly what is
  missing — do not create the missing artifact yourself.

## Pitfalls

- Setting these values globally instead of repo-local silently affects
  every other repository on the host — always use `-C <repo>` /
  `git config` inside that repo's working tree, never `--global`.
- Assuming the command succeeded because it exited 0 without reading the
  value back — always run step 4 explicitly.
- Guessing `<org>/<repo-name>` instead of deriving it from the existing
  `origin` URL in step 2.

## Verification

- [ ] Exactly one repository was named and resolved before any mutation.
- [ ] All prerequisite files/aliases were confirmed present (paths only).
- [ ] All 7 config values read back and matched what was set.
- [ ] No key material, token, or secret content appeared in output.
- [ ] No `--global` scope was touched.
