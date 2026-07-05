---
name: paper-reviewer
version: 0.1.0
description: |
  Perform adversarial academic review on a single draft paper. Reads paper.md
  and cross-checks it against project.json, material.json, and references.json
  to catch structure gaps, citation errors, data mismatches, logical breaks,
  and terminology inconsistencies. This skill simulates a journal reviewer's
  perspective — it does not rewrite the paper, only produces a review report
  with pass/fail per dimension and actionable fix suggestions. Runs after
  paper-writer and before humanizer. One paper at a time.
agent_created: true
---

# Paper Reviewer

Review one draft paper and write a structured review report to
`.edupaper/drafts/{topic-id}/review-report.md`.

## When to trigger

- `.edupaper/drafts/{topic-id}/paper.md` exists (paper-writer has run)
- `.edupaper/drafts/{topic-id}/review-report.md` does not exist
- User has asked to review a specific topic, or orchestrator routes here

## Procedure

1. Read `.edupaper/drafts/{topic-id}/paper.md` (the draft under review).
2. Read `.edupaper/project.json` for 术语表, 核心概念, 研究对象, 评价体系.
3. Read `.edupaper/materials/{topic-id}/material.json` for ground-truth data.
4. Read `.edupaper/references.json` for citation cross-checking.
5. Read `references/review-dimensions.md` for the six review dimensions and
   their pass/fail criteria.
6. Copy `assets/templates/review-report.md` as the starting structure.
7. Evaluate the paper against each dimension. For each, record pass/fail
   with specific evidence (quote the problematic passage, cite the
   conflicting source).
8. Compile the fix list — each fix must be actionable: location + problem +
   suggested change.
9. Compute overall verdict: PASS (≤2 minor issues) / REVISE (any major) /
   REJECT (structure broken or data fabricated).
10. Write to `.edupaper/drafts/{topic-id}/review-report.md`.
11. Run the self-check.

## Six review dimensions

1. **结构完整性** — all sections present, word count on target, section
   proportions reasonable.
2. **引用准确性** — every [n] has a 参考文献 entry and vice versa; GB/T 7714
   format correct; cited content matches source.
3. **数据一致性** — every number in paper matches material.json 数据素材;
   sample sizes match project.json 研究对象.
4. **术语一致性** — 核心概念 and 术语表 from project.json used with correct
   definitions throughout; no undefined jargon.
5. **逻辑流畅性** — argument flows from 问题提出 to 结语; no contradictions;
   claims supported by evidence.
6. **学术规范性** — academic tone, no first-person casual, no unsupported
   superlatives, proper hedging.

## Self-check (quality gate)

- [ ] All six dimensions evaluated with explicit pass/fail
- [ ] Every fail has quoted evidence from the paper
- [ ] Every fail has a specific, actionable fix (location + problem + fix)
- [ ] Overall verdict stated (PASS / REVISE / REJECT)
- [ ] Data consistency check covered every number in 数据素材 section
- [ ] Citation check covered both directions (body→refs and refs→body)
- [ ] No vague comments ("could be better") — all feedback specific

## Constraints

- Review only, never rewrite paper prose. Fixes are suggestions, not edits.
- Be adversarial but fair — flag real problems, not stylistic preferences.
- Do not check AI-writing patterns — that is humanizer's job.
- Do not check cross-paper consistency — that is consistency-checker's job.
- If verdict is REJECT, list the blocking issues clearly at the top.
- Quote exact passages when citing problems — reviewer must be verifiable.
