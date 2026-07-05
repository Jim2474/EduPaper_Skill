---
name: reference-manager
version: 0.1.0
description: |
  Build and maintain a shared reference library (references.json) for an
  education research project. This skill should be used after project-parser
  has produced project.json and before any paper is drafted. It reads the
  project profile to determine which curriculum standards, textbooks, and
  journals apply, then assembles a structured literature library that all
  papers cite consistently. It is the sole writer of references.json — the
  second shared read-only data source in the pipeline.
agent_created: true
---

# Reference Manager

Assemble a shared reference library from the project profile and write it to
`.edupaper/references.json`. All downstream papers cite from this single
library, ensuring no paper invents or contradicts references.

## When to trigger

- `.edupaper/project.json` exists and is valid
- `.edupaper/references.json` does not exist or is empty
- User says "建立文献库" / "整理参考文献"

## Procedure

1. Read `.edupaper/project.json`. Extract: 依据.课标, 依据.教材, 依据.劳动基地,
   研究设计.研究内容, 核心概念.
2. Read `references/reference-schema.md` for the four library categories and
   their field definitions.
3. Read `references/citation-gb7714.md` for GB/T 7714 citation formatting.
4. Assemble the library in four categories:
   - **课标文献**: the curriculum standards named in 依据 (always include
     both 数学课标 and 劳动课标 if the project spans both).
   - **教材文献**: the textbook units relevant to the 研究内容. Specify exact
     unit and page numbers.
   - **期刊文献**: 6-10 education research journal articles relevant to the
     核心概念. Prefer 2020+ publications from journals like 《小学数学教师》
     《教学与管理》《数学教育学报》《课程·教材·教法》.
   - **其他文献**: supplementary sources (政策文件, 学位论文, 网络资源).
5. For each 期刊文献 entry, fill the 相关选题 field to indicate which paper
   topics it supports (use topic letters A, B, C… matching topics.json).
6. Write to `.edupaper/references.json`.
7. Run the self-check below.

## Output

Write to `.edupaper/references.json` — valid JSON, UTF-8, 2-space indent.

## Self-check (quality gate)

- [ ] 课标文献 has at least 1 entry (the project's 课标)
- [ ] 教材文献 has at least 1 entry with specific 单元 and 页码
- [ ] 期刊文献 has 6-10 entries, each with 作者/标题/期刊/年/期/页
- [ ] Every 期刊文献 entry has a non-empty 摘要
- [ ] Every 期刊文献 entry has 相关选题 filled (at least one topic letter)
- [ ] No duplicate entries (same 作者+标题+年)
- [ ] JSON is valid and parseable

If any check fails, fix and re-check (max 3 retries). After 3 failures, write
the file and report the gaps.

## Constraints

- This skill is the **sole writer** of references.json. If it already exists
  and is valid, skip.
- References must be real and findable — do not fabricate citations. If unsure
  whether a specific article exists, omit it rather than guess.
- All citations follow GB/T 7714 format (see `references/citation-gb7714.md`).
- Do not write paper content or generate topics. This skill only builds the
  reference library.
