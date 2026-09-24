---
name: hex-forge
description: Own idea-to-deploy work, gated at apply, publish, deploy.
version: 0.1.0
author: Nyxion, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [nyx, development, discovery, implementation, gitops, deployment, recap, lifecycle]
    category: hex-development
    related_skills: [hex-skillsmith, hex-soulforge]
---

# Hex Forge

Single entry point for the idea → deployed-and-verified project lifecycle: discovery,
specification, readiness, implementation, qualification, optional publication, optional
deployment, and closure — plus a read-only recap/status mode over that same state.
Replaces the former `hex-seed` / `hex-build` / `hex-recap` split: one skill carries the
operator's project through every phase instead of requiring a manual handoff between
three separate skills.

**Durable rule:** authority over APPLY, PUBLISH, and DEPLOY belongs to the operator in
every case, delegated or not, mode or phase. Autonomy applies to how phases connect,
never to who approves a mutation.

## When to Use

- A project idea needs shaping into an implementation-ready specification, through to a
  built, tested, and (optionally) published/deployed result — in one continuous engagement.
- Continuing an already-`.nyx/HANDOFF.md`-tracked project from a fresh Hermes session.
- "recap", "where are we", "summarize current state", "handoff", "continue in new
  session" against an active or past hex-forge project.

Don't use for: creating or auditing Hermes skills (`hex-skillsmith`), forging agent
identity (`hex-soulforge`), persona-specific HexHaven Git operations, or routing
across peer specialist agents. A bounded slice of an already-scoped task can be
delegated without invoking the full hex-forge project lifecycle.

## Modes

Infer from phrasing; default to BUILD when a project or task is being newly described
or continued toward implementation.

| Mode | Trigger phrasing | Behavior |
|---|---|---|
| **BUILD** | project ideas, "implement", "continue", explicit phase request | Advances the lifecycle below, phase by phase, stopping at every gate. |
| **RECAP** | "recap", "where are we", "summarize current state", "compact context" | Read-only report of current hex-forge state. Never advances a phase. See `references/recap.md`. |

If phrasing is ambiguous between the two, produce RECAP (the lighter, non-mutating
artifact) and ask whether to continue into BUILD.

## Lifecycle

```text
IDEA → DISCOVER → SHAPE → SPECIFY → READINESS
     → PLAN → APPLY → QUALIFY_LOCAL
     → [PUBLISH] → [DEPLOY] → QUALIFY_REMOTE → UNIFY
```

Conceptual states: `IDEA → DISCOVERY → SPECIFIED → PLANNED → READY → IN_PROGRESS_LOCAL →
QUALIFIED_LOCAL → AWAITING_PUBLISH_APPROVAL → PUBLISHED → AWAITING_DEPLOY_APPROVAL →
DEPLOYING → QUALIFYING_REMOTE → PASS|FAIL|BLOCKED`.

The first five phases (IDEA…READINESS) replace what `hex-seed` owned; PLAN…UNIFY replace
what `hex-build` owned. A single `.nyx/HANDOFF.md` carries state between phases and
across sessions — see `references/handoff.md`. There is no operator-facing handoff
between two different skills anymore: crossing from READINESS into PLAN is an internal
transition, not a new skill invocation.

PUBLISH and DEPLOY remain optional: a code-only task can close at `QUALIFIED_LOCAL`; a
publication-scoped task can close at `PUBLISHED`.

## Authorization Gates

| Gate | Permits | Does not permit |
|---|---|---|
| **APPLY** | local file edits and local tests/builds | commit, push, deployment, restart/reload |
| **PUBLISH** | `git add` of intended files, explicit commit, push to approved remote/branch | deployment or service action |
| **DEPLOY** | only the approved remote deployment action and its defined rollback scope | other remote changes |

These three gates are unchanged from the former `hex-build` and are not softened by this
skill's greater phase-to-phase autonomy. Tests passing never implies PUBLISH. A
successful push never implies DEPLOY. `READY` (end of SPECIFY/READINESS) is informational
sufficiency, never authorization to implement, commit, deploy, or mutate a remote system.

## Scope of the APPLY Boundary

APPLY governs project implementation: the artifact the task will actually deliver —
source code, configuration the running system consumes, tests, build output. It does
not govern two workflow/specification records, because neither is implementation:

