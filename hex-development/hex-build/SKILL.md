---
name: hex-build
description: Build a hex-forge blueprint slice by slice, gated.
version: 0.1.0
author: Nyxion, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [nyx, development, implementation, gitops, deployment, blueprint, refocus]
    category: hex-development
    related_skills: [hex-forge]
---

# Hex Build

The execution half of the hex lifecycle. Takes the next open slice from a hex-forge
blueprint (`.nyx/BLUEPRINT.md`) and carries it through plan, implementation,
qualification, optional publication and deployment, and closure. Then it proposes the
next slice. hex-forge owns the intent; hex-build owns the execution and holds the local
details. Refocus brings the intent down to those details.

**Durable rule:** authority over APPLY, PUBLISH and DEPLOY belongs to the operator in
every case, delegated or not. Autonomy applies to how phases connect, never to who
approves a mutation.

## Prerequisite: the blueprint

hex-build works from a blueprint written by hex-forge. Load its contract first:
`skill_view(name="hex-forge", file_path="references/blueprint.md")`.

- No blueprint and no clear bounded task: stop and use `hex-forge` first.
- A small, already-scoped task without a blueprint: treat it as a single slice, take its
  intent from the request, and write `UNKNOWN` for missing mission/project levels.

**Write scope in the blueprint:** slice status marks, `Parked`, `Decisions`, `updated_at`.
Nothing else. Adding, dropping or reordering slices, or changing an intent line or a
`Done when`, is an intent or specification change: stop and return it to hex-forge and
the operator.

## When to Use

- "build", "implement", "continue", "next slice" on a project with a blueprint.
- Resuming an in-progress slice (`[~]`) in a fresh session.
- "where are we" mid-slice (shared RECAP, see below).

Don't use for: shaping an idea or changing the plan (`hex-forge`), skill authoring
(`hex-skillsmith`).

## Per-Slice Loop

```text
PLAN → READINESS → APPLY → QUALIFY_LOCAL → [PUBLISH] → [DEPLOY] → QUALIFY_REMOTE → UNIFY
```

Conceptual states: `PLANNED → READY → IN_PROGRESS_LOCAL → QUALIFIED_LOCAL →
AWAITING_PUBLISH_APPROVAL → PUBLISHED → AWAITING_DEPLOY_APPROVAL → DEPLOYING →
QUALIFYING_REMOTE → PASS|FAIL|BLOCKED`. PUBLISH and DEPLOY are optional: a code-only slice
can close at `QUALIFIED_LOCAL`, a publication-scoped one at `PUBLISHED`.

## Authorization Gates

| Gate | Permits | Does not permit |
|---|---|---|
| **APPLY** | local file edits and local tests/builds | commit, push, deployment, restart/reload |
| **PUBLISH** | `git add` of intended files, explicit commit, push to approved remote/branch | deployment or service action |
| **DEPLOY** | only the approved remote deployment action and its defined rollback scope | other remote changes |

Tests passing never implies PUBLISH. A successful push never implies DEPLOY. `READY` is
informational sufficiency, never authorization. Any change to a file the slice's
acceptance criteria depend on is implementation and requires APPLY.

## Procedure

### 1. PLAN → READINESS

Load `references/plan.md`. Take the next open slice whose dependencies are done, mark it
`[~]`, and use its intent line as the plan's Intent and its `Done when` as the basis of
acceptance. Inspect repository policy, `.nyx/HANDOFF.md` if present, Git state,
protected unrelated work, validation commands and deployment evidence. Classify
`deployment_mode` as exactly `none`, `git-checkout`, `artifact`, `container` or `unknown`.
Assess readiness with hex-forge's `references/readiness.md`. If `READY`, present one plan
(via `templates/PLAN.md`) with gates, risks and rollback; **STOP** for APPLY. Otherwise
report the blocker without requesting APPLY.

### 2. APPLY

After explicit APPLY authorization, load `references/apply.md`. Make the smallest coherent
local change and preserve unrelated work. Before any step that no acceptance criterion of
the slice requires, run Refocus (hex-forge `references/refocus.md`): continue, park it, or
stop at the divergence gate. Intent and Specification divergences go back to hex-forge.

