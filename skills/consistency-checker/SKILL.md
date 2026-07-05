---
name: consistency-checker
version: 0.1.0
description: |
  Check cross-paper consistency across all papers in a batch. Reads every
  paper.md and review-report.md under .edupaper/drafts/, plus project.json
  and references.json, then writes a single consistency-report.md. This
  skill catches contradictions between papers (e.g. one paper says the base
  is 200㎡, another says 150㎡), duplicated content, terminology drift, and
  coverage gaps. Runs after all papers are reviewed, before humanizer.
  Distinct from paper-reviewer (single-paper quality) — this is batch-level.
agent_created: true
---

# Consistency Checker

Check all papers in the current batch for cross-paper consistency and write
`.edupaper/consistency-report.md`.

## When to trigger

- At least 2 papers exist under `.edupaper/drafts/*/paper.md`
- Each paper has a review-report.md (paper-reviewer has run)
- `.edupaper/consistency-report.md` does not exist
- Orchestrator routes here after all paper-reviewer stages complete

## Procedure

1. List all topic directories under `.edupaper/drafts/`.
2. Read every `paper.md` — collect into a paper set indexed by topic-id.
3. Read every `review-report.md` — note any unresolved MAJOR issues.
4. Read `.edupaper/project.json` for shared facts (研究对象, 依据, 术语表).
5. Read `.edupaper/references.json` — build a master citation map.
6. Read `.edupaper/topics.json` — verify topic coverage.
7. Read `references/consistency-rules.md` for the five check categories.
8. Copy `assets/templates/consistency-report.md` as starting structure.
9. Run all five consistency checks (see below).
10. Compile findings into the report with per-check pass/fail.
11. Write to `.edupaper/consistency-report.md`.
12. Run the self-check.

## Five consistency checks

1. **共享事实一致** — labor base name/area, sample sizes, grade, class
   counts, teacher names must be identical across all papers. Any
   discrepancy is a MAJOR fail.
2. **术语统一** — same term used the same way across papers. No paper
   defines 量感 differently from another. Spelling consistent.
3. **内容不重复** — no two papers describe the same lesson fragment or
   student work verbatim. Overlap in background is OK; overlap in core
   content is not.
4. **引用不冲突** — a reference cited in multiple papers is cited for
   compatible claims. No paper misattributes a source.
5. **课题覆盖完整** — the selected topics collectively cover the
   project's 研究内容 items. Map each paper to its 依据内容; flag gaps.

## Self-check (quality gate)

- [ ] All papers in the batch were read and compared
- [ ] All five checks executed with explicit pass/fail
- [ ] Every fail names the conflicting papers and quotes both passages
- [ ] Shared-fact check covered every field in project.json 研究对象 and 依据
- [ ] Citation conflict check covered every reference cited in 2+ papers
- [ ] Coverage map shows which 研究内容 each paper addresses
- [ ] No vague findings ("papers seem consistent") — all specific
- [ ] Overall batch verdict stated (CONSISTENT / INCONSISTENT)

## Constraints

- Check only cross-paper issues — single-paper quality is paper-reviewer's job.
- Do not modify papers — only report. Fixes go back to paper-writer.
- If a paper's review-report.md has unresolved REJECT verdict, flag it as
  a blocking issue (that paper should not be in the batch).
- Quote exact passages when citing conflicts — must be verifiable.
- For 2-paper batches (the max), compare directly; no statistical analysis.
