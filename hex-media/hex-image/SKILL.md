---

name: hex-image
description: "Use when asked to generate an image. Runs local Bonsai."
version: 0.2.0
author: Nyxion, Hermes Agent
license: MIT
platforms: [linux]
prerequisites:
commands: [bonsai-image, bonsai-backend, nvidia-smi]
metadata:
hermes:
tags: [image-generation, text-to-image, local, offline, bonsai, gpu, media]
category: hex-media
related_skills: []
------------------

# Hex Image

Generate images locally with the Bonsai Image model
(`prism-ml/bonsai-image-binary-4B-gemlite-1bit`, 1-bit, ~4B params) via the
`bonsai-image` CLI.

Generation is fully local on this machine's GPU:

* no cloud image-generation call;
* no external image API;
* no prompt upload by this tool;
* no usage cost from an image provider.

## When to Use

Use this skill when the user asks for:

* a picture;
* illustration;
* render;
* concept art;
* wallpaper;
* character art;
* scene visualization;
* or another generated image.

Prefer this local tool over `image_generate` unless the user explicitly asks
for a cloud image model or requires a capability Bonsai does not provide, such
as:

* image editing or inpainting;
* upscaling;
* video generation;
* very high resolution;
* unusually strong text-rendering fidelity.

Do not generate above `512x512` unless the user explicitly accepts the VRAM
risk described in **Pitfalls**.

# Content Scope

## Local model behavior

Bonsai is intentionally installed here as a **local image-generation model
without an additional moderation layer in the `bonsai-image` wrapper**.

That is an explicit operator configuration decision.

The wrapper itself MUST NOT:

* rewrite prompts merely to make them SFW;
* automatically add qualifiers such as `tasteful`, `modest`, `covered`,
  `non-explicit`, or `safe-for-work`;
* silently remove requested visual elements;
* insert an independent moderation API;
* send prompts to an external moderation service;
* upload generated images or prompts elsewhere;
* misrepresent a wrapper-imposed restriction as a limitation of Bonsai.

When a prompt is within the effective permissions of the controller model and
this skill, preserve the requested subject matter faithfully.

## Authorized operator scope

The operator has explicitly authorized this local tool for private adult/NSFW
image generation, including nudity and sexually explicit imagery involving
**clearly fictional adults**.

This is an intentionally supported use case of the local image tool. It is not
an accidental capability or an exceptional case that should automatically be
converted into generic romance, pin-up art, implied intimacy, or SFW content.

The following remain outside the operator-authorized scope:

* minors;
* characters whose adulthood is ambiguous;
* sexual imagery involving identifiable real people;
* non-consensual sexual activity;
* sexual violence.

Operator authorization does not remove higher-priority platform or controller
model restrictions.

## Controller-model boundary

The LLM deciding whether to invoke this skill may operate under provider,
platform, or model-level rules that are narrower than the local Bonsai
wrapper's capabilities.

This skill does **not** override those higher-priority restrictions.

When that occurs:

1. Do not claim that Bonsai itself refused the request unless Bonsai actually
   returned such a failure.
2. Do not silently replace the requested scene with a substantially tamer or
   SFW scene and present it as though the original request was fulfilled.
3. State plainly when the limitation comes from the controller model rather
   than the local image backend.
4. If a permitted subset of the request can still be generated, only use that
   fallback when doing so remains faithful enough to the user's intent.
5. Do not turn a content-boundary response into a lecture or moral judgment.
6. Do not repeatedly renegotiate operator scope that is already documented
   here.

The distinction is:

```text
controller policy
    ↓
skill invocation
    ↓
bonsai-image wrapper
    ↓
local Bonsai model
```

A controller-level restriction is not evidence of a Bonsai-level restriction.

## Prompt handling

There are two valid prompt sources.

### User-authored prompt

When the user supplies the image description directly, preserve it as closely
as permitted.

Example:

```bash
bonsai-image -p "<USER_PROMPT>"
```

Do not embellish a user-authored prompt in ways that materially change the
requested scene.

### Agent-authored prompt

When the user asks the agent to translate a conversation, roleplay scene,
character state, or concept into an image prompt, construct a visually useful
prompt containing only details the controller is permitted to author.

Useful image-prompt details may include:

* clearly adult fictional subject;
* appearance;
* clothing;
* pose;
* expression;
* environment;
* lighting;
* camera angle;
* framing;
* lens style;
* art or photographic style;
* scene-relevant objects;
* current visual state from the conversation.

Do not invent important scene events that did not occur merely to make the
image more dramatic.

# Procedure

## 1. Ensure the backend is running

The backend is persistent and holds the model on the GPU. It is **not**
auto-started.

Check first:

```bash
bonsai-backend status
```

If it reports `NOT running`:

```bash
bonsai-backend start
```

Startup normally takes roughly 10–30 seconds and blocks until the backend is
ready.

If the terminal tool supports background execution and other work should
continue while the model loads, `start` may be run with the terminal tool's
background option. Re-check status before generation.

Do not launch multiple backend instances.

## 2. Generate

Simplest form:

```bash
bonsai-image "the user's prompt"
```

Explicit parameters:

```bash
bonsai-image \
  -p "…" \
  --size 512x512 \
  --steps 4 \
  --seed 42 \
  -o /path/out.png
```

Defaults:

