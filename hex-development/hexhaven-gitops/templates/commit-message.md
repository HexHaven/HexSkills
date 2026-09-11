# Commit Message Shape

Follow Conventional Commits for the subject line (see `github-pr-workflow`
for the type list). Keep the subject under ~72 characters.

```text
<type>(<scope>): <concise subject describing what changed>

<body: 1-3 short paragraphs or a bullet list>
- What changed (concrete, not "various fixes")
- Why the change exists (the authorized intent that required it)
- How it relates to the operator's command or repository documentation
  (e.g. "per AGENTS.md §3" or "closes the drift <operator> flagged")
```

## Example (placeholder values)

```text
docs(hexhaven-gitops): fix broken skill cross-reference in README

- README linked to a renamed skill directory that no longer exists
- Requested by <OPERATOR> to keep the skill index navigable
- Aligns with the "every support file has a consumer" rule in
  hex-skillsmith/SKILL.md
```

## Rules

- Never fabricate a rationale — state only what was actually true of the
  task and the evidence inspected.
- Do not reference secrets, tokens, internal hostnames, or credentials in
  the message body.
- Keep the body factual and short; this is not a changelog entry.
- Add `Signed-off-by` via `git commit -s` only when the target repository's
  convention requires DCO sign-off (check its README/CONTRIBUTING first).
