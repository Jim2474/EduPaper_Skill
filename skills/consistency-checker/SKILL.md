---
name: consistency-checker
version: 0.2.0
description: |
  检查批次论文之间的跨篇一致性。当有多篇论文草稿或评审报告存在，需要核对学校名称、
  劳动基地面积等共享事实是否一致，确保没有内容重复、术语漂移或文献引用冲突时触发。
  触发词：一致性检查 / 跨论文核对 / 论文一致性 / consistency check / 检查重复内容 /
  拼写一致性检查 / 共享事实验证。
  本 skill 仅输出批次一致性报告（consistency-report.md），不直接修改论文。
agent_created: false
---

# Consistency Checker

Check all papers in the current batch for cross-paper consistency and write
`.edupaper/consistency-report.md`.

## When to trigger

- At least 1 paper exists under `.edupaper/drafts/*/paper.md`
- The paper has a review-report.md (paper-reviewer has run)
- `.edupaper/consistency-report.md` does not exist
- Orchestrator routes here after the paper-reviewer stage completes

**Single-paper mode:** If only one paper exists, cross-paper checks (1-3)
are skipped and the report focuses on check 4 (citation validity against
references.json) and check 5 (topic coverage). This builds a baseline for
future runs — when a second paper is added later, the full cross-paper
comparison runs.

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

- [ ] All papers under `.edupaper/drafts/` were read
- [ ] For single-paper mode: checks 1-3 marked N/A, checks 4-5 executed
- [ ] For multi-paper mode: all five checks executed with explicit pass/fail
- [ ] Every fail names the conflicting papers and quotes both passages
- [ ] Shared-fact check covered every field in project.json 研究对象 and 依据
- [ ] Citation conflict check covered every reference cited in 2+ papers
- [ ] Coverage map shows which 研究内容 each paper addresses
- [ ] No vague findings ("papers seem consistent") — all specific
- [ ] Overall verdict stated (CONSISTENT / INCONSISTENT / SINGLE-PAPER BASELINE)

## Constraints

- Check only cross-paper issues — single-paper quality is paper-reviewer's job.
- Do not modify papers — only report. Fixes go back to paper-writer.
- If a paper's review-report.md has unresolved REJECT verdict, flag it as
  a blocking issue.
- Quote exact passages when citing conflicts — must be verifiable.
- In single-paper mode, still verify citations against references.json and
  map topic coverage — these are useful even without a second paper.
