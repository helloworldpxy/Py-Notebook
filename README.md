# Py-Notebook 📔

一个基于Python的本地笔记本应用，支持Markdown语法编辑与实时预览，提供直观的文件夹管理功能。

## 主要功能

### 文件管理
- 🗂️ 支持多级文件夹管理
- 📁 右键菜单创建/删除文件夹
- 📝 以`.txt`格式创建/删除笔记
- 🖋️ 笔记与文件夹重命名功能

### 编辑功能
- ✍️ Markdown语法实时识别
- 👀 内置Markdown预览窗口
- ⏱️ 默认以时间戳命名新笔记
- 💾 手动保存笔记内容

### 辅助功能
- ❓ 内置Markdown语法速查表
- ℹ️ 软件功能与开发者介绍
- 🖥️ 跨平台支持（Windows/macOS/Linux）

## 安装与运行

### 环境要求
- Python 3.6+
- Tkinter（通常包含在Python标准库中）

### 安装依赖
```bash
pip install markdown2
```

### 启动应用
```
git clone https://github.com/helloworldpxy/Py-notebook.git
cd Py-notebook
python Py-Notebook.py
```

## 使用指南

### 基本操作
1. **打开文件夹：** 右键点击左侧边栏空白区域 → 选择"打开文件夹"
2. **文件管理：** 右键文件夹：新建笔记/新建子文件夹/重命名/删除；右键笔记：编辑/重命名/删除
3. **编辑界面：**
       - 顶部工具栏显示当前笔记名称
       - 实时编辑自动识别Markdown语法
       - 点击💾按钮手动保存
4. **预览功能：** 点击顶部工具栏"预览"按钮打开独立预览窗口

### 快捷键
| 操作         | 快捷键       |
|--------------|-------------|
| 保存当前笔记 | Ctrl+S      |
| 新建笔记     | Ctrl+N      |
| 打开文件夹   | Ctrl+O      |

## 技术栈
- **GUI框架**: Tkinter
- **Markdown渲染**: markdown2
- **文件管理**: os/shutil模块
- **临时文件处理**: tempfile

## 贡献指南
欢迎通过Issue或Pull Request参与项目改进。

## 许可证
[MIT License](LICENSE)

---

> **提示**：首次使用建议查看"帮助"菜单中的Markdown语法参考！
