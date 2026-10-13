---
name: ultimate-frontend-designer
description: Design a website with generated images first, then implement it in code. Use when building or substantially redesigning a website, landing page, product page, ecommerce storefront, or web app whose visual direction, brand assets, or imagery must be designed before implementation. Not for small UI fixes, standalone image or video requests, UI review or accessibility audits, or Higgsfield-hosted site builds.
metadata:
  version: "4.2.0"
---

# Ultimate Frontend Designer Skill

先用图片模型把设计做出来并确认，再用代码忠实实现。没有真实图片之前，不写正式产品页面。你同时承担品牌视觉总监、UI/UX 设计师、动效导演和前端工程师的职责，用用户当前语言沟通。

## 先选入口，不要默认走全流程

| 入口 | 何时使用 | 执行范围 |
| --- | --- | --- |
| 完整建站 | 从零建站或大范围视觉改版 | 走完整阶段序列 |
| 只要设计 | 用户只要设计稿、品牌或素材 | 走到 Design Gate 交付，implementation 与 verification 标 `not_applicable`，不声称网站已完成 |
| 局部改动 | 已有站点修某个区块、某张图、某个组件 | 只处理受影响阶段，复用现有技术栈、tokens、组件与素材，不重做品牌与全站页面 |
| 不启动 | 写或改 skill、评审方案、改文案、只要一张图或一条视频 | 按普通请求直接处理，不建状态、不开阶段 |

让路规则：用户要求 Higgsfield 托管建站、或修改既有 Higgsfield 网站时，交给 `higgsfield-websites` 的工具契约，本 skill 不并行执行自己的流程；请求只是 UI/UX 审查、可访问性检查或设计系统提取时，不启动本流程。参考 Higgsfield 的图片工作流不等于使用其托管，也不意味着套用暗色风格或加 Higgsfield 品牌。

## 阶段序列与两道门

```text
intake(强制问卷对齐) → research(按许可) → brief → design_system → brand_assets → motion_decision
  → page_design → static_assets → keyframes(仅 animate) → video(仅 animate)
  → prebuild_review → implementation → verification → delivery
```

任一时刻只有一个主阶段。non-animate 把 keyframes 与 video 标 `not_applicable` 并直接进 prebuild_review，H3 可用性不作为其放行条件。`not_applicable` 必须写明理由，它不等于"已完成"。

工作流改进说明（融入数据可视化与 React Bits，保持原有 13 阶段与 2 道门绝对稳定）：
- 包含数据图表/仪表盘/系统架构图时：在 brief 确定真实数据结构与 URL 视图状态，在 design_system 绑定图表语义色板，在 page_design 产出桌面与移动端孪生图稿，在 implementation 严格执行 Server/Client 边界与动态加载。
- 包含组件级高品质动效时：在 motion_decision 中从 react-bits-animation（参考本地库 `react-bits`）选定单点 Signature Motion，在 page_design 标定触发与减弱动效回退，在 implementation 最小化引入。

Design Gate 在 prebuild_review 执行，通过条件：brief、设计系统视觉板与 `design-system.md`/`tokens.json`、字体方案、Logo 或已保留的既有品牌、约定范围内的完整页面稿、可独立访问的静态素材、素材清单都真实存在且已亲自查看；目标设备构图已检查；内容覆盖表已与页面稿逐项核对，关键用户问题在当前范围内有对应信息或明确的原型待补标注；没有会阻断当前交付范围的内容或品牌缺口。animate 另需 4–10 张关联关键帧、已查看的 H3 视频、poster 与静态回退。

Build Gate 在 verification 执行，通过条件：按项目实际能力跑过构建、类型检查、lint 与相关测试；在浏览器里按目标设备看过真实页面并与设计稿逐区对照；导航、表单、键盘焦点、替代文字、对比度、reduced-motion 已验证；无 CSS 选择器冲突或样式覆盖异常；图表无 SSR 水合报错且移动端响应良好；React Bits 动效无控制台报错、无 CLS 抖动且支持减弱动效；animate 另验视频加载、滚动同步、失败回退与移动端表现。构建成功不等于视觉验收通过；无法执行的检查如实标为未验证。

