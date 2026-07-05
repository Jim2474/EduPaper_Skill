# EduPaper Skill 架构设计

> 纯架构文档。不含 Prompt，不含代码，不含论文内容。
> 目标：将单体 Skill 拆分为低耦合、单一职责的 Skill 集合，适合 Agent 调用与新手使用。

---

## ① 新的目录结构

### Skill 目录（~/.workbuddy/skills/）

```
skills/
├── edupaper-orchestrator/      # 编排入口（新手用）
│   ├── SKILL.md
│   └── references/
│       └── pipeline.md          # 流程顺序与数据流说明
│
├── project-parser/             # 解析开题报告
│   ├── SKILL.md
│   └── references/
│       └── project-schema.md   # project.json 字段定义
│
├── topic-generator/            # 生成选题矩阵
│   ├── SKILL.md
│   └── references/
│       └── topic-schema.md     # topics.json 字段定义
│
├── classroom-generator/        # 生成课例素材
│   ├── SKILL.md
│   ├── references/
│   │   ├── material-schema.md  # material.json 字段定义
│   │   └── textbook-guide.md   # 人教版教材单元依据
│   └── assets/
│       └── templates/
│           └── lesson-plan.md  # 教学设计模板
│
├── paper-writer/               # 写论文初稿
│   ├── SKILL.md
│   ├── references/
│   │   └── paper-structure.md  # 论文结构与字数规范
│   └── assets/
│       └── templates/
│           └── paper.md        # 论文骨架模板
│
├── paper-reviewer/             # 学术规范检查
│   ├── SKILL.md
│   └── references/
│       ├── academic-checklist.md  # 格式/数据/查重检查清单
│       └── citation-gb7714.md    # GB/T 7714 文献格式规范
│
└── humanizer/                  # 去 AI 味（已有，原样复用）
    ├── SKILL.md
    └── LICENSE
```

### 工作区数据目录（每个课题项目内，.edupaper/）

```
课题项目目录/
└── .edupaper/                  # 全部中间产物，不进 skill
    ├── project.json            # 课题档案（Project Memory，所有 skill 共享）
    ├── topics.json             # 选题矩阵
    ├── materials/
    │   ├── topic-A/
    │   │   └── material.json   # 选题A的课例素材
    │   └── topic-B/
    │       └── material.json
    ├── drafts/
    │   ├── topic-A/
    │   │   ├── paper.md        # 初稿
    │   │   ├── reviewed.md     # 规范化后
    │   │   ├── review-report.md # 检查报告
    │   │   └── final.md        # 去 AI 味后（终稿）
    │   └── topic-B/
    │       └── ...
    └── papers/                 # 汇编完成的论文集
        ├── A-面积量感.md
        └── B-周长量感.md
```

**设计要点：**
- Skill 目录只放"怎么做"（指令、规范、模板），不放"做了什么"（数据）
- 工作区 `.edupaper/` 只放"做了什么"（中间产物、终稿），不放"怎么做"
- 两者彻底分离，Skill 可跨课题复用，数据随课题走

---

## ② Skill 拆分方案

| # | Skill 名称 | 单一职责 | 触发方式 |
|---|-----------|---------|---------|
| 0 | edupaper-orchestrator | 流程编排：告诉 agent 下一步调谁 | 用户说"生成论文""跑流程" |
| 1 | project-parser | 解析开题报告 → project.json | 输入是开题报告文件 |
| 2 | topic-generator | 生成选题矩阵 → topics.json | 输入是 project.json |
| 3 | classroom-generator | 生成单个选题的课例素材 → material.json | 输入是单个选题 |
| 4 | paper-writer | 写论文初稿 → paper.md | 输入是 material.json |
| 5 | paper-reviewer | 学术规范检查 → reviewed.md | 输入是 paper.md |
| 6 | humanizer | 去 AI 味 → final.md | 输入是 reviewed.md |

**拆分原则：**
- 每个 Skill 只读输入文件、写输出文件，不直接调用其他 Skill
- Skill 之间唯一的耦合是"数据文件"（JSON/MD），不是函数调用
- 任何一个 Skill 可以独立运行（只要输入文件存在）

---

## ③ 数据流设计

