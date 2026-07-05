# Academic Guardrails for Humanizer

The `humanizer` skill (installed at `~/.workbuddy/skills/humanizer/`) is
designed for general prose. When applied to academic papers, certain
elements must be preserved regardless of AI-pattern detection. This file
defines those guardrails.

---

## Principle

Humanizer removes AI writing *style* patterns. It must not remove academic
*content* or *structure*. When in doubt, preserve the original.

---

## Guardrail 1: Citations

### What to preserve

- All `[n]` citation markers in body text — exact position and number.
- The entire 参考文献 section — every entry, every field.
- Citation numbering sequence (must remain [1], [2], [3]… with no gaps).
- The document-type indicators ([J], [M], [S], [A], [D], [C], [EB/OL]).
- GB/T 7714 formatting (punctuation, author order, page ranges).

### What humanizer MAY change

- The sentence *around* a citation can be rephrased for naturalness.
- Example: "研究显示[3]，学生量感有显著提升" → "学生在量感方面有显著提升[3]"
  (citation moved, but preserved).

### What humanizer MUST NOT change

- The citation number itself.
- The reference entry text.
- The mapping between [n] in body and [n] in 参考文献.

---

## Guardrail 2: Data and Numbers

### What to preserve

Every numeric value in the paper must remain identical after humanization:

| Data type | Example | Must preserve |
|-----------|---------|--------------|
| Test scores | 52.3分, 78.5分 | Exact digits |
| Sample sizes | 120人, 40人 | Exact digits |
| Dimensions | 3.2米, 1.8米 | Exact digits |
| Percentages | 26.2% | Exact digits |
| Areas | 2.88平方米 | Exact digits |
| Page references | 第70-72页 | Exact digits |
| Years | 2022年, 2023年 | Exact digits |

### What humanizer MAY change

- The sentence framing a number: "实验班均分为78.5分" → "实验班的平均分达到78.5分"
- Connecting words around data: "提升了26.2分" → "提高了26.2分"

### What humanizer MUST NOT change

- Any digit or decimal point.
- Units (米, 平方米, 分, %, 人).
- The magnitude or comparison direction.

### Post-humanizer verification

After humanizer runs, diff the data numbers between paper.md and final.md.
Any mismatch = guardrail violation → revert that passage.

---

## Guardrail 3: Structure

### What to preserve

- All section headings and their order:
  ```
  标题
  摘要 + 关键词
  一、问题提出
  二、教学设计与实施
  三、教学反思与分析
  四、结语
  参考文献
  ```
- Sub-headings within 教学设计与实施 (（一）（二）（三）（四）).
- The heading numbering scheme (一、二、三 or 1. 2. 3. — must be consistent).

### What humanizer MAY change

- Heading wording slightly (but meaning must be preserved).
  Example: "教学设计与实施" may NOT become "课程设计与执行".

### What humanizer MUST NOT change

- Section count (must remain 7).
- Section order.
- Heading hierarchy (H1 → H2 → H3 levels).

---

## Guardrail 4: Dialogue Fragments

### What to preserve

课堂实录 dialogue from material.json, formatted as:

```
> 师：{teacher speech}
> 生1：{student speech}
> 生2：{student speech}
```

- The `师：` / `生1：` / `生2：` speaker labels.
- The exact words spoken (this is quoted classroom speech, not author prose).
- The block-quote formatting.

### Why

Student dialogue is supposed to sound colloquial and age-appropriate — it's
not AI writing, it's realistic speech. Humanizer might flag it as "too
simple" but it must be preserved.

### What humanizer MAY change

- The narrative text *between* dialogue fragments (author's description of
  the classroom context).

### What humanizer MUST NOT change

- Any line starting with `师：` or `生`.
- The content of dialogue turns.

---

## Guardrail 5: Tables

### What to preserve

Data tables (e.g. 前后测对比表):

```
| 班级 | 样本数 | 前测均分 | 后测均分 | 提升幅度 |
|------|--------|----------|----------|----------|
| 实验班 | 120人 | 52.3 | 78.5 | 26.2 |
```

- Table structure (rows, columns, headers).
- All cell values.
- Table caption (if any).

### What humanizer MAY change

- The narrative sentence introducing the table.

### What humanizer MUST NOT change

- Any cell content.
- Column/row count.
- Header labels.

---

## Guardrail 6: Term Definitions

### What to preserve

First-use definitions of 核心概念 from project.json术语表:

- "量感是指对事物可测量属性及大小关系的直观感知"
- "项目化学习是指围绕真实问题设计并实施系列任务的学习方式"

### What humanizer MAY change

- Hedging language around the definition: "量感通常被定义为…" → "量感是…"
  (but only if the original was over-hedged by AI).

### What humanizer MUST NOT change

- The core definitional content.
- The term being defined.

---

## Conflict resolution

If humanizer's pattern detection flags a passage that falls under a
guardrail:

1. **Preserve the guarded content** — guardrails take precedence.
2. **Humanize only the non-guarded surrounding text.**
3. **Log the conflict** — note which pattern was detected but skipped due
   to guardrail, for transparency.

Example:
- Humanizer detects "transition word overuse" in a passage containing [3]
  citation and a data point (78.5分).
- Action: rewrite the transition words, keep [3] and 78.5分 in place.
- Do NOT delete the citation or round the number to 79.

---

## Post-humanization diff checklist

After writing final.md, verify against paper.md:

- [ ] Citation count identical (count [n] markers — must match)
- [ ] 参考文献 entry count identical
- [ ] Every number in paper.md appears in final.md (grep digits)
- [ ] Section heading count identical
- [ ] Dialogue lines (师：/ 生) identical (diff these lines)
- [ ] Table row/column counts identical
- [ ] Term definitions present and intact
- [ ] No new content added (final.md should be ≤ paper.md in word count)
