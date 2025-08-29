import sys
import os
import subprocess
import json
import requests
import shutil
from time import time
from threading import Timer
from outstream import rgb_to_ansi
from utils import read_config, write_config, read_upath_file

RED = rgb_to_ansi(200, 50, 50)
LIGHT_GREEN = rgb_to_ansi(100, 255, 100)
LIGHT_BLUE = rgb_to_ansi(100, 100, 255)
YELLOW = rgb_to_ansi(255, 255, 100)
ORANGE = rgb_to_ansi(255, 165, 0)
CYAN = rgb_to_ansi(100, 200, 200)
PURPLE = rgb_to_ansi(200, 100, 200)
RESET = "\033[0m"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UPATH_DIRECTORY = os.path.join(SCRIPT_DIR, "memory/UPATH")
IMAGES_DIRECTORY = os.path.join(SCRIPT_DIR, "memory/IMAGES")
URL_DIRECTORY = os.path.join(SCRIPT_DIR, "memory/URL")
CONFIG_FILE = os.path.join(SCRIPT_DIR, "memory/config.json")

os.makedirs(UPATH_DIRECTORY, exist_ok=True)
os.makedirs(IMAGES_DIRECTORY, exist_ok=True)
os.makedirs(URL_DIRECTORY, exist_ok=True)

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"browser": "", "wallpaper_folder": "", "current_wallpaper": ""}, f)

def read_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def write_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f)

def set_browser_path(browser_path):
    config = read_config()
    config["browser"] = browser_path
    write_config(config)
    return f"Browser path set to: {browser_path}"

def get_browser_path():
    config = read_config()
    return config.get("browser", "")

def is_url(path):
    return path.startswith(("http://", "https://", "www."))

