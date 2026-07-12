---
name: edupaper-humanizer
version: 0.2.0
description: |
  对论文进行去 AI 痕迹和学术润色。当论文通过评审和一致性检查后，需要消除其中的 AI 写作
  模式（如口水话、过度过渡句），同时严格保留学术结构、引用及真实实验数据时触发。
  触发词：论文润色 / 去AI痕迹 / 去除AI感 / 降低AI率 / humanize paper / 学术润色 /
  论文降重 / 降低AI写作率。
  本 skill 作为最终抛光阶段运行，输入 paper.md，输出 final.md。
agent_created: false
---

# EduPaper Humanizer

Humanize one draft paper and write the final version to
`.edupaper/drafts/{topic-id}/final.md`.

## When to trigger

- `.edupaper/drafts/{topic-id}/paper.md` exists (paper-writer has run)
- `.edupaper/drafts/{topic-id}/review-report.md` exists with no unresolved
  REJECT verdict (paper-reviewer has run and passed)
- `.edupaper/consistency-report.md` exists with verdict CONSISTENT or
  SINGLE-PAPER BASELINE (consistency-checker has run and passed)
- `.edupaper/drafts/{topic-id}/final.md` does not exist
- Orchestrator routes here as the final prose-polishing stage

## Procedure

0. **前置依赖检测（所有其他步骤之前）**：检查外部 humanizer skill 是否可用。
   - 检测路径：`~/.workbuddy/skills/humanizer/SKILL.md`（优先）或 `~/.claude/skills/humanizer/SKILL.md`
   - **若不存在**：立即告知用户"humanizer skill 未安装，第8步将跳过，直接将 paper.md 复制为 final.md"。
     将 `paper.md` 内容原样复制到 `final.md`，跳过步骤 5-6，直接执行步骤 7（self-check 按"无 humanizer"模式执行）。
   - **若存在**：继续正常流程。

1. Read `.edupaper/drafts/{topic-id}/paper.md` — this is the draft to
   humanize. This is the **primary input** to the humanizer.
2. Read `.edupaper/drafts/{topic-id}/review-report.md` — verify there are
   no unresolved REJECT or blocking MAJOR issues. If any exist, pause and
   report to user before humanizing.
3. Read `.edupaper/consistency-report.md` — verify verdict is CONSISTENT or
   SINGLE-PAPER BASELINE. If INCONSISTENT, pause and report; do not humanize
   a paper flagged for cross-paper conflicts.
4. Read `references/academic-guardrails.md` for what must be preserved.
5. Invoke the `humanizer` skill on the paper content. The humanizer
   identifies and rewrites 33 AI writing patterns (see
   ~/.workbuddy/skills/humanizer/SKILL.md for the full pattern list).
6. After humanizer rewrites, verify the academic guardrails (see below).
   If any guardrail is violated, revert that section and re-apply humanizer
   with the constraint noted.
7. Write the humanized text to `.edupaper/drafts/{topic-id}/final.md`.
8. Run the self-check.

## Academic guardrails (what humanizer must NOT change)

- **Citations** — [n] markers and 参考文献 entries must remain intact and
  correctly numbered.
- **Data** — every number (scores, sample sizes, dimensions) must remain
  identical to material.json. Humanizer may rephrase surrounding text but
  not alter digits.
- **Structure** — all section headings (一、二、三 / 参考文献) must remain.
  Humanizer may not merge or delete sections.
- **Dialogue** — 课堂实录 quotes (师：/ 生：) must remain verbatim. These
  are student speech, not AI prose.
- **Tables** — data tables must remain structurally intact.
- **Term definitions** — first-use definitions of 核心概念 must remain
  precise (humanizer may soften hedging language but not definitions).

## Self-check (quality gate)

- [ ] All [n] citations preserved with correct numbering
- [ ] 参考文献 section intact with all entries
- [ ] Every data number matches paper.md (no digit drift)
- [ ] All section headings present in original order
- [ ] Dialogue fragments (师：/ 生：) unchanged
- [ ] Tables structurally intact
- [ ] No new AI patterns introduced (humanizer's own check passes)
- [ ] Word count within ±5% of original (humanizer should trim, not expand)
- [ ] Meaning preserved — no factual claims altered

## Constraints

- This skill delegates pattern detection to the `humanizer` skill — do not
  reimplement the 33 patterns here.
- If `humanizer` skill is not installed, pause and report to user.
- Do not run humanizer on a paper with unresolved REJECT verdict from
  paper-reviewer — fix first, then humanize.
- One paper at a time. The orchestrator handles batch sequencing.
- The output file is `final.md` — this is the deliverable that gets copied
  to `.edupaper/papers/{topic-id}-标题.md` by the orchestrator.
