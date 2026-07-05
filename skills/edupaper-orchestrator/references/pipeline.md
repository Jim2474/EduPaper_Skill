# Pipeline Data-Flow Contract

Detailed data-flow, file-naming, and directory conventions for the EduPaper
pipeline. All skills must follow these conventions so outputs are predictable
and resumable.

## Directory layout (`.edupaper/`)

```
{project-root}/
└── .edupaper/
    ├── project.json            # shared read-only — written by project-parser
    ├── references.json         # shared read-only — written by reference-manager
    ├── topics.json             # written by topic-generator
    ├── materials/
    │   └── {topic-id}/
    │       └── material.json   # written by classroom-generator (per topic)
    ├── drafts/
    │   └── {topic-id}/
    │       ├── paper.md        # written by paper-writer
    │       ├── review-report.md # written by paper-reviewer
    │       └── final.md        # written by humanizer
    ├── consistency-report.md   # written by consistency-checker
    └── papers/                 # final compiled collection
        └── {topic-id}-标题.md
```

## Topic ID convention

- Format: single uppercase letter, assigned by topic-generator in order (A, B, C…)
- Used as directory name under `materials/` and `drafts/`
- Used as filename prefix under `papers/`

## File contracts

Each file is a contract between the producing skill and the consuming skill.

### project.json

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| meta | object | yes | 课题名称, 批准号, 主持人, 单位, 研究周期 |
| 研究对象 | object | yes | 年级, 总人数, 实验班, 对照班 |
| 依据 | object | yes | 课标, 教材, 劳动基地 |
| 核心概念 | array | yes | concept list |
| 术语表 | object | yes | term → definition |
| 研究设计 | object | yes | 研究目标, 研究内容, 研究方法, 创新点 |
| 评价体系 | object | yes | 维度, 指标 |
| 成员分工 | object | yes | name → responsibility |

Writer: project-parser. Readers: all other skills (read-only).

### references.json

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| 课标文献 | array | yes | {标题, 出处, 年份} |
| 教材文献 | array | yes | {学科, 版本, 年级, 单元, 页码} |
| 期刊文献 | array | yes | {作者, 标题, 期刊, 年, 期, 页, 摘要, 相关选题} |
| 其他文献 | array | no | {类型, 标题, 出处, 年份} |

Writer: reference-manager. Readers: paper-writer, paper-reviewer (read-only).

### topics.json

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| topics | array | yes | list of topic objects |
| topics[].id | string | yes | single uppercase letter (A, B, C…) |
| topics[].标题 | string | yes | working title |
| topics[].知识点 | string | yes | e.g. "长方形面积" |
| topics[].劳动场景 | string | yes | e.g. "种植区域测量" |
| topics[].切入点 | string | yes | e.g. "面积量感建构" |
| topics[].类型 | string | yes | 教学案例 / 评价类 / 调查类 / 理论类 |
| topics[].字数 | number | yes | target word count |

Writer: topic-generator. Reader: orchestrator (to select topics), classroom-generator.

### material.json

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| topic_id | string | yes | matches topics.json id |
| 教学设计 | object | yes | 目标, 重难点, 准备, 过程 |
| 课堂实录 | array | yes | 2-3 key dialogue fragments |
| 学生作品 | array | yes | task sheets, measurements, samples |
| 教学反思 | object | yes | 成功, 不足, 改进 |
| 数据素材 | object | yes | 前测, 后测, 对比 |

Writer: classroom-generator. Reader: paper-writer.

### paper.md / reviewed.md / final.md

Markdown files following the teaching-case paper structure defined in
paper-writer's `references/paper-structure.md`.

## One-paper limit enforcement

The orchestrator enforces this at the topic-selection stage:

1. After topic-generator produces topics.json, present the full topic list
   (4-6 options) to the user.
2. Ask the user to select **one** topic.
3. Record the selection and only run stages 4–7 for that single topic.
4. If the user wants another paper, they run the pipeline again — the
   resume logic skips already-completed stages (project.json,
   references.json, topics.json) and jumps straight to topic selection.

This design keeps each run focused: one decision, one paper, one clean
output. Multiple papers accumulate in `.edupaper/drafts/` across runs, and
consistency-checker can compare them.

## Resume logic

Before starting any stage, check whether the expected output file already
exists:

- If it exists and is non-empty, skip that stage (already done).
- If it exists but is empty or malformed, regenerate.
- If it does not exist, run the producing stage.

This allows the pipeline to resume after interruptions without redoing
completed work.

## Stage transition checklist

Before moving from stage N to stage N+1, verify:

- [ ] Stage N's output file exists at the expected path
- [ ] Output file is non-empty
- [ ] Output file passes the skill's self-check (see each skill's references)
- [ ] If self-check failed 3 times, pause and report to user

Do not proceed if any check fails.
