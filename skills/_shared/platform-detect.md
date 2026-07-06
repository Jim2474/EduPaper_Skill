# 跨平台检测指导

EduPaper pipeline 的所有外部工具调用（导出、脚本执行等）必须先执行本文件
中的检测流程，确保在 macOS、Windows、Linux 上均可正常工作。

## 操作系统检测

使用 Python 检测（Python 3.6+ 在三个平台均可用）：

```python
import sys, os

def detect_platform():
    if sys.platform == 'darwin':
        return 'mac'
    elif sys.platform.startswith('win'):
        return 'windows'
    elif sys.platform.startswith('linux'):
        return 'linux'
    else:
        return 'unknown'
```

## 工具可用性检测

```python
import shutil, subprocess

def check_tool(name):
    """返回工具路径，不可用则返回 None"""
    return shutil.which(name)

def check_pandoc():
    return check_tool('pandoc')

def check_xelatex():
    return check_tool('xelatex') or check_tool('xetex')

def check_python_docx():
    try:
        import docx
        return True
    except ImportError:
        return False
```

## 中文字体优先级

不同平台的中文字体可用性不同，按以下顺序选择：

| 平台 | 正文字体（首选→备用） | 标题字体（首选→备用） |
|------|----------------------|----------------------|
| Windows | 宋体 → SimSun → 仿宋 | 黑体 → SimHei → 微软雅黑 |
| macOS | STSong → 华文宋体 → PingFang SC | STHeiti → 华文黑体 → PingFang SC |
| Linux | Noto Serif CJK SC → WenQuanYi Bitmap Song | Noto Sans CJK SC → WenQuanYi Zen Hei |

## 导出路径决策树

```
pandoc 可用?
├── YES → xelatex 可用?
│   ├── YES → 全功能：DOCX + PDF + HTML（中文字体完整支持）
│   └── NO  → DOCX + HTML（PDF 提示安装 LaTeX）
└── NO  → python-docx 可用?
    ├── YES → DOCX + HTML（python-docx 生成，无 PDF）
    └── NO  → 纯 Markdown 输出 + 显示安装指引
```

## 安装指引（运行时按需展示）

### 安装 pandoc

**macOS（推荐 Homebrew）：**
```bash
brew install pandoc
```

**Windows（推荐 winget 或直接下载）：**
```powershell
winget install JohnMacFarlane.Pandoc
# 或访问 https://pandoc.org/installing.html 下载安装包
```

**Linux：**
```bash
sudo apt install pandoc        # Debian/Ubuntu
sudo dnf install pandoc        # Fedora/RHEL
```

### 安装中文 PDF 支持（XeLaTeX）

**macOS：**
```bash
brew install --cask mactex     # 完整版（约4GB）
# 或
brew install --cask basictex   # 精简版（约90MB），再安装中文支持：
sudo tlmgr install ctex
```

**Windows：**
```
下载 MiKTeX：https://miktex.org/download
安装后首次运行会自动安装缺失包（含中文支持）
```

**Linux：**
```bash
sudo apt install texlive-xetex texlive-lang-chinese  # Debian/Ubuntu
```

### 安装 python-docx（最轻量备用）

**所有平台（需 Python 3）：**
```bash
pip install python-docx
```

## 路径规范（跨平台）

- 所有 skill 中的文件路径使用**正斜杠** `/`，Python 的 `pathlib.Path` 会自动处理平台差异
- 不要在 skill 指令中硬编码 `\` 分隔符
- `.edupaper/` 目录始终相对于项目根目录，不使用绝对路径
