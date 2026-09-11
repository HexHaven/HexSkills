# Hex Media Skills

Hermes-native procedures for producing media artifacts (images, and later audio/video) with local, on-box tooling.

## Skills

| Skill | Owns | Workflow |
|---|---|---|
| `hex-image` | Local text-to-image generation via the `bonsai-image` CLI (Bonsai Image binary 4B, 1-bit, gemlite/CUDA) | `backend status → start if needed → bonsai-image → show MEDIA: path` |

## Prerequisites

`hex-image` assumes the Bonsai Image install and its two CLIs (`bonsai-image`, `bonsai-backend`) are present on `$PATH`, plus an NVIDIA GPU with ≥6 GiB VRAM free. Install/uninstall, layout, and troubleshooting are documented at the install itself (`~/Forge/Repositories/upstream/Bonsai-Image-Demo/AGENTS.md`), not duplicated here.

## Location and activation

Install via a Hermes external skill directory or GitHub tap — see the [HexSkills repo README](../README.md).
