import os
import sys
import json
import inspect
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import subprocess

class Overload:
    def __init__(self):
        self.functions = []

    def register(self, func):
        sig = inspect.signature(func)
        parameters = sig.parameters.values()
        type_hints = []
        for param in parameters:
            if param.annotation is inspect.Parameter.empty:
                raise TypeError(f"参数 {param.name} 缺少类型注解。")
            type_hints.append(param.annotation)
        for existing_sig, existing_th, _ in self.functions:
            if type_hints == existing_th:
                raise ValueError(f"重复注册类型签名 {type_hints} 的函数。")
        self.functions.append((sig, type_hints, func))
        return self

    def __call__(self, *args, **kwargs):
        matched = []
        for sig, type_hints, func in self.functions:
            try:
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()
            except TypeError:
                continue
            valid = True
            for name, value in bound.arguments.items():
                expected_type = sig.parameters[name].annotation
                if not isinstance(value, expected_type):
                    valid = False
                    break
            if valid:
                matched.append((type_hints, func))
        if not matched:
            raise TypeError("没有匹配的函数重载。")
        selected = None
        for th, func in matched:
            if selected is None:
                selected = (th, func)
                continue
            current_th, current_func = selected
            if self._is_more_specific(th, current_th):
                selected = (th, func)
            elif self._is_more_specific(current_th, th):
                continue
            else:
                raise TypeError("函数调用存在二义性，无法确定最具体的重载。")
        return selected[1](*args, **kwargs)

    @staticmethod
    def _is_more_specific(hints_a, hints_b):
        if len(hints_a) != len(hints_b):
            return False
        for a, b in zip(hints_a, hints_b):
            if not issubclass(a, b):
                return False
        return any(a != b for a, b in zip(hints_a, hints_b))


def overload(func):
    name = func.__name__
    if name not in _registry:
        _registry[name] = Overload()
    _registry[name].register(func)
    return _registry[name]

_registry = {}

RED = "\033[38;2;200;50;50m"
LIGHT_GREEN = "\033[38;2;100;255;100m"
LIGHT_BLUE = "\033[38;2;100;100;255m"
YELLOW = "\033[38;2;255;255;100m"
ORANGE = "\033[38;2;255;165;0m" 
RESET = "\033[0m"

def set_working_directory():
    if getattr(sys, 'frozen', False): 
        current_dir = os.path.dirname(sys.executable)
        current_dir = os.path.dirname(os.path.abspath(__file__))
    
    os.chdir(current_dir)
    print(f"工作目录已设置为: {current_dir}")
    return current_dir

def ensure_memory_directories(base_dir):
    memory_dir = os.path.join(base_dir, "memory")
    upath_dir = os.path.join(memory_dir, "UPATH")
    images_dir = os.path.join(memory_dir, "IMAGES")
    url_dir = os.path.join(memory_dir, "URL")
    
    os.makedirs(memory_dir, exist_ok=True)
    os.makedirs(upath_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(url_dir, exist_ok=True)
    
    config_file = os.path.join(memory_dir, "config.json")
    if not os.path.exists(config_file):
        default_config = {
            "browser": "",
            "privacy_mode": True,
            "wallpaper_folder": "",
            "current_wallpaper": ""
        }
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4)
    
    help_file = os.path.join(memory_dir, "help.json")
    if not os.path.exists(help_file):
        default_help = {
            "帮助错误": "帮助文件失效或没有被正确配置，\n您可以将以下错误信息提供给开发者:\n"
            "[BadResult] Missing JSON file 'help'.",
        }
        with open(help_file, "w", encoding="utf-8") as f:
            json.dump(default_help, f, indent=4, ensure_ascii=False)

def read_config(base_dir):
    config_file = os.path.join(base_dir, "memory", "config.json")
    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)

def write_config(config, base_dir):
    config_file = os.path.join(base_dir, "memory", "config.json")
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, separators=(',', ': '))

def set_browser_path(browser_path, base_dir):
    config = read_config(base_dir)
    config["browser"] = browser_path
    write_config(config, base_dir)
    return f"Browser path set to: {browser_path}"

def get_browser_path(base_dir):
    config = read_config(base_dir)
    return config.get("browser", "")

