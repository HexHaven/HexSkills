# ROOT and BLUEPRINT

Turns a specified idea into a project root and a blueprint that is worked off one slice
at a time. This file is the contract between `hex-forge` (writes the plan) and
`hex-build` (works it off). Both skills load it.

## Ownership

| Part of `.nyx/BLUEPRINT.md` | Written by |
|---|---|
| Project intent, missions, slices, intent lines, `Done when`, `Depends`, order | hex-forge, after operator decision |
| Slice status marks, `Parked`, `Decisions`, `updated_at` | hex-build (and hex-forge) |

hex-build never edits hex-forge's parts. When a slice shows the plan is wrong, hex-build
stops and escalates; hex-forge proposes the change and the operator decides.

## ROOT: adapt or create

1. **Look for an existing root first.** Search for a repository or workspace that already
   owns this work. If one exists, **adapt** it: follow its `AGENTS.md` and conventions,
   do not restructure it, and add only the hex-forge records the repository accepts.
2. **Otherwise propose one new root.** Read the host's home and workspace policy (e.g. a
   home-level `AGENTS.md`) and propose exactly one path with its reason: durable
   repository, experiment, or task workspace. Never create a new visible top-level
   directory in the home directory.
3. **Authorization.** Creating the directory, `git init`, and writing the scaffold need
   explicit operator approval of the exact path. This is repository-write authorization
   for specification records, not APPLY. Discussing the idea is not approval. Remotes,
   branches and signing stay untouched unless separately authorized.
4. **Scaffold, nothing more.** Write only specification records:
   - `docs/PROJECT.md` (from `templates/PROJECT.md`), or the repository's own spec location;
   - `.nyx/BLUEPRINT.md` (from `templates/BLUEPRINT.md`);
   - `.nyx/HANDOFF.md` only when authorized per `references/handoff.md`.

   No source code, build files, dependencies or CI. That is slice work under APPLY.

Without write authorization, present the blueprint in chat and continue from there.

## BLUEPRINT: the build plan

`.nyx/BLUEPRINT.md` is the intent hierarchy the work is traced against:

```text
Project intent  (one line, from docs/PROJECT.md Vision)
└── Mission     (an outcome that serves the project; one intent line)
    └── Slice   (one PLAN→APPLY→QUALIFY→UNIFY loop; intent + done-when)
        └── Task (steps inside the slice's PLAN; not recorded here)
```

Rules:

- **Intent lines say why, not how.** One sentence each. They are what Refocus returns
  to the working agent (`references/refocus.md`).
- **One slice = one reviewable change** with an observable `Done when`. If a slice
  needs several plans, split it.
- **Detail only the near missions.** Later missions may stay intent-only and are sliced
  when they come up. Do not plan speculative work in detail.
- **IDs are stable:** `M1`, `M1.S1`, and so on. Never renumber; mark dropped slices instead.
- **Parked** collects useful ideas that do not serve the current intent. Parking is
  how scope inflation is stopped without losing the idea.

Wherever other references say "first task" or "bounded task", they mean the active slice.

## Working it off (hex-build)

1. PLAN takes the next open slice whose dependencies are done, and marks it `[~]`.
2. The slice runs PLAN → READINESS → APPLY → QUALIFY → optional PUBLISH/DEPLOY → UNIFY
   under the unchanged gates.
3. UNIFY sets the slice status (`[x]` PASS, `[!]` BLOCKED/FAIL, `[-]` CANCELLED) and
   proposes the next slice. It does not start it without the operator.

Routine updates need no new approval once the file is in scope: status marks, `Parked`
entries, `Decisions`, `updated_at`. Adding, dropping or reordering slices, or changing any
intent line, is an intent or specification change: hex-build escalates, hex-forge proposes
it, and the operator decides.
