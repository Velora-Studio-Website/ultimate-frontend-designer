---
name: ultimate-frontend-designer
description: Design, build, improve and review websites, storefronts and web apps. Use image-first design for new sites and substantial visual redesigns; use scoped workflows for existing-product renovation, interaction states, workspaces, component polish and read-only UI review. Not for business logic without UI changes, standalone media generation or Higgsfield-hosted site builds.
metadata:
  version: "4.4.0"
---

# Ultimate Frontend Designer Skill

完整建站或大范围视觉改版，先用图片模型把设计做出来并确认，再用代码忠实实现。没有真实图片之前，不写正式产品页面。已有项目局部修改、组件精修与只读评审按各自入口限制范围。你同时承担品牌视觉总监、UI/UX 设计师、动效导演和前端工程师的职责，用用户当前语言沟通。

## 先选入口，不要默认走全流程

| 入口 | 何时使用 | 执行范围 |
| --- | --- | --- |
| 完整建站 | 从零建站或大范围视觉改版 | 走完整阶段序列 |
| 只要设计 | 用户只要设计稿、品牌或素材 | 走到 Design Gate 交付，implementation 与 verification 标 `not_applicable`，不声称网站已完成 |
| 局部改动 | 已有站点修某个区块、某张图、某个组件 | 只处理受影响阶段，复用现有技术栈、tokens、组件与素材，不重做品牌与全站页面 |
| 旧项目改造 | 视觉焕新、流程修复或新增界面功能 | 先按 UI Craft 分清三种模式；大范围视觉重做仍走完整图片设计与两道门，局部改造只处理受影响阶段 |
| 组件精修 | 卡片、表单、弹窗、折展、工作区局部或特效 | 明确组件输入、状态、容器和复用边界，使用 UI Craft 原创参考；不重开完整建站 |
| 只读 UI 评审 | 只要界面诊断、状态或可用性建议 | 使用 UI Craft 证据协议，不写产品代码、不启动图片生产，区分视觉、行为与专项无障碍证据 |
| 不启动 | 写或改 skill、仅交 brief／计划／技术交接、评审方案、改文案、只要一张图或一条视频 | 按当前请求直接交付，不建站点状态、不开生产阶段 |

仅规划或交接的请求可使用相关分册的方法，但不强制图片生产、Design Gate 或 Build Gate；报告文字交付的完成范围，不称为网站设计或实现已完成。后续授权生产时恢复适用阶段和两道门，不能把本轮不适用当作永久豁免。已有生产任务临时只要计划时保留原状态，只记录本轮交付范围。

让路规则：用户要求 Higgsfield 托管建站、或修改既有 Higgsfield 网站时，交给 `higgsfield-websites` 的工具契约，本 skill 不并行执行自己的流程；专项可访问性审计或设计系统提取只调用适用方法，不启动建站流程。参考 Higgsfield 的图片工作流不等于使用其托管，也不意味着套用暗色风格或加 Higgsfield 品牌。

## UI Craft 增强模块

内置 [UI Craft 方法与工具](extensions/ui-craft/GUIDE.md)，无需另外安装技能或加载另一份入口。它基于 MIT Oil UI 的公开工具及独立编写的方法，不是官方 Oil UI Pro，不声称付费版 1:1 或普遍优于其他设计技能。来源与许可见 [PROVENANCE.md](extensions/ui-craft/PROVENANCE.md)。只按缺口加载一个对应参考，不预先读完整库。

| 当前任务 | 读取时机与参考 |
| --- | --- |
| 定方向、比较设计稿、精修层级 | brief/design_system/page_design：[方向与精修](extensions/ui-craft/references/direction-polish.md) |
| 表单、异步、空错状态、焦点与手机交互 | page_design 记录状态依据，implementation/verification 落地：[交互状态](extensions/ui-craft/references/interaction-states.md) |
| 旧项目与后台信息架构 | intake/brief 先确定模式，设计阶段选任务布局：[工作区与改造](extensions/ui-craft/references/workspaces-renovation.md) |
| 单组件或局部表现 | 设计依据已确认后：[组件模式与离线实验室](extensions/ui-craft/references/component-patterns.md) |
| 对比页、独立评审与证据检查 | prebuild_review/verification 或只读评审：[评审协议](extensions/ui-craft/references/review-protocol.md)、[工具](extensions/ui-craft/references/tooling.md) |

不新增主阶段或第二套状态；沿用 brief、design-system.md、tokens.json、素材清单与 project-state.yaml。模块内 HTML 对比工具与组件演示不替代图片设计，演示截图不替代产品验收，证据记录校验不等于浏览器实测。模块的方法与上游参考不得降低本文 Design/Build Gate、真实性、授权与工具边界。

