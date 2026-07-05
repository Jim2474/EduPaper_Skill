# EduPaper 架构集成分析

> 基于 paper-writer-skill（kgraph57/paper-writer-skill）的架构参考，集成进 EduPaper。
> 仅参考架构与实现模式，不照搬 Prompt，不复制医学领域内容。
> 目标：复用值得复用的，不重复建设已有的，重新实现需要适配的。

---

## 一、paper-writer-skill 架构概览

### 它是什么
面向医学/科学论文的完整写作 Skill，83 个文件（37 模板 + 30 参考 + 8 脚本 + 测试）。核心创新：把线性写作流水线升级为"研究引擎循环"。

### 它的架构亮点（值得参考的部分）

| 架构模式 | 做法 | 价值 |
|---------|------|------|
| **质量门系统** | 每阶段有 Gate，PASS 才进下一步，FAIL 自动修复（最多3次），再不行升级用户 | 防止错误向后传播 |
| **文献矩阵** | 结构化文献对比表 + 引用计划 + 差距分析 | 引用有据可查、不重复 |
| **对抗性自审** | 提交前红队攻击自己的核心论点，KILL 则回炉 | 防止"自信的垃圾" |
| **模板/参考分离** | templates/ 放输出骨架，references/ 放指南规范 | context 按需加载 |
| **项目目录结构** | sections/、data/、tables/、figures/、submissions/、revisions/ | 产物可追溯 |
| **人类主权门** | IDEA（选题/伦理）和 DATA（真实数据）两个门必须人类把关 | 防止 AI 越界 |
| **章节质量清单** | 每个章节有 checkbox 检查清单 | 检查标准化 |
| **可重入流水线** | Phase −1 可从中间步骤进入，不强制从头 | 适配不同起点 |

### 它的领域专用部分（不适合教育科研）

| 能力 | 不借鉴原因 |
|------|-----------|
| IRB 伦理审查 / 预注册 / PROSPERO | 医学临床试验专用 |
| PRISMA / CONSORT / STROBE / CARE 等报告指南 | 医学研究报告规范，教育科研不用 |
| PubMed / 系统综述检索流水线 | 教育科研用知网/万方，检索方式不同 |
| 统计报告（SAMPL）/ 功效分析 / 森林图 | 教学案例论文不做统计推断 |
| 7 并行 Agent（haiku/sonnet/opus 分工） | WorkBuddy 是单 Agent 模式 |
| 期刊投稿 portal / cover letter / 级联投稿 | 教育科研小课题是结题论文集，不投期刊 |
| IMRAD 结构 | 教学案例论文用"问题→设计→实施→反思→结语"结构 |
| 多语言（EN/JP）| 本项目是中文教育科研 |

---

## 二、能力映射表

### 复用（借鉴架构模式，不抄 Prompt）

| paper-writer-skill 能力 | EduPaper 集成方式 |
|------------------------|------------------|
| 质量门系统（8门+自动修复） | 简化为**每 Skill 内嵌自检**，检查教育科研标准，最多重试3次。不做独立门系统，保持单一职责 |
| 文献矩阵（对比表+引用计划+差距分析） | 改造为 **reference-manager Skill**，管理课标/教材/教育学期刊文献，产出 references.json |
| 对抗性自审（红队攻击） | 改造为 **consistency-checker Skill**，做多论文一致性检查（人数/术语/数据不矛盾） |
| 模板/参考分离 | 已有，强化：教学案例论文模板放 assets/，规范放 references/ |
| 章节质量清单 | 改造为 paper-reviewer 的 references/academic-checklist.md，用教育科研标准 |
| 项目目录结构 | 借鉴，.edupaper/ 增加 sections/ 结构 |

### 已存在（不重复建设）

| 能力 | EduPaper 已有对应 |
|------|------------------|
| 流水线阶段划分 | 6阶段已有（解析→选题→素材→写作→规范→去AI味） |
| 文件数据流（JSON/MD 中间产物） | project.json→topics.json→material.json→paper.md 已有 |
| Humanizer 去 AI 味 | humanizer Skill 已全局部署，直接复用 |
| Project Memory（共享数据） | project.json 已有，所有 Skill 只读 |
| 论文结构模板 | paper-writer 的 assets/templates/ 已有 |

