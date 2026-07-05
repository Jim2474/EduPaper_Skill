# references.json Schema

Field definitions for the shared reference library.

## Top-level structure

```
references.json
├── 课标文献      # curriculum standards
├── 教材文献      # textbook references
├── 期刊文献      # journal articles
└── 其他文献      # other sources (policies, theses, web)
```

---

## 课标文献

Curriculum standards that all papers must cite as the policy basis.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| 标题 | string | yes | Full standard name, e.g. "义务教育数学课程标准（2022年版）" |
| 出处 | string | yes | Publisher, e.g. "中华人民共和国教育部" |
| 年份 | number | yes | Publication year |
| 引用位置建议 | string | yes | Which paper sections should cite this (e.g. "问题提出/教学设计依据") |
| gb7714 | string | yes | Formatted GB/T 7714 citation string |

Example:
```json
{
  "标题": "义务教育数学课程标准（2022年版）",
  "出处": "中华人民共和国教育部",
  "年份": 2022,
  "引用位置建议": "问题提出；教学设计依据；结语",
  "gb7714": "[1] 中华人民共和国教育部. 义务教育数学课程标准（2022年版）[S]. 北京: 北京师范大学出版社, 2022."
}
```

---

## 教材文献

Textbook units that the teaching cases are based on. Must specify exact unit
and pages so papers can reference concrete content.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| 学科 | string | yes | e.g. "数学" |
| 版本 | string | yes | e.g. "人教版" |
| 年级 | string | yes | e.g. "三年级上册" |
| 单元 | string | yes | Unit title, e.g. "第六单元 多边形的面积" |
| 页码 | string | yes | Page range, e.g. "P70-72" |
| 知识点 | string | yes | The specific knowledge point, e.g. "长方形面积" |
| gb7714 | string | yes | Formatted GB/T 7714 citation string |

---

## 期刊文献

Education research journal articles relevant to the project's core concepts.
6-10 entries, prefer 2020+ publications.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| 作者 | string | yes | All authors, comma-separated |
| 标题 | string | yes | Article title |
| 期刊 | string | yes | Journal name |
| 年 | number | yes | Publication year (≥2020 preferred) |
| 期 | string | yes | Issue number, e.g. "第3期" |
| 页 | string | yes | Page range, e.g. "45-48" |
| DOI | string | no | DOI if available |
| 摘要 | string | yes | 2-3 sentence summary of the article's key finding |
| 相关选题 | array | yes | Topic letters this article supports, e.g. ["A", "C"] |
| gb7714 | string | yes | Formatted GB/T 7714 citation string |

Preferred journals (education research, Chinese):
- 《小学数学教师》
- 《教学与管理》
- 《数学教育学报》
- 《课程·教材·教法》
- 《中小学管理》
- 《中国教育学刊》
- 《教育研究与实验》

Selection criteria:
- Directly relevant to at least one 核心概念
- Published 2020 or later (classic foundational works excepted)
- From a recognized education journal (not predatory)

---

## 其他文献

Supplementary sources that don't fit the above categories.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| 类型 | string | yes | One of: 政策文件 / 学位论文 / 会议论文 / 网络资源 / 专著 |
| 标题 | string | yes | Title |
| 出处 | string | yes | Source (publisher, university, URL, etc.) |
| 年份 | number | yes | Year |
| 摘要 | string | no | Brief description |
| 相关选题 | array | no | Topic letters supported |
| gb7714 | string | yes | Formatted GB/T 7714 citation string |

---

## Topic assignment

The 相关选题 field links each reference to specific paper topics. This lets
paper-writer know which references to cite in which paper.

- Topic letters come from topics.json (assigned by topic-generator: A, B, C…)
- A reference can support multiple topics (e.g. a general 量感 article supports A, B, C)
- 课标文献 and 教材文献 typically support all topics — set 相关选题 to
  ["ALL"] for these.

## Deduplication

Before writing, check for duplicates by comparing 作者+标题+年. If two entries
have the same authors and title and year, keep only one (prefer the one with
more complete fields).
