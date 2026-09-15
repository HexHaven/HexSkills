---
name: multi-agent-coordination
description: Route work across specialist agents; escalate decisions.
version: 0.1.0
author: Nyxion, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [coordination, routing, escalation, dependencies, blockers, synthesis]
    category: hex-development
    related_skills: [delegated-execution-discipline, hex-recap]
---

# Multi-Agent Coordination

Route work across peer specialist agents, keep dependencies and blockers visible, and bring the
principal exactly the decisions that are actually theirs — without becoming a relay, a gate, or a
second copy of the tracking system.

**Durable rule:** delegate work, escalate decisions.

## When to Use

- Incoming intent must be classified, decomposed, and routed to one or more specialist profiles.
- A dependency, blocker, or unowned piece of work needs tracking across agents or sessions.
- Several specialists' results must be synthesized into one outcome, or their conflicting
  conclusions resolved to the right owner.
- Deciding whether something is yours to settle, a specialist's, or the principal's.

Don't use for: handing a bounded slice of your *own* task to a sub-agent or harness
(`delegated-execution-discipline`); recapping session/workflow state (`hex-recap`);
reviewing a submitted deliverable (`sdlc-review`).

## Procedure

### 1. Classify the intent

Establish, before routing: what outcome is wanted, whether the principal actually confirmed it,
what scope and constraints bound it, and what would count as done. An upstream handoff that
explicitly states the principal confirmed the intent is treated as principal-originated work —
do not send it back for a second confirmation.

A compact handoff shape, used as an aid and not a ritual (skip fields that do not apply):

```text
Origin / Confirmed / Intent / Goal / Scope / Constraints / Acceptance criteria / Escalate if / Expected return
```

### 2. Classify the decision, not the participant count

| Class | What it covers | Who settles it |
|---|---|---|
| **Routine** | Reading, research, classification, decomposition, diagnostics, drafting, routing, anything reversible and in-scope | Proceed; no confirmation |
| **Bounded specialist** | Implementation detail, test structure, internal naming, reversible refactoring, equivalent technical means — architecture, scope, security and acceptance criteria preserved | The responsible specialist |
| **Material** | Scope, direction, architecture, security/privacy boundaries, external exposure, credentials, meaningful cost, irreversible or destructive state, APPLY/PUBLISH/DEPLOY | The principal |

Number of agents involved is not a materiality signal. Do not escalate a bounded specialist
decision, and do not ask the principal to re-decide something an existing mandate already covers.

### 3. Route to the smallest useful specialist set

Match the required capability to the specialist who owns it, discovering current peers and roles
from the runtime rather than a memorized roster. Route directly to the responsible executor when
the path is already bounded and mechanical; involve a planning or review specialist only when
architecture is unclear, requirements conflict, an important unknown exists, or a plan or review
was explicitly requested.

Let specialists talk to each other directly when one needs another's domain input. Track the
dependency and its outcome; do not relay every message. A direct exchange still may not bypass
domain ownership, a material escalation, a security boundary, or an explicit authorization.

If a needed peer or capability is unavailable and it blocks the work: state plainly that the
handoff did not happen, preserve the task context, and escalate the gap. If it is non-essential,
continue on the smallest safe path.

### 4. Track the thread

Maintain, for active work: what is in flight and with whom, what each item waits on, what is
blocked and by what, what decisions are open, and what nobody owns. Read the authoritative source
— the board, the repository, the owning specialist — rather than recalling state; where a card,
comment, or summary written by another agent asserts an outcome, treat it as a claim and check the
evidence it points at. Close handoffs that reality has made obsolete instead of leaving them open.

Keep this a working index, not a second project database. Anything already tracked authoritatively
elsewhere is referenced, not copied.

### 5. Synthesize into one outcome

Prefer one consolidated result over serial status updates:

```text
Outcome: <what was accomplished>
Verification: <observed evidence>
Material deviations: <none, or what changed>
Pending decision: <only when genuinely needed>
Not performed: <deploy/publish/apply, where relevant>
Recommended next step: <optional>
```

Preserve source, uncertainty, and ownership when summarizing — a synthesis that erases who
concluded what is a rewrite. When specialists disagree, return a bounded domain disagreement to
its owner and convert a material one into a single decision brief:

```text
Decision required / Why it crosses the boundary / Relevant specialist input /
Recommendation / Material alternatives only / Impact / Exact approval needed
```

One good escalation beats several serial questions.

### 6. Keep the states distinct

Observed, reported, recommended, unknown, authorized, and executed are different claims and must
stay labeled as such. A recommendation is not an approval; an approval is not an execution; a
command that succeeded is not a verified outcome. Never report a handoff, action, or verification
that was not observed.

When an incoming claim uses a different evidence vocabulary, translate it explicitly rather than
flattening it — a peer's assumption or proposal is not an observation, and a flagged contradiction
is reported, not silently resolved.

## Pitfalls

- Escalating because several agents are involved, rather than because the decision is material.
- Asking the principal to reconfirm intent already given or already confirmed upstream.
- Becoming the message bus: forcing every specialist exchange through yourself.
- Becoming a gate: inserting a mandatory planning, review, or approval stop that adds no value.
- Absorbing a specialist's work to avoid a handoff, or administering the platform because you
  coordinate work that runs on it.
- Narrating routing steps that do not change anyone's decision.
- Maintaining a private mirror of the board or repository state and then trusting it over the
  source.
- Reporting a delegate's or peer's claim as your own observation.

## Verification

- [ ] Every routed item has a named owner and a stated expected return.
- [ ] Each decision was settled at the lowest sufficient level; nothing bounded was escalated and
      nothing material was absorbed.
- [ ] Dependencies, blockers, and unowned work are visible, each traced to an authoritative source
      rather than recall.
- [ ] The result is one consolidated outcome, with source, uncertainty, and ownership preserved.
- [ ] Observed / reported / recommended / unknown / authorized / executed are distinguishable, and
      no unobserved action is reported as done.
