#!/usr/bin/env python3
"""
export_python.py — Python fallback exporter for EduPaper papers.
Produces DOCX and HTML when pandoc is not installed.
PDF requires pandoc + LaTeX (see references/export-guide.md).

Usage:
    python3 export_python.py <input.md> <output_dir> [formats]
    formats: all,docx,html (default: all)

Part of edupaper-exporter skill.
"""

import sys
import os
import re
from pathlib import Path

def md_to_docx(md_path: str, docx_path: str):
    """Convert Markdown to DOCX using python-docx."""
    from docx import Document
    from docx.shared import Pt, Cm, Inches
    from docx.oxml.ns import qn
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    doc = Document()

    # Set default font — SimSun for Chinese, Times New Roman for Latin
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    rfonts.set(qn('w:eastAsia'), 'SimSun')

    # Set page margins (2.5cm)
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)

    # Set heading fonts — SimHei for Chinese headings
    for level in range(1, 4):
        heading_style = doc.styles[f'Heading {level}']
        heading_style.font.name = 'Times New Roman'
        heading_style.font.bold = True
        rpr_h = heading_style.element.get_or_add_rPr()
        rfonts_h = rpr_h.get_or_add_rFonts()
        rfonts_h.set(qn('w:eastAsia'), 'SimHei')

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    in_table = False
    table_rows = []

    def flush_table():
        nonlocal table_rows, in_table
        if not table_rows:
            in_table = False
            return
        # Create table
        cols = len(table_rows[0])
        table = doc.add_table(rows=len(table_rows), cols=cols)
        table.style = 'Table Grid'
        for r_idx, row in enumerate(table_rows):
            for c_idx, cell_text in enumerate(row):
                if c_idx < cols:
                    clean = re.sub(r'\*\*(.+?)\*\*', r'\1', cell_text).strip()
                    table.cell(r_idx, c_idx).text = clean
        doc.add_paragraph()
        table_rows = []
        in_table = False

    while i < len(lines):
        line = lines[i].rstrip('\n')

        # Skip YAML frontmatter
        if i == 0 and line == '---':
            while i < len(lines) and lines[i].rstrip('\n') != '---':
                i += 1
            i += 1
            continue

        # Headings
        if line.startswith('# ') and not line.startswith('## '):
            doc.add_heading(line[2:], level=1)
        elif line.startswith('## '):
            flush_table()
            doc.add_heading(line[3:], level=2)
        elif line.startswith('### '):
            flush_table()
            doc.add_heading(line[4:], level=3)
        elif line.startswith('#### '):
            flush_table()
            doc.add_heading(line[5:], level=4)
        # Table rows
        elif line.startswith('|'):
            if '---' in line or '===' in line:
                # Skip separator row
                i += 1
                continue
            cells = [c.strip() for c in line.split('|')[1:-1]]
            table_rows.append(cells)
            in_table = True
        # Empty line
        elif not line.strip():
            flush_table()
        # Bold paragraph (like **摘要：**)
        elif line.startswith('**') and '**' in line[2:]:
            p = doc.add_paragraph()
            parts = re.split(r'\*\*(.+?)\*\*', line)
            for j, part in enumerate(parts):
                if not part:
                    continue
                run = p.add_run(part)
                if j % 2 == 1:  # Odd indices are bold
                    run.bold = True
        # Regular paragraph
        else:
            flush_table()
            # Clean markdown formatting
            clean = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
            clean = re.sub(r'\[(\d+)\]', r'[\1]', clean)
            if clean.strip():
                doc.add_paragraph(clean)

        i += 1

    flush_table()
    doc.save(docx_path)
    print(f"  ✓ DOCX created: {docx_path}")


def md_to_html(md_path: str, html_path: str):
    """Convert Markdown to standalone HTML using markdown library."""
    import markdown

    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Remove YAML frontmatter
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)

    # Convert markdown to HTML
    html_body = markdown.markdown(
        text,
        extensions=['tables', 'toc', 'nl2br', 'sane_lists']
    )

    # Extract title from first H1
    title_match = re.search(r'<h1>(.+?)</h1>', html_body)
    title = title_match.group(1) if title_match else '论文'

    # Build full HTML document
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: "SimSun", "STSong", "PingFang SC", serif;
            font-size: 16px;
            line-height: 1.8;
            max-width: 800px;
            margin: 2em auto;
            padding: 0 2em;
            color: #333;
            background: #fff;
        }}
        h1 {{
            font-family: "SimHei", "PingFang SC", sans-serif;
            font-size: 1.6em;
            text-align: center;
            margin-bottom: 0.5em;
            color: #222;
        }}
        h2 {{
            font-family: "SimHei", "PingFang SC", sans-serif;
            font-size: 1.3em;
            margin-top: 1.5em;
            border-bottom: 1px solid #eee;
            padding-bottom: 0.3em;
        }}
        h3 {{
            font-family: "SimHei", "PingFang SC", sans-serif;
            font-size: 1.1em;
            margin-top: 1em;
        }}
        p {{
            text-indent: 2em;
            margin: 0.5em 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
            font-size: 14px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background-color: #f5f5f5;
            font-family: "SimHei", sans-serif;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #fafafa;
        }}
        blockquote {{
            border-left: 3px solid #ccc;
            margin: 1em 0;
            padding: 0.5em 1em;
            color: #666;
            background: #f9f9f9;
        }}
        strong {{
            font-weight: bold;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        .references {{
            font-size: 14px;
            line-height: 1.6;
        }}
        .references p {{
            text-indent: 0;
            padding-left: 2em;
            text-indent: -2em;
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"  ✓ HTML created: {html_path}")


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input.md> <output_dir> [formats]")
        print(f"  formats: all,docx,html (default: all)")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    formats = sys.argv[3] if len(sys.argv) > 3 else 'all'

    base_name = Path(input_file).stem
    os.makedirs(output_dir, exist_ok=True)

    format_list = ['docx', 'html'] if formats == 'all' else formats.split(',')

    print(f"=========================================")
    print(f"Exporting: {base_name}")
    print(f"Output dir: {output_dir}")
    print(f"Formats: {', '.join(format_list)}")
    print(f"=========================================")

    for fmt in format_list:
        if fmt == 'docx':
            docx_path = os.path.join(output_dir, f"{base_name}.docx")
            try:
                md_to_docx(input_file, docx_path)
            except Exception as e:
                print(f"  ✗ DOCX failed: {e}")
        elif fmt == 'html':
            html_path = os.path.join(output_dir, f"{base_name}.html")
            try:
                md_to_html(input_file, html_path)
            except Exception as e:
                print(f"  ✗ HTML failed: {e}")
        elif fmt == 'pdf':
            print(f"  → PDF: SKIPPED (requires pandoc + LaTeX)")
            print(f"    Install: brew install pandoc && brew install --cask basictex")
        else:
            print(f"  Unknown format: {fmt}")

    print(f"\n=========================================")
    print(f"Export complete!")
    print(f"=========================================")
    for f in os.listdir(output_dir):
        if f.startswith(base_name):
            size = os.path.getsize(os.path.join(output_dir, f))
            print(f"  {f} ({size:,} bytes)")


if __name__ == '__main__':
    main()
