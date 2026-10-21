# 辅助工具与真实证据

路径中的 `<module>` 是当前 UI Craft 模块根目录，不能假定操作系统或用户目录。生成物写到任务工作目录，安装目录只读。

## 离线方向对比

复用保留 MIT 许可的上游生成器：

```text
python <module>/vendor/oil-ui/scripts/build_explorer.py <task>/manifest.json --output <task>/comparison.html
```

输入格式与可选项见 [对比页输入](../vendor/oil-ui/references/style-explorer.md)。先准备实际候选文件；命令不生成设计、不调用图片模型、不运行 manifest 中的命令。默认拒绝覆盖，只有授权更新同一产物才使用 `--force`。HTML 的安全预览会限制脚本，交互验证仍在实际项目入口执行；本机 URL 候选需要已有开发服务器。

## 浏览器与截图

优先宿主实际可用的浏览器与看图能力，沿用其工具契约。包内上游可选 `vendor/oil-ui/scripts/shoot.mjs` 和 `curate-media.mjs` 仅在已有依赖及工具能力适配时使用，先读 `--help`。不自动安装浏览器、改配置、上传文件或下载远程媒体。工具无相应能力时报告 UNAVAILABLE，不能以脚本存在声称截图已验证。

真实 200% 浏览器缩放、局部裁切放大与 viewport 尺寸是不同操作，记录实际使用哪种。状态图必须来自实际状态；录屏、键盘、存储失败与减少动效需要分别执行。遮字图是辅助诊断，不替代正常截图。

## 绑定证据的检查记录

```text
python <module>/scripts/review.py init --scope component --revision <实际修订标识> --out <task>/review.json
python <module>/scripts/review.py record --report <task>/review.json --check visual --status pass --evidence <task>/desktop.png --target <页面或组件> --method screenshot-review --state default --viewport 1440x900 --expected "标题完整可读" --actual "已查看，无裁切" --note "桌面默认状态；手机状态另查"
python <module>/scripts/review.py check --report <task>/review.json
```

`init` 的 scope 支持 component、renovation、full-site、review。它只生成 UNKNOWN 项并记录实际产品修订；`record` 由实际执行者输入结果、目标、方法、状态、预期及实际结果，视觉及响应式项另需视口，并保存证据相对路径与 SHA256。证据必须位于 report 所在任务目录内。记录通过不证明检查真实执行；主 Agent 必须阅读原记录与图像，独立审阅者必须执行自己的审阅。

`check` 检查必要项结果、保留证据的身份、上下文完整性和阻断问题，不联网、不执行目标网页。保留的证据文件改变、必要项 FAIL/UNKNOWN/UNAVAILABLE 或未解决的阻断问题都会返回非零退出码。not_applicable 必须给 `--scope-basis` 写清具体范围依据，视觉与完整站点 Design Gate 不能排除；排除项单独计数，不算通过。可在 report 的 `findings` 添加 id、blocking、status(open/resolved)、description；resolved 的阻断问题需有 repair、recheck_evidence 及 recheck_context（与普通 context 相同的修订、目标、方法、状态、预期和实际字段）。脚本检查字段齐全与身份一致，不能判断理由真实、图片相关或操作确实执行；更新哈希不能替代复查。