### 重新实现（适配教育科研）

| 能力 | 重新实现方式 |
|------|------------|
| 质量门标准 | 用教育科研标准：教学情境真实性、师生对话自然度、课标契合度、数据合理性（非 IMRAD/STROBE） |
| 文献矩阵 | 文献源改为：课标(2022版)、人教版教材、教育学期刊（《小学数学教师》《教学与管理》等），非 PubMed |
| 对抗性审查 | 改为跨论文一致性检查：多篇论文之间人数/术语/数据/引用是否矛盾，非统计方法学红队 |
| 论文结构 | 教学案例论文结构（标题→摘要→问题→设计→实施→反思→结语→文献），非 IMRAD |
| 引用格式 | GB/T 7714 中文格式，非 Vancouver/APA |

### 不借鉴

| 能力 | 原因 |
|------|------|
| 预注册护栏 / HARKing 防护 | 教育科研小课题不做假设预注册 |
| 新颖性检查（实时文献比对） | 教育科研小课题选题已由开题报告确定，不需实时查新 |
| 临床试验注册 | 不适用 |
| 统计报告规范 | 教学案例论文不做统计推断 |
| 多 Agent 并行 | WorkBuddy 单 Agent |
| 投稿/修稿/级联投稿 | 小课题是结题论文集，不投期刊 |

---

## 三、更新后的架构（7 → 9 Skill）

### 新增 2 个 Skill

| 新 Skill | 来源 | 职责 |
|---------|------|------|
| **reference-manager** | 改造自文献矩阵 | 维护课题共享文献库，产出 references.json，所有论文引用同一份 |
| **consistency-checker** | 改造自对抗性自审 | 全部论文成稿后，跨论文检查一致性，产出 consistency-report.md |

### 9 Skill 完整清单

| # | Skill | 职责 | 输入 → 输出 | 质量门 |
|---|-------|------|------------|--------|
| 0 | edupaper-orchestrator | 编排入口 | 用户意图 → 流程指引 | 无 |
| 1 | project-parser | 解析开题报告 | 开题报告 → project.json | 字段完整性 |
| 2 | **reference-manager** | 维护文献库 | project.json → references.json | 文献可查性 |
| 3 | topic-generator | 生成选题矩阵 | project.json → topics.json | 选题不重叠 |
| 4 | classroom-generator | 生成课例素材 | 选题+project → material.json | 素材具体性 |
| 5 | paper-writer | 写论文初稿 | material+references → paper.md | 结构完整性 |
| 6 | paper-reviewer | 学术规范检查 | paper.md → reviewed.md | 规范通过率 |
| 7 | humanizer | 去 AI 味 | reviewed.md → final.md | AI痕迹=0 |
| 8 | **consistency-checker** | 跨论文一致性 | 所有 final.md → consistency-report.md | 矛盾=0 |

---

## 四、更新后的数据流

```
开题报告
    │
    ▼  [project-parser]
project.json  ◄═══════ 共享只读 Memory
    │
    ├──► [reference-manager] ──► references.json  ◄══ 共享只读文献库
    │
    ▼  [topic-generator]
topics.json
    │
    ▼  [classroom-generator]  （每个选题跑一次，读 project.json）
materials/{id}/material.json
    │
    ▼  [paper-writer]  （读 project.json + references.json）
drafts/{id}/paper.md
    │
    ▼  [paper-reviewer]
drafts/{id}/reviewed.md  +  review-report.md
    │
    ▼  [humanizer]
drafts/{id}/final.md
    │
    ▼  [consistency-checker]  （读所有 final.md + project.json + references.json）
consistency-report.md
    │
    ▼
papers/  论文集
```

**关键变化：**
- references.json 成为第二个共享只读数据源（与 project.json 并列）
- consistency-checker 是终末环节，在所有论文都去完 AI 味后才跑
- 每步都有质量门（自检），但不做成独立系统

---

## 五、质量门设计（借鉴 paper-writer-skill，简化）

### 设计原则
- 不做独立的质量门系统（保持 Skill 单一职责）
- 每个 Skill 在写输出文件前**自检**，自检失败则重试（最多3次），再不行标记问题继续
- 自检标准放该 Skill 的 references/ 下

