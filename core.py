import sys
import os
import subprocess
import json
from outstream import rgb_to_ansi

RED = rgb_to_ansi(200, 50, 50)
LIGHT_GREEN = rgb_to_ansi(100, 255, 100)
LIGHT_BLUE = rgb_to_ansi(100, 100, 255)
RESET = "\033[0m"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UPATH_DIRECTORY = os.path.join(SCRIPT_DIR, "memory/UPATH")
CONFIG_FILE = os.path.join(SCRIPT_DIR, "memory/config.json")

os.makedirs(UPATH_DIRECTORY, exist_ok=True)

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"browser": ""}, f)

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

def read_upath_file(filename):
    file_path = os.path.join(UPATH_DIRECTORY, f"{filename}.upath")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    else:
        return f"{RED}err: UPATH '{filename}' not exists.{RESET}"

def launch_path_from_upath(filename):
    path_content = read_upath_file(filename)
    if path_content.startswith("err:"):
        return path_content

    path_content = path_content.strip('"')

    if is_url(path_content):
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
            return f"{RED}err: Path '{path_content}' does not exist.{RESET}"

def create_upath_file(upath_name=None, upath_content=None):
    if upath_name is None:
        upath_name = input(":: Enter the UPATH name (without suffix): ").strip()
    file_path = os.path.join(UPATH_DIRECTORY, f"{upath_name}.upath")
    if os.path.exists(file_path):
        return f"{RED}err: UPATH '{upath_name}' has exists.{RESET}"
    if upath_content is None:
        upath_content = input(":: Enter the UPATH content (path or URL): ").strip()
    else:
        if len(sys.argv) > 4:
            upath_content = ' '.join(sys.argv[4:])
    if not upath_content:
        return "Canceled."
    elif SCRIPT_DIR in upath_content:
        return f"{RED}The root directory of Fuck is not allowed to be used as an UPATH content.{RESET}"
    if not is_url(upath_content) and not (upath_content.startswith('"') and upath_content.endswith('"')):
        upath_content = f'"{upath_content}"'
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(upath_content)
    return f"UPATH '{upath_name}' created successfully."

def delete_upath_file(filename=None):
    if filename is None:
        filename = input("Enter the UPATH name (without suffix) to delete: ").strip()
    file_path = os.path.join(UPATH_DIRECTORY, f"{filename}.upath")
    if os.path.exists(file_path):
        os.remove(file_path)
        return f"UPATH '{filename}' has been deleted successfully."
    else:
        return f"{RED}err: UPATH '{filename}' not exists.{RESET}"

def update_upath_file(upath_name=None, new_upath_content=None):
    if upath_name is None:
        upath_name = input("Enter the UPATH name (without suffix) to update: ").strip()
    file_path = os.path.join(UPATH_DIRECTORY, f"{upath_name}.upath")
    if not os.path.exists(file_path):
        return f"{RED}err: UPATH '{upath_name}' not exists.{RESET}"
    if new_upath_content is None:
        new_upath_content = input("Enter the new UPATH content (path or URL): ").strip()
    if not is_url(new_upath_content) and not (new_upath_content.startswith('"') and new_upath_content.endswith('"')):
        new_upath_content = f'"{new_upath_content}"'
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(new_upath_content)
    return f"UPATH '{upath_name}' has been updated successfully."

def rename_upath_file(current_name=None, new_name=None):
    if current_name is None:
        current_name = input("Enter the current UPATH name (without suffix): ").strip()
    current_path = os.path.join(UPATH_DIRECTORY, f"{current_name}.upath")
    if not os.path.exists(current_path):
        return f"{RED}err: UPATH '{current_name}' not exists.{RESET}"
    if new_name is None:
        new_name = input("Enter the new UPATH name (without suffix): ").strip()
    new_path = os.path.join(UPATH_DIRECTORY, f"{new_name}.upath")
    if os.path.exists(new_path):
        return f"{RED}err: UPATH '{new_name}' already exists.{RESET}"
    os.rename(current_path, new_path)
    return f"UPATH '{current_name}' has been renamed to '{new_name}' successfully."

def list_upath_files():
    upath_directory = UPATH_DIRECTORY
    if not os.path.exists(upath_directory):
        print(f"{RED}Directory '{upath_directory}' does not exist.{RESET}")
        return
    files = os.listdir(upath_directory)
    upath_files = [os.path.splitext(file)[0] for file in files if file.endswith(".upath")]
    if not upath_files:
        print(f"{RED}No UPATH files found.{RESET}")
        return

    max_name_length = max(len(name) for name in upath_files)

    print(f"{LIGHT_BLUE}Existing UPATH files and their contents:{RESET}")
    for file in upath_files:
        file_path = os.path.join(upath_directory, f"{file}.upath")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip().strip('"')
        if is_url(content):
            print(f"{file:<{max_name_length}}  {LIGHT_GREEN}{content}{RESET}")
        else:
            print(f"{file:<{max_name_length}}  {content}")

def cat_upath_file(filename=None):
    if filename is None:
        filename = input("Enter the UPATH name (without suffix) to display: ").strip()
    file_path = os.path.join(UPATH_DIRECTORY, f"{filename}.upath")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        print(f"Content of '{filename}.upath':{RESET}")
        print(f"{LIGHT_GREEN}{content}{RESET}")
    else:
        print(f"{RED}err: UPATH '{filename}' not exists.{RESET}")

def main():
    print(f"{LIGHT_BLUE}---------->>>")
    try:
        if len(sys.argv) < 2:
            print(f"{RED}Usage: core.py <filename> or core.py -m <command> [args]{RESET}")
            return

        if sys.argv[1] != "-m":
            filename = sys.argv[1]
            path_content = read_upath_file(filename)
            if path_content.startswith("err:"):
                print(path_content)
            else:
                print(launch_path_from_upath(filename))
            return

        if len(sys.argv) < 3:
            print(f"{RED}Usage: core.py -m <command> [args]{RESET}")
            print(f"{RED}Available commands: new, del, update, rename, list, cat, browser{RESET}")
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

        else:
            print(f"{RED}Unknown command: {command}{RESET}")
            print(f"{RED}Available commands: new, del, update, rename, list, cat, browser{RESET}")

    finally:
        print(f"{LIGHT_BLUE}---------->>>{RESET}")


if __name__ == '__main__':
    main()