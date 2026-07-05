# project.json Schema

Field definitions, types, and extraction guidance for the project profile.

## Top-level structure

```
project.json
├── meta
├── 研究对象
├── 依据
├── 核心概念
├── 术语表
├── 研究设计
├── 评价体系
└── 成员分工
```

---

## meta

Project metadata — the identity card of the research project.

| Field | Type | Required | Extraction source |
|-------|------|----------|-------------------|
| 课题名称 | string | yes | Cover page or data table title |
| 批准号 | string | yes | Data table (批准号 / 年度编号) |
| 主持人 | string | yes | Data table (课题主持人姓名) |
| 单位 | string | yes | Data table (主持人所在单位) |
| 研究周期 | string | yes | Derive from 阶段性成果 start and 结题 date |

Example:
```json
"meta": {
  "课题名称": "小学中年段数学几何量感在劳动教育中的项目化实施研究——以岑溪市第五小学"雅趣园"基地为例",
  "批准号": "2026XKT-JYKY88",
  "主持人": "李金兰",
  "单位": "广西岑溪市第五小学",
  "研究周期": "2026年2月-2027年6月"
}
```

---

## 研究对象

Who is being studied. Must be consistent across all generated papers.

| Field | Type | Required | Extraction source |
|-------|------|----------|-------------------|
| 年级 | string | yes | 研究对象 section (e.g. "三到四年级") |
| 总人数 | number | yes | Sum of experiment + control classes |
| 实验班 | string | yes | Number and description (e.g. "3个班，约120名") |
| 对照班 | string | yes | Number and description (e.g. "3个班，约120名") |

---

## 依据

Authoritative references all papers must cite consistently.

| Field | Type | Required | Extraction source |
|-------|------|----------|-------------------|
| 课标 | string | yes | Usually 义务教育课程标准 2022版; find in 研究背景 |
| 教材 | string | yes | Derive from subject + grade (e.g. "人教版小学数学三年级") |
| 劳动基地 | string | yes | Name of the labor education base (e.g. "雅趣园") |

---

## 核心概念

Array of concept strings that are central to the research. These must all
appear in 术语表 with definitions.

Extraction source: 研究内容, 研究目标, 创新之处 sections.

Example:
```json
"核心概念": ["几何量感", "劳动教育", "项目化学习", "量感培养"]
```

---

## 术语表

Object mapping each term to its definition. Every term in 核心概念 must have
an entry here. Definitions should be drawn from the 课标 or the report's own
formulation.

| Key | Value | Required |
|-----|-------|----------|
| term string | definition string | yes, for each 核心概念 |

Extraction guidance:
- 几何量感: from 课标 2022 or report's 研究内容①
- 劳动教育: from 义务教育劳动课程标准 2022版
- 项目化学习: from report's 研究方法 or 创新之处
- For any term not defined in the report, mark as `"__MISSING__"` and flag
  for manual completion.

---

## 研究设计

| Field | Type | Required | Extraction source |
|-------|------|----------|-------------------|
| 研究目标 | array of strings | yes | 研究目标 section |
| 研究内容 | array of strings | yes | 研究内容 section (①②③) |
| 研究方法 | array of strings | yes | 研究方法 section |
| 创新点 | array of strings | yes | 创新之处 section |

Each array element is one goal / content item / method / innovation. Preserve
the report's numbering as separate elements.

---

## 评价体系

| Field | Type | Required | Extraction source |
|-------|------|----------|-------------------|
| 维度 | array of strings | yes | 研究内容③ or 评价体系 section |
| 指标 | array of strings | yes | Specific indicators under each dimension |

If the report mentions dimensions but not specific indicators, list the
dimensions and mark 指标 as `["__MISSING__"]`.

---

## 成员分工

Object mapping member names to their responsibilities.

| Key | Value | Required |
|-----|-------|----------|
| name string | responsibility string | yes, at least one |

Extraction source: 课题组成员 table + 详细分工 table. Merge both into a
single name → responsibility mapping. Keep it concise (one sentence per
person).

Example:
```json
"成员分工": {
  "李金兰": "课题整体规划，撰写开题/中期/结题报告，主持理论框架构建",
  "谭坚": "辅助撰写各阶段报告",
  "唐艺芸": "过程性材料收集整理"
}
```

---

## Edge cases

- **Missing field**: use `"__MISSING__"`, never null or omit the key.
- **Ambiguous grade**: if the report says "中年段" without specifying, infer
  from 研究对象 (三到四年级 is common for 小学中年段).
- **Multiple 课标**: if both 数学课标 and 劳动课标 are mentioned, list both
  separated by semicolons.
- **No 评价体系 in report**: set 维度 to the three mentioned in 研究内容③
  (数学应用, 劳动实践, 团队协作) and 指标 to `["__MISSING__"]`.
