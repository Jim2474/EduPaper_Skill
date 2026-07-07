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

1. Read `.edupaper/project.json` for meta, 研究对象, 核心概念, 术语表, 评价体系.
2. Read the topic entry from `.edupaper/topics.json` (match by id) for 标题,
   类型, 字数, 知识点, 劳动场景.
3. Read `.edupaper/materials/{topic-id}/material.json` — all five sections.
4. Read `.edupaper/references.json` — select entries whose 相关选题 includes
   this topic id, plus 课标文献 and 教材文献 (always cited).
5. Read `references/paper-structure.md` as the authoritative structure
   blueprint — follow its section sequence, word allocation, and per-section
   guidance. This is the primary spec.
6. Read `assets/templates/paper.md` to understand the placeholder system
   (`{占位符}` markers, dialogue block format, table format). Use it as a
   formatting reference, **not** as a file to copy verbatim. Construct the
   paper from scratch following paper-structure.md; the template shows you
   what each placeholder slot should contain and how to format it.
   For non-教学案例 types, adapt section 4 per the "Adaptations" section
   in paper-structure.md — the template is 教学案例-centric but the spec
   covers all four types.
7. Write the paper section by section (see below). Cite using [n] markers
   mapped to references.json entries; use data from material.json verbatim
   where numbers appear.
8. Append a 参考文献 section listing cited entries in GB/T 7714 format.
9. Write to `.edupaper/drafts/{topic-id}/paper.md`.
10. Run the self-check.

## Sections (teaching-case type)

1. **标题** — from topics.json, may refine wording.
2. **摘要 + 关键词** — 200-300 chars, 3-5 keywords.
3. **问题提出** — background, 课标依据, research gap, this paper's angle.
4. **教学设计与实施** (核心, ~40% of word count) — lesson design, classroom
   implementation, student work, data. Draw from material.json sections 1-3, 5.
5. **教学反思与分析** — what worked, what didn't, 量感 development
   observations. Draw from material.json section 4.
6. **结语** — summary, contribution, limitations, future work.
7. **参考文献** — GB/T 7714 format, only cited entries.

## Self-check (quality gate)

- [ ] All seven sections present and non-empty
- [ ] Word count within topic's 字数 ±10% (1500-3000 range)
- [ ] Every [n] citation has a matching entry in 参考文献
- [ ] Every 参考文献 entry is cited at least once in body
- [ ] Data in paper matches material.json 数据素材 (numbers identical)
- [ ] At least 2 dialogue fragments from 课堂实录 woven into 教学设计与实施
- [ ] At least 1 学生作品 described in body
- [ ] 核心概念 from project.json used with correct definitions
- [ ] 课标文献 cited in 问题提出
- [ ] No fabricated references — all citations trace to references.json
- [ ] No cited 期刊文献 entry has `verified: false` — if a candidate entry
  has `verified: false`, pause and ask user to confirm before including it

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