## 不可让步的边界

每条只在这里定义一次，后续阶段引用它，不重复展开。

**真实性。** 价格、产品参数、库存、配送、销量、评价、客户 Logo、认证、合作关系、功能接通状态一律不得编造。设计稿可以用明确标注的"待提供"内容，但正式交付中不能让它看起来像真实业务事实。生成产品图不得改变真实商品的结构、包装、颜色与标识。图片模型画出来的数字和标签不可信，必须按真实数据核对。

**授权分层。** 设计自主权不等于付费生成、公开上传、发布上线、绑定域名、覆盖生产站点或发布到社区的授权；这些各自独立，且不因"帮我做完"而自动获得。自检通过不等于用户批准。凭据不写进提示词、前端代码或素材清单。

**先设计后实现。** Design Gate 通过前不写正式产品页面，不搭等待换图的模板，不用 CSS 色块、占位框或文字说明冒充已生成的设计稿。此前可以做的是：读仓库、整理内容、写设计规范与 tokens、准备素材处理与验证脚本。

**审阅与验收。** “直接完成”“你来决定”可以授权自主设计和连续推进，不等于跳过图片设计、适用素材或质量验收。用户不要求逐阶段审阅时，自检通过即可继续；要求先看设计时等待其确认。免去人工审阅不免去 Design Gate。用户明确缩减交付范围时记录新范围与未执行项，不把未执行检查记为 passed，也不把未完成的完整网站标为 completed。

**复用优先。** 已有项目先查技术栈、目录、组件、tokens、品牌素材、路由与测试，遵循 Reuse > Extend > Replace，保护既有登录、支付、数据、SEO 与分析行为，不做无关重构。

**内容范围与视觉确认。** 用户选中一张参考图或设计方向，只确认其中明确表达的视觉选择，不自动确认页面长度、区块数量或整站内容范围；用户明确要求精确复刻或限定范围时按其要求执行。完整页面应覆盖约定的用户理解与行动流程，不能只凭画到页脚就判定完成。内容完整性以任务和信息覆盖为依据，不以页面长度或固定区块数为依据。

**实现忠实。** 重要视觉决策必须能追溯到设计系统、页面稿或已记录的设计修订。需要调整时先改设计依据再改代码；安全、可访问性或技术缺陷不能以"忠实还原"为由保留。

**拒绝模版化与 AI 视觉套路。** 严防“AI Slop”设计通病：无理由的紫色渐变、过度居中排版、统一均质圆角、默认 Inter 字体、标题单字变色、无层级的卡片堆叠、伪装成内容的随机序号（01/02/03）以及无意义的全大写眉标。设计必须扎根于具体业务主题，而不是套用流行 AI 模版。

**一处更大胆量（Signature Element）与香奈儿克制法则。** 让一个核心记忆点成为视觉锚点，其余部分保持严谨克制。遵循香奈儿法则：审视全局并摘掉一件多余饰品——凡是不为业务与用户行动服务的无意义装饰、散落的微动效与多余渐变，一律删去。

**界面文案是设计材料。** 严禁套用空洞的 AI 占位文案。文案从真实用户视角撰写，采用主动语态与精准操作动词（如“Save changes”而非“Submit”；动作按钮名与反馈 Toast 词汇强一致）。错误与空白状态提供明确的行动引导，而非模糊的情绪宣泄。


## Award-level quality standard

以 Awwwards、Webby Awards、FWA 获奖级网站作为视觉与交互品质参考。这里的获奖级表示对构图、节奏、叙事、交互、动效、完成度和原创性的高标准要求，不表示复制任何获奖作品，也不表示项目必然获得奖项。

这些奖项只作为品质参照，不作为模板复制来源：

