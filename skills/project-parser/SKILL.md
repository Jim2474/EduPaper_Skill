---
name: project-parser
version: 0.2.0
description: |
  解析教育科研课题开题报告（PDF/DOCX/MD），提取结构化课题档案，写入 project.json。
  当用户提供开题报告文件且 .edupaper/project.json 不存在时触发。
  触发词：解析开题报告 / 建立课题档案 / 读取开题报告 / 课题档案初始化 /
  parse opening report / 从开题报告建档 / 提取课题信息。
  本 skill 是全流水线的第一步，其输出 project.json 是所有下游 skill 的共享只读
  数据源。适用于任何学科的教育科研开题报告，不局限于特定课题。
  不生成选题、文献、论文内容。
author: Jim2474
agent_created: false
---

# Project Parser

从用户提供的开题报告中提取结构化课题档案，写入 `.edupaper/project.json`。
此文件是整个流水线的单一事实来源——其他所有 skill 只读，不修改。

## 启动时加载

1. 读 `../_shared/project-context.md` — 了解 project.json 的完整字段含义与结构
2. 读 `references/project-schema.md` — 获取字段的详细提取规则和类型定义

## When to trigger

- 用户提供开题报告文件（PDF / DOCX / MD）
- `.edupaper/project.json` 不存在或为空
- 用户说"解析开题报告" / "建立课题档案" / "读取开题报告"

## Procedure

1. 读 `../_shared/project-context.md` 了解目标 JSON 结构（字段含义）。
2. 读开题报告文件：
   - PDF → 用 pypdf 提取全部文字（`pypdf.PdfReader`）
   - DOCX → 用 python-docx 提取段落文字
   - MD/TXT → 直接读取文本
3. 读 `references/project-schema.md` 获取每个字段的提取规则和类型。
4. 将开题报告内容逐字段映射到 schema，做合理推断：
   - 若报告未显式说明某字段，从上下文推断（如从年级+学科推断教材版本）
   - 无法推断的字段填写 `"__MISSING__"` 并记录
5. 检查 `依据.劳动基地.典型活动` 字段：若开题报告提到实践/劳动基地，
   尽量提取 2-5 个具体活动描述（越具体越好，用于后续 topic-generator 生成选题）
6. 构建 JSON 对象，写入 `.edupaper/project.json`（UTF-8，2空格缩进，创建目录如不存在）
7. 读 `../_shared/quality-gate.md` 执行通用质量门，再运行下方 self-check

## Output

写入 `.edupaper/project.json` — 有效 JSON，UTF-8，2空格缩进。

## Self-check (quality gate)

- [ ] `references/project-schema.md` 中所有**必填字段**均非空
- [ ] `meta.课题名称` 和 `meta.主持人` 存在且非空
- [ ] `研究对象.总人数` 为正整数
- [ ] `术语表` 为 `核心概念` 中每个概念都定义了含义
- [ ] `成员分工` 至少有一条记录
- [ ] `依据.课标` 和 `依据.教材` 存在且非空
- [ ] `研究设计.研究内容` 至少有一条记录
- [ ] 所有 `__MISSING__` 字段已列出（提醒用户补充）
- [ ] JSON 有效可解析

若任何检查失败，返回步骤 4 补充缺失信息，最多重试 3 次。
三次失败后：写入含 `__MISSING__` 标记的文件并上报给用户。

## Constraints

- **只提取，不发明**：不生成开题报告中没有的数据
- 找不到的字段用 `"__MISSING__"` 标记，永远不要留空或猜测后标 verified:true
- 不生成选题、文献、论文内容——那是下游 skill 的职责
- **本 skill 是 project.json 的唯一写入者**：若文件已存在且有效，跳过本 skill