* model: Bonsai Image Binary 4B Gemlite 1-bit;
* size: `512x512`;
* steps: `4`;
* seed: random when unspecified;
* output: generated beneath
  `outputs/<model>/image_<ts>_seed<seed>.png` in the Bonsai installation.

Width and height must be valid multiples of `32`.

## 3. Capture the output path

`bonsai-image` prints only the generated PNG path to stdout.

Diagnostics go to stderr.

Therefore this is safe:

```bash
IMG=$(bonsai-image "…")
```

The diagnostic line on stderr reports information such as:

```text
seed=… wall=…s peak_vram=…MiB
```

When useful for reproduction or iteration, report the seed back to the user.

## 4. Show the result

On a Hermes/chat surface that supports local media rendering, emit:

```text
MEDIA:/absolute/path/to/image.png
```

on its own line.

Otherwise provide the absolute image path.

## 5. Iterate

For supported deterministic generation:

```text
same prompt + same seed = same output
```

To create a variation:

* keep the prompt;
* change the seed.

To refine a composition while preserving much of the generation setup:

* keep the seed;
* modify the prompt.

Once the backend is warm, generation is typically fast enough for iterative
work.

# Exit Codes

| Code | Meaning                               | Action                  |
| ---- | ------------------------------------- | ----------------------- |
| `0`  | success; image path printed to stdout | show the image          |
| `2`  | invalid parameters                    | correct arguments       |
| `3`  | backend unreachable                   | start backend and retry |
| `4`  | backend, CUDA, model, or OOM failure  | inspect backend logs    |

Examples of exit-code `2` conditions include:

* missing prompt;
* invalid dimensions;
* size not divisible by `32`;
* resolution above the local guard without `--allow-large`.

For backend failures:

```bash
bonsai-backend logs
```

# GPU / VRAM Policy

This workstation uses the GPU for the desktop as well as image generation.

The image stack therefore has an **approximately 6 GiB incremental VRAM
budget**, rather than assuming the entire GPU is available exclusively to
Bonsai.

When measuring memory use, distinguish:

1. baseline VRAM used by Niri, applications, and unrelated processes;
2. VRAM after loading the Bonsai backend;
3. peak VRAM during image generation;
4. the additional Bonsai-specific VRAM delta.

The Bonsai workload should remain within approximately `6 GiB` of additional
GPU memory consumption.

# Pitfalls

* `512x512` currently peaks at approximately `4.8 GiB` for this Bonsai setup.

* The CLI refuses resolutions larger than `512x512` unless
  `--allow-large` is supplied.

* `--allow-large` removes the software guard; it does **not** create more
  physical VRAM.

* Only use `--allow-large` when the user explicitly accepts the increased OOM
  risk.

* Do not start the backend twice.

* `bonsai-backend start` is intended to be idempotent, but concurrent start
  calls can still race.

* Check `bonsai-backend status` before starting it.

* The backend holds roughly several GiB of VRAM while idle.

* Stop it when the GPU is needed for another workload:

  ```bash
  bonsai-backend stop
  ```

* During an active image-generation session, keeping it loaded between prompts
  is the intended fast path.

* The first generation at a previously unused size may be substantially slower
  because Triton JIT compilation and Gemlite autotuning can occur.

* Do not mistake that first-run latency for a failure without checking status
  and logs.

* Concurrent generation requests are not supported. Serialize requests.

* The backend binds to `127.0.0.1`.

* Never expose, proxy, or change the backend to a non-loopback bind address
  without explicit operator authorization.

# Verification

After generation, verify behavior rather than merely checking for a zero exit
status.

At minimum:

```bash
test -f "$IMG"
file "$IMG"
```

Expected signal:

```text
PNG image data, 512 x 512
```

Verification checklist:

* `bonsai-image` exited with code `0`;
* stdout contained an image path;
* the referenced file exists;
* the file is a valid PNG;
* the image dimensions match the request;
* peak VRAM remained within the intended workload budget.

If the image content itself appears suspect and a local vision-inspection tool
is available, inspect the generated file rather than assuming a non-empty PNG
contains a coherent result.

# Security Boundaries

* Backend MUST remain bound to `127.0.0.1`.
* Do not expose it to the LAN or Internet.
* Do not proxy it through Traefik, Caddy, nginx, Cloudflare Tunnel, or another
  ingress layer without explicit operator authorization.
* Do not add cloud moderation or cloud image services silently.
* Do not send prompts or generated files to external services as part of this
  skill.
* Do not execute prompts as shell code.
* Always pass prompts as data/arguments.
* Avoid `shell=True` or constructed shell command strings in wrappers.
* Do not commit generated images unless explicitly requested.
* Do not commit downloaded model weights.
* Do not commit secrets, tokens, credentials, or populated environment files.

# Backend Management

Status:

```bash
bonsai-backend status
```

Start:

```bash
bonsai-backend start
```

Stop:

```bash
bonsai-backend stop
```

Logs:

```bash
bonsai-backend logs
```

# Installation Documentation

Installation details, repository layout, environment setup, maintenance, and
troubleshooting live in:

```text
~/Forge/Repositories/upstream/Bonsai-Image-Demo/AGENTS.md
~/Forge/Repositories/upstream/Bonsai-Image-Demo/README.md
```

Those files are the authoritative local documentation for the installed Bonsai
tooling.