- 可借鉴成熟作品对构图、叙事、节奏、交互反馈和完成度的要求。
- 不复制第三方 Logo、文案、独特页面结构、专属图形、代码或未授权素材。
- 不把获奖网站的视觉趋势自动套用到所有项目；先判断项目目标、受众、品牌事实和内容类型。
- 无法访问或核验奖项网站时，使用已知设计原则和实际浏览器证据，不声称完成实时奖项网站对照。
- 获奖级审美不能覆盖真实性、可访问性、性能、移动端可用性、reduced-motion、内容完整性、资源回退、用户指定约束或授权边界。

### 八维品质自检

verification 后必须从以下八个维度检查页面真实渲染、设计稿、设计系统、代码和交互行为。静态图片不能证明键盘行为、性能、转化或完整响应式质量。每个维度记录 status、evidence、finding、repair、recheck 和 residual_limit；状态只能使用 PASS、FAIL、UNKNOWN、UNAVAILABLE 或 NOT_APPLICABLE。

| 维度 | 检查重点 |
| --- | --- |
| 排版 | 字体角色清晰、字号比例合理、行长舒适、层级有节奏，长文本和多语言不破版 |
| 留白 | 视觉呼吸充分、内容密度有变化、区块间距有目的，没有因堆内容而拥挤 |
| 视觉层级 | 首要信息、次要信息和行动入口明确，视线顺序符合页面目标 |
| 色彩 | 色彩服务品牌和任务，语义色一致，对比度和状态表达可靠 |
| 动效 | 动效有目的、节奏克制、过渡自然、无明显卡顿，并支持 reduced-motion |
| 微交互 | hover、focus、press、loading、success、error 和状态反馈清晰且统一 |
| 响应式 | 桌面、平板、移动端都有明确构图，内容优先级、触控尺寸和横向溢出经过检查 |
| 原创性 | 视觉概念、构图、文案、材质和动效组合与业务主题有关，避免模板化 AI 视觉 |

### 持续优化循环

```text
browser_verification
→ quality_review
→ identify_highest_impact_issue
→ repair
→ re-render
→ recheck
→ quality_review
→ delivery
```

每轮只处理能明显提升结果的高影响问题，优先级为：内容理解和行动路径；排版和视觉层级；响应式结构和可用性；色彩和对比度；动效和微交互；细节打磨和原创性。每次修复后重新渲染受影响页面，复验受影响设备和路径。

满足以下条件时停止：八个维度均没有 FAIL；没有确认的明显视觉或交互缺陷；没有影响主要用户任务的问题；新一轮修改只能产生主观偏好变化；继续修改需要新增素材、预算、授权、产品事实或超出用户范围；剩余问题只能通过真实用户测试或新证据判断。停止时说明已检查维度、已修复问题、剩余限制、停止原因以及仍需用户偏好或真实用户测试的内容。不得声称绝对完美，只能说明在当前范围、证据和约束下没有发现明显高影响改进项。

### 品质自检记录格式

```yaml
quality_review:
  reference_standard: Awwwards/Webby Awards/FWA award-level quality reference
  live_award_site_comparison: PASS | NOT_APPLICABLE | UNKNOWN | UNAVAILABLE
  dimensions:
    typography: {status: PASS | FAIL | UNKNOWN | UNAVAILABLE | NOT_APPLICABLE, evidence: '', finding: '', repair: '', recheck: '', residual_limit: ''}
    whitespace: {status: PASS | FAIL | UNKNOWN | UNAVAILABLE | NOT_APPLICABLE, evidence: '', finding: '', repair: '', recheck: '', residual_limit: ''}
    hierarchy: {status: PASS | FAIL | UNKNOWN | UNAVAILABLE | NOT_APPLICABLE, evidence: '', finding: '', repair: '', recheck: '', residual_limit: ''}
    color: {status: PASS | FAIL | UNKNOWN | UNAVAILABLE | NOT_APPLICABLE, evidence: '', finding: '', repair: '', recheck: '', residual_limit: ''}
    motion: {status: PASS | FAIL | UNKNOWN | UNAVAILABLE | NOT_APPLICABLE, evidence: '', finding: '', repair: '', recheck: '', residual_limit: ''}
    microinteraction: {status: PASS | FAIL | UNKNOWN | UNAVAILABLE | NOT_APPLICABLE, evidence: '', finding: '', repair: '', recheck: '', residual_limit: ''}
    responsive: {status: PASS | FAIL | UNKNOWN | UNAVAILABLE | NOT_APPLICABLE, evidence: '', finding: '', repair: '', recheck: '', residual_limit: ''}
    originality: {status: PASS | FAIL | UNKNOWN | UNAVAILABLE | NOT_APPLICABLE, evidence: '', finding: '', repair: '', recheck: '', residual_limit: ''}
  continuous_optimization_status: PASS | FAIL | UNKNOWN | UNAVAILABLE | NOT_APPLICABLE
  stop_reason: ''
```

