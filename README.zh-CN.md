# Ultimate Frontend Designer

**先规划完整内容，再用图片设计，然后忠实实现并验证。**

[English](README.md) · [简体中文](README.zh-CN.md) · [示例提示词](examples/prompts.md) · [ChatGPT 项目设置](docs/chatgpt-project.md)

这是一个面向 **Codex 和兼容 ChatGPT 工作环境**的社区 Skill，将设计思维、品牌视觉、UI/UX、素材制作与前端交付放进同一套图片优先流程。

当前版本 **2.0.1** 加入内容完整性检查：用户选中漂亮的视觉参考，不代表同意把网站做成信息不足的短页面。Ultimate 是项目名称，不代表基准测试结论或 OpenAI 官方背书。

## 适合做什么

- 产品与电商网站：先回答顾客的问题，再引导购买。
- Landing Page 与品牌网站：建立统一的视觉系统和独立素材。
- Web App：围绕实际任务设计界面及必要状态。
- 仅设计交付，或在工具齐全的环境里完成前端。
- 通过 Animate 分支制作包含视频叙事的网站。

小改动保持小范围。修改文案、生成单张图片、UI 审查不会启动完整建站；已有项目优先复用技术栈、组件和正确行为。

## 快速开始

### 在 Codex 中安装独立 Skill

向 Codex 的内置安装器发送：

```text
$skill-installer 请安装这个仓库路径中的 Skill：
https://github.com/Velora-Studio-Website/ultimate-frontend-designer/tree/main/skills/ultimate-frontend-designer
```

安装后这样使用：

```text
使用 $ultimate-frontend-designer，为我上传的商品制作响应式电商网站。
选择 Non-Animate，先保留本地预览。
先梳理顾客问题、完整内容结构和缺失资料，再生成完整图片设计稿。
先让我看设计，确认后再实现。不要编造价格、参数、评价或配送规则。
```

