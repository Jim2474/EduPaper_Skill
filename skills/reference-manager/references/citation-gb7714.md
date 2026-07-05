# GB/T 7714-2015 Citation Format Guide

Chinese national standard for bibliographic references (GB/T 7714-2015
《信息与文献 参考文献著录规则》). All citations in references.json must
use this format in the `gb7714` field.

## General rules

- Number citations sequentially in order of first appearance: [1], [2], [3]…
- List all authors; if 4 or more, list first 3 followed by ", 等" (or ", et al.")
- Use half-width (ASCII) punctuation for structural elements: `.` `,` `:`
- Year format: YYYY
- Page format: 起页-止页 (e.g. 45-48), use full range, no "P" prefix
- Author names: surname first, no spaces between Chinese characters
- Multiple authors separated by `, ` (comma + space)

## By document type

### Standard (课标/标准) — [S]

```
[序号] 起草单位. 标准名称: 标准号[S]. 出版地: 出版者, 年.
```

Example:
```
[1] 中华人民共和国教育部. 义务教育数学课程标准（2022年版）[S]. 北京: 北京师范大学出版社, 2022.
```

### Textbook/Monograph (教材/专著) — [M]

```
[序号] 作者. 书名[M]. 版次. 出版地: 出版者, 年: 页码.
```

Example:
```
[2] 人民教育出版社课程教材研究所小学数学课程教材研究开发中心. 义务教育教科书·数学（三年级下册）[M]. 北京: 人民教育出版社, 2022: 60-70.
```

Note: If first edition, omit the 版次 field.

### Journal article (期刊) — [J]

```
[序号] 作者. 题名[J]. 刊名, 年, 卷(期): 起止页码.
```

Without volume number:
```
[序号] 作者. 题名[J]. 刊名, 年(期): 起止页码.
```

Examples:
```
[3] 张华, 李明. 小学数学量感培养的实践路径[J]. 小学数学教师, 2023(3): 45-48.

[4] 王晓东. 项目化学习在小学数学中的应用研究[J]. 课程·教材·教法, 2022, 42(5): 89-95.
```

**Common error**: Do NOT write `年, 第3期:` — the correct format is `年(期):`
without "第" or "期" characters. Volume goes before issue in parentheses:
`年, 卷(期):`.

### Policy document / Legal document (政策文件) — [A/OL] or [EB/OL]

Published policy (print):
```
[序号] 发布机构. 文件名[A]. 发布地: 发布机构, 年.
```

Online policy / electronic resource:
```
[序号] 发布机构. 文件名[EB/OL]. (发布日期)[引用日期]. URL.
```

Legislative document available online:
```
[序号] 发布机构. 文件名[A/OL]. (发布日期)[引用日期]. URL.
```

Example:
```
[5] 中共中央, 国务院. 关于全面加强新时代大中小学劳动教育的意见[A/OL]. (2020-03-20)[2026-07-01]. https://www.gov.cn.
```

### Thesis (学位论文) — [D]

```
[序号] 作者. 题名[D]. 保存地: 保存单位, 年.
```

Example:
```
[6] 陈静. 小学数学几何量感培养的行动研究[D]. 桂林: 广西师范大学, 2021.
```

### Conference paper (会议论文) — [C]

```
[序号] 作者. 题名[C]//编者. 论文集名. 出版地: 出版者, 年: 页码.
```

### Electronic resource (电子资源) — [EB/OL]

```
[序号] 作者. 题名[EB/OL]. (发布日期)[引用日期]. URL.
```

---

## Document type indicators

| Code | Type | Chinese name |
|------|------|-------------|
| [S] | Standard | 标准 |
| [M] | Monograph/Book | 专著/教材 |
| [J] | Journal article | 期刊文章 |
| [D] | Dissertation | 学位论文 |
| [C] | Conference paper | 会议论文 |
| [A] | Anthology/Legal | 汇编/法律文件 |
| [EB/OL] | Electronic online | 电子资源 |
| [A/OL] | Legal online | 法律文件(在线) |
| [R] | Report | 报告 |
| [N] | Newspaper | 报纸文章 |

---

## Common mistakes to avoid

- Writing `年, 第3期: 45-48` — correct: `年(3): 45-48`
- Writing `年, 期: 45-48` — correct: `年(期): 45-48`
- Using "等" when there are 3 or fewer authors (only use "等" for 4+)
- Missing document type indicator ([J], [M], [S], etc.)
- Using full-width punctuation (．，：) for structural elements — use half-width (. , :)
- Missing access date for online resources [EB/OL]
- Missing URL for online resources
- Inconsistent author format — always surname first, comma-separated
