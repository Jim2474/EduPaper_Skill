# EduPaper 导出指引 — macOS

## 快速开始

运行以下命令导出论文（在项目根目录执行）：

```bash
python3 skills/edupaper-exporter/scripts/export_all.py \
  .edupaper/drafts/A/final.md \
  --formats docx,pdf,html \
  --output-dir .edupaper/exports/
```

---

## 工具安装

### 1. pandoc（必须，用于 DOCX 和 HTML）

```bash
# 推荐：Homebrew
brew install pandoc

# 验证：
pandoc --version
```

### 2. XeLaTeX（可选，用于 PDF）

```bash
# 方案一：BasicTeX（轻量，约 90MB）
brew install --cask basictex
# 安装后重启终端，再安装中文支持：
sudo tlmgr update --self
sudo tlmgr install ctex xecjk

# 方案二：MacTeX（完整版，约 4GB，开箱即用）
brew install --cask mactex
```

### 3. python-docx（备用方案，无需 pandoc）

```bash
pip3 install python-docx
```

---

## 中文字体说明

macOS 上 EduPaper 按以下优先级选择中文字体：

| 用途 | 优先顺序 |
|------|---------|
| 正文 | STSong → Songti SC → PingFang SC |
| 标题 | STHeiti → Heiti SC → PingFang SC |

macOS 自带 STSong 和 STHeiti，通常无需额外安装字体。

若 PDF 中文乱码，运行：
```bash
sudo tlmgr install cjk-fonts
```

---

## 典型问题排查

**pandoc: command not found**
→ 未安装 pandoc 或 PATH 未包含 /usr/local/bin
→ 解决：`brew install pandoc` 后重启终端

**xelatex: command not found**  
→ 未安装 LaTeX
→ 解决：`brew install --cask basictex`

**PDF 中出现乱码方块**
→ 中文字体包未安装
→ 解决：`sudo tlmgr install ctex xecjk cjk-fonts`

**Permission denied: python3**
→ 解决：`chmod +x skills/edupaper-exporter/scripts/export_all.py`
