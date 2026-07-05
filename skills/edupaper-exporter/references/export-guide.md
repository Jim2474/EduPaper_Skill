# Export Guide

Detailed pandoc commands, Chinese font configuration, installation
instructions, and Python fallback for the edupaper-exporter skill.

---

## Prerequisites

### Primary path (pandoc + LaTeX)

Install pandoc and XeLaTeX on macOS:

```bash
# Install pandoc
brew install pandoc

# Install LaTeX (for PDF generation with Chinese support)
# Option A: Full MacTeX (large, ~4GB)
brew install --cask mactex

# Option B: BasicTeX (smaller, ~100MB, may need extra packages)
brew install --cask basictex
# After BasicTeX install, add Chinese font support:
sudo tlmgr install ctex xecjk

# Install pandoc-crossref (optional, for cross-references)
brew install pandoc-crossref
```

Verify installation:
```bash
pandoc --version          # should show 2.x or 3.x
xelatex --version         # should show XeTeX 3.x
fc-list :lang=zh          # should list Chinese fonts
```

### Check available Chinese fonts

```bash
# Common Chinese fonts on macOS:
# - SimSun (宋体) — may need manual install
# - PingFang SC (苹方) — default macOS Chinese font
# - STSong (华文宋体) — macOS built-in
# - Heiti SC (黑体) — macOS built-in

fc-list :lang=zh family | sort -u
```

If SimSun is not available, use `PingFang SC` or `STSong` as fallback.

---

## Export commands

### 1. Markdown → DOCX (Word)

```bash
pandoc "$INPUT" -o "$OUTPUT.docx" \
    --from markdown \
    --to docx \
    --toc \
    --toc-depth=2 \
    --highlight-style=tango
```

**With reference document** (for custom styling):

```bash
# Generate a reference docx first (one-time setup):
pandoc -o reference.docx --print-default-data-file reference.docx

# Then use it:
pandoc "$INPUT" -o "$OUTPUT.docx" \
    --reference-doc=reference.docx \
    --toc \
    --toc-depth=2
```

Chinese text renders natively in DOCX — no special font flags needed.
Word will use the system default Chinese font (usually SimSun on Windows,
PingFang SC on macOS).

### 2. Markdown → PDF (XeLaTeX + Chinese)

```bash
pandoc "$INPUT" -o "$OUTPUT.pdf" \
    --pdf-engine=xelatex \
    --template=assets/templates/edupaper.tex \
    --toc \
    --toc-depth=2 \
    -V mainfont="SimSun" \
    -V CJKmainfont="SimSun" \
    -V sansfont="SimHei" \
    -V CJKsansfont="SimHei" \
    -V monofont="Menlo" \
    -V geometry:margin=2.5cm \
    -V fontsize=12pt \
    -V linestretch=1.5
```

**Font fallback chain** (try in order):

```bash
# Try SimSun first, fall back to STSong, then PingFang SC
FONT=$(fc-list :lang=zh family | grep -i "simsun" | head -1)
if [ -z "$FONT" ]; then
    FONT=$(fc-list :lang=zh family | grep -i "stsong" | head -1)
fi
if [ -z "$FONT" ]; then
    FONT="PingFang SC"
fi
```

**Common PDF options:**

| Option | Effect |
|--------|--------|
| `--toc` | Add table of contents |
| `--number-sections` | Number section headings |
| `-V geometry:margin=2.5cm` | Set page margins |
| `-V fontsize=12pt` | Body font size |
| `-V linestretch=1.5` | Line spacing (1.5x) |
| `--highlight-style=tango` | Code syntax highlighting |
| `-V colorlinks=true` | Colored hyperlinks |
| `-V linkcolor=blue` | Link color |

### 3. Markdown → HTML

```bash
pandoc "$INPUT" -o "$OUTPUT.html" \
    --standalone \
    --embed-resources \
    --toc \
    --toc-depth=2 \
    --highlight-style=tango \
    --metadata title="$TITLE" \
    -V lang=zh-CN
```

`--embed-resources` makes the HTML self-contained (CSS, images embedded).
For Chinese HTML, add `lang="zh-CN"` metadata.

**Custom CSS for Chinese academic papers:**

```css
body {
    font-family: "SimSun", "STSong", "PingFang SC", serif;
    font-size: 16px;
    line-height: 1.8;
    max-width: 800px;
    margin: 2em auto;
    padding: 0 1em;
    color: #333;
}
h1, h2, h3 {
    font-family: "SimHei", "PingFang SC", sans-serif;
    font-weight: bold;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}
th, td {
    border: 1px solid #ddd;
    padding: 8px 12px;
    text-align: left;
}
th {
    background-color: #f5f5f5;
    font-weight: bold;
}
```

