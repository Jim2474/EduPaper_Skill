# material.json Schema

Field definitions for the teaching material package.

## Top-level structure

```
material.json
├── topic_id
├── 教学设计
├── 课堂实录
├── 学生作品
├── 教学反思
└── 数据素材
```

---

## topic_id

string — must match the selected topic's id in topics.json (e.g. "A").

---

## 教学设计

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| 课题 | string | yes | Lesson title |
| 教材依据 | string | yes | Textbook unit + page (from textbook-guide.md) |
| 教学目标 | object | yes | { 数学目标, 劳动目标, 量感目标 } |
| 教学重点 | string | yes | Key focus of the lesson |
| 教学难点 | string | yes | Anticipated difficulty |
| 教学准备 | object | yes | { 教师准备, 学生准备, 场地材料 } |
| 教学过程 | array | yes | 4+ stages, each with 环节/教师活动/学生活动/设计意图 |

教学过程 stage object:
```
{
  "环节": "创设情境，提出问题",
  "教师活动": "带学生到雅趣园种植区，指着一块长方形菜地...",
  "学生活动": "观察菜地，讨论如何知道这块地有多大",
  "设计意图": "从真实劳动场景引出面积测量需求"
}
```

---

## 课堂实录

Array of 2-3 dialogue fragment objects.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| 片段标题 | string | yes | e.g. "测量种植区面积" |
| 情境描述 | string | yes | What's happening (1-2 sentences) |
| 对话 | array | yes | Array of {角色, 内容} turns |

对话 turn object:
```
{ "角色": "教师", "内容": "同学们，这块菜地大约有多大？我们怎么量？" }
{ "角色": "学生1", "内容": "可以用尺子量！量多长多宽。" }
{ "角色": "学生2", "内容": "上次我们学了面积，长乘宽就是面积！" }
```

Dialogue rules:
- Student speech: short, colloquial, age-appropriate (三年级 ≈ 9-10 years old)
- Avoid academic vocabulary in student speech
- Include mistakes and corrections for realism
- 5-10 turns per fragment

---

## 学生作品

Array of 3-5 work sample objects.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| 作品编号 | string | yes | e.g. "作品1" |
| 作品类型 | string | yes | 任务单 / 测量记录 / 绘图 / 计算过程 |
| 学生描述 | string | yes | Which group/student (anonymized) |
| 内容描述 | string | yes | What the work shows (specific) |
| 教师评注 | string | yes | Brief assessment note |

Example:
```
{
  "作品编号": "作品3",
  "作品类型": "测量记录",
  "学生描述": "第三组（4人）",
  "内容描述": "用卷尺测量A区种植箱，记录长2.4米、宽1.2米，计算面积2.88平方米。测量时卷尺未拉直，首次记录2.6米，经组员提醒后修正。",
  "教师评注": "能发现并修正测量误差，体现了量感的初步建立。"
}
```

---

## 教学反思

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| 成功之处 | array | yes | 2-3 items, each a string |
| 不足之处 | array | yes | 2-3 items |
| 改进方向 | array | yes | 2-3 items |
| 量感观察 | string | yes | Specific observation of students' 量感 development |

---

## 数据素材

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| 前测 | object | yes | { 描述, 实验班均分, 对照班均分, 样本数 } |
| 后测 | object | yes | { 描述, 实验班均分, 对照班均分, 样本数 } |
| 提升幅度 | object | yes | { 实验班提升, 对照班提升, 差异说明 } |
| 课堂观察 | object | yes | { 观察维度, 实验班表现, 对照班表现 } |

Data plausibility rules:
- 前测 scores: 40-65 range (students haven't learned the concept yet)
- 后测 scores: 70-90 range (after instruction)
- 实验班 post-test should be higher than 对照班 by 5-15 points
- 样本数 must match project.json 研究对象 numbers
- Use one decimal place for averages (e.g. 78.5)

Example:
```
"前测": {
  "描述": "面积量感认知前测（10题，每题10分）",
  "实验班均分": 52.3,
  "对照班均分": 51.8,
  "样本数": "实验班120人，对照班120人"
}
```
