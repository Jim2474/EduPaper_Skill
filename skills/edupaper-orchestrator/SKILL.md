---
name: edupaper-orchestrator
version: 0.2.0
description: |
  教育科研课题论文批量生成流水线编排器。当用户提供教学案例论文相关的开题报告
  或希望生成教学论文时触发。适用于任何学科的小学/中学教育科研课题论文生成。
  每次运行生成一篇论文，用户从选题菜单中选一个，流水线自动完成后续步骤。
  触发词：生成论文 / 写论文 / 帮我写教学案例 / 批量出论文 / 跑论文流程 /
  开始生成 / 出一篇论文 / 生成教学案例论文 / 写一篇教学论文 / 基于开题报告
  生成论文 / generate paper / write teaching case / 继续生成论文 / 接着写 /
  从上次继续 / 继续流程 / 论文流水线 / 帮我生成一篇课题论文。
  本 skill 不执行任何实际生成工作——仅负责路由和编排，所有生成工作委派给下游 skill。
author: Jim2474
agent_created: false
---

# EduPaper Orchestrator

将用户的一份课题开题报告，通过 9 个单一职责 skill 的流水线，转化为符合学术规范
的教学案例论文。**每次只生成 1 篇论文**，用户从选题菜单中选一个。

## 启动时加载

在执行任何操作之前，先读取以下文件，建立全局上下文：

1. `manifest.yaml` — 读取 always_load 列表和 axes 配置
2. 按 manifest 的 `always_load` 依次加载：
   - `../_shared/project-context.md` — project.json 字段含义参考（schema 文档）
   - `../_shared/quality-gate.md` — 统一质量门与重试协议
   - `references/pipeline.md` — 数据流契约与目录规范

## 前置依赖检测

在正式启动流水线前，检测可选外部依赖，提前告知用户：

```
□ humanizer skill 是否已安装？
  → 未安装：提示"第8步 humanize 将跳过，直接输出 paper.md 作为最终稿"
  → 已安装：正常流程

□ pandoc 是否可用（pandoc --version）？
  → 不可用：提示"第9步导出将使用 Python 备用方案，不支持 PDF"
  → 可用：正常流程
```

以上缺失**不阻断**流程，仅提前告知。

## Hard Constraint（硬约束）

**每次运行只生成 1 篇论文。** 选题菜单展示 4-6 个选项，用户选一个。
若用户想要多篇，重新运行选不同选题——已完成的阶段自动跳过（resume 逻辑）。

## Pipeline 执行顺序

每一步的输出文件是下一步的输入。每步完成后验证输出文件存在且非空再继续。

| 步骤 | Skill | 输入 | 输出 |
|------|-------|------|------|
| 1 | **project-parser** | 开题报告（PDF/DOCX/MD）| `.edupaper/project.json` |
| 2 | **reference-manager** | project.json | `.edupaper/references.json` |
| 3 | **topic-generator** | project.json | `.edupaper/topics.json`（4-6个选题） |
| — | **用户选题** | topics.json | 用户选定一个 topic-id |
| 4 | **classroom-generator** | project.json + 选定 topic | `.edupaper/materials/{id}/material.json` 及（若有问卷要求）.edupaper/surveys/* |
| 5 | **paper-writer** | project.json + material.json + references.json +（可选）surveys/* | `.edupaper/drafts/{id}/paper.md` |
| 6 | **paper-reviewer** | paper.md + project.json + material.json | `.edupaper/drafts/{id}/review-report.md` |
| 7 | **consistency-checker** | 所有 paper.md + review-report.md | `.edupaper/consistency-report.md` |
| 8 | **edupaper-humanizer** | paper.md（consistency 通过后）| `.edupaper/drafts/{id}/final.md` |
| 9 | **edupaper-exporter** | papers/*.md | `.edupaper/exports/{id}-标题.{docx,pdf,html}` |

步骤 8 完成后：将 `final.md` 复制到 `.edupaper/papers/{id}-标题.md`。

## 路由规则

- 读 `references/pipeline.md` 获取完整数据流契约、文件命名规范、目录布局
- 每步开始前验证输入文件存在；缺失则运行上游 skill
- 每步结束后确认输出文件已写入；确认后再进入下一步
- 若某 skill 三次 self-check 重试后仍失败，**暂停并上报用户**，不跳过
- 步骤 4-8 针对用户选定的**单个** topic-id 运行
- **问卷调查联动路由**：若 `project.json.研究设计.研究方法` 中包含 `问卷调查法`，步骤 4 必须触发生成问卷和调查报告；步骤 5 在撰写论文时必须读取并融入这部分数据。
- **步骤 7（consistency-checker）必须在步骤 8（humanizer）之前完成**；
  consistency-checker 返回 CONSISTENT 或 SINGLE-PAPER BASELINE 后才允许进入步骤 8
- 步骤 8（edupaper-humanizer）的输入是 `paper.md`（草稿），不是 review-report.md

## 共享只读数据源

两个文件被所有下游 skill 共享读取，但只有其指定写入 skill 可修改：

- `.edupaper/project.json` — **只由 project-parser 写**
- `.edupaper/references.json` — **只由 reference-manager 写**

## Resume 逻辑

若 `.edupaper/` 目录已存在，扫描各步骤的期望输出文件：
- 文件存在且非空 → 跳过该步骤（已完成）
- 文件存在但为空或格式错误 → 重新生成
- 文件不存在 → 运行该步骤

从第一个缺失输出文件处继续，不重新生成已完成的工作。
想要第二篇论文？选不同 topic，steps 1-3 自动跳过，从步骤 4 开始。
