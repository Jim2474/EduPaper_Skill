# EduPaper_Skill

教育科研课题论文批量生成 Skill 集 —— 基于 WorkBuddy / Claude Code Skill 架构。

## 概述

将一份课题开题报告，通过 9 个单一职责 Skill 的流水线，转化为多篇符合学术规范的教学案例论文。

## 架构

```
开题报告 → project-parser → project.json
                              ↓
                    reference-manager → references.json
                              ↓
                    topic-generator → topics.json
                              ↓
              classroom-generator → material.json (×N)
                              ↓
              paper-writer → paper.md (×N)
                              ↓
              paper-reviewer → reviewed.md (×N)
                              ↓
              humanizer → final.md (×N)
                              ↓
              consistency-checker → consistency-report.md
                              ↓
                          papers/ 论文集
```

- **每次最多生成 2 篇论文**
- **双共享只读数据源**：project.json + references.json
- **每个 Skill 单一职责**，通过文件串联，低耦合

## Skill 清单

| # | Skill | 职责 | 状态 |
|---|-------|------|------|
| 0 | edupaper-orchestrator | 编排入口，路由流程 | 开发中 |
| 1 | project-parser | 解析开题报告 → project.json | 待开发 |
| 2 | reference-manager | 维护文献库 → references.json | 待开发 |
| 3 | topic-generator | 生成选题矩阵 → topics.json | 待开发 |
| 4 | classroom-generator | 生成课例素材 → material.json | 待开发 |
| 5 | paper-writer | 写论文初稿 → paper.md | 待开发 |
| 6 | paper-reviewer | 学术规范检查 → reviewed.md | 待开发 |
| 7 | consistency-checker | 跨论文一致性检查 | 待开发 |
| 8 | humanizer | 去 AI 味（已有，复用） | 已就绪 |

## 安装

```bash
# 克隆仓库
git clone https://github.com/Jim2474/EduPaper_Skill.git

# 将 skills/ 下的各 Skill 复制到 WorkBuddy skills 目录
cp -r EduPaper_Skill/skills/* ~/.workbuddy/skills/
```

## 文档

- [架构设计](docs/EduPaper_Skill架构设计.md)
- [集成分析](docs/EduPaper_架构集成分析.md)

## 约束

- 每次运行最多生成 2 篇论文
- 论文类型以教学案例论文为主（1500-3000 字）
- 所有论文共享同一份课题档案（project.json），保证数据一致
- 最终通过 humanizer 去 AI 写作痕迹

## 许可

MIT
