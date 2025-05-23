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