def is_image_path(path):
    return any(path.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif'])

def is_web_or_ip(path):
    return is_url(path) or (path.count('.') == 3 and all(part.isdigit() for part in path.split('.')))

def create_upath_file(upath_name=None, upath_content=None):
    if upath_name is None:
        upath_name = input(":: Enter the UPATH name (without suffix): ").strip()
    file_path = os.path.join(UPATH_DIRECTORY, f"{upath_name}.upath")
    if os.path.exists(file_path):
        return f"{RED}err: UPATH '{upath_name}' has exists.{RESET}"
    if upath_content is None:
        upath_content = input(":: Enter the UPATH content (path/URL/directory): ").strip()
    else:
        if len(sys.argv) > 4:
            upath_content = ' '.join(sys.argv[4:])
    if not upath_content:
        return "Canceled."
    elif SCRIPT_DIR in upath_content:
        return f"{RED}The root directory of Fuck is not allowed to be used as an UPATH content.{RESET}"
    
    # 处理图片URL
    if is_url(upath_content) and is_image_path(upath_content):
        local_path = download_image(upath_content)
        if local_path:
            upath_content = f'"{local_path}"'
        else:
            return f"{RED}Failed to download image{RESET}"
    
    if not is_url(upath_content) and not (upath_content.startswith('"') and upath_content.endswith('"')):
        upath_content = f'"{upath_content}"'
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(upath_content)
    return f"UPATH '{upath_name}' created successfully."

def launch_path_from_upath(filename):
    for directory in [UPATH_DIRECTORY, IMAGES_DIRECTORY, URL_DIRECTORY]:
        file_path = os.path.join(directory, f"{filename}.upath")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read().strip().strip('"')
            return content
    return f"{RED}err: UPATH '{filename}' not exists.{RESET}"

def delete_upath_file(filename=None):
    if filename is None:
        filename = input("Enter the UPATH name (without suffix) to delete: ").strip()
    for directory in [UPATH_DIRECTORY, IMAGES_DIRECTORY, URL_DIRECTORY]:
        file_path = os.path.join(directory, f"{filename}.upath")
        if os.path.exists(file_path):
            os.remove(file_path)
            return f"UPATH '{filename}' has been deleted successfully."
    return f"{RED}err: UPATH '{filename}' not exists.{RESET}"

def update_upath_file(upath_name=None, new_upath_content=None):
    if upath_name is None:
        upath_name = input("Enter the UPATH name (without suffix) to update: ").strip()
    for directory in [UPATH_DIRECTORY, IMAGES_DIRECTORY, URL_DIRECTORY]:
        file_path = os.path.join(directory, f"{upath_name}.upath")
        if os.path.exists(file_path):
            if new_upath_content is None:
                new_upath_content = input("Enter the new UPATH content (path or URL): ").strip()
            if not is_url(new_upath_content) and not (new_upath_content.startswith('"') and new_upath_content.endswith('"')):
                new_upath_content = f'"{new_upath_content}"'
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(new_upath_content)
            return f"UPATH '{upath_name}' has been updated successfully."
    return f"{RED}err: UPATH '{upath_name}' not exists.{RESET}"

def rename_upath_file(current_name=None, new_name=None):
    if current_name is None:
        current_name = input("Enter the current UPATH name (without suffix): ").strip()
    for directory in [UPATH_DIRECTORY, IMAGES_DIRECTORY, URL_DIRECTORY]:
        current_path = os.path.join(directory, f"{current_name}.upath")
        if os.path.exists(current_path):
            if new_name is None:
                new_name = input("Enter the new UPATH name (without suffix): ").strip()
            new_path = os.path.join(directory, f"{new_name}.upath")
            if os.path.exists(new_path):
                return f"{RED}err: UPATH '{new_name}' already exists.{RESET}"
            os.rename(current_path, new_path)
            return f"UPATH '{current_name}' has been renamed to '{new_name}' successfully."
    return f"{RED}err: UPATH '{current_name}' not exists.{RESET}"

def list_upath_files():
    upath_directory = UPATH_DIRECTORY
    images_directory = IMAGES_DIRECTORY
    url_directory = URL_DIRECTORY

    if not os.path.exists(upath_directory):
        print(f"{RED}Directory '{upath_directory}' does not exist.{RESET}")
        return

    if not os.path.exists(images_directory):
        print(f"{RED}Directory '{images_directory}' does not exist.{RESET}")
        return

    if not os.path.exists(url_directory):
        print(f"{RED}Directory '{url_directory}' does not exist.{RESET}")
        return

    upath_files = []
    for root, dirs, files in os.walk(upath_directory):
        for file in files:
            if file.endswith(".upath"):
                upath_files.append((os.path.join(root, file), "default"))

    images_files = []
    for root, dirs, files in os.walk(images_directory):
        for file in files:
            if file.endswith(".upath"):
                images_files.append((os.path.join(root, file), "image"))

    url_files = []
    for root, dirs, files in os.walk(url_directory):
        for file in files:
            if file.endswith(".upath"):
                url_files.append((os.path.join(root, file), "url"))

    all_files = upath_files + images_files + url_files

    if not all_files:
        print(f"{RED}No UPATH files found.{RESET}")
        return

    max_name_length = max(len(os.path.splitext(os.path.basename(file[0]))[0]) for file in all_files)

    print(f"{LIGHT_BLUE}Existing UPATH files and their contents:{RESET}")
    for file, file_type in all_files:
        file_name = os.path.splitext(os.path.basename(file))[0]
        with open(file, "r", encoding="utf-8") as f:
            content = f.read().strip().strip('"')
        if file_type == "image":
            print(f"{file_name:<{max_name_length}}  {content}")
        elif file_type == "url":
            print(f"{file_name:<{max_name_length}}  {LIGHT_GREEN}{content}{RESET}")
        else:
            if content.lower().endswith('.exe'):
                print(f"{file_name:<{max_name_length}}  {content}")
            else:
                if os.path.exists(content):
                    print(f"{file_name:<{max_name_length}}  {ORANGE}{content}{RESET}")
                else:
                    print(f"{file_name:<{max_name_length}}  {content}")

def cat_upath_file(filename=None):
    if filename is None:
        filename = input("Enter the UPATH name (without suffix) to display: ").strip()
    for directory in [UPATH_DIRECTORY, IMAGES_DIRECTORY, URL_DIRECTORY]:
        file_path = os.path.join(directory, f"{filename}.upath")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            print(f"Content of '{filename}.upath':{RESET}")
            print(f"{LIGHT_GREEN}{content}{RESET}")
            return
    print(f"{RED}err: UPATH '{filename}' not exists.{RESET}")

def set_privacy_mode(enabled):
    config = read_config()
    config["privacy_mode"] = enabled
    write_config(config)
    return f"Privacy mode {'enabled' if enabled else 'disabled'}"

def get_privacy_mode():
    config = read_config()
    return config.get("privacy_mode", True)

def execute_wallpaper_module(args):
    wallpaper_script = os.path.join(os.path.dirname(__file__), "wallpaper.py")
    cmd = [sys.executable, wallpaper_script] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stderr)

