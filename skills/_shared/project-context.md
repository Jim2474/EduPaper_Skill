# project.json 字段说明 — EduPaper 共享 Schema 参考

本文件是 EduPaper pipeline 所有 skill 的**字段使用指南**，说明 `project.json`
的结构和每个字段的含义。

**重要**：本文件是 schema 文档，不包含任何具体课题数据。
实际数据由 `project-parser` 从用户提供的开题报告解析后写入 `.edupaper/project.json`。
所有 skill 读取实际数据时，请读 `.edupaper/project.json`，而非本文件。

---

## project.json 完整字段说明

```jsonc
{
  "meta": {
    "课题名称": "string — 课题完整标题",
    "批准号":   "string — 课题批准编号，如 2026XKT-JYKY88，或 __MISSING__",
    "主持人":   "string — 课题主持人姓名",
    "单位":     "string — 主持人所在学校/机构",
    "研究周期": "string — 起止时间，如 '2026年2月—2027年6月'"
  },

  "研究对象": {
    "学段":   "string — 如 '小学中年段（三至四年级）'",
    "年级":   "string — 具体年级，如 '三年级' 或 '二三四年级'",
    "总人数": "integer — 参与研究的学生总数",
    "实验班": {
      "班数":   "integer",
      "每班人数": "integer（约）",
      "小计":   "integer"
    },
    "对照班": {
      "班数":   "integer",
      "每班人数": "integer（约）",
      "小计":   "integer"
    }
  },

  "依据": {
    "课标": "string — 引用的课程标准名称，可多个，用分号分隔",
    "教材": "string — 教材版本，如 '人教版三年级下册'",
    "劳动基地": {
      "名称":   "string — 基地名称，如 '雅趣园'",
      "位置":   "string — 基地位置描述",
      "典型活动": ["string — 基地的典型劳动活动，尽量具体，每项一个字符串"]
    }
  },

  "核心概念": [
    "string — 课题涉及的核心学术概念列表"
  ],

  "术语表": {
    "术语名": "定义文字"
  },

  "研究设计": {
    "研究目标": "string — 课题总体研究目标",
    "研究内容": [
      "string — 研究内容①描述",
      "string — 研究内容②描述",
      "string — 研究内容③描述（如有）"
    ],
    "研究方法": ["string — 研究方法列表"],
    "创新点":   ["string — 课题创新点列表"]
  },

  "评价体系": {
    "维度": ["string — 评价维度名称列表"],
    "指标数": "integer — 评价指标总数",
    "工具":   ["string — 评价工具列表"]
  },

  "成员分工": {
    "姓名": "string — 该成员的职责描述"
  }
}
```

---

## 各 skill 使用本 schema 的方式

| Skill | 关键读取字段 |
|-------|------------|
| topic-generator | 研究对象.年级、依据.劳动基地.典型活动、研究设计.研究内容、研究设计.创新点 |
| classroom-generator | 研究对象、依据.劳动基地、术语表、核心概念 |
| paper-writer | meta、研究对象、核心概念、术语表、评价体系 |
| paper-reviewer | 研究对象、核心概念、术语表、评价体系 |
| consistency-checker | 研究对象、依据、术语表（共享事实验证） |
| reference-manager | 依据.课标、依据.教材、研究设计.研究内容、核心概念 |

---

## 缺失值规范

- 任何在开题报告中找不到的字段，填写 `"__MISSING__"` 而非 `null` 或留空
- project-parser 在三次尝试后仍无法提取的字段，必须标注 `__MISSING__` 并上报
- 下游 skill 遇到 `__MISSING__` 值时，必须暂停并向用户说明缺少哪个字段

---

## 字段类型说明

- `string` — 字符串
- `integer` — 整数
- `["string"]` — 字符串数组
- `{"key": "string"}` — 键值对对象
- `__MISSING__` — 特殊标记，表示该字段在开题报告中未找到，需人工补充
