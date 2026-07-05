# Consistency Rules

Detailed criteria for the five cross-paper consistency checks. The checker
compares all papers in the batch against each other and against the shared
data sources (project.json, references.json, topics.json).

---

## Check 1: 共享事实一致 (Shared Facts Consistency)

Every paper in the batch draws from the same project, so shared facts must
be identical across all papers.

### Fields to verify

| Field | Source | Must be identical across papers |
|-------|--------|-------------------------------|
| 劳动基地名称 | project.json 依据.劳动基地 | ✓ |
| 劳动基地面积/描述 | project.json 依据.劳动基地 | ✓ |
| 学校名称 | project.json meta.单位 | ✓ |
| 年级 | project.json 研究对象.年级 | ✓ |
| 总人数 | project.json 研究对象.总人数 | ✓ |
| 实验班数量 | project.json 研究对象.实验班 | ✓ |
| 对照班数量 | project.json 研究对象.对照班 | ✓ |
| 课题名称 | project.json meta.课题名称 | ✓ |
| 批准号 | project.json meta.批准号 | ✓ |
| 主持人 | project.json meta.主持人 | ✓ |
| 课标版本 | project.json 依据.课标 | ✓ |
| 教材版本 | project.json 依据.教材 | ✓ |

### How to check

For each field, grep every paper.md for mentions. Compare extracted values.
Any mismatch = MAJOR fail.

Example fail:
- Paper A: "雅趣园种植区面积约200平方米"
- Paper B: "雅趣园种植区面积约150平方米"
→ MAJOR: shared fact "劳动基地面积" inconsistent between papers A and B.

### Special case: per-topic data

Some data is topic-specific (前测/后测 scores, specific lesson details). These
do NOT need to match across papers — they come from different material.json
files. Only project-level shared facts must match.

---

## Check 2: 术语统一 (Terminology Uniformity)

### Terms to verify

For each term in project.json术语表 and 核心概念:

1. **Definition consistency** — if multiple papers define the term, the
   definitions must match (or at least not contradict).
2. **Spelling consistency** — exact same characters/words across papers.
3. **Usage consistency** — term used for the same concept, not repurposed.

### Common drift patterns

| Pattern | Example | Severity |
|---------|---------|----------|
| Spelling variant | "量感" vs "数量感" | MAJOR |
| Synonym swap | "项目化学习" vs "项目式学习" | MINOR (flag, suggest unify) |
| Definition contradiction | Paper A: "量感是对量大小的直觉" vs Paper B: "量感是测量技能" | MAJOR |
| Acronym inconsistency | "PBL" in one, "项目化学习" spelled out in another, no link | MINOR |

### How to check

- Build a term index: for each term in 术语表, find all occurrences across
  all papers.
- Check spelling: exact string match.
- Check definitions: compare the sentence containing the term's first
  occurrence in each paper.

---

## Check 3: 内容不重复 (No Content Duplication)

### What must not duplicate

| Content type | Across papers | Severity if duplicated |
|-------------|---------------|----------------------|
| 课堂实录 dialogue fragments | Must differ | MAJOR |
| 学生作品 descriptions | Must differ | MAJOR |
| 教学设计 process | Can share structure, not wording | MAJOR if verbatim |
| 问题提出 background | Overlap OK, verbatim not | MINOR if paraphrased |
| 结语 | Must differ | MAJOR |
| 数据素材 | Per-topic, must differ | MAJOR if identical |

### Acceptable overlap

- Both papers cite the same 课标 in 问题提出 — OK (different framing).
- Both papers mention "雅趣园" — OK (shared setting).
- Both papers use "三维评价体系" — OK (shared concept).

### Unacceptable overlap

- Paper A and Paper B both quote the exact same student dialogue about
  measuring a planting box — MAJOR (one paper's material was copied).
- Paper A's 教学反思 paragraph appears verbatim in Paper B — MAJOR.

### How to check

- For each pair of papers, compare 教学设计与实施 and 教学反思 sections.
- Flag any 50+ character verbatim overlap.
- Flag any identical dialogue fragment across papers.

---

## Check 4: 引用不冲突 (Citation No-Conflict)

### What to check

Build a master citation map from references.json. For each reference cited
in 2+ papers:

1. **Same entry** — all papers cite the same gb7714 string (no typo variants).
2. **Compatible claims** — the claims supported by this reference are not
   contradictory across papers.
3. **Page accuracy** — if a specific page is cited, it's the same page.

### Example fail

- Paper A cites [3] to support: "量感培养应重视估测活动"
- Paper B cites [3] to support: "量感培养应以精确测量为主"
→ MAJOR: same reference cited for contradictory claims.

### Example pass

- Paper A cites [1] (课标) for: "课标将量感列为核心素养"
- Paper B cites [1] (课标) for: "课标要求三年级开展测量实践"
→ OK: different aspects of the same source, not contradictory.

### Format consistency

- Same reference must have identical gb7714 formatting across papers.
- Citation numbering may differ per paper (each paper numbers independently).
- But the underlying reference (author+title+year) must be the same entry.

---

## Check 5: 课题覆盖完整 (Topic Coverage Completeness)

### What to check

Map each paper to its 依据内容 (from topics.json). Verify the selected
topics collectively address the project's research scope.

### Coverage matrix

Build a table:

| 研究内容 | Paper A | Paper B | Coverage |
|---------|---------|---------|----------|
| ① 理论基础构建 | — | — | ✗ GAP |
| ② 项目化活动设计与实施 | ✓ (依据内容: ②) | ✓ (依据内容: ②) | ✓ |
| ③ 多元化评价体系构建 | — | — | ✗ GAP |

### Interpretation

- For a single-paper run, most 研究内容 will not be covered — that's
  expected. Flag gaps as INFO, not fail. The coverage map builds over
  multiple runs as more papers accumulate.
- If multiple papers (across runs) both map to the same 依据内容 and same
  type, flag as MINOR (redundancy risk — ensure they have different 切入点).
- If a paper's 依据内容 doesn't match topics.json, flag as MAJOR.

### What constitutes a gap

- A 研究内容 item with no paper addressing it.
- For early runs (1-2 papers), gaps in ① and ③ are acceptable (typically
  only ② is covered by teaching-case papers).
- Gaps should be noted as "future run" opportunities, not failures.

---

## Verdict

| Verdict | Condition |
|---------|-----------|
| **SINGLE-PAPER BASELINE** | Only one paper exists; checks 1-3 N/A, checks 4-5 executed |
| **CONSISTENT** | 2+ papers, no MAJOR fails; MINOR fails listed as suggestions |
| **INCONSISTENT** | 2+ papers, any MAJOR fail (shared fact mismatch, content duplication, citation conflict) |

When INCONSISTENT, list blocking issues at the top before the check-by-check
analysis. Blocking issues must be resolved by paper-writer before humanizer
runs.
