---
name: topic-generator
version: 0.1.0
description: |
  Decompose an education research project into a matrix of independently
  writable paper topics. This skill should be used after project.json exists
  and before any materials or papers are generated. It reads the project
  profile's research content and produces topics.json — a list of 4-6 paper
  topics, each defined by a knowledge point, a labor scenario, and a research
  angle. Does not generate materials or write papers. The one-paper-per-run
  limit is enforced downstream by the orchestrator (user selects one from
  this matrix); this skill generates the full menu.
agent_created: true
---

# Topic Generator

Decompose the project into a topic matrix and write it to
`.edupaper/topics.json`. Each topic is a self-contained paper.

## When to trigger

- `.edupaper/project.json` exists and is valid
- `.edupaper/topics.json` does not exist or is empty
- User says "生成选题" / "拆解选题" / "写几篇论文"

## Decomposition formula

Each topic = **知识点 × 劳动场景 × 切入点**

- **知识点**: a specific math concept from the textbook (e.g. 长方形面积)
- **劳动场景**: a concrete labor activity at the base (e.g. 种植区域测量)
- **切入点**: the research lens (e.g. 面积量感建构 / 双螺旋设计 / 评价实践)

No two topics may share all three dimensions. Overlap on one or two is fine;
full overlap is a duplicate.

## Procedure

1. Read `.edupaper/project.json`. Focus on: 研究设计.研究内容, 核心概念,
   依据.劳动基地, 依据.教材.
2. Read `references/topic-schema.md` for field definitions and type guidance.
3. List the knowledge points from 研究内容 (e.g. 面积, 周长, 图形认识).
4. List the labor scenarios from the 劳动基地 context (e.g. 种植测量, 围栏
   规划, 区域划分).
5. List the research angles from 创新点 and 研究方法 (e.g. 量感建构, 双螺旋
   设计, 评价实践, 现状调查, 理论构建).
6. Cross-multiply the three lists. Select 4-6 combinations that are
   meaningful and non-overlapping. Prioritize 教学案例 type (knowledge point
   + labor scenario + 量感 angle).
7. Assign IDs (A, B, C…), titles, types, and target word counts.
8. Write to `.edupaper/topics.json`.
9. Run the self-check.

## Output

Write to `.edupaper/topics.json` — valid JSON, UTF-8, 2-space indent.

## Self-check (quality gate)

- [ ] 4-6 topics generated
- [ ] IDs are sequential uppercase letters (A, B, C…)
- [ ] No two topics share all three of 知识点×场景×切入点
- [ ] Each topic has a non-empty 标题, 知识点, 劳动场景, 切入点
- [ ] 类型 is one of: 教学案例 / 评价类 / 调查类 / 理论类
- [ ] At least 2 topics are 教学案例 type
- [ ] 字数 is between 1500 and 3000
- [ ] JSON is valid and parseable

## Constraints

- Do not generate materials or write papers. Only the topic matrix.
- The one-paper limit is NOT enforced here — generate the full menu (4-6
  topics). The orchestrator asks the user to pick one after this skill
  completes.
- Topics should align with the project's 研究内容 — do not invent knowledge
  points or scenarios outside the project scope.
