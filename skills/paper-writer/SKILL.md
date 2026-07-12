---
name: paper-writer
version: 0.2.0
description: |
  撰写单个选题的教学案例论文或教学论文草稿。当需要根据教学素材（material.json）、
  课题基本信息（project.json）和文献库（references.json）撰写具体的论文正文时触发。
  触发词：撰写论文 / 写论文草稿 / 论文初稿生成 / write draft paper / paper writing /
  开始写论文 / 论文写作 / 生成论文正文。
  本 skill 仅负责论文草稿撰写（生成 paper.md），不进行评审或去 AI 痕迹润色。
agent_created: false
---

# Paper Writer

Write a complete draft paper for one topic and save it to
`.edupaper/drafts/{topic-id}/paper.md`.

## When to trigger

- User has selected a topic and classroom-generator has produced
  `.edupaper/materials/{topic-id}/material.json`
- `.edupaper/project.json` and `.edupaper/references.json` exist
- `.edupaper/drafts/{topic-id}/paper.md` does not exist

## Procedure

1. 读 `.edupaper/project.json` for meta, 研究对象, 核心概念, 术语表, 评价体系.
2. 读 the topic entry from `.edupaper/topics.json` (match by id) for 标题, 类型, 字数, 知识点, 劳动场景.
3. 读 `.edupaper/materials/{topic-id}/material.json` — all five sections.
4. **问卷调查数据读取（若存在）**：检测 `.edupaper/surveys/survey-report.md` 是否存在，若存在则读取其中的调查问卷数据、维度分析及各项百分比指标。
5. 读 `.edupaper/references.json` — select entries whose 相关选题 includes this topic id, plus 课标文献 and 教材文献 (always cited).
6. 读 `references/paper-structure.md` as the authoritative structure blueprint — follow its section sequence, word allocation, and per-section guidance.
7. 读 `references/format-spec.md` for detailed formatting rules (heading levels, citation format, table structure, dialogue block syntax). Apply these throughout writing.
8. 读 `assets/templates/paper.md` to understand the placeholder system (`{占位符}` markers, dialogue block format, table format). Construct the paper from scratch following paper-structure.md; the template shows you what each placeholder slot should contain and how to format it.
8. 撰写论文各章节（见下方说明）。**问卷数据整合规则**：若有问卷数据，必须在论文中强力编织问卷分析：
   - 在 **问题提出** 中：引用问卷前测发现（如“问卷调查显示，有 XX% 的学生对平方米无直观表象”），作为本教学设计的现实依据。
   - 在 **教学设计与实施（教学效果数据）** 中：除了测试分数对比表格，必须增加问卷后测百分比分析（如学习兴趣提升、估测信心变化，引用的百分比须与 survey-report.md 一致），并列举 1-2 道典型问卷题目。
9. **字数硬验证（写入前）**：统计全文汉字数量（不含标题、参考文献区）。
   - 目标区间：topic 的 `字数` ±10%（通常 2250–2750）
   - 若超出上限（>字数×1.1）：找出最长的子章节，压缩至核心观点；删除冗余过渡句；附录内容移至独立 MD 文件，不计入正文字数。
   - 若低于下限（<字数×0.9）：在教学反思或问题提出中补充具体事例。
   - 确认在范围内后再执行步骤 10。
10. **引用双向核对（写入前）**：列出 `[1]...[n]` 所有编号 → 确认每个编号在正文中至少出现一次 → 确认参考文献区每条都有对应编号引用。孤儿条目（有编号无引用）必须删除或在正文中补充引用，不得留在参考文献区。
11. 写入 `.edupaper/drafts/{topic-id}/paper.md`。
12. 读 `../_shared/quality-gate.md` 执行通用质量门 + 下方 self-check。

## Sections (teaching-case type)

1. **标题** — from topics.json, may refine wording.
2. **摘要 + 关键词** — 200-300 chars, 3-5 keywords.
3. **问题提出** — background, 课标依据, research gap, this paper's angle. (若有问卷，需融入前测问卷痛点分析)
4. **教学设计与实施** (核心, ~40% of word count) — lesson design, classroom implementation, student work, data. (若有问卷，必须在效果数据中增加后测问卷维度分析和题目列举)
5. **教学反思与分析** — what worked, what didn't, 量感 development observations.
6. **结语** — summary, contribution, limitations, future work.
7. **参考文献** — GB/T 7714 format, only cited entries.

## Self-check (quality gate)

- [ ] All seven sections present and non-empty
- [ ] **汉字计数在目标 ±10% 范围内**（附录不计入正文字数）：实际 _____ 字，目标 _____ 字
- [ ] Every [n] citation has a matching entry in 参考文献
- [ ] **Every 参考文献 entry is cited at least once in body**（逐条核对，无孤儿条目）
- [ ] Data in paper matches material.json 数据素材 (numbers identical)
- [ ] **问卷数据整合校验**：若有问卷要求，论文中必须包含对问卷设计维度、典型问题（至少列出一道）及后测百分比数据的定量分析，且数据与 survey-report.md 完全一致。
- [ ] At least 2 dialogue fragments from 课堂实录 woven into 教学设计与实施
- [ ] At least 1 学生作品 described in body
- [ ] 核心概念 from project.json used with correct definitions
- [ ] 课标文献 cited in 问题提出
- [ ] No fabricated references — all citations trace to references.json
- [ ] No cited 期刊文献 entry has `verified: false` — if a candidate entry has `verified: false`, pause and ask user to confirm before including it

## Constraints

- Write prose, not bullet points (except where structure requires).
- Do not invent data beyond material.json. If material is thin, note it and
  keep the section proportional.
- Match the topic's 类型 — 教学案例 papers follow the structure above; for
  other types (评价类/调查类/理论类) adapt section 4 per paper-structure.md.
- Do not polish style — humanizer handles that. Focus on structure and
  content completeness.
- Cite 课标文献 and 教材文献 in every paper; cite 期刊文献 selectively by
  relevance to the topic.
- **Do not cite any 期刊文献 entry with `verified: false`** without first
  pausing and confirming with the user. If all available entries for a topic
  are unverified, report this before writing the paper.