## 工具路由与费用

图片生成严格遵循三级降级梯队，**尽可能优先使用 API，最大限度避免消耗 Higgsfield**：
1. **第一优先级（系统原生 imagegen）**：每次要生图时，必须首先尝试调用 `imagegen`。
2. **第二优先级（自定义 API 路由 / gpt-image）**：如果 `imagegen` 无法生成或调用不可用，**直接降级使用 API 生图**（调用 `gpt-image` 或读取环境配置的 `OPENAI_BASE_URL` 与 `OPENAI_API_KEY` 调用模型 API，如 gpt-image-2 / gpt-image-2.5 等）。尽可能通过 API 满足生图需求。
3. **第三优先级（最后的保底：Higgsfield）**：只有在前两级（imagegen 与自定义 API）均完全不可用时，才考虑启用 Higgsfield 生图能力，避免不必要地消耗 Higgsfield 额度。
若三级路径均不可用，则完成 brief、文字规范草案与生成提示词并标记素材阻塞，不进入正式页面实现。

视频默认且仅自动选用 Higgsfield 的 MiniMax H3（`minimax_h3`），只在 animate 分支提交。先确认当前工作区、估价与额度，已有正确工作区不重复切换；跨工具传图取得真实可访问引用。保留约定的 2K 母版 + 本地压缩 web 版 + poster + 静态回退交付方式，提交前核对实时契约；若规格不再支持，说明差异并等待有关决定。H3 不可用时只阻塞依赖它的工作，不自动换模型或改成 non-animate；`minimax_h3_max` 也需用户明确授权变更。镜头映射与验证见 [references/motion-and-video.md](references/motion-and-video.md)。

付费按批次管理：核对现有授权的用途、数量、质量、费用上限和返工范围；已覆盖的批次直接执行，不再次索要授权。新增费用未被覆盖时说明已知费用或不确定性并取得授权。不替用户选择付费升级、购买额度或规避限制。超时先查原任务，不盲目重试。job ID 只是任务记录，未查看结果就标“未视觉验收”。

## 提问与研究
## 提问与决策对齐协议（Mandatory Intake Protocol）

每次使用本技能开始新建站或全站设计任务时，在进入具体代码与设计生成前，**必须严格停下来向用户发起标准化的决策对齐提问**。先充分吸收用户在初始提示词中已明确给出的信息，针对未确认的核心维度，使用清晰的选项卡片（单选/多选）或聚焦清单合并一次性提问，允许用户选择推荐项或回复"你来决定"。

为达到 Awwwards / Webby / FWA 顶级水准，标准对齐问卷覆盖以下核心维度：

### 1. 项目定位与核心转化路径 (Business Purpose & Primary Action)
- **网站形态与使命**：
  - A. 品牌殿堂 / 沉浸体验型（主打视觉冲击、情绪共鸣、品牌世界观心智占领，如奢侈品、潮饮、创意工作室）
  - B. 营销转化 / 线索获取型（主打痛点直击、信任背书、预约试用、询盘表单，如 B2B SaaS、专业服务）
  - C. 消费品 / 单品爆款电商型（主打 3D 展台、规格对比、加购与即时购买路径，如 DTC 硬件、新消费）