- `docs/PROJECT.md` (Phase 1, SPECIFY) — the project specification itself. Writing it
  needs its own explicit authorization at SPECIFY (`references/discovery.md`: "a
  discussion of the idea is not write permission"). This is ordinary write hygiene for
  a document the operator reviews before it lands on disk — it is not an APPLY grant
  and not an additional mutation gate; APPLY has not even been reached yet at SPECIFY.
- `.nyx/HANDOFF.md` (written/updated at READINESS, PLAN, APPLY-entry, UNIFY) — a
  lifecycle record that only restates decisions already made in-session (readiness
  state, plan contract, gate status, closure). It carries no new project content, so it
  needs no separate authorization beyond its own conflict-check in
  `references/handoff.md` (stop and ask before overwriting an ACTIVE/PLANNED/
  IN_PROGRESS handoff).

Any change to a file the project's acceptance criteria actually depend on is
implementation and requires APPLY, full stop — no exceptions traced back to this section.

## Procedure

### Phase 1 — IDEA → READINESS (discovery and specification)

Load `references/discovery.md` (question gate, project typing) and
`references/fact-model.md` (six evidence labels: `USER-STATED`, `OBSERVED`, `ASSUMED`,
`PROPOSED`, `UNKNOWN`, `CONTRADICTORY` — no others). Restate intent, inspect read-only
before asking, shape goals/non-goals/flows, and produce `docs/PROJECT.md` (via
`templates/PROJECT.md`) when repository write is authorized. Assign exactly one
readiness state per `references/readiness.md`. Do not implement, commit, push, or deploy
in this phase.

Done when readiness is `READY` (or the operator explicitly wants an earlier state handed
off) — then proceed directly into PLAN using the same in-memory/handoff state. No
separate skill invocation, no re-statement of the idea by the operator.

### Phase 2 — PLAN

Load `references/plan.md`. Inspect repository policy, `.nyx/HANDOFF.md` if present
(validate against fresh evidence per `references/handoff.md`), current Git state,
protected unrelated work, maintained validation commands, and deployment evidence.
Classify `deployment_mode` as exactly `none`, `git-checkout`, `artifact`, `container`, or
`unknown`. Present the plan, authorization gates, risks, and recovery/rollback proposal.
**STOP** for APPLY authorization.

### Phase 3 — APPLY

After explicit APPLY authorization, load `references/apply.md`. Make the smallest
coherent local change; preserve unrelated work; follow the divergence gate for
intent/specification/implementation/environment splits. Bounded sub-steps may be
delegated under the bounds below. Done when the
approved change is implemented, or honestly `BLOCKED`/`CANCELLED`.

### Phase 4 — QUALIFY_LOCAL

Load `references/qualify.md`. Run repository-defined validation; inspect `git diff
--check`, `git diff --stat`, `git diff`. Record every check as `PASS`, `FAIL`,
`BLOCKED`, or `NOT RUN`. Do not proceed to PUBLISH after a validation failure unless the
operator explicitly accepts it.

### Phase 5 — PUBLISH (optional)

Only after explicit PUBLISH authorization, load `references/gitops.md`. Stage exactly
the intended files, review the cached diff, commit, record `LOCAL_COMMIT` (full SHA),
push only to the approved remote/branch, and verify `HEAD` and the remote-tracking
branch both equal `LOCAL_COMMIT`.

### Phase 6 — DEPLOY (optional)

Only after explicit DEPLOY authorization for the named target and rollback scope, load
`references/gitops.md`. Inspect remote state first; never blindly `git pull`. Require a
clean production checkout, fetch, fast-forward safely, verify remote `HEAD ==
LOCAL_COMMIT` before build/install or service work. Capture service state and
`PREVIOUS_DEPLOYED_SHA` before any separately authorized restart/reload.

### Phase 7 — QUALIFY_REMOTE and UNIFY

Remote qualification requires `DEPLOYED_SHA == LOCAL_COMMIT` plus repository/
service-specific checks (`references/qualify.md`). Close with `references/unify.md`:
distinguish local implementation, publication, and deployment explicitly; report `NOT
RUN` for anything unauthorized. Append `## Build Result` to `.nyx/HANDOFF.md` per
`references/handoff.md`; never rewrite the original Goal/Scope/Non-Goals/Acceptance
Criteria.

## RECAP Mode

A read-only report of current state — never advances a phase, never mutates anything.
Load `references/recap.md`. Produces either a compact **RECAP** (operator-facing, under
500 words) or a paste-ready **HANDOFF** (for a fresh session, 500–1200 words, via
`templates/SESSION-HANDOFF.md`) depending on phrasing.

## Delegation

Bounded sub-steps of DISCOVER or APPLY may go to a sub-agent: confirm the subscope
sits inside the phase's own authorization. Review returned work as evidence rather
than truth, and re-run qualification in the integrated state. A sub-agent's
report is never itself an APPLY/PUBLISH/DEPLOY authorization — those three
gates stay between hex-forge and the operator directly, regardless of how much
of the surrounding work was delegated.

## `.nyx/HANDOFF.md` Contract

Canonical schema, frontmatter, archiving convention, and Build Result appendix:
`references/handoff.md`. One skill now owns writing it (READINESS step), validating it
(PLAN), and closing it (UNIFY) — no more split between a "hex-seed side" and a
"hex-build side" of the same document.

## Safety and Git Boundaries

- Read-only discovery precedes local, Git, and remote mutation.
- Preserve unrelated work; never discard it to simplify a task.
- Never automatically commit, push, deploy, restart/reload, reset, clean, restore,
  switch branches, or mutate a remote system.
- Never deploy local uncommitted files directly; never use `git pull` blindly on
  production; never force-push or rewrite shared history; never bypass SSH host-key
  verification or expose credentials.
- Never place tokens, passwords, private keys, cookies, or credentials in a
  specification or handoff; use `<TOKEN>`, `<PASSWORD>`, `<HOST>`, `<IP_ADDRESS>`.
- Verify each authorized external write by reading back the exact target and exact SHA.

## Key References

- `references/discovery.md` — adaptive discovery and project typing.
- `references/fact-model.md` — evidence labels and contradiction handling.
- `references/readiness.md` — state definitions and readiness gate.
- `references/plan.md` — task contract, deployment-mode discovery, approval checkpoint.
- `references/apply.md` — minimal local execution and divergence handling.
- `references/qualify.md` — local/remote evidence statuses and qualification.
- `references/gitops.md` — publication, git-checkout deployment, SHA proof, rollback discipline.
- `references/unify.md` — closure report separating implementation, publication, deployment.
- `references/handoff.md` — canonical `.nyx/HANDOFF.md` contract, lifecycle, archiving, validation.
- `references/recap.md` — RECAP/HANDOFF mode selection and rendering.
- `templates/PROJECT.md`, `templates/PLAN.md`, `templates/SUMMARY.md`,
  `templates/PROJECT-HANDOFF.md`, `templates/SESSION-HANDOFF.md`.

## Pitfalls

- Treating a lighter phase-to-phase flow as license to soften APPLY/PUBLISH/DEPLOY —
  the three gates are exactly as strict as before.
- Treating docs/PROJECT.md or .nyx/HANDOFF.md writes as requiring APPLY, or treating
  APPLY as a prerequisite for them — they are governed separately; see
  "Scope of the APPLY Boundary."
- Turning discovery into a long questionnaire instead of inspecting first.
- Declaring `READY` while a security, data, billing, credential, or deployment blocker remains.
- Treating APPLY approval as approval to publish or deploy.
- Deploying a local working tree rather than a reviewed pushed SHA.
- Trusting "Already up to date" rather than comparing exact SHAs.
- Overwriting an existing `ACTIVE`/`PLANNED`/`IN_PROGRESS` `.nyx/HANDOFF.md` without
  archiving it or asking first.
- Producing a RECAP/HANDOFF that advances or mutates state instead of only reporting it.
- Accepting a sub-agent's completion claim as APPLY/PUBLISH/DEPLOY authorization.

## Verification

- [ ] Every material claim carries a fact label or direct source.
- [ ] Exactly one readiness state, and later exactly one closure state, is reported with evidence.
- [ ] APPLY, PUBLISH, and DEPLOY occurred only under their own explicit, separate approvals.
- [ ] Local qualification includes repository-defined validation and inspected diff evidence.
- [ ] A git-checkout deployment proves `DEPLOYED_SHA == LOCAL_COMMIT` before service qualification.
- [ ] `.nyx/HANDOFF.md` (when in scope) was written/validated/closed by this skill alone,
      with no invented content.
- [ ] Delegated sub-steps were reviewed as evidence, not accepted as an authorization.
- [ ] No unapproved Git, remote, deployment, restart/reload, destructive,
      trust-bypassing, or credential-exposing action occurred.
