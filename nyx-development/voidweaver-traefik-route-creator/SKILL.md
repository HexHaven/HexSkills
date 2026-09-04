---
name: voidweaver-traefik-route-creator
description: Add a Traefik dynamic route on Voidweaver for a local app.
version: 0.1.1
author: Nyxion, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [nyx, traefik, voidweaver, ingress, dynamic-config]
    category: nyx-development
    related_skills: [reverse-proxy-ingress-administration, docker-compose-stack-deployment]
---

# Voidweaver Traefik Route Creator

Create exactly one new dynamic Traefik service rule on the secondary Traefik
instance running on Voidweaver, for a local application reached through the
already-delegated `*.home.nyxion.cloud` namespace. This skill owns only that
one dynamic-file write; it does not own or touch any other layer of the path.

## When to Use

- Exposing a new local application on Voidweaver under `*.home.nyxion.cloud`.
- Adding/auditing a `~/.config/traefik/dynamic/<service>.yaml` file for the
  secondary Traefik instance.

Don't use for: primary Traefik on docker-realm, Cloudflare Tunnel routes,
Cloudflare DNS, Technitium records, Tailscale Serve/DNS, OPNsense/UFW rules,
ACME/certificate configuration, or Docker networking. Those are handled
elsewhere (see `reverse-proxy-ingress-administration` for HAProxy/Tailscale/
OPNsense ingress, `docker-compose-stack-deployment` for Traefik-fronted
Docker stacks on docker-realm). If the request touches any of those layers,
stop and hand off — do not extend this skill's scope.

## Existing Architecture

```text
LAN / Tailnet client
  -> Technitium split DNS
  -> 10.20.30.100:443 (Primary Traefik, docker-realm)
  -> http://voidweaver.nyxion.lan:8080
  -> Secondary Traefik on Voidweaver
  -> local application
```

Primary Traefik already delegates `*.home.nyxion.cloud` to Voidweaver.
Adding a local service therefore requires only one new file under
`~/.config/traefik/dynamic/` on Voidweaver, which the running secondary
Traefik watches automatically.

## Procedure

1. **Collect inputs** — Ask for exactly two things: the domain (or a short
   service name) and the target `IP:Port`. Never invent an IP or port. If
   given a short name like `newapp`, normalize it to `newapp.home.nyxion.cloud`
   and show the normalized hostname before applying anything.

2. **Validate** — Using `search_files` (target="files", path=
   `~/.config/traefik/dynamic/`), confirm: the hostname ends in
   `.home.nyxion.cloud`; the target is a syntactically valid `IP:Port`; no
   existing dynamic rule already serves that hostname (grep file contents
   with `search_files` target="content"); the intended filename
   `<service>.yaml` does not already exist. Where practical, check target
   reachability with `terminal` (e.g. `curl -sS -o /dev/null -w '%{http_code}\n' --max-time 3 http://<ip:port>/`
   or `nc -zv <ip> <port>`). If an existing rule conflicts, stop and report
   it — do not overwrite silently.

3. **Derive the service slug** — Take the hostname's leftmost label
   (`newapp.home.nyxion.cloud` -> `newapp`) as the filesystem-safe,
   deterministic service/router/file name.

4. **Write the dynamic config** — Use `write_file` to create
   `~/.config/traefik/dynamic/<service>.yaml`:

   ```yaml
   http:
     routers:
       <service>:
         rule: "Host(`<domain>`)"
         entryPoints:
           - downstream
         service: <service>

     services:
       <service>:
         loadBalancer:
           passHostHeader: true
           servers:
             - url: "http://<ip:port>"
   ```

   Default to `http://` for the backend unless the operator explicitly asks
   for HTTPS. Default `passHostHeader: true`; only switch to `false` if the
   backend demonstrably rejects the external hostname or needs its original
   local Host header — never flip this preemptively. Do not restart Traefik;
   the dynamic directory is watched automatically. Restart only if a
   configuration reload demonstrably fails and a restart is the actual fix.

5. **Validate after creation** — Check three layers, each with `terminal`:
   - Config loaded: the secondary Traefik on Voidweaver runs as a **Docker
     container**, not a systemd unit — `systemctl status traefik` will
     report "could not be found" even when Traefik is healthy. Use
     `docker ps --filter name=traefik` to confirm the container is up, and
     `docker logs --since 5m <container>` (or `docker compose logs`, if it's
     compose-managed) to check for dynamic-config parse errors.
   - Direct secondary route: `curl -H 'Host: <domain>' http://10.10.10.69:8080/`
   - Full route: `curl https://<domain>/` — confirm expected status, valid
     TLS, and that the request reached the intended backend. An application
     auth redirect (e.g. `302`) is not a routing failure.

   Done when all three checks produce observed evidence (PASS/FAIL each,
   not assumed).

6. **Report** — Summarize file path, domain, backend, and PASS/FAIL for the
   secondary route and full HTTPS route. On any failure, name the failing
   layer explicitly; do not claim success from a file write alone.

