# GitOps Publication and Deployment

## Core invariant

Production must deploy a reviewed Git revision, not an untracked local working tree:

```text
local repository → APPLY → QUALIFY → review diff → commit → push
→ exact commit SHA → production checkout/deploy → verify same SHA
→ service verification
```

Git publication and remote deployment are distinct mutations. APPLY approval never grants either; PUBLISH approval never grants DEPLOY.

## Publication: explicit PUBLISH authorization only

Use the approved repository, remote, branch, intended files, and commit-message convention. Before the first stage of a newly scaffolded toolchain (e.g. Node/TS `node_modules`, build output dirs like `dist/`, lockfile-adjacent caches), check whether `.gitignore` exists and covers generated directories; if it is missing or incomplete, create/extend it as part of APPLY-scope local hygiene (not itself a PUBLISH mutation) before staging, so generated artifacts never enter the index. Preserve unrelated changes and stage only intended files. Review:

```text
git status --short
git diff --cached --check
git diff --cached --stat
git diff --cached
```

Create an explicit commit and record `LOCAL_COMMIT=<full SHA>`. Push only to approved remote/branch; never force-push or rewrite shared history. Verify both equal `LOCAL_COMMIT`:

```text
git rev-parse HEAD
git rev-parse refs/remotes/<approved-remote>/<approved-branch>
```

If they differ, stop. Do not deploy a different SHA.

## Git-checkout deployment: explicit DEPLOY authorization only

Prerequisites: approved host, SSH identity/trust, production path, remote/branch, build/install and service commands, health check, and rollback method. Do not use `git pull` blindly.

On approved host/path inspect first:

```text
git status --short
git fetch --prune <approved-remote>
git rev-parse HEAD
git rev-parse <approved-remote>/<approved-branch>
```

Unexpected non-empty production status means **STOP**. Do not reset, clean, stash, overwrite, or alter a dirty checkout without separately explicit authorization. Record `PREVIOUS_DEPLOYED_SHA=<full SHA>`. Update through repository-defined exact-revision mechanism; for fast-forward branch deployment use an action such as:

```text
git merge --ff-only <approved-remote>/<approved-branch>
```

Verify `git rev-parse HEAD` equals `LOCAL_COMMIT`; “Already up to date” is not proof. Then—and only then—run repository-defined build/install commands. Do not run automatic dependency upgrades, `npm audit fix`, package upgrades, or system upgrades without separate authorization.

## Service, qualification, and rollback

Restart/reload is separate remote mutation. Before it capture service state, retain `PREVIOUS_DEPLOYED_SHA`, and verify approved rollback target. Use only documented service commands. Afterwards observe process state, defined health endpoint, intended user-visible path, and relevant logs. Remote qualification minimally requires `DEPLOYED_SHA == LOCAL_COMMIT`, with each check `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN`.

If verification fails, do not improvise. Use repository-approved rollback only if remote rollback was explicitly authorized: restore `PREVIOUS_DEPLOYED_SHA` through approved method, rebuild/restart only as defined, then re-run health checks. Never automatically reset/clean production.

## Stop conditions

Stop without mutation on SSH trust failure, changed host key, target/host/path mismatch, unexpected production changes, absent rollback evidence, unapproved command, or published/deployed SHA mismatch. Never modify `~/.ssh/config`, accept changed host keys, disable host-key verification, or expose credentials.