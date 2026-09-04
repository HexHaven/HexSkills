---
name: nyx-build
description: Close bounded tasks through plan, build, and proof.
version: 0.2.0
author: Nyxion, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [nyx, development, implementation, gitops, deployment, verification]
    category: nyx-development
    related_skills: []
---

# Nyx Build

Implement an already-specified milestone through a closed, evidence-backed loop. `nyx-seed` owns intent/specification and writes `.nyx/HANDOFF.md`; this skill owns execution, including an optional authorization-gated Git publication and an optional authorization-gated remote deployment.

**GitOps invariant:** production deploys a reviewed Git revision, never an untracked or uncommitted local working tree. A repository may define another deployment model, but do not use arbitrary `scp`/`rsync` working-tree transfer as the normal path unless that model is explicitly evidenced.

## When to Use

- A bounded task has observable acceptance criteria from an operator, project documentation, or `nyx-seed` handoff.
- A reviewed repository change needs local implementation and qualification.
- An approved remote target may require an exact Git revision deployed and verified.

Don't use for: vague project discovery, unbounded architecture exploration, creating Hermes skills, or a task with unresolved high-impact intent. `nyx-seed` remains the owner of project intent and handoff creation.

## Lifecycle

`PLAN → APPLY_LOCAL → QUALIFY_LOCAL → [PUBLISH] → [DEPLOY] → QUALIFY_REMOTE → UNIFY`

Conceptual states:

```text
PLANNED → IN_PROGRESS_LOCAL → QUALIFIED_LOCAL
       → AWAITING_PUBLISH_APPROVAL → PUBLISHED
       → AWAITING_DEPLOY_APPROVAL → DEPLOYING → QUALIFYING_REMOTE
       → PASS | FAIL | BLOCKED
```

PUBLISH and DEPLOY are optional. A code-only task can close at `QUALIFIED_LOCAL`; a publication-scoped task can close at `PUBLISHED`.

## Authorization Gates

Treat these as separate explicit approvals for the named repository, files, remote/branch, and target:

| Gate | Permits | Does not permit |
|---|---|---|
| **APPLY** | local file edits and local tests/builds | commit, push, deployment, restart/reload |
| **PUBLISH** | `git add` of intended files, explicit commit, push to approved remote/branch | deployment or service action |
| **DEPLOY** | only the approved remote deployment action and its defined rollback scope | other remote changes |

Tests passing never imply PUBLISH. A successful push never implies DEPLOY.

## Procedure

### 1. PLAN

Load `references/plan.md`, then inspect repository policy, handoff, current Git state, protected unrelated work, maintained validation commands, and deployment evidence. Classify `deployment_mode` as exactly `none`, `git-checkout`, `artifact`, `container`, or `unknown`.

For `git-checkout`, record only evidence-backed or explicitly USER-STATED values: approved remote, branch, production host, production checkout path, service unit, build/install command, restart/reload command, health verification, and rollback method. `unknown` is visible; do not invent a deployment procedure. Present the plan, authorization gates, risks, and recovery/rollback proposal, then **STOP** for APPLY authorization. Done when the operator can approve local work without implicitly approving publication or deployment.

### 2. APPLY_LOCAL

After explicit APPLY authorization, load `references/apply.md` and make the smallest coherent local change. Preserve unrelated work. If `.nyx/HANDOFF.md` is in scope, preserve its original Goal/Scope/Non-Goals/Acceptance Criteria; append only operator-approved amendments. Done when the approved local change is implemented or honestly `BLOCKED`/`CANCELLED`.

### 3. QUALIFY_LOCAL

Load `references/qualify.md`. Run repository-defined validation, then inspect `git diff --check`, `git diff --stat`, and `git diff`. Record every check as `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN`. Do not proceed to PUBLISH after a validation failure unless the operator explicitly accepts that known failure. Done when every applicable local acceptance criterion has evidence or an explicit gap.

### 4. PUBLISH (optional)

Only after explicit PUBLISH authorization, load `references/gitops.md` and stage exactly the intended files. Review `git status --short`, `git diff --cached --check`, `git diff --cached --stat`, and `git diff --cached`. Create an explicit commit; use the repository convention or operator-provided message rather than inventing one when either exists.

Record `LOCAL_COMMIT` as the full SHA. Push only to the approved remote and branch, without force-push or history rewrite. Verify `HEAD` and the approved remote-tracking branch both equal `LOCAL_COMMIT`. Done when the reviewed commit is demonstrably on the approved remote branch; otherwise stop and report the mismatch.

