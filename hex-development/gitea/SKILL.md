---
name: gitea
description: "Gitea repos, issues, pull requests and reviews via REST."
version: 0.1.0
author: HexHaven, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [gitea, git, repositories, issues, pull-requests, code-review]
    category: hex-development
    related_skills: [hex-forge]
---

# Gitea

Use a specified Gitea instance for repository discovery/creation, issues, pull requests, and review. This is a hosting-service skill, not a mandate to publish local work. No instance, organization, agent account, or repository-creation policy is assumed. For the idea-to-local-build lifecycle, use `hex-forge` instead.

## When to Use

Use for an explicitly named Gitea instance when inspecting or managing its repositories, issues, pull requests, or reviews. Do not use for GitHub (`github`), local-only implementation (`hex-forge`), or an unchosen hosting service. If a Gitea instance has not yet been set up, this skill can describe the required access and policy decisions but cannot assume an available service.

## Before any operation

1. Establish the intended instance URL, repository owner/name, and identity from the request or local configuration. Never infer an organization from a remote name. Read `git remote -v` only if a local checkout is relevant; treat a remote URL as a clue, not authorization to change it.
2. Read `references/api-workflows.md` for endpoint and approval details. Check the instance's `/api/swagger` or `/swagger.v1.json` for its version and accepted request fields; do not assume the public latest API exactly matches the instance.
3. Prefer the separately installed `gitea` tool plugin's typed `gitea_*` tools for its supported repo/issue/PR operations. The plugin reads `GITEA_URL` and `GITEA_TOKEN` from the owning Hermes profile's secret scope; it is not installed or enabled merely because this skill is present. Its metadata-only output does **not** replace an authenticated UI review of titles, bodies, comments, permissions, or CI. PR review submission, merge, Git push and deployment are not plugin tools. If the plugin is absent or reports a profile-scope error, stop and report that setup gap; do not expose a Proton Pass-hydrated token through terminal passthrough or silently switch to the bundled script. The standalone `scripts/gitea_api.py` is a manual single-profile fallback only when an already approved process environment explicitly supplies both variables; do not use it to work around a missing plugin or profile isolation. It requires Python 3 standard library only and prints typed status/ID metadata.
4. Read the current target and relevant discussion before writing. Search existing repos/issues/PRs for duplicates, including pagination where needed. Check account permissions and organization policy; technical permission alone is not approval.
5. Obtain explicit authorization for the exact write (owner/repo, operation and payload), especially repository creation, push, merge, deletion, or branch protection changes. A general request to use Gitea does not authorize creation of a company/org or free creation of repositories.
6. After a write, read the exact created/changed object back by its returned URL or ID; verify requested fields and state. Do not report success solely from a 2xx response. Treat Git pushes separately: inspect intended paths/ref, obtain push approval, push, then fetch/read remote ref and compare exact SHA. Never force-push by default.

## Routing

| Intent | Read in reference |
|---|---|
| Find/create repository or inspect remote configuration | Repository workflow |
| Find/create/update/close issue or comment | Issue workflow |
| Open/review/merge pull request | Pull-request workflow |
| Authenticate, pagination, error handling | API client and preflight |

## Safety and boundaries

- Never put a token in a URL, command argument, file in the repository, chat, log, or Git remote. Do not print credential-bearing responses or use API token-creation endpoints with the generic client.
- Don't create an organization, change memberships, set organization-wide policy, or install a webhook as a side effect of creating a repository. Those need separate approval and a reviewed procedure.
- Branch, issue, PR and release states are independent. A merged PR is not proof a deployment happened. A PR's UI checks are not proof CI passed: read its actual check/status data on this instance or mark them unverified.
- On HTTP 401/403 stop and diagnose access/scope; do not switch accounts or elevate privileges silently. On conflict or stale base, re-read and seek direction rather than overwriting.

## Verification

Run `python3 scripts/test_gitea_api.py` from this skill directory for offline secret-output and boundary regression checks. Live Gitea authentication, permissions, pagination, write/read-back and Git push remain unverified until exercised against an explicitly approved instance.

- [ ] Target instance, owner/repo, API version and identity were established.
- [ ] Existing state and discussions were read before a write.
- [ ] Every mutation had explicit scope and approval; exact target was read back.
- [ ] Push/merge/CI/deployment claims are supported by their own fresh evidence, or marked NOT RUN.
- [ ] No unapproved organization-wide changes or secret exposure occurred.