class UPATHManager:
    def __init__(self, root, base_dir):
        self.root = root
        self.base_dir = base_dir
        self.root.title("Fuck UPATH 管理器")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")
        
        self.ensure_config()
        
        self.ensure_help_file()
        
        self.privacy_mode = self.get_privacy_mode()
        
        if os.path.exists("icon.ico"):
            self.root.iconbitmap("icon.ico")
        
        self.create_widgets()
        self.load_upath_list()
        
        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=25)
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.style.configure("TButton", font=("Arial", 9))
        self.style.configure("TLabel", font=("Arial", 9), background="#f0f0f0")
        self.style.configure("TCheckbutton", font=("Arial", 9), background="#f0f0f0")
        
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
    
    def ensure_config(self):
        config_path = os.path.join(self.base_dir, "memory", "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    if "privacy_mode" not in config:
                        config["privacy_mode"] = True
                        self.write_config(config)
            except:
                config = {"privacy_mode": True}
                self.write_config(config)
        else:
            os.makedirs(os.path.join(self.base_dir, "memory"), exist_ok=True)
            config = {"privacy_mode": True}
            self.write_config(config)
    
    def ensure_help_file(self):
        help_file = os.path.join(self.base_dir, "memory", "help.json")
        if not os.path.exists(help_file):
            default_help = {
                "帮助错误": "帮助文件失效或没有被正确配置，\n您可以将以下错误信息提供给开发者:\n"
                "[BadResult] Missing JSON file 'help'.",
            }
            with open(help_file, "w", encoding="utf-8") as f:
                json.dump(default_help, f, indent=4, ensure_ascii=False)
    
    def create_widgets(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="删除", command=self.delete_upath).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="执行", command=self.execute_upath).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="壁纸目录", command=lambda: self.wallpaper_command("folder")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="轮换壁纸", command=lambda: self.wallpaper_command("next")).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="设置浏览器", command=self.set_browser).pack(side=tk.LEFT, padx=5)
        
        privacy_frame = ttk.Frame(self.root)
        privacy_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.privacy_var = tk.BooleanVar(value=self.privacy_mode)
        privacy_check = ttk.Checkbutton(
            privacy_frame, 
            text="隐私模式", 
            variable=self.privacy_var,
            command=self.toggle_privacy
        )
        privacy_check.pack(side=tk.LEFT)
        
        self.browser_status = ttk.Label(
            privacy_frame, 
            text=f"浏览器: {self.get_browser_display()}"
        )
        self.browser_status.pack(side=tk.RIGHT, padx=10)
        
        search_help_frame = ttk.Frame(self.root)
        search_help_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Label(search_help_frame, text="搜索:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_help_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind("<KeyRelease>", self.on_search)
        
        ttk.Button(search_help_frame, text="帮助", command=self.show_help).pack(side=tk.RIGHT)
        
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        columns = ("name", "path")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="extended")
        
        self.tree.heading("name", text="名称", anchor=tk.W)
        self.tree.heading("path", text="路径/URL", anchor=tk.W)
        
        self.tree.column("name", width=200, minwidth=150)
        self.tree.column("path", width=700, minwidth=300)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(fill="x", padx=10, pady=(0, 10))
    
    def get_browser_display(self):
        browser_path = self.get_browser_path()
        if not browser_path:
            return "未设置"
        
        if self.privacy_mode:
            return "******"
        
        return os.path.basename(browser_path)
    
    def toggle_privacy(self):
        new_mode = self.privacy_var.get()
        self.set_privacy_mode(new_mode)
        self.privacy_mode = new_mode
        self.load_upath_list()
        self.browser_status.config(text=f"浏览器: {self.get_browser_display()}")
        self.status_var.set(f"隐私模式 {'已启用' if new_mode else '已禁用'}")
    
    def set_browser(self):
        browser_path = filedialog.askopenfilename(
            title="选择浏览器可执行文件",
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")]
        )
        
        if browser_path:
            result = self.set_browser_path(browser_path)
            self.browser_status.config(text=f"浏览器: {self.get_browser_display()}")
            self.status_var.set(result)
    
    def load_upath_list(self, search_term=""):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        upath_dir = os.path.join(self.base_dir, "memory", "UPATH")
        images_dir = os.path.join(self.base_dir, "memory", "IMAGES")
        url_dir = os.path.join(self.base_dir, "memory", "URL")
        
        upaths = []
        
        for directory in [upath_dir, images_dir, url_dir]:
            if os.path.exists(directory):
                for filename in os.listdir(directory):
                    if filename.endswith(".upath"):
                        name = filename[:-6]
                        path_content = self.launch_path_from_upath(name)
                        
                        if path_content.startswith("\033[38;2;200;50;50m"):
                            path = path_content
                        else:
                            path = path_content.strip().strip('"')
                        
                        if search_term:
                            search_lower = search_term.lower()
                            if (search_lower not in name.lower() and 
                                search_lower not in path.lower()):
                                continue
                        
                        upaths.append((name, path))
        
        for name, path in sorted(upaths, key=lambda x: x[0]):
            display_path = "******" if self.privacy_mode and not path.startswith("\033") else path
            self.tree.insert("", "end", values=(name, display_path))
        
        self.status_var.set(f"已加载 {len(upaths)} 个 UPATH")
    
    def on_search(self, event):
        search_term = self.search_var.get()
        self.load_upath_list(search_term)
    
    def on_select(self, event):
        selected = self.tree.selection()
        self.status_var.set(f"已选择 {len(selected)} 个项目")
    
    def on_double_click(self, event):
        self.execute_upath()
    
    def delete_upath(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("提示", "请选择要删除的 UPATH")
            return
        
        names = [self.tree.item(item, "values")[0] for item in selected]
        confirm = messagebox.askyesno(
            "确认删除",
            f"确定要删除 {len(names)} 个 UPATH 吗?\n\n{', '.join(names)}"
        )
        
        if confirm:
            for name in names:
                self.delete_upath_file(name)
            
            self.load_upath_list()
            self.status_var.set(f"已删除 {len(names)} 个 UPATH")
    
    def delete_upath_file(self, name):
        directories = [
            os.path.join(self.base_dir, "memory", "UPATH"),
            os.path.join(self.base_dir, "memory", "IMAGES"),
            os.path.join(self.base_dir, "memory", "URL")
        ]
        
        for directory in directories:
            file_path = os.path.join(directory, f"{name}.upath")
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    return True
                except Exception as e:
                    print(f"删除文件错误: {str(e)}")
                    return False
        
        return False
    
    def execute_upath(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("提示", "请选择要执行的 UPATH")
            return
        
        if len(selected) > 1:
            messagebox.showinfo("提示", "一次只能执行一个 UPATH")
            return
        
        item = selected[0]
        name = self.tree.item(item, "values")[0]
        
        result = self.launch_path_from_upath_with_browser(name)
        if result.startswith("err:"):
            messagebox.showerror("错误", result)
        else:
            self.status_var.set(result)
    
    def launch_path_from_upath(self, filename):
        for directory in [os.path.join(self.base_dir, "memory", "UPATH"),
                          os.path.join(self.base_dir, "memory", "IMAGES"),
                          os.path.join(self.base_dir, "memory", "URL")]:
            file_path = os.path.join(directory, f"{filename}.upath")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read().strip().strip('"')
                return content
        return f"{RED}err: UPATH '{filename}' not exists.{RESET}"
    
    def launch_path_from_upath_with_browser(self, filename):
        path_content = self.launch_path_from_upath(filename)
        if isinstance(path_content, str) and path_content.startswith("err:"):
            return path_content

        path_content = path_content.strip('"')
        
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
        
        if path_content.startswith(("http://", "https://", "www.")) or (path_content.count('.') == 3 and all(part.isdigit() for part in path.split('.'))):
            browser_path = self.get_browser_path()
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
    
    def wallpaper_command(self, command):
        if command == "folder":
            folder = filedialog.askdirectory(title="选择壁纸文件夹")
            if folder:
                name = "wallpaper_folder"
                self.save_upath_file(name, folder)
                self.set_wallpaper_folder(name)
                self.status_var.set(f"壁纸文件夹已设置为: {folder}")
        
        elif command == "next":
            self.next_wallpaper()
            self.status_var.set("已切换到下一张壁纸")
    
    def set_wallpaper_folder(self, upath_name):
        config = self.read_config()
        config["wallpaper_folder"] = upath_name
        self.write_config(config)
    
    def next_wallpaper(self):
        config = self.read_config()
        folder_upath = config.get("wallpaper_folder", "")
        if not folder_upath:
            messagebox.showinfo("提示", "未设置壁纸文件夹，请先设置壁纸目录。")
            return
        
        folder_path = self.launch_path_from_upath(folder_upath).strip('"')
        if not os.path.isdir(folder_path):
            messagebox.showinfo("提示", f"壁纸文件夹不存在: {folder_path}")
            return
        
        images = sorted([f for f in os.listdir(folder_path) 
                        if f.lower().endswith(('.png','.jpg','.jpeg','.gif'))])
        
        if not images:
            messagebox.showinfo("提示", f"壁纸文件夹中没有图片: {folder_path}")
            return
        
        current = config.get("current_wallpaper", "")
        current_basename = os.path.basename(current) if current else None
        
        if current_basename in images:
            current_index = images.index(current_basename)
            next_index = (current_index + 1) % len(images)
        else:
            next_index = 0
        
        next_wallpaper = os.path.join(folder_path, images[next_index])
        self.set_current_wallpaper(next_wallpaper)
    
    def set_current_wallpaper(self, path):
        config = self.read_config()
        config["current_wallpaper"] = path
        self.write_config(config)
    
    def read_config(self):
        return read_config(self.base_dir)
    
    def write_config(self, config):
        write_config(config, self.base_dir)
    
    def get_privacy_mode(self):
        config = self.read_config()
        return config.get("privacy_mode", True)
    
    def set_privacy_mode(self, enabled):
        config = self.read_config()
        config["privacy_mode"] = enabled
        self.write_config(config)
    
    def set_browser_path(self, browser_path):
        return set_browser_path(browser_path, self.base_dir)
    
    def get_browser_path(self):
        return get_browser_path(self.base_dir)
    
    def show_help(self):
        help_file = os.path.join(self.base_dir, "memory", "help.json")
        try:
            with open(help_file, "r", encoding="utf-8") as f:
                help_content = json.load(f)
        except Exception as e:
            messagebox.showerror("帮助文件错误", f"无法加载帮助文件: {str(e)}")
            return
        
        self.help_window = tk.Toplevel(self.root)
        self.help_window.title("帮助")
        self.help_window.geometry("400x300")
        
        self.help_listbox = tk.Listbox(self.help_window)
        self.help_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for item in help_content:
            self.help_listbox.insert(tk.END, item)
        
        self.help_text = tk.Text(self.help_window, wrap=tk.WORD, height=10, state=tk.DISABLED)
        self.help_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.back_button = ttk.Button(self.help_window, text="返回上一级", command=self.help_window.destroy)
        self.back_button.pack(side=tk.BOTTOM, pady=10)
        
        def on_double_click(event):
            selection = self.help_listbox.curselection()
            if selection:
                index = selection[0]
                selected_item = list(help_content.keys())[index]
                help_text = help_content[selected_item]
                
                self.help_text.config(state=tk.NORMAL)
                self.help_text.delete(1.0, tk.END)
                self.help_text.insert(tk.END, f"{selected_item}: {help_text}")
                self.help_text.config(state=tk.DISABLED)
        
        self.help_listbox.bind("<Double-Button-1>", on_double_click)
        
        if help_content:
            first_item = list(help_content.keys())[0]
            help_text = help_content[first_item]
            self.help_text.config(state=tk.NORMAL)
            self.help_text.delete(1.0, tk.END)
            self.help_text.insert(tk.END, f"{first_item}: {help_text}")
            self.help_text.config(state=tk.DISABLED)
    
    def save_upath_file(self, name, path):
        upath_dir = os.path.join(self.base_dir, "memory", "UPATH")
        images_dir = os.path.join(self.base_dir, "memory", "IMAGES")
        url_dir = os.path.join(self.base_dir, "memory", "URL")

        if any(path.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
            target_dir = images_dir
        elif any(path.startswith(proto) for proto in ["http://", "https://", "www."]) or (path.count('.') == 3 and all(part.isdigit() for part in path.split('.'))):
            target_dir = url_dir
        else:
            target_dir = upath_dir

        os.makedirs(target_dir, exist_ok=True)

        file_path = os.path.join(target_dir, f"{name}.upath")
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f'"{path}"')
            self.load_upath_list()
            self.status_var.set(f"已保存: {name}")
            messagebox.showinfo("成功", f"UPATH '{name}' 创建成功！")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def delete_upath_file(self, name):
        directories = [
            os.path.join(self.base_dir, "memory", "UPATH"),
            os.path.join(self.base_dir, "memory", "IMAGES"),
            os.path.join(self.base_dir, "memory", "URL")
        ]
        
        for directory in directories:
            file_path = os.path.join(directory, f"{name}.upath")
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    return True
                except Exception as e:
                    print(f"删除文件错误: {str(e)}")
                    return False
        
        return False

if __name__ == "__main__":
    current_dir = set_working_directory()
    ensure_memory_directories(current_dir)
    
    root = tk.Tk()
    app = UPATHManager(root, current_dir)
    root.mainloop()