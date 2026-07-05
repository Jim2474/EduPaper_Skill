# EduPaper_Skill

教育科研课题论文批量生成 Skill 集 —— 基于 WorkBuddy / Claude Code Skill 架构。

## 概述

将一份课题开题报告，通过 9 个单一职责 Skill 的流水线，转化为多篇符合学术规范的教学案例论文。

## 架构

```
开题报告(PDF/DOCX/MD)
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  edupaper-orchestrator (编排入口)                     │
│  路由 8 个下游 Skill，执行 2 篇论文限制                │
└─────────────────────────────────────────────────────┘
    │
    ▼
project-parser ──→ .edupaper/project.json          ← 共享只读数据源①
    │
    ▼
reference-manager ──→ .edupaper/references.json    ← 共享只读数据源②
    │
    ▼
topic-generator ──→ .edupaper/topics.json (4-6 选题全菜单)
    │
    ▼  (用户选 ≤2 个选题)
    │
    ├─[选题A]─────────────────────────────────────────┐
    │  classroom-generator → materials/A/material.json │
    │  paper-writer → drafts/A/paper.md                │
    │  paper-reviewer → drafts/A/review-report.md      │
    │  edupaper-humanizer → drafts/A/final.md          │
    ├─[选题B]─────────────────────────────────────────┤
    │  classroom-generator → materials/B/material.json │
    │  paper-writer → drafts/B/paper.md                │
    │  paper-reviewer → drafts/B/review-report.md      │
    │  edupaper-humanizer → drafts/B/final.md          │
    │                                                   │
    ▼                                                   │
consistency-checker → .edupaper/consistency-report.md  │
    │                                                   │
    ▼                                                   │
papers/{topic-id}-标题.md  (最终论文集) ←──────────────┘
```

- **每次最多生成 2 篇论文**（orchestrator 在选题后强制）
- **双共享只读数据源**：project.json + references.json，各由唯一 Skill 写入
- **每个 Skill 单一职责**，通过文件串联，低耦合
- **质量门机制**：每个 Skill 内嵌自检，最多 3 次重试

## Skill 清单

| # | Skill | 职责 | 输入 | 输出 | 状态 |
|---|-------|------|------|------|------|
| 1 | edupaper-orchestrator | 编排入口，路由流程，2篇限制 | 用户指令 | — | ✅ 完成 |
| 2 | project-parser | 解析开题报告 | PDF/DOCX/MD | project.json | ✅ 完成 |
| 3 | reference-manager | 维护文献库 | project.json | references.json | ✅ 完成 |
| 4 | topic-generator | 生成选题矩阵 | project.json | topics.json | ✅ 完成 |
| 5 | classroom-generator | 生成课例素材 | project.json + topics.json | material.json | ✅ 完成 |
| 6 | paper-writer | 写论文初稿 | project.json + material.json + references.json + topics.json | paper.md | ✅ 完成 |
| 7 | paper-reviewer | 学术规范审查 | paper.md + project.json + material.json + references.json | review-report.md | ✅ 完成 |
| 8 | consistency-checker | 跨论文一致性检查 | 所有 paper.md + review-report.md + project.json + references.json | consistency-report.md | ✅ 完成 |
| 9 | edupaper-humanizer | 去 AI 味（包装 humanizer） | paper.md | final.md | ✅ 完成 |

## 数据流契约

```
.edupaper/
├── project.json            # ① 共享只读 — project-parser 写入
├── references.json         # ② 共享只读 — reference-manager 写入
├── topics.json             # topic-generator 写入
├── materials/
│   └── {topic-id}/
│       └── material.json   # classroom-generator 写入（每选题一份）
├── drafts/
│   └── {topic-id}/
│       ├── paper.md        # paper-writer 写入
│       ├── review-report.md # paper-reviewer 写入
│       └── final.md        # edupaper-humanizer 写入
├── consistency-report.md   # consistency-checker 写入
└── papers/
    └── {topic-id}-标题.md   # orchestrator 汇编最终论文集
```

## 安装

```bash
# 克隆仓库
git clone https://github.com/Jim2474/EduPaper_Skill.git

# 将 skills/ 下的各 Skill 复制到 WorkBuddy skills 目录
cp -r EduPaper_Skill/skills/* ~/.workbuddy/skills/

# humanizer 是外部依赖，需单独安装（edupaper-humanizer 会调用它）
# 参见 https://github.com/blader/humanizer
```

## 使用

1. 将开题报告（PDF/DOCX/MD）放入工作目录
2. 告诉 WorkBuddy："用 edupaper-orchestrator 批量生成论文"
3. orchestrator 会依次调用各 Skill，在选题阶段让你选择 ≤2 个选题
4. 最终论文输出到 `.edupaper/papers/` 目录

## 文档

- [架构设计](docs/EduPaper_Skill架构设计.md)
- [集成分析](docs/EduPaper_架构集成分析.md)

## 约束

- 每次运行最多生成 2 篇论文
- 论文类型以教学案例论文为主（1500-3000 字）
- 所有论文共享同一份课题档案（project.json），保证数据一致
- 所有引用遵循 GB/T 7714-2015 中文引用格式标准
- 最终通过 edupaper-humanizer 去 AI 写作痕迹，保留学术内容

## 依赖

- [humanizer](https://github.com/blader/humanizer) — AI 写作痕迹去除（MIT，v2.8.2）

## 许可

MIT
