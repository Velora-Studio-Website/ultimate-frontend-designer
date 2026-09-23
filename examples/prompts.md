# Example prompts / 示例提示词

[English README](../README.md) · [中文 README](../README.zh-CN.md)

In clients with a skill picker, select the installed skill first. `$ultimate-frontend-designer` below is the Codex-style mention; a ChatGPT client may expose it through its own picker. In project-reference mode, replace the mention with “Use the uploaded Ultimate Frontend Designer workflow.”

支持 Skill 选择器的客户端先选择已安装技能。以下 `$ultimate-frontend-designer` 是 Codex 风格调用；ChatGPT 客户端可能使用自己的选择入口。项目资料模式可改成“使用已上传的 Ultimate Frontend Designer 工作流”。

## 1. Static ecommerce / 静态电商

```text
Use $ultimate-frontend-designer to build a local ecommerce frontend for my
attached product. Non-Animate, desktop and mobile, English website copy.
Reuse the supplied product appearance. First map customer questions to sections,
including use, confirmed features, specifications, package contents and policies
where relevant. Mark missing facts instead of inventing them. My selected
reference approves the visual style, not a three-section content limit.
Show the complete design before coding. No payment connection or deployment.
```

```text
使用 $ultimate-frontend-designer，为附件商品制作本地电商前端。
Non-Animate，支持电脑和手机，网页文案用英文，与我沟通用中文。
保留原商品外观。先将顾客问题映射到区块，按适用性覆盖用途、真实特点、规格、
包装内容和业务政策。缺失事实明确标注，不编造。
我选的参考图只确认视觉风格，不代表内容只能有三个区块。
完整设计先让我看，确认后再写代码。不接支付、不部署。
```

## 2. Design only / 仅设计

```text
Use $ultimate-frontend-designer for design-only delivery of my service website.
Use the supplied brand and confirmed service information. Propose content
coverage and a visual direction, then generate complete responsive page designs
and the independent assets they need. Non-Animate. I delegate ordinary visual
decisions to you; flag only material gaps. Deliver designs, tokens and handoff
notes. Do not build or deploy a site.
```

```text
使用 $ultimate-frontend-designer，仅设计我的服务网站。
沿用提供的品牌与已确认服务资料，先整理内容覆盖和视觉方向，再生成完整响应式
页面稿及所需独立素材。Non-Animate。常规视觉决定由你负责，只提出关键资料缺口。
交付设计、tokens 与交接说明，不建站、不部署。
```

## 3. Animate with a cost boundary / 有费用边界的动画网站

```text
Use $ultimate-frontend-designer in Animate mode for my product website.
Plan the complete static content first, then explain where video helps users
understand the product. Prepare related keyframes and inspect the current
Higgsfield minimax_h3 contract. Show the quantity, estimated cost and fallback
plan before submitting any paid video jobs. My video-generation budget is not
yet authorized. Continue independent design work while that approval is pending.
```

```text
使用 $ultimate-frontend-designer 的 Animate 分支设计商品网站。
先完成静态内容结构，再说明视频在哪里帮助用户理解产品。
准备关联关键帧并核对 Higgsfield minimax_h3 的当前能力。
提交收费视频任务前，说明数量、估价和回退方案；我尚未授权视频生成预算。
等待该授权时，继续不依赖视频生成的设计工作。
```

## 4. Existing site, bounded change / 已有网站的局部修改

```text
Use $ultimate-frontend-designer only for the product-detail section in this repo.
Keep the existing framework, brand, checkout and other sections. Inspect the
current content gap, design the affected area and implement only that change.
Reuse valid assets. Do not restart the complete website workflow.
```

```text
使用 $ultimate-frontend-designer，只改当前仓库的商品详情区域。
保留现有框架、品牌、结账和其他区块。先检查内容缺口，再设计并实现受影响部分。
复用合格素材，不重新启动整站设计。
```
