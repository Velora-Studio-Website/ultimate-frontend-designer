# Ultimate Frontend Designer

<p align="center">
  <img src="assets/ultimate-designer-logo.svg" alt="Ultimate Designer Skill logo" width="200">
</p>

**Plan the content. Design with images. Build what was designed. Verify the result.**

[English](README.md) · [简体中文](README.zh-CN.md) · [Quick-start prompts](examples/prompts.md) · [ChatGPT project setup](docs/chatgpt-project.md)

A community-built, image-first frontend design skill for **Codex and compatible ChatGPT workflows**. It combines design thinking, brand direction, UI/UX, asset planning and frontend delivery into one staged workflow.

Version **4.3.0** adds adaptive intake, explicit image/API routing, UI-only Animate, optional specialist composition and deterministic package regressions. “Ultimate” is the project name, not a benchmark claim or an OpenAI endorsement.

## What it helps you create

- Product and ecommerce websites that answer customer questions before asking for a purchase.
- Landing pages and brand websites with a coherent visual system and independent image assets.
- Web-app interfaces designed around actual tasks and necessary states.
- Design-only deliverables, or a complete frontend when the host provides development tools.
- Optional video-led experiences through the Animate branch.

Small fixes stay small. A copy edit, standalone image request or UI audit does not trigger a full website rebuild. Existing code, components and valid behavior are reused first.

## Start here

### Codex: install the standalone skill

In Codex, ask its built-in installer:

```text
$skill-installer install the skill at
https://github.com/Velora-Studio-Website/ultimate-frontend-designer/tree/main/skills/ultimate-frontend-designer
```

Then start a task with:

```text
Use $ultimate-frontend-designer to build a responsive ecommerce website
for the product images I attached. Use Non-Animate mode and keep it local.
First map the customer questions and missing information, then create the
complete image-based design. Show me the design before implementation.
Do not invent prices, specifications, reviews or shipping policies.
```