未出现时刷新或重启客户端。更新前让安装器检查现有安装，不要在多个发现目录里重复安装同名 Skill。参考 [官方 Skill 文档](https://developers.openai.com/codex/skills)。

也可以下载仓库，将 **整个** `skills/ultimate-frontend-designer/` 文件夹复制到客户端支持的 Skill 目录。当前 Codex 文档列出用户级 `~/.agents/skills/` 与项目级 `.agents/skills/`；内置安装器也可能使用其配置的 `$CODEX_HOME/skills`。不要只复制 `SKILL.md` 而漏掉四个分册。

### 在 ChatGPT 中使用

**环境支持原生 Skill／插件时：** 使用该客户端支持的安装入口，然后选择已安装的 Skill。仓库提供标准 `plugin.json` 和 `.codex-plugin/plugin.json` 兼容清单。GitHub 发布不等于自动上架 OpenAI 插件目录；能否安装仍取决于客户端功能、账号和工作区策略。参见 [插件包装说明](https://developers.openai.com/plugins/build/plugins)。

**项目资料模式：** 将 `SKILL.md` 和四个 `references/*.md` 上传到 ChatGPT Project，再使用 [项目设置文档](docs/chatgpt-project.md) 的说明。上传文件只是提供工作流资料，不会自动安装工具、登录 Higgsfield 或获得本地文件及部署权限。[ChatGPT Projects 官方说明](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)。

需要完整代码交付时，选择具备文件、终端和浏览器工具的工作环境。普通聊天中，应按当前实际工具交付设计与实现资料，不假装代码已构建或网站已上线。

## 需要准备什么

这个发布包本身是工作流说明，**仅阅读和使用指令不要求安装 Node.js、Python、API Key 或购买订阅**。实际执行按任务需要相应能力。

| 能力 | 何时需要 | 需要准备 |
| --- | --- | --- |
| 能读取 Skill 与分册的 Agent | 所有模式 | Codex 或兼容环境，以及可读取的项目资料 |
| 图片生成与视觉检查 | 图片优先设计 | 原生图片工具，或可用的 Higgsfield 图片集成 |
| 文件编辑、终端、项目运行环境 | 前端实现 | 可写工作区及项目真实依赖 |
| 浏览器检查 | 视觉与交互验收 | Agent 可调用的浏览器工具 |
| Higgsfield + `minimax_h3` | 仅 Animate | 已连接服务、实时可用模型及费用授权 |
| 视频检查与转码 | 动画交付 | 播放／抽帧能力及 FFmpeg 等本地编码器 |

图片路线：原生工具 → Higgsfield 图片能力 → 图片阶段阻塞。两条路线都不可用时，可以整理简报与提示词，但不能宣称图片设计完成，也不能越过设计门开始正式页面实现。

生成视频前必须核对实时参数。分册中的 H3 参数表是历史工具快照，不保证服务当前仍完全相同；不得自动替换视频模型。Non-Animate 不需要 H3，但仍需要图片设计，并保留正常按钮、菜单、切图等交互。

文中提到的专业设计 Skills 和 Product Design 都是**可选参考能力**，不是必须全部安装的清单。本仓库不附带它们的工具、源文件、账号或付费额度。

## 工作流程

```text
需求收集 → 可选研究 → 简报 → 设计系统 → 品牌素材
→ 动静选择 → 页面设计 → 静态素材
→ [仅 Animate：关键帧 → 视频]
→ Design Gate → 前端实现 → 验证 → 交付
```

| 模式 | 包含 | 不代表 |
| --- | --- | --- |
| Non-Animate | 完整图片设计、独立静态素材、响应式前端、可用控件 | 装饰性动效、自动播放或视频生成 |
| Animate | 静态基础、4–10 张关联关键帧、授权 H3 视频、poster、静态与 reduced-motion 回退 | 无限预算或自动换模型 |
| 只要设计 | 约定的设计与素材交付 | 代码、支付或部署已经完成 |
| 局部修复 | 只处理受影响阶段 | 重做品牌或无关重构 |

内容检查在原有 brief／page_design 阶段内完成，不增加另一套阶段，也不强制增加审批回合。

## 先确保内容完整，再生成页面图

每个关键用户问题都应有对应的信息与位置：

| 用户问题 | 所需信息 | 页面／区块 | 来源或状态 |
| --- | --- | --- | --- |
| 这个产品用来做什么？ | 已确认用途和适用场景 | 概览／场景 | 商家提供的事实 |
| 适不适合我？ | 相关规格与限制 | 详情／规格 | 核实前标待补 |
| 我会收到什么？ | 包装内容 | 包装清单 | 核实前标待补 |
| 下单后会怎样？ | 价格、配送与退换 | 购买区／FAQ／政策页 | 真实业务规则 |

这是映射方法，不是强制四个区块或长页面。可以合并信息，也必须尊重用户明确要求的短页和精确复刻。缺少事实时记录缺口，不能编造，也不能默默删除必要信息结构。

长页面使用整体总览加可读的分区稿，不能因为一张生成图放不下，就缩减网站。**确认视觉方向与确认内容范围是两件事。**

## 两道质量门

**Design Gate：** 检查简报及内容覆盖、真实生成的设计系统、tokens、可用字体与品牌素材、完整页面稿、独立素材与设备构图。Animate 另检查关键帧、视频和回退。文件存在不等于质量合格，自检通过不等于用户已批准。

**Build Gate：** 运行适用的项目检查，实际用浏览器对照设计检查布局、响应式、任务路径、键盘焦点和媒体失败。不能执行的检查如实标注；构建成功不等于视觉还原，静态图也不能证明可用性或转化效果。

## 典型交付物

`brief.md`、`design-system.md`、`tokens.json`、页面稿、独立素材、`asset-manifest.json`、`project-state.yaml`，以及用户要求的前端代码。Animate 另交付约定视频母版、网页压缩版、poster 和静态回退。

生成状态、质量检查与用户批准分开记录。本地原型、可用前端、接通交易、已经上线是不同状态。

## 怎样给出好的需求

提供网站目的、目标受众、主要行动、原始产品／品牌资料、真实业务事实、已有代码、目标设备、动静模式和审阅偏好。涉及收费生成时说明预算上限。设计方向可以说“我不知道，你来提案”，但这不代表允许编造业务事实。

[中英文示例提示词](examples/prompts.md) 覆盖静态电商、仅设计和动画场景。Skill 跟随用户当前语言沟通；核心指令目前以中文配合英文标识编写，README 与示例提供中英文版本。

## 仓库结构

```text
plugin.json                         标准插件元数据
.codex-plugin/plugin.json           Codex 兼容元数据
skills/ultimate-frontend-designer/
  SKILL.md                          核心规则与工作流
  agents/openai.yaml                展示信息
  references/
    design-foundation.md            设计思维与视觉系统
    pages-and-assets.md             内容完整性、页面与素材
    motion-and-video.md             关键帧、H3 和动效交付
    prompts-and-state.md            提示词与状态结构
docs/chatgpt-project.md              ChatGPT 项目模式设置，中英文
examples/prompts.md                  可复制提示词，中英文
scripts/validate.py                 离线发布包检查
```

## 验证与贡献

维护者可用 Python 3.10+ 运行 `python scripts/validate.py`，检查目录结构、版本、分册链接和发布文件卫生。使用 Skill 指令本身不需要 Python。该检查不模拟 Agent、不生成图片，也不证明所有客户端都兼容。

反馈问题时，请提供环境、Skill 版本、任务范围、预期／实际结果，以及去除敏感信息后的复现步骤。修改应保留原流程、避免重复规则、同步双语文档，并且不增加隐含的花费或发布权限。

方法参考来源列在 `SKILL.md` 中，未分发第三方 Skills 源文件。OpenAI、Codex、ChatGPT、Higgsfield、MiniMax 名称仅用于说明对应产品，不表示合作或背书。本仓库只发布可复用工作流，不包含私人项目文件或示例商品素材。

## 许可

首次发布暂未选择开源许可证；公开可见不等于授予通用复用许可。维护者可以后续添加许可证。第三方服务、模型和用户素材仍适用各自条款。