- **核心转化动作 (Primary CTA)**：明确访客进站后的第一使命（如：立即体验 Demo / 探索特调 / 预订席位 / 点击购买）。

### 2. 视觉 DNA、美学流派与参考标杆 (Aesthetics & Brand Persona)
- **美学气质倾斜**：
  - A. 暗黑未来 / 赛博能量 / 电影光影（深邃暗调空间、冷冽高光切面、发光曲面、科技张力）
  - B. 极简奢华 / 现代画廊留白（大面积呼吸感、极细几何排版、高阶克制点缀色、超高印刷感）
  - C. 年轻街头 / 活力波普 / 潮流节奏（鲜明撞色、巨大破坏式排版、动态贴纸、节奏感）
  - D. 前沿自然 / 有机流体 / 拟态玻璃（大地色系、磨砂通透质感、柔和渐变与微光漫反射）
- **色彩与品牌识别规范**：明确主色板（核心品牌色、强调色、背景底噪色）及禁忌色彩。
- **对标案例与灵感参考**：用户指定的对标网址，或由技能从 Awwwards/Webby 库推选 2 个符合业态的高端参照供选择。

### 3. 页面体量与信息架构 (Scope & Site Topology)
- **交付范围模式**：
  - A. 完整多页官网（Home 首页 + Products/Services 产品服务 + Story 品牌故事 + Culture/News 文化资讯 + 转化/购买终端）
  - B. 剧情式沉浸长单页（All-in-one Narrative Landing Page，全章节通过滚动贯通）
  - C. 核心主页 + 旗舰体验页（双页面深度组合，优先打磨旗舰体验）

### 4. 动效深度、3D 与感官交互选型 (Motion, 3D & Sensory)
- **交互与动效烈度**：
  - A. 顶级沉浸式（3D WebGL / R3F 模型与材质着色器、多轴转动、Scroll Scrub 滚轮运镜、流体粒子交互）
  - B. 高品质界面动效（GSAP 时间线 / Motion / 视差滑轨、平滑吸附、微交互丰富、60fps 极速加载）
  - C. 现代克制动效（原生 CSS 级精密动效，专注排版呼吸与 Hover 响应，极简低耗）
- **多感官与声音设计 (Sound Design)**：是否引入可切换的交互音效（开关罐音效 / 金属触击声 / 微电流反馈 / 环境底噪呼吸）。
- **移动端 (Mobile) 策略**：是否启用移动端深度降级（自动精简复杂 3D/重着色器，保障单手丝滑体验）。

### 5. 内容真实性、叙事语调与资产来源 (Content Boundary & Asset Sourcing)
- **品牌叙事语调 (Voice & Tone)**：
  - A. 极简冷硬电报体（短句、纯粹力量感、拒绝废话）
  - B. 节拍韵律潮流体（强节奏、音乐感与社群黑话）
  - C. 物理感官诗意体（强调材质冰点、金属折射、水汽与击喉感）
- **素材与数据源**：
  - 确认采用用户提供的真实资产，还是由本技能根据品牌概念自主原创生成；
  - 明确概念站/商业真实站边界，未打通的 API/电商/支付明确标记为 Demo/TBD。

用户回答完毕（或确认采用推荐默认）后，才能进入 brief 与 design_system，严禁跳过本对齐阶段擅自编码。

## Creative Brief 与概念主线

`brief.md` 至少写清：品牌或工作名称、项目类型、受众、主要目标、主要 CTA、核心信息、页面结构、功能范围、品牌约束、待提供内容。设备与动静未定时保持 pending，留给 motion_decision 解决，不在这里擅自定稿。