## Optional: Exposing the Traefik API/Dashboard itself (`api@internal`)

Routing a hostname to Traefik's own API/dashboard (e.g.
`traefik-home.home.nyxion.cloud/dashboard/`) is a variant of the normal
procedure, not a different skill — but it needs one extra gated step because
it is the one case where the router's `service` is the built-in
`api@internal` instead of a `loadBalancer` pointing at an external backend.

1. **Gate-check first**: read the active static config from the *running*
   container, not a checked-out copy on disk — `docker exec <container> cat
   /etc/traefik/traefik.yaml | grep -A2 '^api:'`. If `dashboard: false`,
   this is a static-configuration change, outside this skill's normal
   dynamic-file-only scope. Stop and report exactly what would need to
   change (`api.dashboard: true`, `api.insecure` stays `false` — never flip
   `insecure: true`, that opens an unauthenticated listener). Get **explicit
   user authorization** before touching the static file or restarting the
   container; do not infer it from "build the route" alone.
2. If authorized: back up the static config file first (timestamped copy
   next to the original), then flip `api.dashboard` to `true` only, and
   restart the container (`docker restart <container>` is sufficient for a
   bind-mounted config file — no full recreate needed). Poll
   `docker inspect --format '{{.State.Health.Status}}'` until `healthy`
   before proceeding.
3. Write the dynamic router with `service: api@internal` and a rule that
   scopes to both `/api` and `/dashboard` path prefixes — see
   `templates/api-internal-dashboard-route.yaml`. No `services:` block is
   needed; `api@internal` is built in.
4. Verify router resolution directly against the Traefik API on the real
   entryPoint address (not `127.0.0.1` — see pitfall below):
   `curl -H 'Host: <domain>' http://<entrypoint-ip>:<port>/api/http/routers/<service>@file`
   and confirm `"service":"api@internal"` in the response.
5. The Traefik dashboard requires the trailing slash: `/dashboard/` returns
   200, `/dashboard` (no slash) returns 404 by design — that is not a
   routing failure.
6. Full details and a worked example: `references/api-internal-dashboard-enablement.md`.

## Safety Boundaries

- Touch only `~/.config/traefik/dynamic/<service>.yaml` on Voidweaver. Never
  create, edit, or delete any other file in that directory.
- Never modify primary Traefik, Cloudflare Tunnel/DNS, Technitium, Tailscale
  (Serve or split-DNS), OPNsense, UFW, ACME/certificate config, or Docker
  networking from this skill.
- Never overwrite an existing service configuration silently; stop and
  report a conflict instead.
- If the new file breaks the secondary Traefik configuration, roll it back
  (remove the file) rather than leaving a broken route live.
- Use `<HOST>`, `<IP_ADDRESS>`, and `<PORT>` placeholders in any illustrative
  example; never hardcode secrets or unrelated internal identifiers.
- The static-config exception (`api@internal` dashboard) is the only case
  where this skill may touch `traefik.yaml` and restart the container, and
  only with explicit per-instance authorization plus a backup taken first.

## Pitfalls

- Treating a short service name as a full hostname without normalizing and
  confirming it with the operator first.
- Assuming a target is reachable without an actual check when practical to
  perform one.
- Assuming Traefik is systemd-managed and checking `systemctl` for its
  status/logs — on Voidweaver it runs in Docker; use `docker ps`/`docker
  logs` instead.
- Running plain `docker ps`/`docker inspect` and seeing no `voidweaver-traefik`
  container — the default Docker CLI context on this host can point at
  Docker Desktop instead of the native engine socket. Check
  `docker context ls` and use `docker --context default ...` (or whichever
  context lists it) before concluding the container is missing.
- Probing the Traefik API on `127.0.0.1` when the container runs with
  `network_mode: host` and the entryPoint is bound to a specific LAN IP
  (e.g. `10.10.10.69:8080`) — `127.0.0.1` inside the container's own network
  namespace will refuse the connection; use the actual entryPoint address.
- Restarting Traefik reflexively instead of relying on the dynamic-file
  watcher.
- Reporting the route as live from the written file alone, without the
  secondary-route and full-HTTPS-route checks.
- Treating an HTTP redirect from application-level auth as a routing
  failure.

## Verification

- [ ] Hostname ends in `.home.nyxion.cloud` and target is a valid `IP:Port`.
- [ ] No pre-existing rule or filename conflict (or conflict reported and
      stopped).
- [ ] `~/.config/traefik/dynamic/<service>.yaml` written with correct router,
      service, and backend.
- [ ] Secondary route (`curl -H 'Host: ...' http://10.10.10.69:8080/`)
      observed PASS/FAIL.
- [ ] Full HTTPS route (`curl https://<domain>/`) observed PASS/FAIL.
- [ ] No other dynamic rule or unrelated infrastructure layer was touched.
