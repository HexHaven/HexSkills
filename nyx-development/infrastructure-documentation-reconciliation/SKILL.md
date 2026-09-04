---
name: infrastructure-documentation-reconciliation
description: Use when reconciling infra docs with live evidence.
version: 0.1.0
author: Nyxion, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [nyxcloud, infrastructure, inventory, documentation, reconciliation, evidence]
    category: nyx-development
    related_skills: [nyx-build]
---

# Infrastructure Documentation Reconciliation

Maintain infrastructure documentation from authoritative live read-only evidence. This is a class-level workflow for inventory, topology, routing, firewall, exposure, and access-name records—not a deployment workflow.

## When to Use

- Refresh shared homelab or infrastructure documentation from current hosts.
- Reconcile documented guest inventory with Proxmox and gateway state.
- Record current firewall, VLAN, routing, or ingress observations without changing infrastructure.
- Investigate stale documentation after migrations, renames, or guest replacement.

Don't use for: applying firewall/DNS/Proxmox changes, deployment, service restarts, secrets, or documenting a service-specific stack that belongs in another repository.

## Authority Order

Use this order when facts conflict:

1. Explicit current operator statement.
2. Fresh live evidence from the named authoritative host.
3. Executable repository configuration and registries.
4. Current canonical documentation.
5. Historical notes and assistant memory.

Never silently reconcile a conflict. State the conflict, identify the authoritative source, preserve uncertainty, and make the smallest documentation change.

## Workflow

`SCOPE → DISCOVER → COLLECT → RECONCILE → PATCH → QUALIFY → REPORT`

### 1. SCOPE

Confirm the repository root, target documentation directory, authoritative hosts, and read-only boundary. Read applicable `AGENTS.md`, inspect `git status --short`, and identify unrelated modified or untracked files as protected. Define affected files and non-goals before editing.

For NyxCloud homelab work, the canonical repository is the shared infrastructure documentation repository; service deployment repositories remain out of scope unless explicitly requested.

### 2. DISCOVER

Read the collector or verification script before running it. Read the affected docs and trace each claim to its section, table, or source. Do not invent IPs, CT-IDs, MACs, ports, firewall rules, status, backup class, exposure, or service health.

Use operator-maintained SSH aliases exactly as supplied. Do not replace an alias with a guessed hostname, raw address, relaxed host-key policy, or modified SSH configuration.

### 3. COLLECT

Run the repository's read-only collector fresh, not cached output. For the NyxCloud Proxmox inventory:

```bash
./scripts/collect-voidforge-inventory.sh
```

Use narrow follow-up reads on the authoritative targets when the collector omits a needed field. Typical evidence includes `pct list`, `pct config`, `qm list`, `qm config`, QEMU guest-agent output, gateway interface state, ARP mappings, and the active PF ruleset. Keep commands read-only and avoid dumping secrets or unrelated configuration.

Record the collector's generated timestamp and distinguish:

- **Observed:** directly returned by a current command.
- **Configured:** declared in documentation or config but not proven live.
- **Inferred:** derived from a verified schema, such as CT-ID/address mapping.
- **Unknown:** absent, ambiguous, or not collected.

### 4. RECONCILE

Compare live roster, identity, address, MAC, VLAN/tag, firewall flag, protection flag, unprivileged flag, and status against the documentation. Check for:

- guests newly present, absent, renamed, or repurposed;
- duplicate or conflicting IP/MAC/CT-ID claims;
- stale migration and replacement statements;
- changed guest-firewall or protection flags;
- gateway VLAN interfaces and explicit PF rules that support documented flows;
- claims that exceed the evidence, especially backup, exposure, health, and deletion state.

An absent guest is not proof of deletion or decommissioning. A present guest with a changed hostname is not proof of unchanged role. Mark disposition and ownership as needing verification when evidence is incomplete.

### 5. PATCH

Apply the smallest reviewable documentation patch. Update every affected canonical file only when its claims changed:

- `inventory.md` for mutable guest state;
- `topology.md` for placement, addressing, VLAN, DNS, or ingress architecture;
- `security.md` for verified policy, firewall observations, or explicit unknowns;
- `README.md` only when the golden-state summary changed.

Preserve unrelated work. Keep raw collector output out of the repository unless explicitly requested. Do not automatically overwrite documentation from raw command output.

### 6. QUALIFY

Run the documented checks and fresh consistency checks:

```bash
git diff --check
git status --short
```

Also validate internal Markdown links and search for stale contradictory statements from the old evidence timestamp or old guest identity. Confirm that table records match the fresh roster and that every changed security claim includes source, destination, protocol, port, purpose, and validation evidence where applicable.

Use separate statuses: `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN`. A successful SSH command proves only the returned observation, not claims that were not queried.

### 7. REPORT

Summarize changed files, evidence timestamps, observed discrepancies, unresolved unknowns, validation results, and untouched pre-existing changes. State explicitly that no remote mutation, deployment, restart, commit, or push occurred unless separately authorized and verified.

## Evidence Reference

See `references/proxmox-opnsense-evidence.md` for the reusable evidence matrix and reconciliation checklist.

## Safety Boundaries

- Read-only discovery precedes all edits.
- Never weaken SSH host-key verification or bypass permissions.
- Never expose secrets, credentials, tokens, private keys, cookies, or full sensitive configuration.
- Do not infer backup class, exposure, deletion, firewall policy, or service health from absence or a partial command.
- Do not mutate Proxmox, OPNsense, DNS, Cloudflare, services, or remote files in this workflow.
- Do not commit, push, deploy, restart, or discard unrelated local changes.

## Pitfalls

- Treating an old documentation timestamp as current evidence.
- Marking an absent guest deleted or a renamed guest unchanged.
- Recording a CT-ID-derived address without distinguishing derivation from live address evidence.
- Updating only the inventory table while leaving topology, security, aliases, or migration notes contradictory.
- Calling a target firewall policy implemented when only intent or a partial PF rule observation was collected.
- Treating a successful collector exit code as proof of fields it did not output.
- Overwriting docs directly from raw collector output and losing reviewed context.
- Mixing pre-existing user changes into the task diff or “cleaning” them up opportunistically.

## Verification

- [ ] Repository policy, status, and protected unrelated changes were inspected.
- [ ] Collector/script and affected docs were read before editing.
- [ ] Fresh authoritative read-only evidence was collected and timestamped.
- [ ] Conflicts and unknowns are visible rather than silently reconciled.
- [ ] Each documentation change traces to observed evidence or is explicitly labeled configured/inferred.
- [ ] Markdown links and `git diff --check` pass.
- [ ] No unauthorized remote or Git mutation occurred.