Save as `assets/templates/style.css` and reference with `--css=style.css`.

---

## Batch export

The `scripts/export_all.sh` script exports a single Markdown file to all
three formats:

```bash
# Export one paper to all formats:
bash scripts/export_all.sh .edupaper/papers/A-论文标题.md

# Export all papers:
for f in .edupaper/papers/*.md; do
    bash scripts/export_all.sh "$f"
done
```

Output goes to `.edupaper/exports/` with the same base filename.

---

## Python fallback (when pandoc is not installed)

If pandoc is unavailable, use Python libraries as a fallback. This produces
DOCX and HTML only — PDF requires pandoc + LaTeX.

### Install Python dependencies

```bash
pip install python-docx markdown weasyprint
```

### DOCX via python-docx

```python
from docx import Document
from docx.shared import Pt, Cm
from docx.oxml.ns import qn
import re

def md_to_docx(md_path, docx_path):
    doc = Document()
    # Set default font to SimSun for Chinese
    style = doc.styles['Normal']
    style.font.name = 'SimSun'
    style.font.size = Pt(12)
    style.element.rPr.rFonts.set(qn('w:eastAsia'), 'SimSun')

    with open(md_path, 'r') as f:
        for line in f:
            line = line.rstrip()
            if line.startswith('# '):
                doc.add_heading(line[2:], level=1)
            elif line.startswith('## '):
                doc.add_heading(line[3:], level=2)
            elif line.startswith('### '):
                doc.add_heading(line[4:], level=3)
            elif line.startswith('|'):
                # Skip table formatting rows, handle simple tables
                doc.add_paragraph(line)
            elif line.strip():
                doc.add_paragraph(line)

    doc.save(docx_path)
```

### HTML via markdown

```python
import markdown

def md_to_html(md_path, html_path):
    with open(md_path, 'r') as f:
        text = f.read()
    html = markdown.markdown(text, extensions=['tables', 'toc'])
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>论文</title>
<style>
body {{ font-family: "SimSun", "STSong", "PingFang SC", serif;
       font-size: 16px; line-height: 1.8; max-width: 800px;
       margin: 2em auto; padding: 0 1em; }}
h1, h2, h3 {{ font-family: "SimHei", sans-serif; }}
table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
th, td {{ border: 1px solid #ddd; padding: 8px; }}
th {{ background: #f5f5f5; }}
</style></head>
<body>{html}</body></html>"""
    with open(html_path, 'w') as f:
        f.write(full_html)
```

---

## Troubleshooting

### PDF: "CJKmainfont not found"

XeLaTeX can't find the specified Chinese font. Fix:

```bash
# List available Chinese fonts
fc-list :lang=zh family | sort -u

# Use an available font name exactly as listed
# Common macOS Chinese fonts:
#   PingFang SC
#   STSong
#   Heiti SC
#   Songti SC
```

### PDF: "latexmk: command not found"

LaTeX is not installed. Install via:

```bash
brew install --cask basictex
# or full version:
brew install --cask mactex
```

### DOCX: Chinese characters show as boxes

The Word document doesn't have a Chinese font set. Use a reference docx
with Chinese font configured, or set the font in the pandoc command:

```bash
pandoc input.md -o output.docx -V mainfont="SimSun"
```

### HTML: CSS not applied

Ensure `--standalone` and `--embed-resources` flags are used. For custom
CSS, use `--css=style.css` and `--embed-resources` to inline it.

### Tables not rendering in DOCX

Pandoc handles pipe tables natively. Ensure the Markdown table has proper
separator rows:

```markdown
| Col1 | Col2 |
|------|------|
| a    | b    |
```

### Citations [n] appear as plain text in DOCX

Citation markers like [1], [2] are plain text in the Markdown, not pandoc
citation syntax. They will appear as-is in all formats. This is correct
for EduPaper papers — the 参考文献 section lists them manually.

---

## EduPaper integration

The exporter integrates with EduPaper's directory structure:

```
.edupaper/
├── papers/                    # Source Markdown files (input)
│   └── A-论文标题.md
└── exports/                   # Exported files (output)
    ├── A-论文标题.docx
    ├── A-论文标题.pdf
    └── A-论文标题.html
```

The export script reads from `papers/` and writes to `exports/`, never
modifying the source files.
