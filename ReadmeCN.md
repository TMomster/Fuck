# Fuck 程序使用指南

---

## 概述

Fuck 是一个高效的文件路径和资源管理器，通过 UPATH 文件系统快速访问常用路径、URL 和应用程序。程序提供了命令行界面，支持路径管理、浏览器集成、壁纸切换等功能。

---

## 基本用法

将 Fuck 的安装目录添加到 Path 环境变量以后，在命令行中输入 fuck，出现以下信息说明安装成功：

```
[[FUCK]] Missing Parameter...
Usage: fuck <command> [args...]
```

---

## 核心功能

### 1. UPATH 文件管理

- **创建**：`fuck -m new [名称] [内容]`
- **删除**：`fuck -m del [名称]`
- **更新**：`fuck -m update [名称] [新内容]`
- **重命名**：`fuck -m rename [旧名称] [新名称]`
- **列出**：`fuck -m list`
- **查看内容**：`fuck -m cat [名称]`
- **整理分类**：`fuck -m check`

### 2. 快速访问

- 直接启动资源：`fuck [UPATH名称]`
  - 支持文件、目录、URL 和应用程序

### 3. 浏览器管理

- **设置浏览器路径**：`fuck -m browser set [路径]`
- **查看浏览器路径**：`fuck -m browser get`

### 4. 壁纸管理

- **设置壁纸**：`fuck -wp set [图片路径/UPATH]`
- **设置壁纸文件夹**：`fuck -wp folder [UPATH名称]`
- **切换下一张壁纸**：`fuck -wp next`

---

## 文件结构

```
fuck/
├── core.py         # 核心功能模块
├── fuck.c          # C语言入口程序
├── outstream.py    # ANSI颜色输出工具
├── overload.py     # 函数重载支持
├── utils.py        # 工具函数
└── wallpaper.py    # 壁纸管理模块
memory/
├── UPATH/          # UPATH文件存储
├── IMAGES/         # 图片资源存储
├── URL/            # URL资源存储
└── config.json     # 配置文件
```

---

## 使用示例

### 创建 UPATH

```bash
fuck -m new project_dir "D:/Projects"
fuck -m new github https://github.com
```

### 访问资源

```bash
# 打开目录
fuck project_dir

# 访问网站
fuck github
```

### 壁纸管理

```bash
# 设置壁纸文件夹
fuck -wp folder wallpapers

# 切换到下一张壁纸
fuck -wp next
```

---

## 颜色标识系统

- **红色**：错误消息
- **浅绿色**：URL内容
- **浅蓝色**：标题和分隔符
- **黄色**：可执行文件
- **橙色**：有效路径

---

## 注意事项

1. UPATH 文件存储在 `memory/` 目录的三个子文件夹中：
   
   - `UPATH/`：普通路径
   - `IMAGES/`：图片路径
   - `URL/`：网址资源

2. 程序会自动检测并分类 UPATH 文件类型

3. 使用图片 URL 创建 UPATH 时会自动下载图片到本地

---

## 开发者说明

程序使用 Python 编写，通过 C 语言入口调用，支持跨平台使用（Windows/macOS/Linux）。颜色输出使用 ANSI 转义序列实现，在支持 ANSI 的终端中效果最佳。

【提示】

程序名称 "Fuck" 仅为项目代号，实际使用时可通过编译 C 文件生成自定义名称的可执行文件。

---

TMomster, 2025.05.19

TMomster, 2025.08.07
