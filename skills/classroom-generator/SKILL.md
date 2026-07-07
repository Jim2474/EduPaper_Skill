---
name: classroom-generator
version: 0.2.0
description: |
  为单个选题生成完整的教学素材包（material.json），包含教学设计、课堂实录、
  学生作品、教学反思和数据素材五个部分。在 project.json 和 topics.json 存在、
  用户已选定选题、material.json 尚不存在时触发。适用于任何学科的教学案例研究，
  根据 project.json 中的劳动基地/实践情境动态生成素材，不硬编码任何基地信息。
  触发词：生成素材 / 生成教学材料 / 准备素材 / generate materials / 课堂素材生成。
  不写论文正文，只生成原始素材供 paper-writer 使用。
author: Jim2474
agent_created: false
---

# Classroom Generator

为一个选题生成完整素材包，写入 `.edupaper/materials/{topic-id}/material.json`。

## 启动时加载

1. 读 `../_shared/project-context.md` — 了解 project.json 字段含义
2. 读 `.edupaper/project.json` — 获取研究对象、劳动基地/实践情境、术语表、评价体系
3. 读 `.edupaper/topics.json` 中选定 topic 的条目 — 获取知识点、实践场景、切入点
4. 读 `references/material-schema.md` — 了解 material.json 五个部分的字段定义
5. 读 `references/textbook-guide.md` — 找到该知识点对应的教材单元和页码

## When to trigger

- 用户已从 topics.json 中选定一个 topic（如"选题A"）
- `.edupaper/project.json` 和 `.edupaper/topics.json` 均存在
- `.edupaper/materials/{topic-id}/material.json` 不存在

## 素材生成原则

所有素材必须**锚定 project.json 的实际上下文**：
- 实践场景从 `project.json.依据.劳动基地.典型活动` 或研究内容中取，不发明
- 学生年级/语言特征从 `project.json.研究对象.年级` 推断
- 数据（前后测均分、样本数）从 `project.json.研究对象` 的班级人数推算，保持内部一致
- 术语定义遵循 `project.json.术语表`

若 project.json 无劳动基地信息，用"课堂实践活动"替代，描述合理的课堂情景。

## Procedure

1. 读上方"启动时加载"的所有文件。
2. 根据选题的知识点和实践场景，确定课堂活动的具体形式。
3. 生成五个素材部分（详见下方）。每个部分的细节都要具体，不能泛化。
4. 数据素材中的数字必须内部一致（前后测均分、提升幅度、样本数与 project.json 匹配）。
5. **问卷调查生成（联动逻辑）**：检测 `project.json.研究设计.研究方法` 是否包含 `问卷调查法`。若是，则同步在 `.edupaper/surveys/` 目录下生成三个调查文件：
   - `student-questionnaire.md`（包含 10-12 道关于几何量感表象、估测信心、劳动与数学结合兴趣的单选或量表题）。
   - `teacher-questionnaire.md`（包含 8-10 道关于度量教学痛点、户外活动组织难度、项目评价手段的教师调查题）。
   - `survey-report.md`（问卷调查分析报告。样本量必须与 `project.json` 研究对象完全一致，即实验班与对照班各 120 人，共 240 人。包含各项问题的关键数据占比与对比分析）。
6. 写入 `.edupaper/materials/{topic-id}/material.json`（UTF-8，2空格缩进）。
7. 读 `../_shared/quality-gate.md` 执行通用质量门 + 下方 self-check。

## 五个素材部分

### 1. 教学设计（教学设计）
- 教材依据（版本、年级、单元、页码）
- 教学目标（三维：学科目标 + 实践/劳动目标 + 核心素养目标）
- 教学重难点
- 教学准备（教师/学生/场地材料）
- 完整教学过程（导入→探究→实践→总结，至少4个环节，每个环节有教师行为+学生行为+设计意图）

### 2. 课堂实录（课堂实录）
- 2-3 个关键课堂对话片段
- 格式：`师：…` / `生1：…` / `生2：…`
- 语言必须符合 project.json 中研究对象的年级水平（小学生的自然口语）
- 不能用学术语言替代学生发言

### 3. 学生作品（学生作品）
- 3-5 件学生作品的具体描述
- 每件作品：内容描述（测量记录、计算过程、绘图等）+ 教师评注 + 量感发展观察
- 描述要具体（"第三组测得种植区长3.2米、宽1.8米" 而非 "学生完成了测量"）

### 4. 教学反思（教学反思）
- 成功之处（2-3点，配具体课堂证据）
- 不足之处（2-3点，诚实且具体）
- 量感/核心素养发展观察
- 改进方向（2-3点）

### 5. 数据素材（数据素材）
- 前测：实验班均分、对照班均分（两班接近，体现同质性）
- 后测：实验班均分、对照班均分
- 提升幅度：实验班显著高于对照班
- 样本数必须与 project.json.研究对象 一致
- 数字需合理（小学数学测试，满分100，均分50-85区间合理）

## Self-check (quality gate)

- [ ] 五个部分均存在且非空
- [ ] 教学设计有目标 + 4段以上的教学过程
- [ ] 课堂实录有 2-3 个对话片段，含真实对话（非摘要）
- [ ] 学生作品有 3-5 件，描述具体（含数字或细节）
- [ ] 数据素材的数字内部一致（前测接近 → 后测实验班显著高于对照班）
- [ ] 所有数字与 project.json.研究对象 的班级人数一致
- [ ] 学生对话语言符合 project.json 研究对象年级的表达水平
- [ ] 具体细节 ≥ 3 处（具体数字、具体物品、具体操作步骤）
- [ ] **问卷联动检查**：若项目要求问卷调查，验证 `.edupaper/surveys/` 目录下 `student-questionnaire.md`、`teacher-questionnaire.md` 和 `survey-report.md` 存在且非空，报告数据（如样本数、学校等）与 project.json 完全吻合。
- [ ] JSON 有效可解析

## Constraints

- 只生成素材，不写论文正文（论文由 paper-writer 生成）
- **具体性是第一要求**：泛化描述（"学生积极参与"）不通过 self-check
- 数据不得与 project.json 矛盾（年级、班级数、人数）
- 实践场景必须能从 project.json 溯源，不发明不存在的活动
- 若 project.json 缺乏实践场景信息，使用通用"课堂动手操作"场景并备注
