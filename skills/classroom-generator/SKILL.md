---
name: classroom-generator
version: 0.1.0
description: |
  Generate teaching materials for a single paper topic — lesson plan, classroom
  dialogue fragments, student work samples, teaching reflection, and assessment
  data. This skill should be used after the user has selected topics from
  topics.json and before paper-writer runs. It reads project.json and one topic
  from topics.json, then produces material.json. Since education research
  projects often lack pre-collected data, this skill generates plausible,
  specific materials grounded in the real textbook and labor-base context.
  Does not write paper prose — only raw materials.
agent_created: true
---

# Classroom Generator

Generate a complete material package for one topic and write it to
`.edupaper/materials/{topic-id}/material.json`.

## When to trigger

- User has selected a topic from topics.json (e.g. "选题A")
- `.edupaper/project.json` and `.edupaper/topics.json` exist
- `.edupaper/materials/{topic-id}/material.json` does not exist

## Procedure

1. Read `.edupaper/project.json` for 研究对象, 依据, 评价体系, 术语表.
2. Read the selected topic from `.edupaper/topics.json` (match by id).
3. Read `references/material-schema.md` for the five material sections and
   their field definitions.
4. Read `references/textbook-guide.md` to find the exact textbook unit and
   page numbers for the topic's 知识点.
5. Copy `assets/templates/lesson-plan.md` as the starting structure for the
   教学设计 section.
6. Generate all five material sections (see below). Ground every detail in
   the real textbook content and the project's labor-base context.
7. Write to `.edupaper/materials/{topic-id}/material.json`.
8. Run the self-check.

## Five material sections

1. **教学设计** — goals (math + labor + 量感), key points, preparation,
   full lesson process (导入→探究→实践→总结).
2. **课堂实录** — 2-3 key dialogue fragments. Spoken language, age-appropriate
   (三年级 students). Include teacher questions, student responses, key events.
3. **学生作品** — 3-5 work samples: task sheets, measurement records, drawings.
   Describe content, not just "学生完成了任务单".
4. **教学反思** — what worked, what didn't, improvement directions. Tie to
   量感 development observations.
5. **数据素材** — pre-test, post-test, experiment-vs-control comparison.
   Numbers must be realistic for the grade level and sample size.

## Self-check (quality gate)

- [ ] All five sections present and non-empty
- [ ] 教学设计 has goals + process with at least 4 stages
- [ ] 课堂实录 has 2-3 fragments with actual dialogue (not summary)
- [ ] 学生作品 has 3-5 samples with described content
- [ ] 数据素材 has pre/post numbers that are internally consistent
- [ ] At least 3 concrete details (specific dimensions, crop names, steps)
- [ ] Student dialogue sounds like 三年级 students (not academic prose)
- [ ] All numbers match project.json 研究对象 (sample size, grade)
- [ ] JSON is valid and parseable

## Constraints

- Generate only materials, never paper prose.
- Specificity is paramount — vague descriptions ("学生积极参与") fail the
  self-check. Use concrete details ("第三组用卷尺测得种植区长3.2米宽1.8米").
- Data must be plausible: 三年级 students measuring lengths should produce
  numbers in the 1-10 meter range, not 0.01mm or 500m.
- Do not contradict project.json — use the same grade, class count, base name.