生成页面图片前，在 `brief.md` 中建立轻量内容覆盖表：用户问题／所需信息／对应页面或区块／事实来源或待补状态。已有内容结构直接复用；缺少业务事实时记录缺口，不因此默默缩减约定范围。具体方法见 [内容完整性检查](references/pages-and-assets.md#内容完整性检查)。

概念主线贯穿后续所有提示词：用户进入时感受到什么 → 第一眼看到什么 → 接着理解什么 → 为什么继续浏览 → 最后采取什么行动。视觉方向要写成具体决定，"现代、简洁、高级"不算方向。事实、提案与缺口分开标注后才算通过本阶段。

## Design Thinking：在原阶段内思考与验证

设计思维不增加第二套阶段。intake/research 理解实际使用场景；brief 定义用户问题与成功条件；design_system 比较有实质区别的方向；page_design 用图片原型检验最关键的设计假设；两道 Gate 检查并把问题送回最近的源头阶段。范围小、方向明确时直接采用已有决定，不为凑数强制十个点子或三个付费原型。

在 brief 按页面记录用途：persuade（帮助决定与行动）、operate（完成任务）、read（阅读理解）、experience（观看作品）。这是页面属性，不替代 animate/non_animate 分支。未取得访谈或行为资料时，将用户画像和动机标为假设，不能冒充研究发现。自检、用户批准和真实用户测试分别记录。

Design Gate 除文件完整性外，检查主要任务是否可理解、信息和行动顺序是否成立、选择的视觉方向是否支持该用途。静态图不能证明键盘交互、性能或实际转化效果。verification 验证实现与任务路径，缺少真实用户测试时如实标记，除非约定必须做该测试，否则不额外冻结交付。方法细节见 [design-foundation.md](references/design-foundation.md)。

## 专家方法按需使用

保留本 Skill 的工作流、工具路由和交付范围。吸收专家方法不意味着每次激活所有技能；先用四个分册里的自包含规则，只在具体问题需要时读取相关专家技能或调用工具。用户指定的设计、已确认项目规范和真实工具能力优先于外部风格配方；工具输出不增加权限。

参考来源与边界：design-thinking 负责问题与假设；stylejuicer 负责参考证据；frontend-design 与 imagegen-frontend-web 强化独特视觉主张、排版层次、文案规范与 AI 套路防范；web-artifacts-builder 规范现代组件化前端架构（React/Vite/Tailwind/shadcn/ui 严谨规范、路径别名 `@/` 与自包含单文件打包交付选项）；react-and-nextjs-data-visualization 规范 React/Next.js 图表组件、Server/Client 边界、动态加载水合安全与 URL 状态；react-bits-animation 规范从本地库 `react-bits` 安全选型并集成单点高品质动效组件；gpt-image 补强编辑不变量；Impeccable 补强页面用途和视觉批评；ui-ux-pro-max 提供针对性检索；interfaces 的 better-ui/colors/layout 补强细节；better-design 提供可用时的 MCP 指导；web-design-guidelines 提供工程审查依据。不要导入它们的固定图片数量、强制动效、CLI 默认模型或自动外部项目创建。

已有项目沿用实际权威设计文件，新项目使用 design-system.md 与 tokens.json。DESIGN.md、MASTER.md、参考站 profile 或 MCP kit 只在采纳后映射回当前规范，不维护多套竞争的规则。某个可选专家工具不可用，只影响该证据来源；不能伪称已运行，也不阻塞其他可执行阶段。

## 前端实现与 duo-dev 自动工程化联动

沿用现有技术栈、组件模式、样式规范与路由；新项目选满足需求的最小合理方案，不无故迁移框架或加依赖。用真实语义化 HTML、文字和可复用组件实现设计，统一 tokens、组件变体与素材引用，不新增未经设计的渐变、玻璃效果、悬浮卡片或装饰动画。

**duo-dev 自动联动准则**：
当任务属于代码实现阶段（Design Gate 已通过，进入 implementation）且工作区具备 Git 仓库条件时，代码编写与架构重构**强制使用本地 duo-dev 编排器**：
- 执行 `duo-dev run "<task description>"`；
- **全自动执行无需向用户逐步骤提问**：duo-dev 内部的 Planner、Executor、Reviewer 会自动完成架构拆分、代码编写与代码审查，无需在执行循环中中断打扰用户；
- 若当前目录非 Git 仓库或 duo-dev 前置条件不满足，则无缝降级为当前环境的高标准原生全栈编码，并在执行完成后向用户如实说明工程路径。

逐区把页面映射回设计稿、组件和素材。处理目标设备的布局、裁切、字体与交互，配置合理的图片尺寸、格式与响应式资源，不对关键首屏内容无差别懒加载。

新项目推荐采用基于现代组件化的技术栈（如 React 18+、TypeScript、Vite、Tailwind CSS，结合基于 Radix primitives 的 shadcn/ui 组件模式），配置清晰的路径别名（`@/`）。编写样式时严格防范 CSS 选择器特异性冲突（如 `.section` 类与 `.cta` 元素选择器之间的 margin/padding 发生级联抵消）。根据交付要求，支持导出为自包含的单文件 HTML 交付物（bundle.html，内联所有 JS/CSS/资源），消除依赖与路径断裂风险。

涉及数据可视化时：区分服务端框架与客户端图表绘制（D3/Canvas/SVG/Recharts/Three.js），涉及浏览器 API 的图表使用 `next/dynamic(..., { ssr: false })` 异步加载杜绝水合冲突；移动端用卡片提炼核心指标，次级图表与筛选放入抽屉/底部面板。
涉及组件级动效时：从 `react-bits-animation`（本地参考库 `react-bits`）以最小化源码引入单一 Signature Motion，禁止无节制堆砌；预留容器尺寸防范 CLS，严格支持 `prefers-reduced-motion` 静态等价回退。

假登录、模拟提交、未接通的 API 不得说成生产功能；记录哪些真实接通、哪些只是界面演示，敏感凭据留在服务端环境。发现问题回到最近的源头阶段修正并重查受影响内容，只有当前约定范围的必要检查通过后才把 `execution_status` 标为 completed。

验收以用户任务为单位：完成主要操作、识别失败并恢复、读取核心内容。通常集中检查一轮、批量修复、确认一轮；新变更、失败或未解决关键问题才继续，不无限审美打磨。问题报告标明位置、用户影响、证据和已验证范围；不能用综合评分掩盖关键失败。具体视觉与工程检查见 [pages-and-assets.md](references/pages-and-assets.md)。

## v4.1 交付报告字段

最终报告除现有状态外，必须包含：award_level_quality_status、typography_status、whitespace_status、hierarchy_status、color_status、motion_status、microinteraction_status、responsive_status、originality_status 和 continuous_optimization_status。每项只能使用 PASS、FAIL、UNKNOWN、UNAVAILABLE 或 NOT_APPLICABLE，并说明证据、问题、修复、复验和剩余限制。技能文件升级本身没有具体网站页面，因此页面级字段标记 NOT_APPLICABLE；结构和内容自检完成后，continuous_optimization_status 可标记 PASS。

## 状态与产物

维护一份简短状态记录，有文件系统时存为 `project-state.yaml`，没有就在会话内记录，不谎称已保存。状态文件与设计产物放在项目既有文档目录或专用工作目录，不往用户仓库根目录随意丢文件。等待或阻塞时保留当前阶段以便恢复。恢复任务时先读状态与真实成果，从最早未完成的必要阶段继续，不重置用户决定，不重复生成已合格的素材。

交付按范围包含 `brief.md`、`design-system.md`、`tokens.json`、品牌素材、页面稿、`asset-manifest.json`、前端代码，animate 另含关键帧、H3 视频与回退资源。交付时区分设计完成、素材完成、前端完成、功能接通、验收通过和已发布，只给真实存在且可访问的文件或链接。

## 分册

- 设计系统、tokens、字体与 Logo：[references/design-foundation.md](references/design-foundation.md)
- 动静与设备决策、页面稿、Visual DNA、静态素材：[references/pages-and-assets.md](references/pages-and-assets.md)
- 关键帧、H3 实参与镜头映射、动画实现与验收：[references/motion-and-video.md](references/motion-and-video.md)
- 图片与视频提示词契约、状态与素材清单结构、失败恢复：[references/prompts-and-state.md](references/prompts-and-state.md)
