# Gitea API workflows

Sources: [Gitea API usage](https://docs.gitea.com/development/api-usage/), [API reference](https://docs.gitea.com/api/). The target instance's `/api/swagger` and `/swagger.v1.json` are authoritative for its installed version. The paths below are relative to `/api/v1`.

## API client and preflight

The standalone plugin (when separately installed and enabled) exposes `gitea_identity`; repository, issue and PR list/read/create tools under the `gitea_*` prefix; plus `gitea_issue_comment` and `gitea_comment_list`. It resolves each call's profile-scoped Gitea settings in-process, not through a terminal child. Its results are intentionally metadata-only; use the authenticated UI for content, discussions, duplicate checks, permission review, and full write read-back. It does not submit reviews, merge, push Git branches, create organizations, or manage SSH keys. The tool descriptions ask for human approval, but do not implement a hard approval gate. Never infer permission to mutate from mere tool availability.

### Token injection (script path)

Without the plugin, run the script as a child of the secret manager's own injector, so the token exists only in that child's environment:

```sh
# refs file (scratch dir, references only, delete afterwards):
#   GITEA_URL=https://<HOST>
#   GITEA_TOKEN=pass://<Vault>/<Item>/<FIELD>
pass-cli run --env-file <refs-file> -- python3 scripts/gitea_api.py GET /user
```

- Proton Pass references have exactly three components. A slash inside an item title is `%2F`: item `Gitea/Alpha` is `pass://Agents/Gitea%2FAlpha/GITEA_TOKEN`. An unencoded slash fails with "Could not find item with name Gitea".
- Several calls: put them in one small shell script and run that script under one `pass-cli run`, rather than one secret fetch per call.
- Never export the token into the interactive shell, a dotenv file, a Git remote or a log. If a profile-scoped plugin is installed, prefer it; this path does not bypass a plugin's profile isolation.

`python3 scripts/gitea_api.py METHOD '/endpoint?query' [--data-stdin]` uses `GITEA_URL` and `GITEA_TOKEN` already supplied in its environment; run from the skill directory or use its absolute script path. No credential is accepted on the command line or echoed. For JSON writes, pipe a prepared, reviewed JSON body to `--data-stdin`. Keep it free of secrets. Use the instance's configured base URL (including an installation subpath if any); HTTPS is required except for a loopback test. No redirect is followed. Do not use a generic API client to create or inspect access tokens or admin endpoints. Do not dump environment variables or enable verbose HTTP tracing.

Preflight: `GET /user` verifies the request succeeds, but the bundled client prints only the numeric user ID, not the login. Confirm the identity by that ID or in the authenticated UI. Check the actor's organization rights with `GET /users/{login}/orgs/{org}/permissions` before any org write; team-admin rights include repository deletion, so keep writes to the approved target. `GET /repos/{owner}/{repo}` can confirm existence and return ID/visibility metadata; inspect target fields and permissions in the UI. An HTTP 401 means missing/invalid authentication; 403 may mean insufficient permission or an organization policy. Stop rather than elevate. For read-only public operations, the web UI may suffice if API authentication is not available. Do not make mutation calls without a known identity and approval.

Gitea paginates lists with `page` and `limit`; follow the `Link` header when available or continue through pages until exhausted. The bundled client prints only HTTP status and typed IDs, booleans and known states—not titles, bodies, URLs or response headers. Page explicitly (`?page=1&limit=50`, then page 2, and so on) for candidate IDs; inspect each candidate in the UI for duplicates and discussion. Do not equate one page with the complete set or metadata-only output with verification of written content.

## Repository workflow

- Look up `GET /repos/{owner}/{repo}` (a 404 before creation is expected); search within the intended owner/organization and inspect existing repository names before creating anything. Confirm the organization's policy permits this actor to create a repo and establish visibility, ownership, default branch, and initial contents intentionally.
- Personal repository: `POST /user/repos`; organization repository: `POST /orgs/{org}/repos`. For a creation body, confirm fields against instance Swagger; at minimum specify `name` and `private` explicitly, and choose initialization/default branch settings deliberately. Obtain separate approval for repository creation even if the account is technically permitted. Read back `GET /repos/{owner}/{repo}` and compare owner, name, visibility, default branch and URLs.
- A new local remote and a push are separate operations. Read `git status --short --branch`, `git remote -v`, intended branch and commit SHA first. Require explicit approval for remote configuration and another for publishing the exact branch to that URL. After push, read the remote branch SHA and compare; a local commit alone is not publication. Do not embed API tokens in remote URLs.
- Never create an organization, enable team-wide rights, or grant agents general repo-creation privileges as an incidental step.

## Issue workflow

- List `GET /repos/{owner}/{repo}/issues?state=all&page=1&limit=50` and inspect relevant issue details/comments before editing. This listing can include pull requests depending on version; inspect the object type and do not treat every entry as a standalone issue.
- Create: `POST /repos/{owner}/{repo}/issues` with explicit `title` and `body`; optional labels/assignees only if confirmed against instance Swagger and authorized. Read back `GET /repos/{owner}/{repo}/issues/{index}` and compare content.
- Comment: `POST /repos/{owner}/{repo}/issues/{index}/comments` with `body`; read back the returned comment by ID or list comments and match its ID/body. Edit/close only after re-reading current state and discussion; review exact method and fields in instance Swagger.

## Pull-request workflow

- Review base/head and actual remote branch SHAs. List `GET /repos/{owner}/{repo}/pulls?state=all&page=1&limit=50` and check for existing PRs. Opening a PR does not push a branch: push needs its own authorization and SHA verification.
- Create: `POST /repos/{owner}/{repo}/pulls` with explicit `title`, `body`, `head`, and `base` as supported by instance Swagger. Read back `GET /repos/{owner}/{repo}/pulls/{index}` and check state/base/head; fetch changed files, commits, and conversations before claiming it is ready.
- Review: inspect `GET /repos/{owner}/{repo}/pulls/{index}/files`, `/commits`, and issue-style comments (`/issues/{index}/comments`), plus review and status/check endpoints supported by the instance. Do not post a review merely because the diff was read; approval/comments are writes requiring explicit authorization.
- Merge: re-read PR state, target branch, checks and approvals; obtain specific merge authorization and use the merge endpoint only with the agreed method/branch handling. Read back PR state and target branch SHA. A successful API response alone is insufficient, and a merge is not deployment.

## Failure handling

On 404 verify origin, owner/repo and visibility before concluding the object does not exist. Status codes are version-specific: Gitea 1.25 answers an issue `PATCH` with 201, not 200, and a repository `DELETE` with 204 and no body. On 409/422 inspect current state and validation errors in the instance UI or Swagger; don't retry with a different payload blindly. On rate limiting or network errors, report the blocker and do not invent remote results. The client intentionally omits HTTP error bodies to avoid accidental credential disclosure; use a safe authenticated browser/UI inspection when more detail is needed.