```
开题报告.pdf
     │
     ▼  ┌─ project-parser ─┐
     │  └──────────────────┘
     ▼
project.json  ◄═══════ Project Memory（所有 Skill 共享读取）
     │
     ▼  ┌─ topic-generator ─┐
     │  └───────────────────┘
     ▼
topics.json
     │
     ▼  ┌─ classroom-generator ─┐  （每个选题跑一次）
     │  └───────────────────────┘
     ▼
materials/{topic-id}/material.json
     │
     ▼  ┌─ paper-writer ─┐
     │  └────────────────┘
     ▼
drafts/{topic-id}/paper.md
     │
     ▼  ┌─ paper-reviewer ─┐
     │  └──────────────────┘
     ▼
drafts/{topic-id}/reviewed.md  +  review-report.md
     │
     ▼  ┌─ humanizer ─┐
     │  └─────────────┘
     ▼
drafts/{topic-id}/final.md
     │
     ▼  （复制到 papers/）
papers/{topic-id}-标题.md
```

**数据流规则：**
- 箭头方向严格单向，不回流
- 每个中间文件是"契约"：上游 Skill 的输出 = 下游 Skill 的输入
- project.json 是唯一的共享只读数据，所有 Skill 都可以读，只有 project-parser 能写
- 任何一步失败，只需从该步重跑，不影响上下游

---

## ④ Memory 设计（Project Memory）

### 唯一数据源：`.edupaper/project.json`

所有 Skill 从这里读取课题的固定信息，保证多篇论文之间不矛盾。

**字段设计：**

```
project.json
├── meta                    # 课题元信息
│   ├── 课题名称
│   ├── 批准号
│   ├── 主持人
│   ├── 单位
│   └── 研究周期
│
├── 研究对象                 # 保证所有论文引用一致的人数/班级
│   ├── 年级
│   ├── 总人数
│   ├── 实验班
│   └── 对照班
│
├── 依据                    # 保证所有论文引用一致的课标/教材
│   ├── 课标
│   ├── 教材
│   └── 劳动基地
│
├── 核心概念                 # 保证所有论文用词统一
│   └── [概念列表]
│
├── 术语表                   # key: 术语, value: 统一定义
│   └── { "几何量感": "...", "项目化学习": "..." }
│
├── 研究设计
│   ├── 研究目标
│   ├── 研究内容
│   ├── 研究方法
│   └── 创新点
│
├── 评价体系                 # 保证所有论文评价标准一致
│   ├── 维度
│   └── 指标
│
└── 成员分工                 # 保证论文署名一致
    └── { "姓名": "负责内容" }
```

**为什么这样设计：**
- 人数、班级、教材版本写一次，所有论文引用同一份数据，不会出现"A论文写240人、B论文写220人"的矛盾
- 术语表统一定义，避免不同论文对"几何量感"表述不一致
- 成员分工固化，论文署名与开题报告一致

**读写权限：**

| Skill | 对 project.json 的权限 |
|-------|----------------------|
| project-parser | 写（唯一写入者） |
| 其他所有 Skill | 只读 |

---

## ⑤ 每个 Skill 的职责

### 0. edupaper-orchestrator（编排入口）

- **职责**：流程编排。不做实际工作，只告诉 agent"现在该调哪个 Skill、读写哪个文件"。
- **存在理由**：新手（小学老师）只需说"帮我生成论文"，orchestrator 引导走完全程；高级用户可跳过它直接调单个 Skill。
- **内容**：SKILL.md 极短，只描述流程顺序和文件路径约定。详细流程放 references/pipeline.md。

### 1. project-parser（课题解析）

- **职责**：读取开题报告（PDF/MD/DOCX），提取结构化信息，生成 project.json。
- **不做**：不生成选题、不写论文、不做评价。
- **关键**：这是整个流程的"入口数据"，质量决定后续所有论文的一致性。

### 2. topic-generator（选题矩阵）

- **职责**：读取 project.json，基于研究内容拆解出 N 个可独立成文的选题，生成 topics.json。
- **不做**：不生成素材、不写论文。只决定"写几篇、每篇写什么"。
- **关键**：选题之间不重叠，每个选题 = 知识点 × 劳动场景 × 切入点。

### 3. classroom-generator（课例素材）