def organize_upaths():
    upath_directory = UPATH_DIRECTORY
    images_directory = IMAGES_DIRECTORY
    url_directory = URL_DIRECTORY

    if not os.path.exists(upath_directory):
        print(f"{RED}Directory '{upath_directory}' does not exist.{RESET}")
        return

    for root, dirs, files in os.walk(upath_directory):
        for file in files:
            if file.endswith(".upath"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip().strip('"')
                
                if is_image_path(content):
                    new_path = os.path.join(images_directory, file)
                    shutil.move(file_path, new_path)
                    print(f"Moved '{file}' to IMAGES directory.")
                elif is_web_or_ip(content):
                    new_path = os.path.join(url_directory, file)
                    shutil.move(file_path, new_path)
                    print(f"Moved '{file}' to URL directory.")
                else:
                    print(f"'{file}' remains in UPATH directory.")

def launch_path_from_upath_with_browser(filename, open_directory=False):
    path_content = launch_path_from_upath(filename)
    if isinstance(path_content, str) and path_content.startswith("err:"):
        return path_content

    path_content = path_content.strip('"')
    
    # 处理打开目录的情况
    if open_directory:
        if is_url(path_content) or is_web_or_ip(path_content):
            # 如果是URL，正常打开
            browser_path = get_browser_path()
            if not browser_path:
                return f"{RED}err: No browser configured. Use '-m browser set <path>' to set browser path.{RESET}"
            try:
                extra_args = sys.argv[3:] if len(sys.argv) > 3 else []
                subprocess.Popen([browser_path] + extra_args + [path_content])
                return f"Launched URL in browser: {path_content}"
            except Exception as e:
                return f"{RED}err: Failed to launch URL {path_content}. Error: {str(e)}{RESET}"
        elif os.path.isdir(path_content):
            # 如果是目录，直接打开
            try:
                if sys.platform == "win32":
                    os.startfile(path_content)
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", path_content])
                else:
                    subprocess.Popen(["xdg-open", path_content])
                return f"Opened directory: {path_content}"
            except Exception as e:
                return f"{RED}err: Failed to open directory {path_content}. Error: {str(e)}{RESET}"
        else:
            # 如果是文件，打开其所在目录
            directory = os.path.dirname(path_content)
            if os.path.exists(directory):
                try:
                    if sys.platform == "win32":
                        os.startfile(directory)
                    elif sys.platform == "darwin":
                        subprocess.Popen(["open", directory])
                    else:
                        subprocess.Popen(["xdg-open", directory])
                    return f"Opened directory containing: {path_content}"
                except Exception as e:
                    return f"{RED}err: Failed to open directory {directory}. Error: {str(e)}{RESET}"
            else:
                return f"{RED}err: Directory '{directory}' not found.{RESET}"
    
    # 正常启动逻辑
    if os.path.isdir(path_content):
        try:
            if sys.platform == "win32":
                os.startfile(path_content)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path_content])
            else:
                subprocess.Popen(["xdg-open", path_content])
            return f"Opened directory: {path_content}"
        except Exception as e:
            return f"{RED}err: Failed to open directory {path_content}. Error: {str(e)}{RESET}"
    
    # 处理.lnk快捷方式
    if path_content.lower().endswith('.lnk'):
        try:
            if sys.platform == "win32":
                # 在Windows上使用start命令打开.lnk文件
                subprocess.Popen(f'start "" "{path_content}"', shell=True)
                return f"Opened shortcut: {path_content}"
            else:
                # 在非Windows系统上，尝试使用默认程序打开
                subprocess.Popen(["xdg-open", path_content])
                return f"Opened shortcut: {path_content}"
        except Exception as e:
            return f"{RED}err: Failed to open shortcut {path_content}. Error: {str(e)}{RESET}"
    
    if is_url(path_content) or is_web_or_ip(path_content):
        browser_path = get_browser_path()
        if not browser_path:
            return f"{RED}err: No browser configured. Use '-m browser set <path>' to set browser path.{RESET}"
        try:
            extra_args = sys.argv[2:] if len(sys.argv) > 2 else []
            subprocess.Popen([browser_path] + extra_args + [path_content])
            return f"Launched URL in browser: {path_content}"
        except Exception as e:
            return f"{RED}err: Failed to launch URL {path_content}. Error: {str(e)}{RESET}"
    else:
        if os.path.exists(path_content):
            try:
                extra_args = sys.argv[2:] if len(sys.argv) > 2 else []
                subprocess.Popen([path_content] + extra_args)
                return f"Launched: {path_content}"
            except Exception as e:
                return f"{RED}err: Failed to launch {path_content}. Error: {str(e)}{RESET}"
        else:
            return f"{RED}err: Path '{path_content}' not found.{RESET}"

