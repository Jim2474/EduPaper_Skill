---
name: project-parser
version: 0.1.0
description: |
  Parse an education research project opening report (开题报告) in PDF, DOCX, or
  Markdown format and extract a structured project profile to project.json.
  This skill should be used when an opening report file is provided and the
  .edupaper/project.json does not yet exist. It is the first stage of the
  EduPaper pipeline — its output becomes the shared read-only memory for all
  downstream skills. Does not generate topics, materials, or papers.
agent_created: true
---

# Project Parser

Extract a structured project profile from an opening report and write it to
`.edupaper/project.json`. This file is the single source of truth for the
entire pipeline — all other skills read it, none modify it.

## When to trigger

- An opening report file (开题报告) is provided (PDF / DOCX / MD)
- `.edupaper/project.json` does not exist or is empty
- User says "解析开题报告" / "建立课题档案"

## Procedure

1. Read the opening report file. For PDF, extract text first (e.g. pypdf).
   For DOCX, extract text from the document XML.
2. Read `references/project-schema.md` for the full field definitions, types,
   and extraction guidance.
3. Map the report content to the schema fields. Make reasonable inferences
   where the report is implicit (e.g. derive 教材 version from the grade and
   subject mentioned).
4. Build the JSON object and write it to `.edupaper/project.json`. Create the
   `.edupaper/` directory if it does not exist.
5. Run the self-check below. If it fails, fix and re-check (max 3 retries).

## Output

Write to `.edupaper/project.json` — valid JSON, UTF-8, 2-space indent.

## Self-check (quality gate)

Before writing the file, verify:

- [ ] All required fields in `references/project-schema.md` are non-empty
- [ ] `meta.课题名称` and `meta.主持人` are present
- [ ] `研究对象.总人数` is a positive integer
- [ ] `术语表` defines every term listed in `核心概念`
- [ ] `成员分工` has at least one entry
- [ ] `依据.课标` and `依据.教材` are present
- [ ] JSON is valid and parseable

If any check fails, return to step 3 and fill the gap. After 3 failed
attempts, write the file with the gaps marked as `"__MISSING__"` and report
to the user which fields need manual input.

## Constraints

- Extract only — do not invent data that is not in or reasonably inferable
  from the report.
- If a field cannot be found, use `"__MISSING__"` as the value (never leave
  it absent or null).
- Do not generate topics, literature, or paper content. That is downstream
  skills' job.
- This skill is the **sole writer** of project.json. Never read-modify-write
  an existing project.json — if it exists and is valid, skip this skill.