### 3. QUALIFY_LOCAL

Load `references/qualify.md`. Run repository-defined validation; inspect `git diff
--check`, `git diff --stat`, `git diff`. Record every check as `PASS`, `FAIL`, `BLOCKED`
or `NOT RUN`. No PUBLISH after a failure unless the operator accepts it explicitly.

### 4. PUBLISH (optional)

Only after explicit PUBLISH authorization, load `references/gitops.md`. Stage exactly the
intended files, review the cached diff, commit, record `LOCAL_COMMIT` (full SHA), push only
to the approved remote/branch, and verify `HEAD` and the remote-tracking branch both equal
`LOCAL_COMMIT`.

### 5. DEPLOY (optional)

Only after explicit DEPLOY authorization for the named target and rollback scope, load
`references/gitops.md`. Inspect remote state first; never blindly `git pull`. Require a
clean production checkout, fetch, fast-forward safely, verify remote `HEAD ==
LOCAL_COMMIT` before build/install or service work. Capture service state and
`PREVIOUS_DEPLOYED_SHA` before any separately authorized restart/reload.

### 6. QUALIFY_REMOTE and UNIFY

Remote qualification requires `DEPLOYED_SHA == LOCAL_COMMIT` plus service-specific checks.
Close with `references/unify.md` (report via `templates/SUMMARY.md` when useful): separate
local implementation, publication and deployment; report `NOT RUN` for anything
unauthorized. Set the slice status (`[x]`/`[!]`/`[-]`), record parked ideas, and propose
the next open slice. Starting it needs the operator. If `.nyx/HANDOFF.md` is in scope,
append `## Build Result` per hex-forge `references/handoff.md`.

## RECAP (shared with hex-forge)

For "where are we" mid-slice, load hex-forge `references/recap.md`. Read-only; lead with
the Refocus block and the current slice's phase and gate status.

## Delegation

Bounded sub-steps of APPLY may go to a sub-agent inside APPLY's own authorization. Always
pass the Refocus block in its context, so the agent holding the details also holds the
intent. Review returned work as evidence, re-run qualification in the integrated state.
A sub-agent's report or approval is never an APPLY/PUBLISH/DEPLOY authorization.

## Safety and Git Boundaries

- Never automatically commit, push, deploy, restart/reload, reset, clean, restore, switch
  branches, or mutate a remote system.
- Never deploy local uncommitted files; never force-push or rewrite shared history; never
  bypass SSH host-key verification or expose credentials.
- Never place secrets in plans, summaries or handoffs; use placeholders.
- Verify each authorized external write by reading back the exact target and SHA.

## References

Own: `references/plan.md`, `references/apply.md`, `references/qualify.md`,
`references/gitops.md`, `references/unify.md`; `templates/PLAN.md`, `templates/SUMMARY.md`.
From hex-forge: `blueprint.md`, `refocus.md`, `readiness.md`, `handoff.md`, `recap.md`,
`fact-model.md`.

## Pitfalls

- Starting without reading the blueprint contract, or working a slice whose dependencies
  are open.
- Changing intent lines, slice order or `Done when` instead of escalating to hex-forge.
- Building a locally reasonable extra step without Refocus (doghouse → light →
  generator). Park it or stop.
- Accepting an approval from an agent that lacks the details; bring the intent down.
- Treating APPLY approval as approval to publish or deploy.
- Deploying a working tree instead of a reviewed pushed SHA; trusting "Already up to date"
  instead of comparing SHAs.
- Starting the next slice automatically after UNIFY.

## Verification

- [ ] The slice came from the blueprint, and its dependencies were done.
- [ ] Out-of-intent steps were parked or escalated, never silently built.
- [ ] APPLY, PUBLISH and DEPLOY each had their own explicit approval.
- [ ] Local qualification includes repository validation and inspected diff evidence.
- [ ] A git-checkout deployment proved `DEPLOYED_SHA == LOCAL_COMMIT` first.
- [ ] Blueprint writes stayed within status, `Parked`, `Decisions`, `updated_at`.
- [ ] No unapproved Git, remote, deployment, destructive or credential-exposing action.