### 各 Skill 质量门标准

| Skill | 自检内容 | 通过标准 |
|-------|---------|---------|
| project-parser | 必填字段是否齐全 | meta/研究对象/依据/研究设计 无空缺 |
| reference-manager | 文献是否真实可查 | 每条文献有作者/标题/出处，课标和教材必有 |
| topic-generator | 选题是否重叠 | 任意两选题的知识点×场景×切入点 不完全相同 |
| classroom-generator | 素材是否具体 | 有具体尺寸/作物名/步骤/师生对话，无空泛描述 |
| paper-writer | 结构是否完整 | 标题/摘要/关键词/问题/设计/实施/反思/结语/文献 齐全 |
| paper-reviewer | 规范是否通过 | 格式/文献格式/字数/查重预估 全部达标 |
| humanizer | AI 痕迹是否清除 | 33 种 AI 写作模式扫描，高优先级=0 |
| consistency-checker | 跨论文是否矛盾 | 人数/术语/教材/引用 跨论文一致 |

### 自检流程（每个 Skill 内部）

```
生成输出 → 自检
  ├─ PASS → 写入文件，进入下一步
  ├─ FAIL（重试<3）→ 修正问题 → 重新自检
  └─ FAIL（重试≥3）→ 标记问题写入文件，在 review-report 中记录，继续
```

---

## 六、新增 Skill 详细设计

### reference-manager（文献库管理）

**职责**：维护课题的共享文献库，确保所有论文引用同一份真实文献。

**输入**：project.json
**输出**：.edupaper/references.json

**references.json 结构**：
```
{
  "课标文献": [{ 标题, 出处, 年份, 引用位置建议 }],
  "教材文献": [{ 学科, 版本, 年级, 单元, 页码 }],
  "期刊文献": [{ 作者, 标题, 期刊, 年, 期, 页, DOI, 摘要, 相关选题 }],
  "其他文献": [{ 类型, 标题, 出处, 年份 }]
}
```

**与 paper-writer-skill 文献矩阵的差异**：
- 文献源：知网/万方/维普（非 PubMed）
- 矩阵字段：去掉 Design/N/Population/Intervention，改为 学段/学科/研究方法/核心观点
- 引用计划：按论文选题分配，而非按 IMRAD 章节分配
- 不做实时检索（教育科研文献量小，人工确认即可）

