# Fuck: Local Shortcut Launcher System

> 📌 **中文使用者请参阅 [ReadmeCN.md](ReadmeCN.md)**

`Fuck` is a lightweight command-line shortcut launcher designed to boost productivity. By defining `.upath` files, you can quickly launch applications, open directories, browse URLs, or manage wallpapers with simple commands.

---

## 📦 Features

- 🔧 **Quick Launch**: Use `fuck <name>` to launch programs or files instantly
- 🌐 **Browser Integration**: Set a default browser and open web links directly
- 🖼️ **Wallpaper Management**: Set, switch, and manage wallpaper folders
- 📁 **Smart Categorization**: Automatically organizes UPATH files into IMAGES, URL, and UPATH directories
- 🛠 **Command Management**: Create, delete, update, and rename UPATH entries
- 🖱️ **Open Containing Folder**: Use `-d` to open the directory of a target file

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure Python 3 is installed and added to your system PATH.

### 2. Initialize the Environment

Run the initializer script to set up the directory structure and config:

```bash
python initializer.py
```

### 3. Create Your First UPATH

```bash
fuck -m new notepad "C:\Windows\System32\notepad.exe"
```

### 4. Launch It!

```bash
fuck notepad
```

---

## 🛠 Usage Examples

| Command                                   | Description                                      |
| ----------------------------------------- | ------------------------------------------------ |
| `fuck chrome`                             | Launch the program defined in chrome.upath       |
| `fuck -d workdoc`                         | Open the directory containing the workdoc target |
| `fuck -m list`                            | List all UPATH entries                           |
| `fuck -m new blog https://myblog.com`     | Create a URL shortcut                            |
| `fuck -wp next`                           | Switch to the next wallpaper                     |
| `fuck -m browser set "C:\...\chrome.exe"` | Set default browser path                         |

---

## 📁 Project Structure

```
/Fuck
├── fuck.exe                  # Main executable
├── root.txt                  # Points to the core Python script
├── initializer.py            # Setup script
├── core.py                   # Core logic (Python)
├── wallpaper.py              # Wallpaper module
├── memory/
│   ├── config.json           # Configuration file
│   ├── UPATH/                # General UPATH files
│   ├── IMAGES/               # Image-type UPATHs
│   └── URL/                  # URL-type UPATHs
```

---

## ⚠ Notes

- The `root.txt` file must exist and contain the correct path to `core.py`.
- Avoid using the root directory of `Fuck` as a UPATH content to prevent recursion.
- Absolute paths are recommended when creating UPATH entries.

---

## 📄 License & Example Usage

The example domain [example.com](https://www.example.com) is used in documentation. This domain is reserved for illustrative examples and may be used freely without permission.

---

> 💡 Tip: Run `fuck -m help` for an interactive help system.

---

TMomster, 2025.08.07
