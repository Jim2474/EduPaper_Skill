---
name: edupaper-exporter
version: 0.2.0
description: |
  将论文 Markdown 文件导出为标准格式（DOCX、PDF、HTML）。
  在 final.md 或 paper.md 存在时触发。适用于 macOS、Windows、Linux，
  自动检测可用工具，优雅降级。
  触发词：导出论文 / 转成Word / 转成PDF / 生成Word / 下载论文 / 导出Word /
  export paper / convert to docx / 把论文转成文件 / 输出最终文件。
  本 skill 是流水线最后一步，不修改论文内容，只负责格式转换。
author: Jim2474
agent_created: false
---

# EduPaper Exporter

将 `.edupaper/drafts/{id}/final.md`（或 paper.md）转为 DOCX / PDF / HTML，
写入 `.edupaper/exports/`。

## 启动时加载

1. 读 `../_shared/platform-detect.md` — 了解跨平台检测方法和字体优先级
2. 读 `references/export-guide-mac.md` 或 `references/export-guide-windows.md`
   — 按用户平台加载对应安装指引（检测到 Windows 则读 Windows 版）

## When to trigger

- `.edupaper/drafts/{id}/final.md` 存在（humanizer 已完成）
  — 优先使用 final.md
- 或 `.edupaper/drafts/{id}/paper.md` 存在（humanizer 未安装时的回退）
- 用户说"导出论文" / "转成Word" / "生成PDF"

## 导出决策树

在运行任何导出命令之前，先检测环境。默认情况下仅导出 DOCX 格式（若用户无特别指定）：

```
默认流程：
- 导出 DOCX (优先使用 pandoc，若无则使用 python-docx 降级导出)
- 若用户明确要求 PDF 且 xelatex 可用，或明确要求 HTML 且 pandoc 可用，则按需导出对应格式。
```

## Procedure

1. 读 `../_shared/platform-detect.md`，检测平台和工具可用性（参考其中的检测代码）。
2. 根据平台选择中文字体（参考 `platform-detect.md` 中的 FONT_MAP）。
3. 向用户展示检测结果（平台、可用工具，默认仅导出 DOCX）。
4. 运行 `scripts/export_all.py` 执行实际导出（默认仅导出 docx）：
   ```
   python scripts/export_all.py <input.md> --formats docx --output-dir .edupaper/exports/
   ```
   - Windows：`python` 或 `py`（取决于安装方式）
   - macOS/Linux：`python3`
5. 确认输出文件存在且大小 > 0。
6. 运行 self-check。

## 直接调用（无 Python）

若无法运行 Python 脚本，退回到直接调用 pandoc 命令：

**DOCX（macOS/Linux）：**
```bash
pandoc input.md -o output.docx
```

**DOCX（Windows PowerShell）：**
```powershell
pandoc input.md -o output.docx
```

**PDF（需 XeLaTeX，macOS 示例）：**
```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex \
  -V CJKmainfont="STSong" -V geometry:margin=2.54cm
```

**PDF（Windows 示例，宋体）：**
```powershell
pandoc input.md -o output.pdf --pdf-engine=xelatex `
  -V CJKmainfont="宋体" -V geometry:margin=2.54cm
```

## Self-check (quality gate)

- [ ] 请求格式中至少有一个导出成功（DOCX / PDF / HTML）
- [ ] 导出文件大小 > 0 字节
- [ ] 论文标题出现在 DOCX 或 HTML 文件中（格式未损坏）
- [ ] 若 PDF 导出失败，已向用户说明原因和安装方法

## Constraints

- 不修改论文 Markdown 内容，只做格式转换
- 若所有工具均不可用，输出清晰的安装指引（参考 platform-detect.md）而非报错退出
- Windows 用户：路径分隔符在命令行中使用反斜杠 `\` 或加引号的正斜杠
- 导出前先向用户确认将要导出的格式和目标路径
