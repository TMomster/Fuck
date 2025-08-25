# Fuck Program User Guide

如果您是中文使用者，请参阅[ReadmeCN](./ReadmeCN.md)。

## Overview

Fuck is a highly efficient file path and resource manager that leverages the UPATH file system to facilitate rapid access to frequently used paths, URLs, and applications. The program offers a robust command-line interface, supporting path management, browser integration, wallpaper switching, and more.

## Core Features

### 1. UPATH File Management

- **Create**: `fuck -m new [name] [content]`
- **Delete**: `fuck -m del [name]`
- **Update**: `fuck -m update [name] [new content]`
- **Rename**: `fuck -m rename [old name] [new name]`
- **List**: `fuck -m list`
- **View Content**: `fuck -m cat [name]`
- **Organize**: `fuck -m check`

### 2. Quick Access

- Launch resources directly: `fuck [UPATH name]`
  - Supports files, directories, URLs, and applications

### 3. Browser Management

- **Set browser path**: `fuck -m browser set [path]`
- **View browser path**: `fuck -m browser get`

### 4. Wallpaper Management

- **Set wallpaper**: `fuck -wp set [image path/UPATH]`
- **Set wallpaper folder**: `fuck -wp folder [UPATH name]`
- **Switch to next wallpaper**: `fuck -wp next`

## File Structure

```
fuck/
├── core.py         # Core functionality module
├── fuck.c          # C language entry program
├── outstream.py    # ANSI color output tool
├── overload.py     # Function overloading support
├── utils.py        # Utility functions
└── wallpaper.py    # Wallpaper management module
memory/
├── UPATH/          # UPATH file storage
├── IMAGES/         # Image resource storage
├── URL/            # URL resource storage
└── config.json     # Configuration file
```

## Usage Examples

### Creating a UPATH

```bash
fuck -m new project_dir "D:/Projects"
fuck -m new github https://github.com
```

### Accessing Resources

```bash
# Open directory
fuck project_dir

# Visit website
fuck github
```

### Wallpaper Management

```bash
# Set wallpaper folder
fuck -wp folder wallpapers

# Switch to next wallpaper
fuck -wp next
```

## Color Coding System

- **Red**: Error messages
- **Light Green**: URL content
- **Light Blue**: Titles and separators
- **Yellow**: Executable files
- **Orange**: Valid paths

## Notes

1. UPATH files are stored in three subdirectories within the `memory/` directory:
   
   - `UPATH/`: Regular paths
   - `IMAGES/`: Image paths
   - `URL/`: Website resources

2. The program automatically detects and classifies UPATH file types.

3. When creating a UPATH with an image URL, the image is automatically downloaded to the local storage.

## Developer Notes

The program is written in Python and invoked via a C language entry point, supporting cross-platform use (Windows/macOS/Linux). Color output is achieved using ANSI escape sequences, which work best in ANSI-compatible terminals.

---

**Note**

The program name "Fuck" is merely a project codename. In actual use, you can generate a custom-named executable file by compiling the C file.

---

TMomster, 2025.05.19

TMomster, 2025.08.07
