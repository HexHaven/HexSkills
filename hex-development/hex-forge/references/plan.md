# PLAN Stage

## Entry conditions

- Task intent is sufficiently specified to inspect without inventing high-impact facts.
- Source of truth, repository/workspace target, and operator scope are known.
- PLAN is read-only except for an explicitly authorized plan artifact.

## Repository and deployment discovery

1. Locate/read applicable `AGENTS.md`, project/task docs, repository-native state, CI, manifests, service definitions, and deployment/runbook docs.
2. In Git, run and record actual output — using whatever terminal/shell tool the
   current runtime exposes, never assume the result:

   ```bash
   git status --short && git branch --show-current && git log -1 --oneline && git remote -v
   ```

3. Identify unrelated modified/untracked files as protected unless explicitly in scope.
4. Inspect maintained validation and deployment commands; do not infer them from technology names.
5. Classify `deployment_mode` as exactly:

   | Mode | Evidence threshold |
   |---|---|
   | `none` | Evidence says no deployment is part of task/service. |
   | `git-checkout` | A remote production checkout and Git revision update are documented or USER-STATED. |
   | `artifact` | Artifact release/handoff is documented or USER-STATED. |
   | `container` | Image/manifest deployment is documented or USER-STATED. |
   | `unknown` | Evidence is absent, incomplete, or contradictory. |

For `git-checkout`, record approved remote, branch, production host/path, service unit, build/install command, restart/reload command, health verification, and rollback method. Each is `OBSERVED`, `USER-STATED`, or `UNKNOWN`; never substitute plausible values. Record these under the `## Deployment` addition defined in `references/handoff.md` when `.nyx/HANDOFF.md` is in scope.

## Handoff validation

If `.nyx/HANDOFF.md` exists, load `references/handoff.md` and compare its task contract to fresh evidence. A high-impact contradiction (security, architecture, credentials, public exposure, data handling, acceptance criteria, or deployment target) means **STOP** before PLAN. Absence is normal; do not create `.nyx/` automatically.

## Task contract and checkpoint

Define only intent, scope, dependencies, expected/protected files, non-goals, observable acceptance criteria, exact known validation, deployment facts/unknowns, risks/recovery, and separate APPLY/PUBLISH/DEPLOY authorization gates. A deployment plan requests deployment and defined rollback authorization together, but neither is implied by APPLY/PUBLISH.

Present Git state, protected work, deployment classification, target facts/unknowns, validation, risks, and rollback proposal. **STOP.** APPLY begins only after explicit local-scope authorization; PUBLISH and DEPLOY stay unapproved unless expressly granted.
