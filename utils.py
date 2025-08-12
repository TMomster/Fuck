import os
import json
from outstream import rgb_to_ansi

RED = rgb_to_ansi(200, 50, 50)
LIGHT_GREEN = rgb_to_ansi(100, 255, 100)
RESET = "\033[0m"

def read_upath_file(filename):
    UPATH_DIRECTORY = os.path.join(os.path.dirname(__file__), "memory/UPATH")
    file_path = os.path.join(UPATH_DIRECTORY, f"{filename}.upath")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    else:
        return f"{RED}err: UPATH '{filename}' not exists.{RESET}"

def read_upath_file_with_comment(filename):
    UPATH_DIRECTORY = os.path.join(os.path.dirname(__file__), "memory/UPATH")
    IMAGES_DIRECTORY = os.path.join(os.path.dirname(__file__), "memory/IMAGES")
    URL_DIRECTORY = os.path.join(os.path.dirname(__file__), "memory/URL")
    
    for directory in [UPATH_DIRECTORY, IMAGES_DIRECTORY, URL_DIRECTORY]:
        file_path = os.path.join(directory, f"{filename}.upath")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    try:
                        data = json.loads(content)
                        return {
                            "path": data.get("path", ""),
                            "comment": data.get("comment", ""),
                            "type": "new"
                        }
                    except:
                        return {
                            "path": content.strip('"'),
                            "comment": "",
                            "type": "old"
                        }
            except Exception as e:
                return f"{RED}err: Failed to read UPATH: {str(e)}{RESET}"
    return f"{RED}err: UPATH '{filename}' not exists.{RESET}"

def read_config():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE = os.path.join(SCRIPT_DIR, "memory/config.json")
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def write_config(config):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE = os.path.join(SCRIPT_DIR, "memory/config.json")
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f)

def write_upath_file(filename, path, comment=""):
    UPATH_DIRECTORY = os.path.join(os.path.dirname(__file__), "memory/UPATH")
    IMAGES_DIRECTORY = os.path.join(os.path.dirname(__file__), "memory/IMAGES")
    URL_DIRECTORY = os.path.join(os.path.dirname(__file__), "memory/URL")
    
    target_directory = UPATH_DIRECTORY
    if path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        target_directory = IMAGES_DIRECTORY
    elif path.startswith(("http://", "https://", "www.")) or (path.count('.') == 3 and all(part.isdigit() for part in path.split('.'))):
        target_directory = URL_DIRECTORY
    
    file_path = os.path.join(target_directory, f"{filename}.upath")
    
    data = {
        "path": path,
        "comment": comment
    }
    
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)
        return True, ""
    except Exception as e:
        return False, f"{RED}err: Failed to write UPATH: {str(e)}{RESET}"