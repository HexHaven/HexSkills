# Aurelius Completion Report

Fill in every field with observed evidence, not assumption. Use `NOT RUN` /
`UNVERIFIABLE` rather than omitting a field you couldn't check.

```markdown
## Aurelius GitOps Report

**Repository:** <owner/repo>
**Branch:** <branch>
**Commit:** <full SHA>

**Change summary:** <1-2 sentences: what changed>

**Rationale:** <why the change exists — tie to operator command / repo docs>

**Validation performed:**
| Check | Result |
|---|---|
| Formatting | PASS / FAIL / NOT APPLICABLE |
| Lint | PASS / FAIL / NOT APPLICABLE |
| Tests | PASS / FAIL / NOT APPLICABLE |
| Config validation | PASS / FAIL / NOT APPLICABLE |

**Push verification:**
- Local HEAD: <SHA>
- Remote <remote>/<branch>: <SHA>
- Match: VERIFIED_MATCH / MISMATCH

**Signature:** PASS / FAIL / UNVERIFIABLE

**CI / GitOps status observed:** <what was seen, or "none observable">

**Escalations raised:** none / <boundary condition + what's needed>
```
