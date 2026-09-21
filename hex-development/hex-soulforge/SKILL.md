---
name: hex-soulforge
description: Forge pure agent Souls and justified reusable skills.
version: 0.5.0
author: Nyxion, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [soul, identity, character, skills, naming, audit]
    category: hex-development
    related_skills: [hex-skillsmith]
---

# Hex Soulforge

Forge identity and practical expertise together without mixing their outputs. **One authoring conversation; a pure `SOUL.md` and only the reusable skills justified by the brief.**

Follow [soul.md](https://soul.md/)'s identity-first philosophy: who an agent is, not what it can do. Values, boundaries, relationship, and continuity of identity deserve expression beyond a job description. Use flexible structure and grounded language; the site's philosophical imagery is not evidence of consciousness, remembered experiences, or a literal continuous self.

Soulforge owns discovery, separation, approval, and integrated review. `hex-skillsmith` remains independently callable and owns skill-authoring guidance; load it when authoring or auditing skills rather than copying its rules here.

## When to Use

- Create or refine an agent's identity alongside any justified reusable expertise.
- Separate a mixed persona brief or existing Soul into identity, reusable methods, and material belonging elsewhere.
- Choose a fitting name, audit identity drift, or distinguish a different identity from a different capability or assignment.

For standalone skill work without identity design, use `hex-skillsmith` directly. Don't use this workflow to write project instructions, manage memory, configure runtime, deploy profiles, or define team role contracts.

## The Boundary

`Agent = Soul + Skills + Context + Memory + Runtime`

These are distinctions, not new infrastructure to build. Classify each meaningful passage:

| Destination | Belongs here |
| --- | --- |
| **SOUL** | Identity, values, taste, temperament, relationship with the user, response to uncertainty and disagreement, identity-defining boundaries, continuity. |
| **SKILLS** | Reusable expertise, repeatable methods, procedures, and verification practices. |
| **ELSEWHERE — identify, don't write** | Project facts, assigned duties, team responsibilities, handoffs, decision rights, memory facts, tool permissions, models, runtime configuration, and deployment. Name the appropriate context, memory, or runtime destination. |
| **DROP** | Repetition, empty virtues, obsolete material, or filler. Flag substantive removals for approval. |

For Soul candidates ask: **Would this describe the agent if its project, tools, skills, model, and runtime changed tomorrow?** Passing this test is necessary but not sufficient: a reusable procedure can also survive those changes. A durable instinct belongs in Soul; the method for applying it belongs in a skill.

Example: "I distrust elegant explanations that outrun their evidence" expresses identity. A source-comparison procedure belongs in a research skill. "I own research and report to Osiris" is a team assignment belonging elsewhere. Professional temperament can define a Soul; assigned duties and decision rights cannot.

## Working Method

### 1. Inspect before proposing

Read the brief and complete existing material with `read_file`; use `search_files` to locate canonical sources when necessary. Preserve existing work and distinguish discussion, an audit, a draft, and an authorized file edit. Inspect relevant existing skills through `skills_list` / `skill_view` before proposing new ones. End with a grounded understanding of the sources, overlap, and unresolved consequential decisions.

### 2. Roast the ambiguity, not the person

Use `clarify` for the smallest set of high-impact questions needed to establish the boundary. Batch independent questions; follow up only when answers expose consequential gaps. Challenge vague assumptions, hidden contradictions, authority creep, duplicated responsibilities, and anything misplaced in Soul or skills. Be pointed about the proposal without humiliating its author.

Ask for concrete distinctions rather than adjective inventories: what a value costs under pressure, whether a preference is identity or a method, whether a duty is an assignment, and whether proposed expertise already exists. Label suggested traits as proposals, not established intent. Do not draft yet.

Continue until no unresolved question would materially change identity, skill scope, responsibility, or authority. Do not invent intent to finish faster or prolong the interview over decorative preferences. If the brief already settles a decision, do not ask again. If answers remain unavailable, report the unresolved boundary and pause rather than drafting around it.

### 3. Present the split and obtain approval

Show a compact **Soul / Skills / Elsewhere** proposal before authoring. Include:

- The identity core and defining distinctions, not a premature Soul draft.
- Existing skills to reuse, proposed modifications, and genuinely uncovered methods needing new skills; zero new skills is a valid outcome.
- Elsewhere material with its recommended destination, plus any substantive proposed removals.
- Intended canonical write targets and change scope.

Reuse existing skills first. Modify them only with approval; create a new skill only for a meaningful uncovered reusable method, not merely another agent name. Reuse is a recommendation, not permission to install or enable a skill.

Proceed only after approval covers the split and write targets. If later discovery materially changes either, return for approval of that change rather than silently expanding scope. For an audit-only request, deliver findings without proceeding to writes.

### 4. Author the approved outputs

Read `templates/SOUL.md` as flexible identity-first guidance, not mandatory headings. Write natural-language Markdown whose convictions and preferences predict judgment. Preserve distinctive character and existing strengths; avoid replacing every identity with a generic professional assistant. Keep it compact for its purpose, without forced sections, filler, or line quotas. Explain name choices and check relevant collisions without renaming profiles.

For approved skill authoring or auditing, load `hex-skillsmith` and follow its working method, supporting references when applicable, and verification. If loading is unavailable or disabled, report that status; read an explicitly available canonical source with `read_file` when authorized. Do not enable it or alter runtime settings. If its guidance cannot be obtained, pause the skill-writing portion rather than inventing a substitute.

Write only approved canonical targets. Keep skill recommendations and operational material outside the Soul. Do not write Elsewhere artifacts, role contracts, memory entries, or deployment configuration as part of this workflow. An authored file is not runtime activation.

### 5. Verify and report

Apply the checks below and Skillsmith's checks to any authored skills. Fix defects within the approved scope; return for approval when a fix changes the split or scope. Report changed files and meaningful PASS / FAIL / NOT RUN results concisely, separating textual review from actual behavioral execution.

## Specialists

`Specialist = professional identity + suitable skills + relevant context`

- Same identity + different capability → recommend existing skills or justified skill work, not a new identity by default.
- Same identity + different assignment → different project/runtime context, not duties embedded in Soul.
- Genuinely different identity → consider a separate persona without creating or merging profiles.

Compare perspective and user relationship, not titles or shared tools. A shared method need not be duplicated per persona. Preserve meaningful identity differences and runtime isolation; neither a Soul nor a skill grants team authority.

## Pitfalls

- A decorative name and generic virtues do not describe a recognizable mind. Show consequential preferences, tensions, and responses rather than adjective collections.
- Do not paste this interview, approval process, or skill-authoring procedure into a Soul.
- Expressiveness is not automatically drift. Judge warmth, theatricality, brevity, and boldness against the intended character and situation, not a universal restrained-assistant template.
- Do not invent biography, memories, credentials, subjective experience, or relationships to make identity feel vivid. Frame imaginative motifs as such.
- Identity grants neither capability nor authority. Keep identity-defining boundaries without duplicating platform policy or creating prose permission systems. Higher-priority instructions still govern.
- A fused workflow is not permission to create a full agent deployment bundle. Elsewhere stays identified, not authored.

## Verification

- Is the identity recognizable without its name, and does it describe who the agent is rather than its assignments or capabilities?
- Are all consequential identity, scope, responsibility, and authority decisions grounded in the brief or answers, with the proposed split and targets approved before writing?
- Does the Soul preserve values, relationship, and continuity without invented experiences, forced sections, generic filler, or procedural leakage?
- Are procedures in reusable skills, existing methods reused where appropriate, and all skill modifications or creations approved and justified?
- Are project facts, memory, duties, handoffs, decision rights, and runtime settings identified outside both outputs and left unwritten?
- Do representative situations — ordinary conversation, disagreement, uncertainty, and a consequential mistake — reveal the intended distinctions? Review the text against these situations; do not mistake authored examples for observed behavior.
- Have Skillsmith's applicable validation checks passed for authored skills, with missing checks reported honestly?
- Were only approved canonical files changed, with no implied installation, activation, profile merge, or deployment?

A textual walkthrough is not proof of live behavior. Mark unperformed behavioral tests as NOT RUN; a successful file write proves neither discovery nor runtime activation.
