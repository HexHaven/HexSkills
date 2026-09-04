# Enabling the Traefik dashboard via `api@internal`

Worked example observed on Voidweaver (`voidweaver-traefik`, Docker,
`network_mode: host`, static config `~/.config/traefik/traefik.yaml`,
dynamic dir `~/.config/traefik/dynamic/`).

## Why this needs a gate

The normal dynamic-route procedure only ever points a router at an external
`loadBalancer` backend (`http://<ip:port>`). Routing to Traefik's own API/
dashboard uses the built-in `api@internal` service instead, which only
exists when the *static* config has `api.dashboard: true`. That static
setting is outside this skill's normal scope (which owns only the dynamic
file), so it is gated behind explicit authorization rather than applied
automatically just because a route was requested.

## 1. Gate-check the live static config

Read it from the **running container**, not a checked-out copy on disk —
the checked-out copy can be stale or, in one observed case, superseded
entirely by a relocated authoritative directory:

```sh
docker --context default exec voidweaver-traefik cat /etc/traefik/traefik.yaml | grep -A2 '^api:'
```

If this prints `dashboard: false`, stop before writing anything. Report the
exact change required:

```yaml
api:
  dashboard: true
  insecure: false   # never flip this to true — it opens an unauthenticated listener
```

and that applying it requires a container restart to take effect. Do not
touch the file or restart the container without the operator's explicit,
per-instance authorization — do not infer it from a plain "build the route"
request.

## 2. If authorized: apply the static change safely

```sh
cp ~/.config/traefik/traefik.yaml ~/.config/traefik/traefik.yaml.pre-dashboard-enable-$(date +%Y%m%dT%H%M%S%z)
```

Then flip only `api.dashboard` to `true` (leave `insecure: false`) with a
targeted patch — not a full file rewrite. Restart the container; for a
bind-mounted config file a plain restart is sufficient, no recreate needed:

```sh
docker --context default restart voidweaver-traefik
```

Poll health before proceeding:

```sh
docker --context default inspect voidweaver-traefik --format '{{.State.Health.Status}}'
```

Also check `docker --context default logs --since 20s voidweaver-traefik`
for parse errors — a successful restart is not itself proof of a valid
config.

## 3. Write the dynamic route

Use `templates/api-internal-dashboard-route.yaml` as the shape. No
`services:` block — `api@internal` is built in. Scope the rule to both
`/api` and `/dashboard` path prefixes so both the API and the dashboard UI
work under the one hostname.

## 4. Verify router resolution against the real entryPoint

When the container runs with `network_mode: host`, `127.0.0.1` inside the
container's own namespace refuses connections — the entryPoint is bound to
a specific LAN address (e.g. `10.10.10.69:8080`), observed in
`entryPoints.downstream.address` in the static config. Query the Traefik
API on that real address:

```sh
curl -H 'Host: <domain>' http://<entrypoint-ip>:<port>/api/http/routers/<service>@file
```

Confirm the response contains `"service":"api@internal"` and
`"status":"enabled"`.

## 5. Full end-to-end check

The dashboard requires a trailing slash:

```sh
curl -o /dev/null -w '%{http_code}\n' https://<domain>/dashboard/   # expect 200
curl -o /dev/null -w '%{http_code}\n' https://<domain>/dashboard    # expect 404 by design, not a failure
```

Also re-check any pre-existing route on the same Traefik instance was not
disturbed by the restart (same secondary-route and full-route curl checks
as the normal procedure).

## Rollback

If anything fails: remove the newly written dynamic file, restore
`api.dashboard: false` from the timestamped backup, restart the container
again, and re-verify the pre-existing routes.
