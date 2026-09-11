---
name: delegated-execution-discipline
description: Use when handing part of a task to a sub-agent or harness.
version: 0.1.0
author: Nyxion, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [delegation, sub-agents, verification, provenance, scope]
    category: hex-development
    related_skills: [hex-build]
---

# Delegated Execution Discipline

Hand a bounded portion of your own authorized work to a sub-agent or coding harness without losing scope, authority, or accountability for the result.

**Durable rule:** delegation changes *who performs* the work, never *what work is authorized*.

## When to Use

- Splitting an authorized task across sub-agents, `delegate_task`, or an external coding harness (Claude Code, Codex, OpenCode).
- Integrating and judging returned work that you did not write yourself.
- Deciding whether a piece of work may be delegated at all.

Don't use for: choosing which harness to invoke (see the harness's own skill), routing work between peer agents on a board, or granting authority you do not already hold.

## Before Delegating

1. **Confirm you hold the authority yourself.** Capability to invoke a sub-agent is not authorization to use it for this action. If you may not publish, your delegate may not publish.
2. **Cut a subscope, not a copy.** The assigned subscope must sit *inside* your scope. Narrowing is allowed; widening is not, and neither is delegating the ambiguous remainder so someone else resolves it.
3. **Check it is delegable.** Work needing a decision that is not yours, an unresolved acceptance criterion, or credentials you should not spread is not ready to hand off.

## The Handoff

Send only what the delegate needs to work correctly:

- Goal, parent scope, assigned subscope
- Constraints and acceptance criteria
- Relevant context and files
- Forbidden actions (publish, deploy, external mutation, out-of-scope paths)
- Expected return format

Keep secrets out of delegated context unless the work genuinely requires them and that disclosure is authorized. Do not micromanage implementation details that belong to the delegate's own bounded judgment — you asked for a result, not a transcript.

## Reviewing What Comes Back

Sub-agent output is **evidence to review, not truth to inherit**. A harness exiting cleanly, a summary saying "done", or a claimed file write proves only that the process finished.

- Read the actual diff or artifact, not the report about it.
- Verify claimed external side effects by reading back the exact target (path, SHA, URL, record).
- Re-run the relevant validation yourself in the integrated state; the delegate's green run happened in its context, not yours.
- Check the delegate stayed inside the assigned subscope — unrequested adjacent edits are a scope finding, not a bonus.
- Reconcile contradictions between two delegates rather than merging both hopefully.

You remain accountable for the integrated outcome: selection, context, scope preservation, review, integration, and sufficient verification.

## Provenance

Keep enough trace to distinguish work you performed, work a delegate produced, work only proposed, work integrated, work verified, and work not verified. Routine tasks need a sentence, not a log. Never write secret material into a provenance record.

## Nested Delegation

Do not assume it is available. Where the runtime and current authority support it, every level stays inside inherited scope and authority, remains attributable, and remains verifiable.

> Delegation depth must not create authority depth.

## Pitfalls

- Treating a completed harness run as verification.
- Delegating the undecided part of a task instead of deciding it or escalating.
- Passing full credentials or an entire environment because it was easier than scoping context.
- Accepting a large refactor that "also fixed some things" outside the subscope.
- Reporting a delegate's claim as your own observation.
- Fanning out work whose sub-results silently depend on each other, then merging conflicting answers.

## Verification

- [ ] Delegated authority did not exceed your own; subscope stayed inside parent scope.
- [ ] Returned work was inspected as artifacts/diffs, not accepted as a summary.
- [ ] Validation was re-run in the integrated state, and its result recorded as PASS / FAIL / BLOCKED / NOT RUN.
- [ ] External side effects were confirmed by reading back the exact target.
- [ ] Performed, proposed, integrated, verified, and unverified work are distinguishable in the report.