def show_help():
    """显示交互式帮助系统"""
    help_topics = {
        "1": {
            "title": "UPATH文件定义",
            "content": f"""
{ORANGE}UPATH文件定义:{RESET}
UPATH是Fuck系统的核心概念，它是一个包含路径、URL或目录引用的文本文件。

{ORANGE}UPATH类型:{RESET}
1. {LIGHT_GREEN}普通UPATH{RESET}: 存储文件路径、目录路径或程序路径
2. {LIGHT_GREEN}图像UPATH{RESET}: 存储图像文件路径，会自动归类到IMAGES目录
3. {LIGHT_GREEN}URL UPATH{RESET}: 存储网页链接，会自动归类到URL目录

{ORANGE}UPATH文件格式:{RESET}
- 普通UPATH: 直接包含路径，如 "C:\\Program Files\\App\\app.exe"
- 图像UPATH: 包含图像文件路径，如 "C:\\Wallpapers\\image.jpg"
- URL UPATH: 包含网页链接，如 "https://www.example.com"

{ORANGE}创建UPATH:{RESET}
使用命令: {CYAN}fuck -m new <upath名称> <路径/URL>{RESET}
"""
        },
        "2": {
            "title": "基本用法",
            "content": f"""
{ORANGE}基本用法:{RESET}

1. {LIGHT_GREEN}启动UPATH:{RESET}
   {CYAN}fuck <upath名称>{RESET} - 启动指定的UPATH

2. {LIGHT_GREEN}创建UPATH:{RESET}
   {CYAN}fuck -m new <名称> <路径/URL>{RESET} - 创建新的UPATH

3. {LIGHT_GREEN}删除UPATH:{RESET}
   {CYAN}fuck -m del <名称>{RESET} - 删除指定的UPATH

4. {LIGHT_GREEN}更新UPATH:{RESET}
   {CYAN}fuck -m update <名称> <新路径/URL>{RESET} - 更新UPATH内容

5. {LIGHT_GREEN}重命名UPATH:{RESET}
   {CYAN}fuck -m rename <旧名称> <新名称>{RESET} - 重命名UPATH

6. {LIGHT_GREEN}列出所有UPATH:{RESET}
   {CYAN}fuck -m list{RESET} - 显示所有UPATH及其内容

7. {LIGHT_GREEN}查看UPATH内容:{RESET}
   {CYAN}fuck -m cat <名称>{RESET} - 显示指定UPATH的内容
"""
        },
        "3": {
            "title": "快捷键参数",
            "content": f"""
{ORANGE}快捷键参数:{RESET}

1. {LIGHT_GREEN}-d 参数:{RESET}
   {CYAN}fuck -d <upath名称>{RESET} - 打开UPATH指向文件所在的目录
   例如: {CYAN}fuck -d myapp{RESET} 会打开myapp UPATH指向的文件所在目录

2. {LIGHT_GREEN}-wp 参数:{RESET}
   {CYAN}fuck -wp <command>{RESET} - 壁纸相关功能
   子命令:
     - {CYAN}set <图像UPATH>{RESET}: 设置壁纸
     - {CYAN}folder <目录UPATH>{RESET}: 设置壁纸目录
     - {CYAN}next{RESET}: 切换到下一张壁纸

3. {LIGHT_GREEN}-m 参数:{RESET}
   {CYAN}fuck -m <command>{RESET} - 管理UPATH文件
   子命令: new, del, update, rename, list, cat, browser, check
"""
        },
        "4": {
            "title": "使用技巧",
            "content": f"""
{ORANGE}使用技巧:{RESET}

1. {LIGHT_GREEN}快速启动:{RESET}
   为常用程序创建UPATH，然后只需输入 {CYAN}fuck <名称>{RESET} 即可快速启动

2. {LIGHT_GREEN}组织UPATH:{RESET}
   使用 {CYAN}fuck -m check{RESET} 自动将UPATH文件分类到正确的目录

3. {LIGHT_GREEN}浏览器集成:{RESET}
   使用 {CYAN}fuck -m browser set <浏览器路径>{RESET} 设置默认浏览器
   然后可以使用UPATH直接打开网页链接

4. {LIGHT_GREEN}壁纸循环:{RESET}
   设置壁纸目录后，使用 {CYAN}fuck -wp next{RESET} 可以循环切换壁纸

5. {LIGHT_GREEN}目录快捷方式:{RESET}
   为常用目录创建UPATH，然后使用 {CYAN}fuck <名称>{RESET} 快速打开目录
   或使用 {CYAN}fuck -d <名称>{RESET} 打开该目录

6. {LIGHT_GREEN}.lnk文件支持:{RESET}
   Fuck支持直接使用Windows快捷方式(.lnk文件)作为UPATH内容
"""
        }
    }
    
    print(f"{LIGHT_BLUE}---------- Fuck帮助系统 ----------{RESET}")
    print("输入序号选择帮助主题，输入'q'退出帮助")
    print()
    
    for key, topic in help_topics.items():
        print(f"{ORANGE}[{key}]{RESET} {topic['title']}")
    
    print()
    
    while True:
        choice = input(f"{LIGHT_GREEN}请输入选项 (1-4) 或 'q' 退出: {RESET}").strip().lower()
        
        if choice == 'q':
            print(f"{LIGHT_BLUE}退出帮助系统{RESET}")
            break
        
        if choice in help_topics:
            print(f"\n{ORANGE}=== {help_topics[choice]['title']} ==={RESET}")
            print(help_topics[choice]['content'])
            print(f"{LIGHT_BLUE}--------------------------------{RESET}")
        else:
            print(f"{RED}无效选项，请重新选择{RESET}")

