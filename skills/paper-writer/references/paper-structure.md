# Paper Structure Specification

Detailed section-by-section guidance for the teaching-case paper. This is
the authoritative structure reference for paper-writer. Other topic types
(评价类/调查类/理论类) adapt section 4 as noted at the end.

## Overall structure

```
标题
摘要 + 关键词
一、问题提出
二、教学设计与实施    ← core section, ~40% of word count
三、教学反思与分析
四、结语
参考文献
```

Word allocation (for a 2500-word paper; scale proportionally):

| Section | Words | % |
|---------|-------|---|
| 摘要+关键词 | 200-300 | 10% |
| 问题提出 | 400-500 | 18% |
| 教学设计与实施 | 1000-1200 | 44% |
| 教学反思与分析 | 400-500 | 18% |
| 结语 | 200-300 | 10% |

---

## 1. 标题

- Take from topics.json `标题` field.
- May refine wording for academic tone, but keep 知识点+场景+切入点 intact.
- Format: `[场景动作]中的[知识点][切入点]——以[劳动基地][场景]为例`
- Example: `种植区域测量中的长方形面积量感建构——以"雅趣园"种植区为例`

---

## 2. 摘要 + 关键词

**摘要** (200-300 chars, single paragraph):
- Sentence 1: background/problem (why this matters)
- Sentence 2: what this paper does (method + scope)
- Sentence 3-4: key findings/results (use 1-2 concrete numbers from material)
- Sentence 5: conclusion/contribution

**关键词** (3-5 terms):
- Always include: 量感, 项目化学习 (or 劳动教育)
- Add: the 知识点, the 切入点, one method term

Example:
```
摘要：几何量感是小学数学核心素养的重要内容。本研究以"雅趣园"劳动基地为场域，
在长方形面积教学中融入种植区域测量任务，引导三年级学生在真实劳动情境中建构
面积量感。教学实施表明，实验班后测均分较前测提升26.2分，显著高于对照班的
9.8分，学生在估测、单位选择、空间推理等方面均有明显发展。研究显示，项目化
劳动实践能有效促进量感从"数"向"量"的转化。

关键词：量感；长方形面积；项目化学习；劳动教育；小学数学
```

---

## 3. 问题提出

Four moves, ~400-500 words:

1. **背景** — 引用课标文献[1]说明量感在课标中的定位与要求。
2. **现状不足** — 引用2-3篇期刊文献说明当前量感教学的问题
   （脱离真实情境、重计算轻估测、缺乏单位体验等）。
3. **项目化劳动的契机** — 简述劳动教育政策依据[5]与本课题的研究设计，
   说明为什么劳动基地是量感培养的天然场域。
4. **本文聚焦** — 点明本论文聚焦哪个知识点×场景×切入点，
   与project.json的研究内容②对应。

Citations required in this section:
- 至少1条 课标文献
- 至少2条 期刊文献
- 1条 政策文件（如references.json中有）

---

## 4. 教学设计与实施（核心）

This is the heart of the paper, ~1000-1200 words. Draw heavily from
material.json sections 1 (教学设计), 2 (课堂实录), 3 (学生作品), 5 (数据素材).

### 4.1 教学设计概要

- 教材依据（从material.json教学设计.教材依据）
- 教学目标（三目标：数学、劳动、量感）
- 教学重难点
- 教学准备（教师/学生/场地材料）

Write as 1-2 paragraphs, not a bullet list. Example opening:
> 本课以人教版三年级下册"面积"单元为依据，依托"雅趣园"种植区开展项目化
> 学习。教学目标定位于三点：一是……二是……三是……

### 4.2 教学实施过程

Describe the lesson process as a narrative. Use material.json教学过程 stages
as the backbone. For each stage:
- What the teacher did (1-2 sentences)
- What students did (1-2 sentences)
- Design intent (1 sentence)

Insert 1-2 dialogue fragments from material.json课堂实录 verbatim or lightly
edited, formatted as block quotes or inline dialogue. Example:

> 师：同学们，这块菜地大约有多大？我们怎么量？
> 生1：可以用尺子量！量多长多宽。
> 生2：上次我们学了面积，长乘宽就是面积！

### 4.3 学生作品与分析

Select 2-3 学生作品 from material.json. For each:
- Describe what the work shows (from 内容描述)
- Quote or paraphrase the 教师评注
- Connect to 量感 development

### 4.4 教学效果数据

Present material.json数据素材 in narrative + table form:

> 为检验教学效果，对实验班（120人）与对照班（120人）进行前后测。
> 前测两班均分接近（实验班52.3分，对照班51.8分），后测实验班均分
> 78.5分，较前测提升26.2分；对照班61.6分，提升9.8分。实验班提升
> 幅度显著高于对照班（p<0.05）。

Optionally include a simple comparison table. Numbers MUST match
material.json exactly — do not round or alter.

---

## 5. 教学反思与分析

~400-500 words. Draw from material.json教学反思 (section 4).

Structure:
1. **成功之处** — 2-3 points from 成功之处 array, expand each to 2-3
   sentences with classroom evidence.
2. **不足之处** — 2-3 points from 不足之处 array, be honest and specific.
3. **量感发展观察** — Use 量感观察 field. Describe specific student
   behaviors showing 量感 growth (estimation accuracy, unit flexibility,
   spatial reasoning).
4. **改进方向** — 2-3 points from 改进方向 array.

Tie reflection back to project.json评价体系 dimensions where possible.

---

## 6. 结语

~200-300 words:
- Summarize what this paper did and found (2-3 sentences)
- State the contribution to the project's overall research (1-2 sentences)
- Acknowledge limitations (sample size, single lesson, etc.)
- Suggest future directions (1-2 sentences, link to other 研究内容)

---

## 7. 参考文献

- List only entries actually cited in the body with [n] markers.
- Use GB/T 7714-2015 format (see reference-manager's citation-gb7714.md).
- Number sequentially in order of first appearance.
- Typical count: 6-10 references for a teaching-case paper.

Order by citation number, not alphabetically.

---

## Adaptations for non-教学案例 types

### 评价类 (evaluation)
Section 4 becomes "评价体系设计与实施":
- 4.1 评价维度构建（基于project.json评价体系）
- 4.2 评价工具设计（量表/任务/观察记录）
- 4.3 多场景应用数据（跨多个material.json，如有多topic）
- 4.4 评价结果分析

### 调查类 (survey)
Section 4 becomes "调查设计与结果":
- 4.1 调查方法与样本
- 4.2 问卷/访谈设计
- 4.3 数据分析
- 4.4 主要发现

### 理论类 (theoretical)
Section 4 becomes "理论建构":
- 4.1 概念界定（核心概念+术语表）
- 4.2 文献综述
- 4.3 模型构建（如三维融合模型）
- 4.4 模型阐释

Other sections (问题提出/反思/结语) remain, adjusted in content.

---

## Common pitfalls

- **Data mismatch**: numbers in paper differ from material.json → fail self-check
- **Orphan citations**: [n] with no 参考文献 entry → fail self-check
- **Unused references**: 参考文献 entry never cited → fail self-check
- **Thin core section**: 教学设计与实施 under 800 words → likely incomplete
- **Missing dialogue**: no 课堂实录 fragments woven in → loses authenticity
- **Generic reflection**: 教学反思 without specific student evidence → weak
