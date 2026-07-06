---
name: reference-manager
version: 0.2.0
description: |
  为教育科研课题构建共享文献库，写入 references.json。
  在 project.json 存在且 references.json 不存在时触发。适用于任何学科的教育科研课题。
  触发词：建立文献库 / 整理参考文献 / 生成参考文献 / 文献管理 /
  manage references / build reference library / 整理文献 / 查文献资源。
  本 skill 是 references.json 的唯一写入者，下游论文均从此库引用。
  不写论文内容或生成选题。
author: Jim2474
agent_created: false
---

# Reference Manager

从课题档案中构建共享文献库，写入 `.edupaper/references.json`。
所有下游论文从此单一库引用，确保不同论文之间引用一致、不矛盾。

## 启动时加载

1. 读 `../_shared/project-context.md` — 了解 project.json 字段含义
2. 读 `.edupaper/project.json` — 获取课标、教材、研究内容、核心概念等实际数据
3. 读 `references/reference-schema.md` — 四类文献的字段定义
4. 读 `references/citation-gb7714.md` — GB/T 7714 引用格式

## When to trigger

- `.edupaper/project.json` 存在且有效
- `.edupaper/references.json` 不存在或为空
- 用户说"建立文献库" / "整理参考文献" / "生成参考文献"

## Procedure

1. 读上方"启动时加载"的所有文件。
2. 从 `project.json` 提取：`依据.课标`、`依据.教材`、`研究设计.研究内容`、`核心概念`。
3. 按四类组装文献库：
   - **课标文献**：`project.json.依据.课标` 中列出的所有课程标准。
     若课题涉及多学科（如数学+劳动），两种课标均需包含。
   - **教材文献**：`project.json.依据.教材` 对应的单元和页码。
     若 project.json 未给出具体页码，根据教材目录合理推断。
   - **期刊文献**：与 `核心概念` 和 `研究内容` 相关的 2020 年后学术期刊论文，6-10篇。
     选择与该课题学科领域匹配的权威期刊。
     每篇设置 `verified` 字段：
       - `"verified": true` — 确定该文章真实存在（作者+标题+期刊+年份+期号）
       - `"verified": false` — 不确定是否真实存在，始终标注，不得省略
       - **不确定时标 false，绝不猜测后标 true**
   - **其他文献**：补充来源（政策文件、学位论文、网络资源）。
4. 为每篇 `期刊文献` 填写 `相关选题` 字段，标注支持哪些选题 ID（A、B、C…）。
5. 写入 `.edupaper/references.json`（UTF-8，2空格缩进）。
6. 读 `../_shared/quality-gate.md` 执行通用质量门 + 下方 self-check。

## Output

写入 `.edupaper/references.json` — 有效 JSON，UTF-8，2空格缩进。

## Self-check (quality gate)

- [ ] 课标文献 ≥ 1 条（project.json 中的课标）
- [ ] 教材文献 ≥ 1 条，含具体 单元 和 页码（或 `__MISSING__`）
- [ ] 期刊文献 6-10 条，每条含 作者/标题/期刊/年/期/页
- [ ] 每条期刊文献有非空 摘要
- [ ] 每条期刊文献有 `verified` 字段（true 或 false，不得缺失）
- [ ] 每条期刊文献有 相关选题（至少一个选题字母）
- [ ] 无重复条目（相同 作者+标题+年）
- [ ] 无条目标注 `verified: true` 但实际无把握
- [ ] JSON 有效可解析

若任何检查失败，修复后重试，最多3次；失败后上报用户。

## Constraints

- **本 skill 是 references.json 的唯一写入者**；若文件已存在且有效，跳过
- **防幻觉规则**：不确定时将 `verified` 设为 `false`。下游 paper-writer 的
  self-check 会拒绝引用 `verified: false` 的条目（需用户确认），
  从而防止虚假引用出现在最终论文中
- 若找不到足够的 `verified: true` 期刊文献，包含 `verified: false` 占位条目
  并向用户说明，而非发明 `verified: true` 的假文献
- 所有引用遵循 GB/T 7714 格式（见 `references/citation-gb7714.md`）
- 不写论文内容，不生成选题
