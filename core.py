import sys
import os
import subprocess
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UPATH_DIRECTORY = os.path.join(SCRIPT_DIR, "memory/UPATH")
CONFIG_FILE = os.path.join(SCRIPT_DIR, "memory/config.json")

os.makedirs(UPATH_DIRECTORY, exist_ok=True)

# 初始化配置文件
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
        return f"err: UPATH '{filename}' not exists."

def launch_path_from_upath(filename):
    path_content = read_upath_file(filename)
    if path_content.startswith("err:"):
        return path_content
    
    path_content = path_content.strip('"')
    
    if is_url(path_content):
        browser_path = get_browser_path()
        if not browser_path:
            return "err: No browser configured. Use '-m browser set <path>' to set browser path."
        try:
            subprocess.Popen([browser_path, path_content])
            return f"Launched URL in browser: {path_content}"
        except Exception as e:
            return f"err: Failed to launch URL {path_content}. Error: {str(e)}"
    else:
        if os.path.exists(path_content):
            try:
                subprocess.Popen(path_content)
                return f"Launched: {path_content}"
            except Exception as e:
                return f"err: Failed to launch {path_content}. Error: {str(e)}"
        else:
            return f"err: Path '{path_content}' does not exist."

def create_upath_file(upath_name=None, upath_content=None):
    if upath_name is None:
        upath_name = input(":: Enter the UPATH name (without suffix): ").strip()
    file_path = os.path.join(UPATH_DIRECTORY, f"{upath_name}.upath")
    if os.path.exists(file_path):
        return f"err: UPATH '{upath_name}' has exists."
    if upath_content is None:
        upath_content = input(":: Enter the UPATH content (path or URL): ").strip()
    else:
        if len(sys.argv) > 4:
            upath_content = ' '.join(sys.argv[4:])
    if not upath_content:
        return "Canceled."
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
        return f"err: UPATH '{filename}' not exists."

def update_upath_file(upath_name=None, new_upath_content=None):
    if upath_name is None:
        upath_name = input("Enter the UPATH name (without suffix) to update: ").strip()
    file_path = os.path.join(UPATH_DIRECTORY, f"{upath_name}.upath")
    if not os.path.exists(file_path):
        return f"err: UPATH '{upath_name}' not exists."
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
        return f"err: UPATH '{current_name}' not exists."
    if new_name is None:
        new_name = input("Enter the new UPATH name (without suffix): ").strip()
    new_path = os.path.join(UPATH_DIRECTORY, f"{new_name}.upath")
    if os.path.exists(new_path):
        return f"err: UPATH '{new_name}' already exists."
    os.rename(current_path, new_path)
    return f"UPATH '{current_name}' has been renamed to '{new_name}' successfully."

def list_upath_files():
    upath_directory = UPATH_DIRECTORY
    if not os.path.exists(upath_directory):
        print(f"Directory '{upath_directory}' does not exist.")
        return
    files = os.listdir(upath_directory)
    upath_files = [os.path.splitext(file)[0] for file in files if file.endswith(".upath")]
    if not upath_files:
        print("No UPATH files found.")
        return
    print("Existing UPATH files:")
    for file in upath_files:
        print(file)

def cat_upath_file(filename=None):
    if filename is None:
        filename = input("Enter the UPATH name (without suffix) to display: ").strip()
    file_path = os.path.join(UPATH_DIRECTORY, f"{filename}.upath")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        print(f"Content of '{filename}.upath':")
        print(content)
    else:
        print(f"err: UPATH '{filename}' not exists.")

def main():
    if len(sys.argv) < 2:
        print("Usage: core.py <filename> or core.py -m <command> [args]")
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
        print("Usage: core.py -m <command> [args]")
        print(":: Command ")
        print("new, del, update, rename, cat, ls, browser")
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

    elif command == "ls":
        list_upath_files()

    elif command == "cat":
        filename = sys.argv[3] if len(sys.argv) > 3 else None
        cat_upath_file(filename)
        
    elif command == "browser":
        if len(sys.argv) < 4:
            print("Usage: core.py -m browser <set|get> [path]")
            return
        subcmd = sys.argv[3]
        if subcmd == "set":
            if len(sys.argv) < 5:
                print("Please specify browser path")
                return
            browser_path = ' '.join(sys.argv[4:])
            print(set_browser_path(browser_path))
        elif subcmd == "get":
            print(f"Current browser path: {get_browser_path()}")
        else:
            print(f"Unknown browser command: {subcmd}")

    else:
        print(f"Unknown command: {command}")
        print("Available commands: new, del, update, rename, ls, cat, browser")

if __name__ == "__main__":
    print("---------->>>")
    main()
    print("---------->>>")