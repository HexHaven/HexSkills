# Proxmox and OPNsense Evidence Matrix

Use this reference when refreshing NyxCloud-style infrastructure documentation. It is a compact workflow aid, not a substitute for repository-local policy.

## Collection targets

| Claim | Preferred read-only evidence | What it establishes | What it does not establish |
|---|---|---|---|
| Guest exists and status | `pct list`, `qm list` on `voidforge` | Current LXC/VM roster and runtime status | Deletion, backup, exposure, or service health |
| LXC identity and controls | `pct config <CTID>` | Hostname, `net0`, MAC, VLAN tag, firewall flag, protection, unprivileged flag | DHCP lease or application role beyond configured labels |
| VM identity and controls | `qm config <VMID>` | Name, network, MAC, VLAN tag, agent, protection, tags | Guest OS health unless agent output is returned |
| Guest IP | QEMU guest-agent output or ARP/DHCP evidence from `voidgate` | Current address mapping when directly returned | Future reservation, DNS correctness, or reachability of every service |
| Routed VLANs | `ifconfig` on `voidgate` | Active interface names, descriptions, VLAN IDs, gateway addresses | Complete policy intent |
| Firewall flow | `pfctl -sr` on `voidgate` | Current loaded PF rule matching the exact source/destination/protocol/port | Proxmox guest-firewall rules or application-level authorization |

## Reconciliation checklist

1. Capture the collector-generated timestamp.
2. Enumerate live CT/VM IDs exactly; compare programmatically or line-by-line with the documentation.
3. For each current guest, compare hostname, IP, MAC, VLAN/tag, status, `firewall=1`, `protection: 1`, and `unprivileged: 1`.
4. Move absent documented guests to a migration/disposition section; do not call them deleted without independent evidence.
5. Treat a changed hostname or reused CT-ID as a possible repurpose. Record the new observed identity and mark role/alias ownership unknown if not directly verified.
6. Cross-check DHCP-assigned addresses with a narrow gateway ARP/DHCP read when the collector only reports `ip=dhcp`.
7. For security claims, copy only exact PF evidence and preserve source, destination, protocol, port, purpose, owner, and validation date.
8. Search all affected docs for the old timestamp, old identity, and stale status wording after patching.
9. Validate links and whitespace, then report unresolved fields explicitly.

## Interpretation rules

- CT-ID/address schema is a consistency check, not live proof of address assignment.
- A `firewall=1` guest NIC flag proves Proxmox firewall support is enabled, not that a desired guest rule exists.
- An observed OPNsense PF rule proves the loaded rule exists, not that the application is healthy end-to-end.
- A successful SSH session proves target reachability and command execution only for the returned command.
- Raw output belongs in transient evidence or an explicitly requested fleeting note, not in canonical docs by default.
