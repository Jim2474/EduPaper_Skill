#!/bin/bash
# export_all.sh — Export a Markdown paper to DOCX, PDF, and HTML
# Usage: bash export_all.sh <input.md> [output_dir] [formats]
# formats: all | docx | pdf | html (comma-separated, default: all)
#
# Part of edupaper-exporter skill.

set -euo pipefail

INPUT_FILE="${1:?Usage: $0 <input.md> [output_dir] [formats]}"
OUTPUT_DIR="${2:-.edupaper/exports}"
FORMATS="${3:-all}"

# Resolve paths
INPUT_FILE="$(cd "$(dirname "$INPUT_FILE")" && pwd)/$(basename "$INPUT_FILE")"
BASE_NAME="$(basename "$INPUT_FILE" .md)"
mkdir -p "$OUTPUT_DIR"

# Detect Chinese font (try SimSun → STSong → Songti SC → PingFang SC)
detect_cjk_font() {
    local font
    font=$(fc-list :lang=zh family 2>/dev/null | grep -i "simsun" | head -1 | tr -d ',')
    [ -n "$font" ] && echo "$font" && return
    font=$(fc-list :lang=zh family 2>/dev/null | grep -i "stsong" | head -1 | tr -d ',')
    [ -n "$font" ] && echo "$font" && return
    font=$(fc-list :lang=zh family 2>/dev/null | grep -i "songti" | head -1 | tr -d ',')
    [ -n "$font" ] && echo "$font" && return
    echo "PingFang SC"
}

CJK_FONT=$(detect_cjk_font)
echo "Using CJK font: $CJK_FONT"

# Check pandoc
if ! command -v pandoc &>/dev/null; then
    echo "ERROR: pandoc is not installed."
    echo "Install: brew install pandoc"
    echo "Or use the Python fallback (DOCX + HTML only)."
    echo "See references/export-guide.md for details."
    exit 1
fi

# Determine which formats to export
if [ "$FORMATS" = "all" ]; then
    FORMAT_LIST="docx pdf html"
else
    FORMAT_LIST=$(echo "$FORMATS" | tr ',' ' ')
fi

# Get script directory for templates
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEMPLATE_DIR="$(dirname "$SCRIPT_DIR")/assets/templates"
LATEX_TEMPLATE="$TEMPLATE_DIR/edupaper.tex"

# Export DOCX
export_docx() {
    local output="$OUTPUT_DIR/${BASE_NAME}.docx"
    echo "  → DOCX: $output"
    pandoc "$INPUT_FILE" -o "$output" \
        --from markdown \
        --to docx \
        --toc \
        --toc-depth=2 \
        --highlight-style=tango 2>&1 || echo "  WARN: DOCX export had warnings"
    [ -f "$output" ] && echo "  ✓ DOCX created" || echo "  ✗ DOCX failed"
}

# Export PDF
export_pdf() {
    local output="$OUTPUT_DIR/${BASE_NAME}.pdf"

    # Check xelatex
    if ! command -v xelatex &>/dev/null; then
        echo "  → PDF: SKIPPED (xelatex not installed)"
        echo "    Install: brew install --cask basictex (or mactex)"
        return 0
    fi

    echo "  → PDF: $output"

    local pdf_args=(
        pandoc "$INPUT_FILE" -o "$output"
        --pdf-engine=xelatex
        --toc
        --toc-depth=2
        --highlight-style=tango
        -V CJKmainfont="$CJK_FONT"
        -V mainfont="$CJK_FONT"
        -V geometry:margin=2.5cm
        -V fontsize=12pt
        -V linestretch=1.5
        -V colorlinks=true
        -V linkcolor=blue
    )

    # Add LaTeX template if available
    if [ -f "$LATEX_TEMPLATE" ]; then
        pdf_args+=(--template="$LATEX_TEMPLATE")
    fi

    "${pdf_args[@]}" 2>&1 || echo "  WARN: PDF export had warnings"
    [ -f "$output" ] && echo "  ✓ PDF created" || echo "  ✗ PDF failed"
}

# Export HTML
export_html() {
    local output="$OUTPUT_DIR/${BASE_NAME}.html"
    local title="$BASE_NAME"
    echo "  → HTML: $output"
    pandoc "$INPUT_FILE" -o "$output" \
        --standalone \
        --embed-resources \
        --toc \
        --toc-depth=2 \
        --highlight-style=tango \
        --metadata title="$title" \
        -V lang=zh-CN 2>&1 || echo "  WARN: HTML export had warnings"
    [ -f "$output" ] && echo "  ✓ HTML created" || echo "  ✗ HTML failed"
}

# Run exports
echo "========================================="
echo "Exporting: $BASE_NAME"
echo "Output dir: $OUTPUT_DIR"
echo "Formats: $FORMAT_LIST"
echo "========================================="

for fmt in $FORMAT_LIST; do
    case "$fmt" in
        docx) export_docx ;;
        pdf)  export_pdf ;;
        html) export_html ;;
        *)    echo "  Unknown format: $fmt" ;;
    esac
done

echo ""
echo "========================================="
echo "Export complete!"
echo "========================================="
ls -lh "$OUTPUT_DIR/${BASE_NAME}".* 2>/dev/null || echo "No files exported."