**references/** 内容：
- `reference-schema.md`：references.json 字段定义
- `citation-gb7714.md`：GB/T 7714 中文引用格式规范

### consistency-checker（跨论文一致性检查）

**职责**：所有论文成稿后，检查多篇论文之间是否存在矛盾。这是 paper-writer-skill 对抗性自审的教育科研适配版。

**输入**：所有 final.md + project.json + references.json
**输出**：.edupaper/consistency-report.md

**检查维度**：

| 检查项 | 检查内容 | 严重度 |
|--------|---------|--------|
| 数据一致性 | 人数/班级/教材版本 跨论文是否矛盾 | 致命 |
| 术语一致性 | 同一术语在不同论文中定义/用法是否一致 | 致命 |
| 引用一致性 | 引用的文献是否都在 references.json 中 | 重要 |
| 选题不重叠 | 两篇论文是否覆盖相同知识点×场景 | 重要 |
| 署名一致性 | 署名是否与 project.json 成员分工一致 | 重要 |
| AI 痕迹模式 | 跨论文是否有重复的 AI 写作模式 | 一般 |
| 课标引用一致 | 引用课标条款是否跨论文一致 | 一般 |

**与 paper-writer-skill 对抗性自审的差异**：
- 不攻击统计方法学（教学案例论文无统计推断）
- 不做"证伪零假设"的 steelman
- 改为跨论文一致性（因为我们是批量生成，一致性问题比单篇质量更突出）
- KILL 标准：出现"致命"级矛盾才 KILL，要求重写

---

## 七、更新后的目录结构

### Skill 目录（~/.workbuddy/skills/）

```
skills/
├── edupaper-orchestrator/
│   ├── SKILL.md
│   └── references/
│       └── pipeline.md
│
├── project-parser/
│   ├── SKILL.md
│   └── references/
│       └── project-schema.md
│
├── reference-manager/          # NEW
│   ├── SKILL.md
│   └── references/
│       ├── reference-schema.md
│       └── citation-gb7714.md
│
├── topic-generator/
│   ├── SKILL.md
│   └── references/
│       └── topic-schema.md
│
├── classroom-generator/
│   ├── SKILL.md
│   ├── references/
│   │   ├── material-schema.md
│   │   └── textbook-guide.md
│   └── assets/templates/
│       └── lesson-plan.md
│
├── paper-writer/
│   ├── SKILL.md
│   ├── references/
│   │   ├── paper-structure.md
│   │   └── quality-gate-pattern.md   # NEW: 共享自检模式说明
│   └── assets/templates/
│       └── paper.md
│
├── paper-reviewer/
│   ├── SKILL.md
│   └── references/
│       ├── academic-checklist.md
│       └── plagiarism-guide.md       # NEW: 查重策略
│
├── consistency-checker/        # NEW
│   ├── SKILL.md
│   └── references/
│       └── consistency-rules.md
│
└── humanizer/                  # 已有，原样复用
    └── SKILL.md
```

### 工作区数据目录（.edupaper/）

```
.edupaper/
├── project.json              # 课题档案（共享只读）
├── references.json           # NEW: 共享文献库（共享只读）
├── topics.json               # 选题矩阵
├── materials/
│   └── {topic-id}/
│       └── material.json
├── drafts/
│   └── {topic-id}/
│       ├── paper.md          # 初稿
│       ├── review-report.md  # 规范检查报告
│       └── final.md          # 去AI味后
├── consistency-report.md     # NEW: 跨论文一致性报告
└── papers/                   # 论文集终稿
    └── {topic-id}-标题.md
```

---

## 八、最终推荐架构总结

### 共享只读数据源（2个）

| 数据源 | 内容 | 唯一写入者 |
|--------|------|-----------|
| project.json | 课题档案（人数/教材/术语/分工） | project-parser |
| references.json | 文献库（课标/教材/期刊文献） | reference-manager |

### 流水线（9 Skill，2个共享数据源）

```
开题报告
  ↓ [project-parser]        → project.json ◄──共享──┐
  ↓ [reference-manager]     → references.json ◄共享─┤
  ↓ [topic-generator]       → topics.json           │
  ↓ [classroom-generator]   → material.json (×N)    │ 读
  ↓ [paper-writer]          → paper.md (×N)         │ 取
  ↓ [paper-reviewer]        → reviewed.md (×N)      │ 共
  ↓ [humanizer]             → final.md (×N)         │ 享
  ↓ [consistency-checker]   → consistency-report.md ┘
  ↓
papers/ 论文集
```

### 对比：集成前 vs 集成后

| 维度 | 集成前（7 Skill） | 集成后（9 Skill） |
|------|------------------|------------------|
| Skill 数量 | 7 | 9 |
| 共享数据源 | 1（project.json） | 2（+references.json） |
| 质量保障 | 无自检 | 每 Skill 内嵌自检（最多3次重试） |
| 文献管理 | 无（各论文自己找） | 统一文献库，所有论文引用一致 |
| 跨论文检查 | 无 | consistency-checker 终末检查 |
| 引用一致性 | 无保障 | references.json 统一管理 |
| 错误传播 | 错误向后传 | 自检拦截 + 终末检查兜底 |

### 借鉴了什么 / 没借鉴什么

**借鉴了（架构模式）：**
- 质量门 → 简化为内嵌自检
- 文献矩阵 → 改造为 reference-manager
- 对抗性自审 → 改造为 consistency-checker
- 模板/参考分离 → 强化
- 项目目录结构 → 借鉴

**没借鉴（领域不匹配）：**
- 医学报告指南（PRISMA/CONSORT/STROBE）
- 预注册/新颖性检查/临床试验注册
- 统计报告/功效分析
- 多 Agent 并行
- 期刊投稿流程
- IMRAD 结构
- 多语言

**没重复建设（已有）：**
- 流水线阶段
- 文件数据流
- Humanizer
- Project Memory
- 模板/参考分离

---

*集成分析完成。仅参考架构，未照搬 Prompt，未复制医学领域内容。*
