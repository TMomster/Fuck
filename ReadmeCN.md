# Fuck：本地快捷启动系统

> 📌 **English speaker are recommanded to read [Readme.md](Readme.md)**

`Fuck` 是一个轻量级的命令行快捷启动工具，专为提升日常效率而设计。通过自定义 `.upath` 文件，你可以用一条简单命令快速启动程序、打开目录、访问网页或切换壁纸。

---

## 📦 功能特性

- 🔧 **快捷启动**：`fuck <名称>` 一键启动程序或文件
- 🌐 **浏览器集成**：配置默认浏览器，直接打开网页链接
- 🖼️ **壁纸管理**：支持设置壁纸、轮换壁纸、指定壁纸目录
- 📁 **智能分类**：自动将 UPATH 按类型归类（图像、URL、普通）
- 🛠 **命令管理**：支持创建、删除、更新、重命名 UPATH
- 🖱️ **打开所在目录**：使用 `-d` 参数快速访问文件所在文件夹

---

## 🚀 快速开始

### 1. 安装依赖

确保系统已安装 Python 3 并将其加入环境变量。

### 2. 初始化环境

运行提供的 `initializer.py` 脚本以生成配置文件和目录结构：

```bash
python initializer.py
```

### 3. 创建第一个 UPATH

```bash
fuck -m new notepad "C:\Windows\System32\notepad.exe"
```

### 4. 启动它！

```bash
fuck notepad
```

---

## 🛠 使用示例

| 命令                                        | 说明                     |
| ----------------------------------------- | ---------------------- |
| `fuck chrome`                             | 启动 chrome.upath 指向的浏览器 |
| `fuck -d workdoc`                         | 打开 workdoc 指向文件所在的目录   |
| `fuck -m list`                            | 列出所有 UPATH             |
| `fuck -m new blog https://myblog.com`     | 创建一个网页 UPATH           |
| `fuck -wp next`                           | 切换下一张壁纸                |
| `fuck -m browser set "C:\...\chrome.exe"` | 设置默认浏览器                |

---

## 📁 目录结构

```
/Fuck
├── fuck.exe                  # 主程序
├── root.txt                  # 指向核心 Python 脚本路径
├── initializer.py            # 初始化脚本
├── core.py                   # 核心逻辑（Python）
├── wallpaper.py              # 壁纸模块
├── memory/
│   ├── config.json           # 配置文件
│   ├── UPATH/                # 普通 UPATH 文件
│   ├── IMAGES/               # 图像类 UPATH
│   └── URL/                  # 网页类 UPATH
```

---

## ⚠ 注意事项

- `root.txt` 必须存在且包含正确的 `core.py` 路径。
- 不要将 `Fuck` 的根目录作为 UPATH 内容，防止递归风险。
- 推荐使用绝对路径创建 UPATH，避免路径解析问题。

---

## 📄 许可与示例

本项目中的示例域名使用了 [example.com](https://www.example.com)，该域名可用于文档示例，无需授权。

---

> 💡 提示：输入 `fuck -m help` 可查看交互式帮助系统。

----

TMomster, 2025.08.07
