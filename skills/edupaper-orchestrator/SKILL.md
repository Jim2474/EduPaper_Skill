---
name: edupaper-orchestrator
version: 0.1.0
description: |
  Education research paper batch-generation pipeline orchestrator. Triggers when
  a user wants to generate teaching-case papers (教学案例论文) from an education
  research project opening report (开题报告). Routes the agent through a sequence
  of single-responsibility skills that transform the opening report into a paper
  collection. Enforces a hard limit of two papers per run. Delegates all actual
  work to downstream skills — this skill only sequences and routes.
agent_created: true
---

# EduPaper Orchestrator

Route the user through the paper-generation pipeline. Do not perform any
generation work directly — delegate each stage to its dedicated skill.

## When to trigger

- User provides an opening report (开题报告) and wants papers generated
- User says "生成论文" / "跑论文流程" / "批量出论文"
- User asks to continue an existing `.edupaper/` project

## Hard constraint

Generate at most **two papers per run**. If the topic matrix contains more
than two topics, ask the user to pick two. Never exceed this limit.

## Pipeline sequence

Execute in order. Each step's output file is the next step's input.

1. **project-parser** — opening report → `.edupaper/project.json`
2. **reference-manager** — project.json → `.edupaper/references.json`
3. **topic-generator** — project.json → `.edupaper/topics.json`
4. **classroom-generator** — (per selected topic) → `.edupaper/materials/{id}/material.json`
5. **paper-writer** — material.json + references.json → `.edupaper/drafts/{id}/paper.md`
6. **paper-reviewer** — paper.md → `.edupaper/drafts/{id}/reviewed.md`
7. **humanizer** — reviewed.md → `.edupaper/drafts/{id}/final.md`
8. **consistency-checker** — all final.md → `.edupaper/consistency-report.md`

After step 8, copy each `final.md` into `.edupaper/papers/{id}-标题.md`.

## Routing rules

- Read `references/pipeline.md` for the full data-flow contract, file-naming
  conventions, and the `.edupaper/` directory layout before starting.
- Before each stage, verify the input file exists. If missing, run the
  upstream stage first.
- After each stage, confirm the output file was written before proceeding.
- If a stage fails after three self-check retries, pause and report to the
  user — do not skip ahead.
- Steps 4–7 run once per selected topic (up to two topics).

## Shared read-only data

Two files are shared across all skills as read-only (except their writer):

- `.edupaper/project.json` — written only by project-parser
- `.edupaper/references.json` — written only by reference-manager

All other skills read these two files but never modify them.

## Resuming

If `.edupaper/` already exists, scan for completed stages and resume from the
first missing output file. Do not regenerate files that already exist unless
the user explicitly requests a redo.
