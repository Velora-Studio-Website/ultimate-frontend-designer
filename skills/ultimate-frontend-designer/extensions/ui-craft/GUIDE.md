# UI Craft：任务驱动的设计增强

先识别交付物与当前缺口。沿用现有 brief、tokens、组件、路由和验收记录；只加载本次需要的参考。完整项目、局部修复和只读评审不共用一套强制流程。

## 选择方法

| 当前缺口 | 读取与行动 |
| --- | --- |
| 设计方向未定、候选看起来相似 | [方向与精修](references/direction-polish.md)；候选数量按用户要求与实际分歧决定 |
| 表单、弹窗、异步状态、手机操作 | [交互与状态](references/interaction-states.md)，先写关键状态转移，再实现 |
| 旧界面改造、后台工作区选择 | [工作区与改造](references/workspaces-renovation.md)，先明确改造模式与必须保留的行为 |
| 单组件、卡片、折展和装饰动效 | [组件模式](references/component-patterns.md)，查看 [离线组件实验室](assets/component-lab.html)，只移植选中模式 |
| 独立视觉评审、任务走查、修复追踪 | [评审协议](references/review-protocol.md) 与 [工具](references/tooling.md) |

只读评审交付证据与建议，不改产品代码。代码修复沿用项目实际技术栈。生成图片、对外请求、付费、发布与安装依赖遵守既有授权。没有对应工具时报告该项限制，继续可执行部分。

## 与图片优先流程结合

完整建站与大范围视觉重做先完成宿主要求的图片设计与 Design Gate。方向比较可以比较已有设计稿，不能以 HTML 候选绕过图片设计。生成器支持原生 HTML 是工具能力，不是跳过宿主阶段的许可。开发组件参考库、工具或修改 Skill 本身不构成正式产品建站，无需为其生成无关图片。

对已确认方向做差异检查，不强迫重新做三版。对旧项目仅修一个流程时，保留品牌与已确认视觉，只补受影响的状态或设备依据。改变重要视觉决定时先更新设计依据。

## 证据边界

截图文件存在不等于已查看；静态检查不等于交互通过；独立审阅不等于用户研究。所有成果按实际发生的检查报告。`review.py` 仅校验记录、文件身份和声明一致性，不判断画面好看、不自动产生浏览器 PASS。

上游参考仅作局部方法来源：[设计方向](vendor/oil-ui/references/design-direction.md)、[视觉语言](vendor/oil-ui/references/visual-language.md)、[滚动叙事](vendor/oil-ui/references/scroll-narrative.md)、[小游戏](vendor/oil-ui/references/play.md)。不加载上游完整入口，不导入其固定变体数、工具强制、营销推荐或更新机制。当前主技能的事实、授权、图片、阶段、验收与工程规则优先。
