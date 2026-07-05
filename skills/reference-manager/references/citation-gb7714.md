# GB/T 7714 Citation Format Guide

Chinese national standard for bibliographic references (GB/T 7714-2015).
All citations in references.json must use this format in the `gb7714` field.

## General rules

- Number citations sequentially: [1], [2], [3]…
- List all authors; if more than 3, list first 3 followed by ", 等" (et al.)
- Use full-width punctuation within Chinese citations
- Year format: YYYY
- Page format: 起页-止页 (e.g. 45-48)

## By document type

### Standard (课标) — [S]

```
[序号] 起草单位. 标准名称: 标准号[S]. 出版地: 出版者, 年.
```

Example:
```
[1] 中华人民共和国教育部. 义务教育数学课程标准（2022年版）[S]. 北京: 北京师范大学出版社, 2022.
```

### Textbook (教材) — [M]

```
[序号] 作者. 书名[M]. 版次. 出版地: 出版者, 年: 页码.
```

Example:
```
[2] 人民教育出版社课程教材研究所. 义务教育教科书·数学（三年级上册）[M]. 北京: 人民教育出版社, 2022: 70-72.
```

### Journal article (期刊) — [J]

```
[序号] 作者. 题名[J]. 刊名, 年, 期: 起止页码.
```

Example:
```
[3] 张华, 李明. 小学数学量感培养的实践路径[J]. 小学数学教师, 2023, 第3期: 45-48.
```

With volume:
```
[4] 王晓东. 项目化学习在小学数学中的应用研究[J]. 课程·教材·教法, 2022, 42(5): 89-95.
```

### Policy document (政策文件) — [A] or [EB/OL]

Published policy:
```
[序号] 发布机构. 文件名[A]. 发布地: 发布机构, 年.
```

Online policy:
```
[序号] 发布机构. 文件名[EB/OL]. (发布日期)[引用日期]. URL.
```

Example:
```
[5] 中共中央, 国务院. 关于全面加强新时代大中小学劳动教育的意见[EB/OL]. (2020-03-20)[2026-07-01]. http://www.gov.cn/zhengce/2020-03/20/content_5493601.htm.
```

### Thesis (学位论文) — [D]

```
[序号] 作者. 题名[D]. 保存地: 保存单位, 年.
```

Example:
```
[6] 陈静. 小学数学几何量感培养的行动研究[D]. 桂林: 广西师范大学, 2021.
```

### Monograph (专著) — [M]

```
[序号] 作者. 书名[M]. 版次. 出版地: 出版者, 年.
```

Example:
```
[7] 史宁中. 基本概念与运算法则[M]. 北京: 高等教育出版社, 2013.
```

### Conference paper (会议论文) — [C]

```
[序号] 作者. 题名[C]//编者. 论文集名. 出版地: 出版者, 年: 页码.
```

---

## Common mistakes to avoid

- Using English-style citation format (Vancouver/APA) — this is Chinese GB/T 7714
- Missing document type indicator ([J], [M], [S], etc.)
- Inconsistent author format — always list surname first, no spaces between
  Chinese characters
- Missing page numbers for journal articles
- Using "等" when there are 3 or fewer authors (only use "等" for 4+)