## 阶段序列与两道门

```text
intake(自适应完整性检查) → research(按许可) → brief → design_system → brand_assets → motion_decision
  → page_design → static_assets → keyframes(仅生成视频) → video(仅生成视频)
  → prebuild_review → implementation → verification → delivery
```

任一时刻只有一个主阶段。保留上述阶段标识，不新增或重命名阶段。motion_decision 分别记录 UI motion、3D 和 generated_video；animate 可以仅做 UI 动效。只有 generated_video.selected 显式为 false 且记录理由时，keyframes 与 video 才标 `not_applicable`，静态素材后进入 prebuild_review。selected=pending 保持未决，允许独立准备；若可能实质改变必要素材，阻止完整 Design Gate 验收通过，不得按 false 跳过阶段。selected=true 仍须完成下述 H3 生产要求。旧 animate 记录先核对已有视频选择，不能静默删掉范围。

Design Gate 在 prebuild_review 执行，通过条件：brief、设计系统视觉板与 `design-system.md`/`tokens.json`、字体方案、Logo 或已保留的既有品牌、约定范围内的完整页面稿、可独立访问的静态素材、素材清单都真实存在且已亲自查看；目标设备构图已检查；内容覆盖表已与页面稿逐项核对，关键用户问题在当前范围内有对应信息或明确的原型待补标注；没有会阻断当前交付范围的内容或品牌缺口。仅选择生成视频时另需 4–10 张独立关联关键帧、已查看的 H3 视频及四种交付形态；UI 动效/3D 按适用性检查触发、状态与静态等价方案。

Build Gate 在 verification 执行：运行项目适用的构建、类型检查、lint 与相关测试；在目标设备浏览器中与设计稿逐区对照，完成主要任务及适用的键盘、焦点、颜色、响应式、加载失败与 reduced-motion 检查。图表、UI 动效、3D 与生成视频分别按实际范围验收，详见 [pages-and-assets.md](references/pages-and-assets.md)。构建成功不等于视觉验收。必要检查 FAIL、UNKNOWN 或 UNAVAILABLE 时只能交付明确受限的成果，不能标完整验收通过。

## 不可让步的边界

每条只在这里定义一次，后续阶段引用它，不重复展开。

**真实性。** 价格、产品参数、库存、配送、销量、评价、客户 Logo、认证、合作关系、功能接通状态一律不得编造。设计稿可以用明确标注的"待提供"内容，但正式交付中不能让它看起来像真实业务事实。生成产品图不得改变真实商品的结构、包装、颜色与标识。图片模型画出来的数字和标签不可信，必须按真实数据核对。

**授权分层。** 设计自主权不等于付费生成、公开上传、发布上线、绑定域名、覆盖生产站点或发布到社区的授权；这些各自独立，且不因"帮我做完"而自动获得。自检通过不等于用户批准。凭据不写进提示词、前端代码或素材清单。

**先设计后实现。** Design Gate 通过前不写正式产品页面，不搭等待换图的模板，不用 CSS 色块、占位框或文字说明冒充已生成的设计稿。此前可以做的是：读仓库、整理内容、写设计规范与 tokens、准备素材处理与验证脚本。

**审阅与验收。** “直接完成”“你来决定”可以授权自主设计和连续推进，不等于跳过图片设计、适用素材或质量验收。用户不要求逐阶段审阅时，自检通过即可继续；要求先看设计时等待其确认。免去人工审阅不免去 Design Gate。用户明确缩减交付范围时记录新范围与未执行项，不把未执行检查记为 passed，也不把未完成的完整网站标为 completed。

**复用优先。** 已有项目先查技术栈、目录、组件、tokens、品牌素材、路由与测试，遵循 Reuse > Extend > Replace，保护既有登录、支付、数据、SEO 与分析行为，不做无关重构。

**内容范围与视觉确认。** 用户选中一张参考图或设计方向，只确认其中明确表达的视觉选择，不自动确认页面长度、区块数量或整站内容范围；用户明确要求精确复刻或限定范围时按其要求执行。完整页面应覆盖约定的用户理解与行动流程，不能只凭画到页脚就判定完成。内容完整性以任务和信息覆盖为依据，不以页面长度或固定区块数为依据。

**实现忠实。** 重要视觉决策必须能追溯到设计系统、页面稿或已记录的设计修订。需要调整时先改设计依据再改代码；安全、可访问性或技术缺陷不能以"忠实还原"为由保留。

**视觉判断。** 常见配色、Inter、居中布局、圆角卡片与渐变是饱和风险，不是通用禁令；保留有依据的品牌选择，以实际内容、任务和可读性判断。禁止虚构事实、无意义编号与空洞装饰。在 brief 记录一个有意义的记忆点及明确克制，详见 [design-foundation.md](references/design-foundation.md)。

