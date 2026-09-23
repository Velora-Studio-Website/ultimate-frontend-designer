# 提示词契约、状态与素材清单

## 图片提示词

每次重要图片请求都说明：

- 项目与品牌背景，本次交付物类型（设计系统板 / 字体板 / Logo / 页面稿 / 独立素材 / 关键帧）
- 受众与核心任务
- 页面用途与待验证假设：该图应帮助用户理解或完成什么，成功条件是什么
- 概念主线：用户先感受到什么 → 第一眼看到什么 → 接着理解什么 → 为什么继续浏览 → 最后采取什么行动
- 必须保持的 Visual DNA：品牌、主体身份或产品结构、配色、材质、光线、图像处理与构图逻辑
- 本次必须包含的真实内容，以及不可编造的业务事实
- 允许模型自主决定的美学细节
- 禁止出现的元素、风格或信息
- 目标设备、画幅、构图与文字安全区，以及素材的实际用途

侧重点按交付物调整：设计板强调规则与组件可读，字体板强调真实语言样例，Logo 强调独立使用与小尺寸辨识，页面稿强调完整信息架构，素材强调与布局适配，关键帧强调前后状态与统一视觉。

## MiniMax H3 提示词

每次视频请求都说明：已确认的视觉世界（品牌、主体身份、环境、材质、配色、光线方向）；起始状态与结束状态；主体的不变结构与动作变化；相机路径、方向与节奏；光线、曝光与前后片段的连续性要求；网页文字安全区（视频内不放文字，文字与按钮由 HTML 实现）；要避免的闪烁、抖动、结构漂移、随机字幕与 Logo 变形；每个参考素材在工具里的真实输入角色。

模型、时长、画幅、分辨率、批量和参考角色通过工具的实际参数设置，不能只在提示词里写了规格就声称工具按该规格输出。

## project-state.yaml

```yaml
project:
  current_phase: intake
  execution_status: ready        # ready / working / waiting_user / waiting_tool / blocked / completed
  delivery_scope: pending        # design_only / full_build / local_fix
  research_permission: pending
  motion_mode: pending           # pending / animate / non_animate
  target_devices: pending        # pending / desktop / mobile / both
  functional_scope: pending
  review_mode: pending           # pending / user_review / autonomous；不豁免质量检查
  brand_constraints: []
  image_tool:
    provider: pending
    model: pending
    availability: unchecked
  video_tool:
    provider: Higgsfield
    required_model: minimax_h3
    resolved_model_id: null
    availability: unchecked
  authorizations:
    paid_generation: pending
    external_asset_upload: pending
    publishing: pending
    brand_change: pending
  design_version: 0
  decisions: []                  # 每项标 user_confirmed / delegated_decision / assumption
  surfaces: []                   # 页面 id、purpose、primary_task、success_condition
  hypotheses: []                 # id、statement、evidence、method、status、result、affected_refs
  scope_changes: []              # 用户明确变更的范围、原请求和未执行项
  phase_results: {}              # 每阶段使用下述结果结构
  gates:
    design: pending
    delivery: pending            # 对应 SKILL.md 的 Build Gate
  blockers: []
```

等待或阻塞时保留 `current_phase`。每阶段结果用对象记录 status（pending / active / passed / not_applicable / blocked）、artifact_refs、checks 和 reason；每项 check 分别记录 method（static / browser / user_test）、status（pending / passed / failed / not_verified / not_applicable）、evidence 和 scope。Gate 使用 pending / passed / failed / blocked / not_applicable。不适用需要理由，未执行不等于通过。

假设状态使用 untested / supported / contradicted / inconclusive，并标明依据是自检还是真实用户证据；假设影响范围内的页面和素材由 affected_refs 引用。无法验证用户行为时维持 untested，不因图稿获批自动改为 supported。决策、用户批准与 QA 不互相覆盖。

旧状态兼容：读取既有决定和结果，不清空重建。旧 phase_results 字符串视作 status，证据缺失则记录未知。旧 user_override 要回查实际用户原话：仅“直接完成”归入 autonomous；确有范围变更写 scope_changes，不自动豁免必要检查。按实际受影响部分迁移，保持恢复位置。

## asset-manifest.json

每项素材记录：`id`、`purpose`、`page_section`、`type`、`source`、`provider`、`model`、`path_or_ref`、`size`、`aspect_ratio`、`device`、`crop_rule`、`alt`、`reference_inputs`、`design_version`、`fallback`。

状态分四轨，不要用一个 approved 混淆：

- `generation_status`：not_applicable / pending / generating / generated / failed / blocked；复用现有素材用 not_applicable，并记录来源
- `qa_status`：pending / needs_review / passed / rejected / blocked
- `user_approval`：not_requested / pending / approved / changes_requested / not_applicable
- `implementation_status`：not_applicable / pending / integrated / verified / stale

旧 generation_status 的 needs_review / passed / rejected 迁移到 QA 轨；只有实际文件或任务证据支持时才将生成轨记为 generated，否则保持 pending/blocked。新建记录可增加 job_id、batch_id、authorization_ref、file_hash、qa_evidence 和 supersedes，用于查原任务、定位版本与避免重复扣费；工具未提供的字段写 null，不捏造。

未生成、不可访问或未查看的素材不能标为已验收。临时生成地址要在允许范围内落实为稳定资产，不检查可访问性就写进交付页面不算完成。

## 版本与失败恢复

设计改动后提升 `design_version`，只把受影响的素材、页面与测试标为待更新，修正错的部分并保留正确成果，不每次全站重做。

在原记录中沿“问题/假设 → 设计决定 → 页面 → 素材 → 实现 → 检查”追踪影响。更新受影响对象的版本与 implementation_status，不将未变对象全部标为过期。保存必要的旧版本与替换关系；最终只有当前范围的必要检查通过才能 completed。缺少可选用户研究不阻塞已约定的工程交付，但必须说明未验证的用户效果。

区分额度、权限、计费、模型不可用、无效输入和生成质量问题，再采取对应处理；超出已授权范围前停下来取得决定。当前环境不支持连续执行全部阶段时，保留状态并如实说明停在哪一步，不声称后台还在继续，也不编造预计完成时间。