If the skill does not appear, refresh or restart your client. Ask the installer to inspect an existing installation before updating it; do not install duplicate copies under different discovery paths. See the [official skills guide](https://developers.openai.com/codex/skills).

Manual alternative: download this repository and copy the **entire** `skills/ultimate-frontend-designer/` directory into a skill location supported by your client. Current Codex documentation lists `~/.agents/skills/` for user skills and `.agents/skills/` for repository skills; the bundled installer may use its configured `$CODEX_HOME/skills` location. Keep all four reference files beside `SKILL.md`.

### ChatGPT: choose the supported route

**Native skill/plugin support available:** use your client's supported skill or plugin installation flow, then select the installed skill. This repo includes a portable `plugin.json` and a `.codex-plugin/plugin.json` compatibility manifest. Publishing on GitHub does **not** automatically list it in OpenAI's plugin directory. Client features, account access and workspace policies still apply. See [plugin packaging](https://developers.openai.com/plugins/build/plugins).

**Project-reference fallback:** upload `SKILL.md` and the four `references/*.md` files to a ChatGPT Project, then paste the instructions in [ChatGPT project setup](docs/chatgpt-project.md). These files guide the conversation; uploading them does not install tools, authenticate Higgsfield or grant filesystem/deployment access. Projects support files and project instructions; see [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt).

For end-to-end code delivery, use a workspace-enabled environment with file, shell and browser tools. In a chat-only environment, request design and handoff artifacts within the tools actually available.

## Requirements

The package itself is instructions: **no Node.js, Python, API key or paid subscription is needed merely to read it.** Execution requirements depend on the requested work.

| Capability | When needed | What to provide |
| --- | --- | --- |
| Agent that can read skill/reference files | All modes | Codex or a compatible host; readable project files |
| Image generation and visual inspection | Image-first design | Host-supported native or configured API tools; Higgsfield only by explicit choice |
| File editing, shell and project runtime | Frontend implementation | A writable workspace and the actual project's dependencies |
| Browser inspection | Visual and interaction verification | A browser tool accessible to the agent |
| Higgsfield + `minimax_h3` | Selected generated video only | Working integration, current model availability and authorized budget |
| Video inspection and transcoding | Generated-video delivery | Playback/frame inspection and a local encoder such as FFmpeg |

Explicit tool, provider and exact model override applicable configured defaults, including a user’s gpt-image/API preference. Verify host capabilities and permissions; model lists do not establish image support. No first-model selection, silent provider/model fallback or automatic Higgsfield image fallback. Check only the existence of OPENAI_API_KEY and OPENAI_BASE_URL, never their values; User/Machine fallback is process-only. Runners must honor both variables and preserve the API root without blindly appending /v1; do not change persistent variables or .env files. Inspect ambiguous paid timeouts before resubmission. Image-stage failure blocks dependent work, while independent preparation continues.

Video parameters must be checked against the live tool contract before submission. The reference chapter includes a historical H3 parameter snapshot, not a guarantee of current service availability. No automatic substitution with another video model. Non-Animate requires no H3 integration and still includes image design and normal interactive controls.

Referenced expert skills and Product Design are **optional**, not an installation checklist. This package does not bundle their tools, source files, credentials or subscriptions.

## The workflow

```text
Intake → optional research → brief → design system → brand assets
→ motion decision → page design → static assets
→ [Selected generated video only: keyframes → video]
→ Design Gate → implementation → verification → delivery
```

| Mode | Includes | Does not imply |
| --- | --- | --- |
| Non-Animate | Complete image-based design, independent still assets, responsive frontend, usable controls | Decorative motion, autoplay or video generation |
| Animate | Static foundation and selected UI motion/3D; only selected video adds 4–10 independent keyframes and authorized H3 master/web/poster/static | Video authorization, unlimited spend or model substitution |
| Design only | Agreed design and asset deliverables | Code, checkout or deployment completion |
| Local fix | Only affected stages | A new brand system or unrelated refactor |

Intake internally checks task/CTA, scope/devices, real content/brand, direction and motion/assets. Reuse supplied answers and delegated decisions; bundle only material gaps. Retain requested review and applicable naming gates. UI-only Animate marks keyframes/video not_applicable with reasons; do not silently remove previously selected video scope. The original phase sequence is preserved. Content planning happens inside the existing brief/page-design phases; it is not an extra mandatory approval loop.

## Content completeness before pictures

For each important user question, record:

| User question | Required information | Page or section | Evidence/status |
| --- | --- | --- | --- |
| What is this product for? | Confirmed purpose and suitable uses | Overview/use cases | Merchant-provided facts |
| Will it fit my needs? | Relevant specifications and limitations | Details/specifications | Pending until verified |
| What will I receive? | Confirmed package contents | What's included | Pending until verified |
| What happens after purchase? | Price, delivery and returns | Purchase/FAQ/policy page | Real merchant policy |

This is a mapping method, not a requirement for four sections or a long page. Merge sections when useful. Respect explicitly requested short pages and exact reproductions. Missing facts remain marked as missing; they do not justify invented claims or silently deleting the information architecture.

For long pages, generate an overall view plus readable sectional designs. A single short image must not become the accidental limit of the website. Selecting a visual direction and approving information scope are separate decisions.

## Two quality gates

**Design Gate:** brief and content coverage, a real generated visual system, design tokens, usable typography/brand assets, complete page designs, independent assets and target-device compositions. Selected generated video adds reviewed keyframes/video and four delivery forms; UI-only Animate checks UI states and fallbacks without H3. File existence alone does not establish quality or user approval.

**Build Gate:** appropriate project checks plus actual browser inspection, comparison with the design, responsive layout, task paths, keyboard/focus behavior and media failures. Report unavailable checks; unresolved mandatory checks prevent full acceptance. A successful build does not prove visual accuracy, and a static mockup does not prove usability or conversion.

## Typical deliverables

`brief.md`, `design-system.md`, `tokens.json`, page designs, standalone assets, `asset-manifest.json`, `project-state.yaml`, and frontend code when requested. Only selected generated video additionally includes the agreed video master, web-compressed version, poster and static fallback.

Keep generation status, visual QA and user approval separate. Local prototype, working frontend, connected commerce and deployed site are different delivery states.

## Give the agent a useful brief

Provide the website's purpose, audience, desired action, original product/brand assets, confirmed facts, existing codebase, target devices, mode and review preference. Include budget limits when generation may incur charges. “I don't know—propose a direction” is a valid answer for design decisions, not permission to fabricate business facts.

Use [the bilingual prompts](examples/prompts.md) for a static store, design-only work or an animated site. The skill follows your conversation language; its canonical instruction files currently use Chinese with English identifiers, while this README and the examples support both languages.

## Repository layout

```text
plugin.json                         Portable plugin metadata
.codex-plugin/plugin.json           Codex compatibility metadata
skills/ultimate-frontend-designer/
  SKILL.md                          Canonical workflow and rules
  agents/openai.yaml                Skill display metadata
  references/
    design-foundation.md            Design thinking and visual system
    pages-and-assets.md             Content coverage, pages and assets
    motion-and-video.md             Keyframes, H3 and motion delivery
    prompts-and-state.md            Prompt contracts and state schemas
docs/chatgpt-project.md              ChatGPT fallback setup, EN/ZH
examples/prompts.md                  Copyable prompts, EN/ZH
scripts/validate.py                 Offline package checks
```

## Validation and contributing

Run the following with Python 3.10+ for package integrity and mutation regressions:

```text
python -X utf8 scripts/validate.py
python -X utf8 -m unittest discover -s tests -p "test_*.py" -v
python -O -X utf8 scripts/validate.py
```

The stdlib validator checks strict UTF-8/no entrypoint BOM, bounded metadata, semantic versions, aligned manifests, four references, local Markdown targets and distributable text hygiene including Python/YAML/JSON. It scans tracked files plus declared new package files, excluding work/cache; unpacked copies use bounded package directories. Diagnostics do not echo credential values. Python is for this optional maintainer check, not for using the instructions. These checks do not simulate an agent, generate images or certify compatibility with every host.

When reporting an issue, include the host, skill version, requested scope, expected/observed behavior and a redacted reproduction. Improvements should preserve the original workflow, avoid duplicated rules, keep the English/Chinese documentation aligned and add no silent spending or publishing permissions.

See [assessed methods and source limits](docs/design-skill-sources.md). Start with the core plus one targeted specialist; expand only for a concrete need. Known or installed methods do not prove invocation. Third-party skills are not redistributed. OpenAI, Codex, ChatGPT, Higgsfield and MiniMax names identify their respective products, not sponsorship. This repository publishes the reusable workflow only; private project files and the example product's media are not included.

## License

No open-source license has been selected for this initial publication. Public visibility alone does not grant a general reuse license. A license can be added by the maintainer later. Third-party services, models and user-supplied assets remain subject to their own terms.