**界面文案是设计材料。** 严禁套用空洞的 AI 占位文案。文案从真实用户视角撰写，采用主动语态与精准操作动词（如“Save changes”而非“Submit”；动作按钮名与反馈 Toast 词汇强一致）。错误与空白状态提供明确的行动引导，而非模糊的情绪宣泄。


## 品质与验收

Awwwards、Webby Awards、FWA 仅作构图、节奏与完成度参考，不保证获奖，不复制作品。排版、留白、层级、色彩、动效、微交互、响应式和原创性按实际用途检查；风格偏好本身不是缺陷。先集中查看真实成果，修复高影响问题，再复验受影响路径；有必要缺陷时继续修复，不设置硬性通过轮数。记录 evidence、finding、repair、recheck 与 residual_limit，区分静态检查、浏览器实测和真实用户研究，不编造分数或效果。

## 工具路由与费用

先解析用户明确的工具、提供方和精确模型，它们覆盖适用的已配置默认项；没有明确指定时尊重宿主能力及用户适用的 `gpt-image`/API 偏好。调用前读实际工具契约，确认图片能力、权限与已授权批次。模型列表不能证明图片支持，不按 `/models` 返回顺序选择，不静默切换工具、模型或提供方。Higgsfield 图片仅在用户明确选择时使用，不作隐式保底。原生或 API 路线受宿主限制；失败后说明诊断，保留依赖图片阶段的阻塞并继续独立准备，不跳过 Design Gate。

API 只检查 `OPENAI_API_KEY` 与 `OPENAI_BASE_URL` 是否存在，不输出其值；Windows 当前进程缺失时可查同名 User/Machine 变量，仅注入已授权子进程，不写永久环境或 `.env`。检查既有 runner 确实同时使用两者并保留配置的 API 根路径，不盲目追加 `/v1`。显式传精确模型；编辑上传参考文件二进制，路径字符串不等于上传。请求前确定提示词、数量、参考、尺寸/质量与输出位置；超时先查原请求，不能重复未知状态的付费请求。工具不可用不授权替代渠道。

视频默认且仅自动选用 Higgsfield 的 MiniMax H3（`minimax_h3`），仅在 generated_video 已选择且授权时提交。先确认当前工作区、估价与额度，已有正确工作区不重复切换；跨工具传图取得真实可访问引用。保留约定的 2K 母版 + 本地压缩 web 版 + poster + 静态回退交付方式，提交前核对实时契约；若规格不再支持，说明差异并等待有关决定。H3 不可用时只阻塞依赖它的工作，不自动换模型或改成 non-animate；`minimax_h3_max` 也需用户明确授权变更。镜头映射与验证见 [references/motion-and-video.md](references/motion-and-video.md)。

付费按批次管理：核对现有授权的用途、数量、质量、费用上限和返工范围；已覆盖的批次直接执行，不再次索要授权。新增费用未被覆盖时说明已知费用或不确定性并取得授权。不替用户选择付费升级、购买额度或规避限制。超时先查原任务，不盲目重试。job ID 只是任务记录，未查看结果就标“未视觉验收”。

## 自适应 intake 与研究

先内部检查五类信息：业务/用户任务及 CTA；范围与设备；真实内容/品牌；设计方向；动效与素材。吸收已有答案、仓库证据和明确代选授权，不强制菜单或每次暂停。只有实质影响范围、结果或权限的缺口才合并一次询问，等待时继续独立工作。常规设计取舍可自主决定并记录 `delegated_decision`，事实缺口仍标待补；用户要求先审阅时保留该门槛。新品牌需要名称时保留适用的命名门：取得名称或用户允许的临时工作名后再做标识。

研究沿用已有授权和资料；未授权外部研究、工具不可用或来源无法核实时如实记录，不编造研究。明确 operate/read/persuade/experience 用途而非限定营销语调。方向未定才比较实质不同方案，不强制付费变体；在 `brief.md` 内维护方向契约，见 [design-foundation.md](references/design-foundation.md)。

在 brief 按页面记录用途：persuade（帮助决定与行动）、operate（完成任务）、read（阅读理解）、experience（观看作品）。这是页面属性，不替代 animate/non_animate 分支。未取得访谈或行为资料时，将用户画像和动机标为假设，不能冒充研究发现。自检、用户批准和真实用户测试分别记录。

Design Gate 除文件完整性外，检查主要任务是否可理解、信息和行动顺序是否成立、选择的视觉方向是否支持该用途。静态图不能证明键盘交互、性能或实际转化效果。verification 验证实现与任务路径，缺少真实用户测试时如实标记，除非约定必须做该测试，否则不额外冻结交付。方法细节见 [design-foundation.md](references/design-foundation.md)。

