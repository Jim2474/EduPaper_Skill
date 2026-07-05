---
name: edupaper-exporter
version: 0.1.0
description: |
  Export Markdown papers to Word (DOCX), PDF, and HTML formats. Designed as
  the default export module for EduPaper projects — reads from
  .edupaper/papers/*.md and writes to .edupaper/exports/. Uses pandoc as the
  primary engine with XeLaTeX for Chinese-aware PDF generation. Includes a
  Python fallback when pandoc is not installed. Handles Chinese academic
  paper formatting: SimSun body font, SimHei headings, proper margins, and
  GB/T 7714 reference styling. This skill should be used after
  edupaper-humanizer produces final.md and the paper is copied to
  .edupaper/papers/.
agent_created: true
---

# EduPaper Exporter

Export one or more Markdown papers to Word, PDF, and HTML. Read from
`.edupaper/papers/` and write to `.edupaper/exports/`.

## When to trigger

- User says "导出论文" / "export papers" / "转成 Word" / "生成 PDF"
- `.edupaper/papers/*.md` exists and needs format conversion
- Orchestrator routes here as the final export stage

## Procedure

1. Check if `pandoc` is installed (`pandoc --version`). If not, read
   `references/export-guide.md` for installation instructions and the
   Python fallback path.
2. List all `.md` files in `.edupaper/papers/`.
3. For each paper, ask the user which formats to export (or export all
   three if user says "全部导出").
4. Read `references/export-guide.md` for the exact pandoc commands and
   Chinese font configuration.
5. Run `scripts/export_all.sh` with the paper path and desired formats.
6. Verify each output file was created in `.edupaper/exports/`.
7. Run the self-check.

## Export formats

1. **DOCX (Word)** — `pandoc input.md -o output.docx --reference-doc=template`
   Uses a reference document for consistent styling. Chinese text renders
   natively. Tables and citations preserved.
2. **PDF** — `pandoc input.md -o output.pdf --pdf-engine=xelatex
   --template=edupaper.tex -V CJKmainfont="SimSun"`
   XeLaTeX with CJK font support. Chinese-aware margins and headings.
3. **HTML** — `pandoc input.md -o output.html --standalone
   --embed-resources --css=style.css`
   Self-contained HTML with embedded CSS. Suitable for web publishing.

## Self-check (quality gate)

- [ ] All requested format files exist in `.edupaper/exports/`
- [ ] PDF opens without encoding errors (Chinese characters render)
- [ ] DOCX opens in Word with correct formatting (headings, tables)
- [ ] HTML displays correctly in browser (CSS embedded, no broken links)
- [ ] No pandoc warnings about missing fonts or packages
- [ ] Export filenames match source paper filenames

## Constraints

- Default output directory is `.edupaper/exports/`. Create if not exists.
- If pandoc is not installed, use the Python fallback (see
  `references/export-guide.md` "Fallback" section). Python fallback
  produces DOCX and HTML only — PDF requires pandoc + LaTeX.
- Chinese font: use SimSun (宋体) for body, SimHei (黑体) for headings.
  If these fonts are unavailable, fall back to PingFang SC / STSong.
- Do not modify the source `.md` files — only read and convert.
- Preserve all [n] citation markers and 参考文献 section in exports.
