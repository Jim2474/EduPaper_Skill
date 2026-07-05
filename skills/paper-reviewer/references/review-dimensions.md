# Review Dimensions

Detailed pass/fail criteria for each of the six review dimensions. The
reviewer evaluates the paper against each dimension and records specific
evidence for any failure.

---

## Dimension 1: 结构完整性 (Structure Completeness)

### Check items

| Item | Pass criterion |
|------|----------------|
| Sections present | All 7 sections exist: 标题/摘要+关键词/问题提出/教学设计与实施/教学反思与分析/结语/参考文献 |
| Word count | Within topic's 字数 ±10% (absolute range 1500-3000) |
| Section proportion | 教学设计与实施 is the longest section (~40%); 摘要 200-300 chars |
| 摘要 structure | Contains background + method + finding (with number) + conclusion |
| 关键词 | 3-5 terms, includes 量感 and the 知识点 |
| 参考文献 count | 6-10 entries for teaching-case type |

### Common failures

- Missing 结语 or 参考文献 section
- 教学设计与实施 under 800 words (too thin for core section)
- 摘要 without any concrete data number
- 关键词 fewer than 3 or more than 5

---

## Dimension 2: 引用准确性 (Citation Accuracy)

### Check items — bidirectional

**Body → References (forward check):**
- Every [n] marker in body has a matching entry in 参考文献
- Citation numbering is sequential (no gaps: [1],[2],[3] not [1],[3],[5])
- Cited content is relevant to the claim being supported

**References → Body (reverse check):**
- Every 参考文献 entry is cited at least once in body
- No orphan references (listed but never used)

**Format check:**
- GB/T 7714 format correct (document type indicator present: [J]/[M]/[S] etc.)
- Author format: surname first, no spaces between Chinese characters
- Page numbers present for journal articles
- "等" used only when 4+ authors

### Cross-source verification

- Citations in paper must trace to entries in references.json
- If a citation in paper does not exist in references.json → MAJOR fail
  (fabricated reference)
- 课标文献 must be cited in 问题提出
- 教材文献 must be cited in 教学设计与实施 (教材依据)

### Common failures

- [3] in body but no [3] in 参考文献 (orphan citation)
- 参考文献 has [4] but [4] never appears in body (unused reference)
- Journal article missing page numbers
- Policy document missing URL or access date

---

## Dimension 3: 数据一致性 (Data Consistency)

### Check items

For every number appearing in the paper, verify it matches material.json:

| Paper mentions | Must match |
|----------------|------------|
| Sample size (e.g. "120人") | material.json 数据素材.前测.样本数 |
| 前测均分 | material.json 数据素材.前测.实验班均分 / 对照班均分 |
| 后测均分 | material.json 数据素材.后测.实验班均分 / 对照班均分 |
| 提升幅度 | material.json 数据素材.提升幅度 |
| Grade level (三年级) | project.json 研究对象.年级 |
| Class count | project.json 研究对象 (实验班/对照班 count) |
| Labor base name | project.json 依据.劳动基地 |

### Plausibility re-check

- 前测 scores in 40-65 range
- 后测 scores in 70-90 range
- 实验班 post-test higher than 对照班 by 5-15 points
- Averages use one decimal place

### Common failures

- Paper says "提升28分" but material.json says 26.2 (number drift)
- Paper says "三年级" but project.json says 四年级
- Paper rounds 52.3 to 52 (minor) or 50 (major)
- Paper invents a data point not in material.json (MAJOR — fabrication)

---

## Dimension 4: 术语一致性 (Terminology Consistency)

### Check items

For each term in project.json术语表 and 核心概念:

- Term is used in paper with the exact definition from 术语表
- Term is spelled consistently throughout (e.g. not mixing "量感" and "数量感")
- Core concepts from project.json核心概念 are referenced where relevant
- No undefined jargon (terms used without explanation that aren't in 术语表)

### Specific checks

- "量感" defined/explained on first use, not assumed
- "项目化学习" / "项目化实施" used consistently (pick one, stick with it)
- Labor base name matches project.json exactly (e.g. "雅趣园" not "雅趣苑")
- 评价体系 dimensions referenced by their project.json names

### Common failures

- Paper uses "PBL" without defining it (not in 术语表)
- Labor base name misspelled or inconsistent
- 核心概念 listed in project.json but never mentioned in paper

---

## Dimension 5: 逻辑流畅性 (Logical Flow)

### Check items

- 问题提出 → 教学设计: the problem stated is addressed by the lesson design
- 教学设计 → 教学反思: reflection discusses what actually happened in design
- 教学反思 → 结语: conclusion summarizes reflection findings
- No contradictions (e.g. "前测两班无差异" then "实验班基础更好")
- Claims have evidence (e.g. "学生量感有发展" must cite specific student behavior or data)
- 教学反思 成功之处 and 不足之处 don't overlap or contradict

### Argument structure check

- 问题提出 ends with clear "本文聚焦" statement
- 教学设计与实施 has a logical lesson flow (导入→探究→实践→总结)
- 结语 acknowledges limitations
- No circular reasoning

### Common failures

- 问题提出 discusses 面积 but 教学设计 is about 周长 (topic drift)
- 教学反思 claims success but data shows minimal improvement
- 结语 overclaims ("完全解决了量感培养问题")

---

## Dimension 6: 学术规范性 (Academic Standards)

### Check items

- Academic tone throughout (no casual first person: "我觉得", "我们试试")
- No unsupported superlatives ("极大地", "完美地" without evidence)
- Proper hedging ("可能", "在一定程度上" where claims aren't definitive)
- No bullet-point lists in body prose (tables and numbered sections OK)
- Dialogue formatted consistently (block quote or inline, not mixed)
- No copy-paste from material.json without integration (raw JSON dump)
- Section headings follow academic convention (一、二、三 or 1. 2. 3.)

### Common failures

- "我觉得这个设计很好" (casual first person)
- "极大地提升了学生量感" (unsupported superlative)
- Raw material.json fields pasted into paper without prose integration
- Mixed dialogue formatting (some block quotes, some inline)

---

## Verdict rules

| Verdict | Condition |
|---------|-----------|
| **PASS** | ≤2 minor fails, no major fails |
| **REVISE** | Any major fail, or 3+ minor fails |
| **REJECT** | Structure broken (missing core section) OR data fabricated OR >5 major fails |

**Major fail** = breaks academic integrity or structural requirement
(citation mismatch, data fabrication, missing section, logical contradiction)

**Minor fail** = stylistic or formatting issue
(rounding, heading format, missing keyword)

When verdict is REJECT, list blocking issues at the top of the report before
the dimension-by-dimension analysis.
