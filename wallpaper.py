import os
import sys
import json
import requests
import subprocess
from time import time
from threading import Timer
from utils import read_upath_file, read_config, write_config  # 导入 utils 中的函数

RED = "\033[38;2;200;50;50m"
LIGHT_GREEN = "\033[38;2;100;255;100m"
RESET = "\033[0m"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, "memory/IMAGES")
UPATH_DIRECTORY = os.path.join(SCRIPT_DIR, "memory/UPATH")

def get_wallpaper_folder():
    config = read_config()
    return config.get("wallpaper_folder", "")

def set_wallpaper_folder(upath_name):
    config = read_config()
    config["wallpaper_folder"] = upath_name
    write_config(config)

def get_current_wallpaper():
    config = read_config()
    return config.get("current_wallpaper", "")

def set_current_wallpaper(path):
    config = read_config()
    config["current_wallpaper"] = path
    write_config(config)

def set_wallpaper(path):
    if not os.path.exists(path):
        return f"{RED}err: Wallpaper file not found{RESET}"
    try:
        if sys.platform == 'win32':
            import ctypes
            ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
        elif sys.platform == 'darwin':
            subprocess.run(['osascript', '-e', f'tell application "Finder" to set desktop picture to POSIX file "{path}"'])
        else:
            subprocess.run(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', f"file://{path}"])
        set_current_wallpaper(path)
        return f"Wallpaper set to: {os.path.basename(path)}"
    except Exception as e:
        return f"{RED}err: Failed to set wallpaper: {str(e)}{RESET}"

def handle_wallpaper_command(args):
    if len(args) < 1:
        print(f"{RED}Usage: -wp <set|folder|next> [args]{RESET}")
        return
    
    subcmd = args[0]
    
    if subcmd == "set":
        if len(args) < 2:
            print(f"{RED}Please specify image path or UPATH name{RESET}")
            return
        
        target = args[1]
        if target.endswith('.upath') or os.path.exists(os.path.join(UPATH_DIRECTORY, f"{target}.upath")):
            path_content = read_upath_file(target.replace('.upath', '')).strip('"')
        else:
            path_content = target
        
        if not os.path.exists(path_content):
            print(f"{RED}Wallpaper file not found: {path_content}{RESET}")
            return
        
        print(set_wallpaper(path_content))
    
    elif subcmd == "folder":
        if len(args) < 2:
            print(f"{RED}Please specify UPATH name of wallpaper folder{RESET}")
            return
        
        set_wallpaper_folder(args[1])
        print(f"Wallpaper folder set to: {args[1]}")
    
    elif subcmd == "next":
        folder_upath = get_wallpaper_folder()
        if not folder_upath:
            print(f"{RED}No wallpaper folder configured. Use '-wp folder <upath>' first.{RESET}")
            return
        
        folder_path = read_upath_file(folder_upath).strip('"')
        if not os.path.isdir(folder_path):
            print(f"{RED}Wallpaper folder not found: {folder_path}{RESET}")
            return
        
        images = sorted([f for f in os.listdir(folder_path) 
                        if f.lower().endswith(('.png','.jpg','.jpeg','.gif'))])
        
        if not images:
            print(f"{RED}No images found in wallpaper folder{RESET}")
            return
        
        current = get_current_wallpaper()
        current_basename = os.path.basename(current) if current else None
        
        if current_basename in images:
            current_index = images.index(current_basename)
            next_index = (current_index + 1) % len(images)
        else:
            next_index = 0
        
        next_wallpaper = os.path.join(folder_path, images[next_index])
        print(set_wallpaper(next_wallpaper))
    
    else:
        print(f"{RED}Unknown wallpaper command: {subcmd}{RESET}")
        print(f"{LIGHT_GREEN}Available commands:{RESET}")
        print(f"  -wp set <image/upath>    Set wallpaper")
        print(f"  -wp folder <upath>       Set wallpaper folder")
        print(f"  -wp next                 Switch to next wallpaper")

def main():
    try:
        if len(sys.argv) < 2:
            print(f"{RED}Usage: wallpaper <set|folder|next> [args]{RESET}")
            return
        handle_wallpaper_command(sys.argv[1:])
    except Exception as e:
        print(f"{RED}Error: {str(e)}{RESET}")

if __name__ == '__main__':
    main()