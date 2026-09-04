# Dispatch Adapter

Concrete shapes for the CARDIFY and DISPATCH steps, and the boundary between board dispatch and
in-session delegation.

## CARDIFY — creating the parent card

```python
kanban_create(
    title="<short project/milestone title>",
    assignee="<profile that owns this project's coordination, e.g. the seed author or an orchestrator>",
    board="<explicit-board-slug>",
    body=open("templates/CARD_BODY.md filled in").read(),
)
```

Do not omit `board=`. If the card already exists (re-entering CARDIFY after an update), prefer
`kanban_comment` to append the refreshed summary rather than trying to rewrite the original body,
so history remains auditable.

## DISPATCH — creating the build child task

```python
kanban_create(
    title=f"Build: {topic}",
    assignee="<executor profile, e.g. sirius or another bounded-execution profile>",
    board="<same-explicit-board-slug>",
    parents=[cardify_task_id],
    body=(
        "Run hex-build against .nyx/HANDOFF.md at <path> "
        "(or against this card's spec if no repository exists). "
        "hex-build's own PLAN -> APPLY_LOCAL -> QUALIFY_LOCAL -> [PUBLISH] -> [DEPLOY] "
        "-> QUALIFY_REMOTE -> UNIFY lifecycle and its APPLY/PUBLISH/DEPLOY authorization "
        "gates apply unchanged. This card's existence is coordination only and is not "
        "itself an authorization for any gate."
    ),
)
```

`parents=[cardify_task_id]` is what makes the dispatcher hold the build task until the parent
card's prerequisite state is satisfied and gives TRACK/RECONCILE a stable link back.

## delegate_task vs. kanban_create — do not conflate them

`delegate_task` spawns an isolated in-session subagent for a bounded reasoning task; its output
returns directly into the caller's own turn and it cannot touch the kanban board at all (hard
platform restriction — every kanban DB operation, including reads, is refused from a
`delegate_task` child context). `kanban_create` spawns an independently dispatchable, resumable
board task that a *different* profile or a *later* session can pick up, and that can itself use
kanban tools (post progress comments, block, request review, complete).

Use `kanban_create` for the build dispatch specifically because `hex-build`'s own lifecycle needs
to report status back onto the board (TRACK depends on this). Using `delegate_task` here would
produce a subagent that finishes invisibly to the board, defeating the purpose of coordinating
through Kanban in the first place.

## Escalating to the Review-Gate pattern

Plain `parents=[...]` linkage (as above) is sufficient for a single seed→build handoff. Escalate
to the full Review-Gate pattern (documented in the `hermes-project-kanban-ops` skill's
review-gate-pattern reference file) only when the project has more than two coordinated stages
*and* a distinct validator role that
must sign off with discretion (not just dependency completion) between them — e.g. a multi-
milestone project where a coordinator profile reviews each milestone's build output before the
next milestone starts. Do not add gate cards to a simple two-stage project; that only introduces a
validator bottleneck with no corresponding benefit.