### 5. DEPLOY (optional)

Only after explicit DEPLOY authorization for the named target and rollback scope, load `references/gitops.md`. For an approved `git-checkout` target, inspect remote state first; never blindly use `git pull`. Require a clean production checkout, fetch the approved remote/branch, fast-forward safely (or use the repository-defined exact-revision mechanism), and verify remote `HEAD == LOCAL_COMMIT` before repository-defined build/install or service work.

Before a separately authorized restart/reload, capture service state and `PREVIOUS_DEPLOYED_SHA`; ensure the approved rollback target is known. Run only repository-defined commands. Stop on SSH trust failure, a changed host key, unexpected production working-tree modifications, target mismatch, or SHA mismatch. Done when the intended revision and approved service action have observed evidence.

### 6. QUALIFY_REMOTE and UNIFY

Remote qualification requires `DEPLOYED_SHA == LOCAL_COMMIT` plus repository/service-specific checks. A running process alone is insufficient. Load `references/qualify.md` and `references/unify.md`; distinguish local implementation, publication, and deployment explicitly. If deployment was not authorized, report `Deployment: NOT RUN`. Done when every stage is accounted for as `PASS`, `FAIL`, `BLOCKED`, `NOT RUN`, or `CANCELLED` without implying publication was deployment.

## Handoff Contract

When `.nyx/HANDOFF.md` is in scope, validate it against fresh repository evidence before PLAN. A deployment-capable build may append this section without altering `nyx-seed`'s original handoff ownership:

```markdown
## Deployment

mode: none|git-checkout|artifact|container|unknown
target: UNKNOWN
remote: UNKNOWN
branch: UNKNOWN
production_path: UNKNOWN
service: UNKNOWN
health_check: UNKNOWN
rollback: UNKNOWN
```

All unresolved values remain `UNKNOWN`. A task is not deployment-ready while required high-impact deployment fields are unresolved.

## Safety and Git Boundaries

- Read-only discovery precedes local, Git, and remote mutation.
- Preserve unrelated work; never discard it to simplify a task.
- Never automatically commit, push, deploy, restart/reload, reset, clean, restore, switch branches, or mutate a remote system.
- Never deploy local uncommitted files directly.
- Never use `git pull` blindly on production, force-push, rewrite shared history, reset a dirty production checkout, or use `git clean` there.
- Never bypass SSH host-key verification, modify `~/.ssh/config`, accept changed host keys, weaken TLS/security controls, or expose credentials.
- Verify each authorized external write by reading back the exact target and exact SHA.

## Key References

- `references/plan.md` — task contract, deployment-mode discovery, and approval checkpoint.
- `references/apply.md` — minimal local execution and divergence handling.
- `references/qualify.md` — local/remote evidence statuses and qualification.
- `references/gitops.md` — publication, git-checkout deployment, SHA proof, and rollback discipline.
- `references/unify.md` — closure report separating implementation, publication, and deployment.
- `references/handoff.md` — `nyx-build` supplement to `nyx-seed`'s canonical handoff contract.

## Pitfalls

- Treating APPLY approval as approval to publish or deploy.
- Deploying a local working tree rather than a reviewed pushed SHA.
- Trusting “Already up to date” rather than comparing exact SHAs.
- Resetting, cleaning, stashing, or overwriting an unexpected dirty production checkout.
- Inventing build, service, health, or rollback commands when deployment evidence is incomplete.
- Treating a process as healthy without the defined endpoint or user-visible path check.
- Rewriting `nyx-seed` handoff intent instead of appending build/deployment state.

## Verification

- [ ] PLAN records Git state, protected unrelated work, deployment mode, and separate authorization gates.
- [ ] APPLY, PUBLISH, and DEPLOY occur only under their own explicit approvals.
- [ ] Local qualification includes repository-defined validation and inspected diff evidence.
- [ ] Publication records an explicit full SHA and proves it reached the approved remote branch.
- [ ] A git-checkout deployment proves `DEPLOYED_SHA == LOCAL_COMMIT` before service qualification.
- [ ] Remote checks, rollback readiness, and `NOT RUN` stages are visible in UNIFY.
- [ ] No unapproved Git, remote, deployment, restart/reload, destructive, trust-bypassing, or credential-exposing action occurred.