- **职责**：读取 project.json + 单个选题，生成该选题的教学素材包 material.json。
- **不做**：不写论文正文。只产出"原料"（教学设计、课堂实录、学生作品、数据）。
- **关键**：素材的"具体性"决定论文的"实操感"和"低查重率"。教材依据放 references/textbook-guide.md。

### 4. paper-writer（论文写作）

- **职责**：读取 project.json + material.json，按论文结构写成初稿 paper.md。
- **不做**：不做格式检查、不去 AI 味。只负责"把素材组织成文章"。
- **关键**：论文结构规范放 references/paper-structure.md，骨架模板放 assets/templates/paper.md。

### 5. paper-reviewer（学术规范）

- **职责**：读取 paper.md，检查格式/文献/数据/查重，输出 reviewed.md + review-report.md。
- **不做**：不重写文章、不去 AI 味。只做"规范化修补"。
- **关键**：检查清单放 references/academic-checklist.md，文献格式放 references/citation-gb7714.md。

### 6. humanizer（去 AI 味）

- **职责**：读取 reviewed.md，去除 AI 写作痕迹，输出 final.md。
- **不做**：不改论文结构、不动数据。只改"语感"。
- **关键**：已有 Skill，原样复用，不修改。

---

## ⑥ 每个 Skill 的输入输出

| Skill | 输入 | 输出 | 依赖的共享数据 |
|-------|------|------|---------------|
| edupaper-orchestrator | 用户意图 | 流程指引（无文件输出） | 无 |
| project-parser | 开题报告文件 | .edupaper/project.json | 无 |
| topic-generator | .edupaper/project.json | .edupaper/topics.json | project.json |
| classroom-generator | .edupaper/topics.json（单个选题） | .edupaper/materials/{id}/material.json | project.json |
| paper-writer | .edupaper/materials/{id}/material.json | .edupaper/drafts/{id}/paper.md | project.json |
| paper-reviewer | .edupaper/drafts/{id}/paper.md | .edupaper/drafts/{id}/reviewed.md + review-report.md | project.json |
| humanizer | .edupaper/drafts/{id}/reviewed.md | .edupaper/drafts/{id}/final.md | 无 |

**输入输出原则：**
- 每个 Skill 的输入是"文件路径"，输出是"文件路径"，不依赖内存传递
- agent 调用任何 Skill 时，只需告诉它"读哪个文件、写哪个文件"
- 中间文件全部落在 `.edupaper/` 下，可追溯、可重跑

---

## ⑦ 哪些应该保留

| 保留项 | 理由 |
|-------|------|
| 六阶段流水线的顺序逻辑 | 顺序正确，无需改 |
| 选题矩阵的概念（选题 = 知识点 × 场景 × 切入点） | 拆解逻辑有效 |
| 课题档案作为"母本"的设计 | 升级为 project.json，作为唯一共享数据源 |
| humanizer Skill | 已独立、已验证，原样复用 |
| 论文结构模板（标题→摘要→问题→设计→反思→结语→文献） | 结构合理 |
| GB/T 7714 文献格式要求 | 学术规范必需 |

---

## ⑧ 哪些应该删除

| 删除项 | 理由 |
|-------|------|
| 单体 Skill 中各阶段重复的质量要求描述 | 拆分后每个 Skill 只管自己的质量标准，消除重复 |
| SKILL.md 中的详细论文写作技巧 | 移到 paper-writer/references/paper-structure.md，不占 Prompt |
| SKILL.md 中的教材内容（人教版单元分析） | 移到 classroom-generator/references/textbook-guide.md |
| SKILL.md 中的检查清单全文 | 移到 paper-reviewer/references/academic-checklist.md |
| 各阶段之间"如果上一步失败怎么办"的分支逻辑 | 数据流是单向文件流，失败只需重跑当前步，不需要分支 |
| 方案文档中的"待确认事项"等讨论性内容 | 不属于 Skill，属于项目记忆 |

---

## ⑨ 哪些应该合并