def main():
    print(f"{LIGHT_BLUE}---------->>>")
    try:
        if len(sys.argv) < 2:
            print(f"{RED}Usage: core.py <filename> or core.py -m <command> [args]{RESET}")
            print(f"{RED}       core.py -d <filename> (open directory containing the file){RESET}")
            return

        # 处理 -d 参数
        if sys.argv[1] == "-d":
            if len(sys.argv) < 3:
                print(f"{RED}Usage: core.py -d <filename>{RESET}")
                return
            filename = sys.argv[2]
            path_content = launch_path_from_upath_with_browser(filename, open_directory=True)
            if isinstance(path_content, str) and path_content.startswith("err:"):
                print(path_content)
            else:
                print(path_content)
            return

        if sys.argv[1] == "-wp":
            execute_wallpaper_module(sys.argv[2:])
            return

        if sys.argv[1] != "-m":
            filename = sys.argv[1]
            path_content = launch_path_from_upath_with_browser(filename)
            if isinstance(path_content, str) and path_content.startswith("err:"):
                print(path_content)
            else:
                print(path_content)
            return

        if len(sys.argv) < 3:
            print(f"{RED}Usage: core.py -m <command> [args]{RESET}")
            print(f"{RED}Available commands: new, del, update, rename, list, cat, browser, wallpaper, check, help{RESET}")
            return

        command = sys.argv[2]

        if command == "new":
            upath_name = sys.argv[3] if len(sys.argv) > 3 else None
            upath_content = ' '.join(sys.argv[4:]) if len(sys.argv) > 4 else None
            result = create_upath_file(upath_name, upath_content)
            print(result)

        elif command == "del":
            upath_name = sys.argv[3] if len(sys.argv) > 3 else None
            result = delete_upath_file(upath_name)
            print(result)

        elif command == "update":
            upath_name = sys.argv[3] if len(sys.argv) > 3 else None
            new_upath_content = sys.argv[4] if len(sys.argv) > 4 else None
            result = update_upath_file(upath_name, new_upath_content)
            print(result)

        elif command == "rename":
            current_name = sys.argv[3] if len(sys.argv) > 3 else None
            new_name = sys.argv[4] if len(sys.argv) > 4 else None
            result = rename_upath_file(current_name, new_name)
            print(result)

        elif command == "list":
            list_upath_files()

        elif command == "cat":
            filename = sys.argv[3] if len(sys.argv) > 3 else None
            cat_upath_file(filename)

        elif command == "browser":
            if len(sys.argv) < 4:
                print(f"{RED}Usage: core.py -m browser <set|get> [path]{RESET}")
                return
            subcmd = sys.argv[3]
            if subcmd == "set":
                if len(sys.argv) < 5:
                    print(f"{RED}Please specify browser path{RESET}")
                    return
                browser_path = ' '.join(sys.argv[4:])
                print(set_browser_path(browser_path))
            elif subcmd == "get":
                print(f"Current browser path: {get_browser_path()}")
            else:
                print(f"{RED}Unknown browser command: {subcmd}{RESET}")

        elif command == "check":
            organize_upaths()
            print("UPATH files have been organized.")
            
        elif command == "help":
            show_help()

        else:
            print(f"{RED}Unknown command: {command}{RESET}")
            print(f"{RED}Available commands: new, del, update, rename, list, cat, browser, wallpaper, check, help{RESET}")

    except Exception as e:
        print(f"{RED}Error: {str(e)}{RESET}")

    finally:
        print(f"{LIGHT_BLUE}---------->>>{RESET}")


if __name__ == '__main__':
    main()