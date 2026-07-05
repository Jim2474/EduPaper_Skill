# topics.json Schema

Field definitions and decomposition guidance for the topic matrix.

## Top-level structure

```json
{
  "topics": [ { ... }, { ... } ]
}
```

## Topic object

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | string | yes | Single uppercase letter, sequential: A, B, C, D, E, F |
| 标题 | string | yes | Working title, ≤25 chars, reflects 知识点+场景+切入点 |
| 知识点 | string | yes | Specific math concept from textbook |
| 劳动场景 | string | yes | Concrete labor activity at the base |
| 切入点 | string | yes | Research lens / angle |
| 类型 | string | yes | One of: 教学案例 / 评价类 / 调查类 / 理论类 |
| 字数 | number | yes | Target word count, 1500-3000 |
| 依据内容 | string | yes | Which 研究内容 item this maps to (e.g. "研究内容②") |

---

## Type guidance

### 教学案例 (teaching case) — primary type

Structure: knowledge point + labor scenario + 量感 angle.

A teaching-case paper describes one lesson's design and implementation in a
labor context, with classroom dialogue, student work, and reflection.

Examples:
- 长方形面积 × 种植区域测量 × 面积量感建构
- 周长 × 围栏规划 × 周长量感发展
- 综合测量 × 种植区域规划 × 双螺旋模式应用

Target: at least 2 topics of this type. Word count: 2000-3000.

### 评价类 (evaluation)

Structure: evaluation tool + full scenarios + evaluation angle.

An evaluation paper documents the design and application of the assessment
system across multiple activities.

Example:
- 三维评价工具 × 全场景 × 评价体系构建

Target: 0-1 topics. Word count: 2500-3000.

### 调查类 (survey)

Structure: survey method + questionnaire + current-state angle.

A survey paper reports questionnaire findings about students' or teachers'
current state of 量感 awareness.

Example:
- 问卷调查 × 师生调查 × 量感认知现状

Target: 0-1 topics. Word count: 2500-3000.

### 理论类 (theoretical)

Structure: theoretical framework + literature + model-building angle.

A theoretical paper constructs the project's conceptual model (e.g. the
三维融合 model) with literature support.

Example:
- 三维融合模型 × 文献研究 × 理论构建

Target: 0-1 topics. Word count: 2500-3000.

---

## Overlap rules

Two topics overlap if they share **all three** dimensions (知识点 × 场景 ×
切入点). This is a duplicate and must be removed.

Sharing one or two dimensions is acceptable and encouraged — it shows the
project's coherence. For example:
- Topic A: 长方形面积 × 种植测量 × 量感建构
- Topic B: 周长 × 围栏规划 × 量感建构

These share 切入点 (量感建构) but differ on 知识点 and 场景. Valid.

- Topic A: 长方形面积 × 种植测量 × 量感建构
- Topic C: 长方形面积 × 种植测量 × 双螺旋设计

These share 知识点 and 场景 but differ on 切入点. Valid — one is a case
study, the other is a design-pattern paper.

---

## Title formula

Working title format:

```
[场景动作]中的[知识点][切入点]——以[劳动基地][场景]为例
```

Example:
```
种植区域测量中的长方形面积量感建构——以"雅趣园"种植区为例
```

Or for non-case types:

```
[切入点]的[类型]——基于[劳动基地]的[方法]
```

Example:
```
几何量感项目化实施评价体系构建——基于"雅趣园"的实证研究
```

---

## Mapping to 研究内容

Each topic should map to one of the project's 研究内容 items. This ensures
the topic matrix covers the full research scope:

| 研究内容 | Typical topic type |
|---------|-------------------|
| ① 理论基础构建 | 理论类 |
| ② 项目化活动设计与实施 | 教学案例 (primary) |
| ③ 多元化评价体系构建 | 评价类 |
| (derived from ②) | 调查类 |

Fill 依据内容 with the matching 研究内容 number.
