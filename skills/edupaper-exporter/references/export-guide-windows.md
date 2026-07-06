# EduPaper 导出指引 — Windows

## 快速开始

在项目根目录打开 **PowerShell** 或 **命令提示符**，运行：

```powershell
python skills\edupaper-exporter\scripts\export_all.py `
  .edupaper\drafts\A\final.md `
  --formats docx,html `
  --output-dir .edupaper\exports\
```

> 提示：Windows 上用 `\` 作路径分隔符，或在引号内使用 `/`

---

## 工具安装

### 1. Python 3（必须）

官网下载：https://www.python.org/downloads/

**安装时勾选 "Add Python to PATH"**（非常重要）

验证：
```powershell
python --version
```

### 2. pandoc（推荐，用于 DOCX 和 HTML）

**方法一：winget（Windows 10/11 内置包管理）**
```powershell
winget install JohnMacFarlane.Pandoc
```

**方法二：官网下载安装包**
https://pandoc.org/installing.html
→ 下载 pandoc-x.x.x-windows-x86_64.msi，双击安装

安装后**重启 PowerShell**，验证：
```powershell
pandoc --version
```

### 3. MiKTeX（可选，用于 PDF，含中文支持）

官网下载：https://miktex.org/download

选择 **Complete MiKTeX**（包含中文支持）。

首次编译 PDF 时，MiKTeX 会自动安装缺失的 LaTeX 包（需联网），
稍等几分钟即可。

### 4. python-docx（备用方案，无需 pandoc）

```powershell
pip install python-docx
```

---

## 中文字体说明

Windows 上 EduPaper 按以下优先级选择中文字体：

| 用途 | 优先顺序 |
|------|---------|
| 正文 | 宋体（SimSun）→ 仿宋 → Times New Roman |
| 标题 | 黑体（SimHei）→ 微软雅黑 → Arial |

Windows 自带宋体和黑体，通常无需额外安装字体。

---

## 导出命令示例

**仅导出 DOCX（最常用）：**
```powershell
python skills\edupaper-exporter\scripts\export_all.py .edupaper\drafts\A\final.md --formats docx
```

**导出 DOCX + PDF：**
```powershell
python skills\edupaper-exporter\scripts\export_all.py .edupaper\drafts\A\final.md --formats docx,pdf
```

**指定输出目录：**
```powershell
python skills\edupaper-exporter\scripts\export_all.py .edupaper\drafts\A\final.md --formats docx,html --output-dir C:\Users\用户名\Desktop\论文输出
```

---

## 典型问题排查

**'python' 不是内部或外部命令**
→ Python 未加入 PATH
→ 解决：重新安装 Python，勾选 "Add Python to PATH"；或使用 `py` 代替 `python`

**'pandoc' 不是内部或外部命令**
→ pandoc 未安装或 PATH 未更新
→ 解决：安装后重启 PowerShell

**PDF 编译卡住不动**
→ MiKTeX 正在下载缺失的 LaTeX 包（首次运行需联网等待）
→ 解决：耐心等待 3-5 分钟，或提前运行 MiKTeX Console 更新所有包

**PDF 中文显示为方框（乱码）**
→ 缺少中文字体包
→ 解决：打开 MiKTeX Console → Packages → 搜索 "ctex" → 安装

**脚本报 UnicodeDecodeError**
→ 文件编码问题
→ 解决：确保 final.md 保存为 UTF-8（在文本编辑器中另存为 UTF-8）
