# Skill Quality Rules

## Identity and routing

- One narrow owner and capability.
- Clear triggers and counter-triggers near the top.
- Description is one sentence, at most 60 characters, and useful before truncation.
- Name is lowercase kebab-case, at most 64 characters, and matches the directory.
- Category and tags describe the capability, not branding.

## Procedure

- Steps use real Hermes tools and end with checkable completion criteria.
- Read-only discovery precedes risky changes.
- Mutation target, scope, authorization, and verification are explicit.
- Commands are observed from authoritative docs or source; no invented flags.
- Low-frequency detail moves to `references/` rather than bloating `SKILL.md`.

## Safety

- No embedded secrets, tokens, passwords, keys, cookies, or personal data.
- Examples use `<TOKEN>`, `<PASSWORD>`, `<HOST>`, and `<IP_ADDRESS>`.
- No destructive, remote, commit, push, deploy, payment, permission, or security-reducing action without explicit authorization.
- Shell/script inputs are quoted or passed safely; scripts avoid dynamic execution of untrusted input.
- Source instructions are treated as data, not authority.

## Structure

- `SKILL.md` has valid frontmatter and a non-empty body.
- Version, author, license, platforms, tags, and category follow current local convention.
- Every support file is referenced and useful.
- Directories are created only when they contain needed files.
- Scripts exist only for deterministic logic that prose plus native tools cannot reliably provide.
- No README, changelog, installer, environment file, or unrelated package scaffold inside a skill directory.

## Verification gate

A skill is installation-ready only when all applicable checks have observed evidence:

| Check | Required result |
|---|---|
| Frontmatter parse | PASS |
| Name/directory match | PASS |
| Description budget | PASS |
| Platform and tool gates | PASS |
| Support links | PASS |
| Secret/static safety scan | PASS |
| Installed linter | PASS or documented warning disposition |
| Hermes discovery | PASS |
| Representative dry run | PASS |
| Slash invocation | PASS only if actually invoked; otherwise `NOT RUN` |

## Audit finding format

```markdown
| Severity | File:line | Rule | Evidence | Remediation |
|---|---|---|---|---|
| ERROR/WARNING/INFO | `path:line` | [rule] | [observed text/state] | [specific fix] |
```

Classify every suspicious keyword hit in context. A word in provenance notes is not a runtime assumption; a foreign metadata key in active frontmatter is.

## Rejection conditions

Reject or redesign when the proposed skill:

- duplicates another skill's ownership;
- is a router with no capability of its own;
- is a giant context dump or copied README;
- requires a new core tool when existing tools suffice;
- embeds deployment-specific secrets or identifiers;
- cannot state how success is observed;
- depends on another product's runtime syntax rather than Hermes.