| 合并项 | 合并到 | 理由 |
|-------|-------|------|
| 课题档案提取 + Project Memory | project-parser 产出 project.json | 档案即记忆，不需要两份 |
| 格式检查 + 查重预检 | paper-reviewer | 都是"规范化"职责，一个 Skill 统一做 |
| 学术规范 + Humanizer？ | **不合并** | 规范化改的是"格式"，去 AI 味改的是"语感"，职责不同，保持分离 |
| 教学设计生成 + 课堂实录生成 + 学生作品生成 | classroom-generator | 都是"素材生成"职责，一个 Skill 产出一个 material.json |

---

## ⑩ 最终推荐架构

### 架构总览

```
                    ┌─────────────────────────────┐
                    │   edupaper-orchestrator      │  ← 新手入口
                    │   （只做路由，不做实际工作）   │
                    └──────────────┬──────────────┘
                                   │ 指引顺序
          ┌────────────────────────┼────────────────────────┐
          ▼                        ▼                        ▼
   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
   │   project   │         │    topic    │         │ classroom   │
   │   parser    │ ──────► │  generator  │ ──────► │  generator  │
   └──────┬──────┘         └──────┬──────┘         └──────┬──────┘
          │                       │                       │
          ▼                       ▼                       ▼
    project.json            topics.json           material.json
     (Memory)                                            │
     ◄──共享只读─── ── ── ── ── ── ── ── ── ── ── ── ── ┘
          │                                              │
          │              ┌─────────────┐                 │
          │              │    paper    │ ◄───────────────┘
          └────────────► │   writer    │
                         └──────┬──────┘
                                ▼
                           paper.md
                                │
                         ┌──────┴──────┐
                         │  paper      │
                         │  reviewer   │
                         └──────┬──────┘
                                ▼
                          reviewed.md
                                │
                         ┌──────┴──────┐
                         │ humanizer   │  ← 已有，复用
                         └──────┬──────┘
                                ▼
                           final.md
                                │
                                ▼
                           papers/  （论文集）
```

### 内容分层规则（Prompt / Reference / Memory / Template）

| 内容类型 | 存放位置 | 加载时机 | 例子 |
|---------|---------|---------|------|
| **Prompt**（触发条件 + 操作步骤 + I/O 路径） | SKILL.md | Skill 触发时自动加载 | "读取 .edupaper/project.json，生成 topics.json" |
| **Reference**（详细规范、Schema、检查清单） | references/*.md | Skill 运行中按需加载 | project-schema.md、citation-gb7714.md |
| **Memory**（跨 Skill 共享的课题数据） | .edupaper/project.json | 所有 Skill 只读 | 人数、教材、术语表 |
| **Template**（输出骨架） | assets/templates/* | 写文件时复制使用 | paper.md 骨架、lesson-plan.md |

**SKILL.md 长度目标：每个 < 500 字。** 详细内容全部下沉到 references/。

### 设计原则总结

1. **单一职责**：每个 Skill 只做一件事，输入一个文件、输出一个文件
2. **数据流单向**：JSON/MD 文件串联，不回流、不跳步
3. **共享只读 Memory**：project.json 是唯一共享数据，只 project-parser 可写
4. **Prompt 极短**：SKILL.md 只留触发条件和 I/O 路径，规范下沉 references/
5. **低耦合**：Skill 之间不互相调用，只通过文件交接
6. **可独立运行**：任何 Skill 只要输入文件存在就能单独跑
7. **可复用**：换课题只需替换 project.json，Skill 不动
8. **新手友好**：orchestrator 做入口，一句话启动全流程

### 对比：改造前 vs 改造后

| 维度 | 改造前（单体） | 改造后（拆分） |
|------|--------------|--------------|
| Skill 数量 | 1 个大 Skill | 7 个小 Skill |
| 单个 SKILL.md 长度 | ~5000 字 | < 500 字 |
| 复用性 | 整体复用或不用 | 每个 Skill 独立复用 |
| 维护 | 改一处影响全局 | 改一个 Skill 不影响其他 |
| Context 占用 | 一次性全加载 | 按需加载 references |
| 失败恢复 | 从头重跑 | 从失败步骤重跑 |
| 新手使用 | 需理解整个流程 | 一句话触发 orchestrator |
| 多课题扩展 | 复制整个 Skill | 换 project.json 即可 |

---

*架构设计完成。不含 Prompt、不含代码、不含论文内容。*
