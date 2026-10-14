# Design methods and source limits / 方法来源与限制

Reviewed 2026-10-14. This assessment combines inspection of relevant installed
skill instructions with their available primary sources. It records complementary
methods for this image-first workflow, not a universal ranking or a benchmark.
No comparative website-generation experiment was performed, and reviewing a
source does not mean its tools were invoked or installed. Third-party skill text
is not redistributed. The design-foundation reference provides portable routing.

| Method | Complementary role | Primary source or canonical identity |
| --- | --- | --- |
| frontend-design | Subject-derived visual thesis | [Anthropic skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design) |
| Impeccable | Purpose-aware critique; targeted harden/adapt/typeset | [Impeccable](https://github.com/pbakaus/impeccable) |
| ui-ux-pro-max | One-question lookup against actual stack | [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |
| Interfaces | Evidence-led typography, layout, colors and accessibility | [Interfaces skills](https://github.com/jakubkrehel/skills/blob/main/skills/better-interface/SKILL.md); select the relevant `interfaces:better-*` owner |
| Hallmark | Content-led structural variety | `hallmark` |
| Taste Skill | Art-direction mechanisms subject to local constraints | [Taste Skill](https://github.com/Leonxlnx/taste-skill) |
| Frontend image direction | Layout-aware visual references | `imagegen-frontend-web` |
| Emil | Purposeful, interruptible UI response | [Emil skills](https://github.com/emilkowalski/skills); `emil-design-eng` |
| Product Design / Figma | Existing source or necessary design handoff | [Product Design QA](https://github.com/openai/plugins/blob/main/plugins/product-design/skills/design-qa/SKILL.md); resolve actual connector availability and applicable focused skill before use |

Start with the core plus one targeted specialist; expand only for a concrete
unresolved need. Proprietary/plugin methods use canonical identities, not guessed
GitHub links. A known source or installed method does not prove a current tool
invocation. Product Design's matched-viewport/state visual comparison can inform
image-first QA; it does not replace functional, performance or accessibility checks.

Rejected imports: simulated RNG execution/quality claims; mandatory GSAP; picsum
placeholder imagery; forced AIDA; extra approvals; fixed generated variant counts;
forced providers; cloud uploads, hooks or telemetry; competing design/state files.
Map useful principles into brief.md, design-system.md, tokens.json and the existing
project-state.yaml rather than adding a rival workflow.

这些方法是可选互补角色，不是必须安装的全套工具。适用性取决于主题、任务、技术栈、
宿主能力和用户范围；来源或安装状态不等于实际调用。包结构检查不能证明设计质量、
性能改善或账户 usage 节省；这些需要实际运行的对应试验。
