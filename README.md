# EduPaper Skill

> 面向教育科研课题的论文批量生成 Skill — 适用于任何学科的教学案例论文

将一份**开题报告**，通过 9 个单一职责 Skill 的流水线，自动生成符合学术规范的
**教学案例论文**（DOCX / PDF / HTML 三格式输出）。

---

## ✨ 特性

| 特性 | 说明 |
|------|------|
| **通用型** | 适用于任何学科（数学、语文、科学等）的教育科研课题，不局限于特定基地或课题 |
| **即装即用** | Mac / Windows / Linux 全平台兼容，自动检测工具，优雅降级 |
| **防幻觉** | 期刊文献 `verified` 字段机制，虚假引用不进入最终论文 |
| **可恢复** | 中断后从断点继续，已完成阶段自动跳过，不浪费算力 |
| **质量门** | 每个 Skill 有 self-check 清单，三次重试协议，失败上报而非静默跳过 |

---

## 🏗️ 架构

```
EduPaper_Skill/
├── skills/
│   ├── _shared/                       ← 跨 skill 共享层（schema + 规范）
│   │   ├── project-context.md         # project.json 字段说明（schema）
│   │   ├── quality-gate.md            # 统一质量门与三次重试协议
│   │   └── platform-detect.md        # 跨平台工具检测指导
│   │
│   ├── edupaper-orchestrator/         ← 流水线入口（路由器）
│   │   ├── SKILL.md                   # 9步流水线编排
│   │   ├── manifest.yaml              # 声明式配置（always_load + axes）
│   │   └── references/
│   │       └── pipeline.md            # 数据流契约与目录规范
│   │
│   ├── project-parser/                ← Step 1：解析开题报告
│   ├── reference-manager/             ← Step 2：构建文献库
│   ├── topic-generator/               ← Step 3：生成选题菜单
│   ├── classroom-generator/           ← Step 4：生成教学素材
│   ├── paper-writer/                  ← Step 5：撰写论文草稿
│   ├── paper-reviewer/                ← Step 6：论文审阅
│   ├── consistency-checker/           ← Step 7：跨论文一致性检查
│   ├── edupaper-humanizer/            ← Step 8：文本人性化（可选）
│   └── edupaper-exporter/             ← Step 9：多格式导出
│       ├── SKILL.md
│       ├── scripts/
│       │   └── export_all.py          # 跨平台 Python 导出脚本
│       └── references/
│           ├── export-guide-mac.md    # macOS 安装指引
│           └── export-guide-windows.md # Windows 安装指引
```

### 数据流

```
开题报告 (PDF/DOCX/MD)
    │
    ▼
project-parser → project.json ──────────────────────────┐
    │                                                     │
    ▼                                                     │
reference-manager → references.json ──────────┐          │
    │                                          │          │
    ▼                                          │          │
topic-generator → topics.json                 │          │
    │ [用户选一个]                              │          │
    ▼                                          │          │
classroom-generator → material.json           │          │
    │                                          │          │
    ▼                                          ▼          ▼
paper-writer → paper.md ← (material + references + project)
    │
    ▼
paper-reviewer → review-report.md
    │
    ▼
consistency-checker → consistency-report.md
    │ [通过后]
    ▼
edupaper-humanizer → final.md   (可选，需安装)
    │
    ▼
edupaper-exporter → output.docx / output.pdf / output.html
```

**共享只读数据源**（一次写入，所有 skill 只读）：
- `project.json` — 仅由 project-parser 写
- `references.json` — 仅由 reference-manager 写

---

## 🚀 快速开始

### 安装

将整个 `EduPaper_Skill/skills/` 目录放到你的 Skill 根目录下：

```bash
# macOS / Linux
cp -r EduPaper_Skill/skills/* ~/.your-agent/skills/

# Windows（PowerShell）
Copy-Item -Recurse EduPaper_Skill\skills\* ~\.your-agent\skills\
```

唯一必需的运行时依赖是 **Python 3**（导出脚本）。其余工具按需安装。

### 使用

1. 准备你的**开题报告**（PDF / DOCX / MD 均可）
2. 对 agent 说：**"帮我生成论文"** 或 **"基于这份开题报告生成教学案例论文"**
3. Agent 自动运行 project-parser，然后展示选题菜单
4. 选一个选题，等待流水线完成
5. 最终文件在 `.edupaper/exports/` 目录下

### 导出工具安装

| 平台 | 最简安装 |
|------|---------|
| macOS | `brew install pandoc` |
| Windows | `winget install JohnMacFarlane.Pandoc` |
| Linux | `sudo apt install pandoc` |
| 任意平台（备用）| `pip install python-docx` |

详细安装指引见：
- [macOS 导出指引](skills/edupaper-exporter/references/export-guide-mac.md)
- [Windows 导出指引](skills/edupaper-exporter/references/export-guide-windows.md)

---

## 📐 设计原则

本 Skill 参考 [nature-skills](https://github.com/Yuan1z0825/nature-skills) 的架构哲学：

1. **单一职责**：每个 Skill 只做一件事，边界清晰，职责不重叠
2. **文件驱动**：Skill 间通过文件通信，任何平台均适用，可随时中断恢复
3. **数据驱动而非硬编码**：Skill 不包含任何特定课题数据，所有内容来自运行时的开题报告
4. **渐进式披露**：SKILL.md 是路由层（简短），深度知识在 `references/` 按需加载
5. **防幻觉设计**：`verified` 字段标记文献真实性，形成从 reference-manager 到 paper-writer 的闭环
6. **三次重试协议**：失败上报而非静默跳过，防止错误向下游传播

---

## 🔄 复用其他课题

无需修改任何 Skill 文件，直接提供新的开题报告即可：

```
新课题开题报告 → project-parser（自动解析新课题信息）→ 后续流水线照常运行
```

每个项目有自己的 `.edupaper/` 目录，互相隔离：

```
项目A/
├── 开题报告A.pdf
└── .edupaper/
    ├── project.json   # 课题A的信息
    ├── topics.json
    └── ...

项目B/
├── 开题报告B.pdf
└── .edupaper/
    ├── project.json   # 课题B的信息
    └── ...
```

---

## 📄 许可证

MIT License
