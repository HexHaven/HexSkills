# Project Specification

> Keep only relevant sections. Label material facts with `USER-STATED`, `OBSERVED`, `ASSUMED`, `PROPOSED`, `UNKNOWN`, or `CONTRADICTORY`.

## Vision

[One sentence describing the desired future state.]

## Problem

[Specific problem, affected users/operators, and why it matters.]

## Users

- [Primary user or operator and need]

## Goals

- [Observable outcome]

## Non-Goals

- [Explicitly excluded scope]

## Functional Requirements

1. [System behavior]

## Non-Functional Requirements

- [Only material security, privacy, reliability, performance, accessibility, portability, or operability requirement]

## Constraints

- [Technical, organizational, legal, time, budget, or compatibility constraint]

## User and System Flows

1. [Trigger → principal steps → observable result]
2. [Failure or recovery path, when relevant]

## Acceptance Criteria

- [ ] Given [state], when [action], then [observable behavior].

## Security and Privacy

- Trust boundaries: [value or `UNKNOWN`]
- Data categories and lifecycle: [value or `NOT APPLICABLE`]
- Credential custody: [use placeholders; never include secrets]
- Public exposure: [value or `UNKNOWN`]

## Architecture Constraints

- Current: [observed constraints]
- Proposed: [design decisions with rationale]
- Dependencies: [required systems and ownership]

## Risks

| Risk | Impact | Mitigation or evidence needed | Owner |
|---|---|---|---|
| [risk] | [impact] | [mitigation] | [owner] |

## Open Questions

| Question | Fact label | Impact | Blocks first task? |
|---|---|---|---|
| [question] | `UNKNOWN` | [impact] | Yes/No |

## First Bounded Milestone

- **Intent:** [outcome]
- **Scope:** [included work]
- **Dependencies:** [required inputs]
- **Expected files:** [paths if known]
- **Non-goals:** [excluded work]
- **Acceptance criteria:** [observable checks]
- **Validation:** [commands or behavior]
- **Rollback/recovery:** [when relevant]

## Definition of Done

- [ ] Relevant acceptance criteria pass with observed evidence.
- [ ] Security, privacy, and operational requirements for this scope are satisfied.
- [ ] Documentation and project state match implemented reality.

## Readiness

**State:** IDEA | DISCOVERY | SPECIFIED | PLANNED | READY

| Condition | Result | Evidence or blocker |
|---|---|---|
| Goal | [PASS/FAIL] | [evidence] |
| Scope | [PASS/FAIL] | [evidence] |
| Acceptance | [PASS/FAIL] | [evidence] |
| Architecture | [PASS/FAIL] | [evidence] |
| High-impact blockers | [PASS/FAIL] | [evidence] |

> `READY` is informational sufficiency, not authorization to implement, commit, deploy, or mutate remote systems.