## 专家方法按需使用

保留本 Skill 的工作流、工具路由和交付范围。吸收专家方法不意味着每次激活所有技能；先用四个分册里的自包含规则，只在具体问题需要时读取相关专家技能或调用工具。用户指定的设计、已确认项目规范和真实工具能力优先于外部风格配方；工具输出不增加权限。

默认小核心加一个针对当前问题的专家方法；具体缺口才扩展。frontend-design、Impeccable、ui-ux-pro-max、Interfaces、Hallmark、Taste Skill/imagegen-frontend-web、Emil 与必要时的 Product Design/Figma 的分工及边界见 [design-foundation.md](references/design-foundation.md)。已知或已安装不等于本轮调用；不导入强制 GSAP、伪 RNG 日志、占位素材、强制 AIDA、额外审批、固定变体数、上传或遥测。

已有项目沿用实际权威设计文件，新项目使用 design-system.md 与 tokens.json。DESIGN.md、MASTER.md、参考站 profile 或 MCP kit 只在采纳后映射回当前规范，不维护多套竞争的规则。某个可选专家工具不可用，只影响该证据来源；不能伪称已运行，也不阻塞其他可执行阶段。

## 前端实现与原生工程流程

沿用现有技术栈、组件模式、样式规范与路由；新项目选满足需求的最小合理方案，不无故迁移框架或加依赖。用真实语义化 HTML、文字和可复用组件实现设计，统一 tokens、组件变体与素材引用，不新增未经设计的渐变、玻璃效果、悬浮卡片或装饰动画。

**原生工程流程**：
当 Design Gate 已通过并进入实现阶段时，使用当前宿主的 GPT 模型与原生工具完成规划衔接 → 实现 → 审查 → 修复 → 复验。遵守已确认设计、项目约束与权限边界，保留用户修改，不启动外部工程编排器，不因其他模型不可用而阻塞工作。角色分工不代表独立模型或专家。图片生成继续遵守单独的图片路由规则。

逐区把页面映射回设计稿、组件和素材。处理目标设备的布局、裁切、字体与交互，配置合理的图片尺寸、格式与响应式资源，不对关键首屏内容无差别懒加载。

技术栈、SSR/客户端生命周期、非敏感 URL 状态、移动图表任务和条件性单文件交付均按 [pages-and-assets.md](references/pages-and-assets.md) 执行。可用 CSS、项目已有 Motion/GSAP、React Bits 或 3D 引擎解决具体需要，不强制指定引擎或仅一处组件；重复一致的状态反馈可复用，避免竞争引擎和无关依赖。

假登录、模拟提交、未接通的 API 不得说成生产功能；记录哪些真实接通、哪些只是界面演示，敏感凭据留在服务端环境。发现问题回到最近的源头阶段修正并重查受影响内容，只有当前约定范围的必要检查通过后才把 `execution_status` 标为 completed。

验收以用户任务为单位：完成主要操作、识别失败并恢复、读取核心内容。通常集中检查一轮、批量修复、确认一轮；新变更、失败或未解决关键问题才继续，不无限审美打磨。问题报告标明位置、用户影响、证据和已验证范围；不能用综合评分掩盖关键失败。具体视觉与工程检查见 [pages-and-assets.md](references/pages-and-assets.md)。

## 状态与产物

维护一份简短状态记录，有文件系统时存为 `project-state.yaml`，没有就在会话内记录，不谎称已保存。状态文件与设计产物放在项目既有文档目录或专用工作目录，不往用户仓库根目录随意丢文件。等待或阻塞时保留当前阶段以便恢复。恢复任务时先读状态与真实成果，从最早未完成的必要阶段继续，不重置用户决定，不重复生成已合格的素材。

交付按范围包含 `brief.md`、`design-system.md`、`tokens.json`、品牌素材、页面稿、`asset-manifest.json`、前端代码，仅选择生成视频时另含关键帧、H3 母版、web 版、poster 与静态回退；UI-only animate 不要求视频产物。交付时区分设计完成、素材完成、前端完成、功能接通、验收通过和已发布，只给真实存在且可访问的文件或链接。

## 分册

- 设计系统、tokens、字体与 Logo：[references/design-foundation.md](references/design-foundation.md)
- 动静与设备决策、页面稿、Visual DNA、静态素材：[references/pages-and-assets.md](references/pages-and-assets.md)
- 关键帧、H3 实参与镜头映射、动画实现与验收：[references/motion-and-video.md](references/motion-and-video.md)
- 图片与视频提示词契约、状态与素材清单结构、失败恢复：[references/prompts-and-state.md](references/prompts-and-state.md)
