import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import subprocess
import os
import platform

help = """>>> Textor help
【命令】
help: 显示帮助
cls: 清屏
exit: 结束
undo: 撤回消息
s: 超转发（显示输出）
sh: 超转发（不显示输出）
set: 控制
export: 导出消息
【键盘】
return: 发送
c-return: 换行
backspace: 删除选中
delete: 删除选中
c-plus: 字体加
c-minus: 字体减
c-mouse3: 字体增减
"""

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.font_size = 12
        self.message_history = []
        self.selected_line = None

        # 设置初始窗口大小和标题
        self.root.geometry("800x600")
        self.root.title("Textor")

        # 配置字体
        self.root.option_add("*Font", f"TkDefaultFont {self.font_size}")

        # 文本显示区域
        self.text_display = tk.Text(self.root, wrap='word', state='disabled', bg='#f8f9fa', padx=10, pady=10)
        self.text_display.pack(expand=True, fill='both')

        # 滚动条
        self.scrollbar = tk.Scrollbar(self.text_display)
        self.scrollbar.pack(side='right', fill='y')
        self.text_display.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_display.yview)

        # 编辑栏
        self.entry = tk.Entry(self.root)
        self.entry.pack(fill='x', padx=10, pady=10)
        self.entry.focus_set()

        # 绑定事件
        self.entry.bind('<Return>', self.send_message)
        self.entry.bind('<Control-Return>', self.insert_newline)
        self.root.bind("<BackSpace>", self.delete_message)
        self.root.bind("<Delete>", self.delete_message)
        self.root.bind("<Control-plus>", self.increase_font)
        self.root.bind("<Control-minus>", self.decrease_font)
        self.root.bind("<Control-MouseWheel>", self.font_wheel_zoom)
        self.root.bind("<Control-Button-4>", self.increase_font)
        self.root.bind("<Control-Button-5>", self.decrease_font)
        self.text_display.bind("<Button-1>", self.select_message)

    def send_message(self, event=None):
        message = self.entry.get()
        if message.startswith('/'):
            self.handle_command(message)
        else:
            self.add_message_to_display(message)
        self.entry.delete(0, tk.END)

    def handle_command(self, command):
        args = command.split()
        if not args:
            return

        cmd = args[0].lower()
        if cmd == '/set' and len(args) >= 4 and args[1].lower() == 'window-size':
            try:
                width = int(args[2])
                height = int(args[3])
                self.root.geometry(f"{width}x{height}")
            except ValueError:
                self.add_message_to_display(">>> Error: Invalid window size.")
        elif cmd == '/set' and len(args) >= 3 and args[1].lower() == 'title':
            new_title = ' '.join(args[2:])
            self.root.title(new_title)
        elif cmd == '/undo':
            self.undo_last_message()
        elif cmd == '/cls':
            self.clear_messages()
        elif cmd == '/exit':
            self.root.destroy()
        elif cmd == '/s' and len(args) > 1:
            sys_command = ' '.join(args[1:])
            self.execute_system_command(sys_command)
        elif cmd == '/sh' and len(args) > 1:
            sh_command = ' '.join(args[1:])
            self.execute_sh_command(sh_command)
        elif cmd == '/export':
            if len(args) == 1:
                self.export_messages_with_dialog()
            else:
                file_path = ' '.join(args[1:])
                self.export_messages_to_path(file_path)
        elif cmd == '/help':
            self.add_message_to_display(help)
        else:
            self.add_message_to_display(f">>> Unknown command: {command}")

    def add_message_to_display(self, message):
        self.text_display.config(state='normal')
        current_time = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{current_time}] {message}\n"
        self.text_display.insert(tk.END, formatted_message)
        self.text_display.config(state='disabled')
        self.text_display.see(tk.END)
        self.message_history.append(formatted_message)

    def select_message(self, event):
        self.text_display.config(state='normal')
        line = self.text_display.index("@%d,%d" % (event.x, event.y)).split('.')[0]
        self.selected_line = line
        self.text_display.tag_remove("selected", "1.0", tk.END)
        self.text_display.tag_add("selected", f"{line}.0", f"{line}.end")
        self.text_display.tag_config("selected", background="#e6e6e6")
        self.text_display.config(state='disabled')

    def delete_message(self, event=None):
        if self.selected_line:
            self.text_display.config(state='normal')
            self.text_display.delete(f"{self.selected_line}.0", f"{self.selected_line}.end")
            self.selected_line = None
            self.text_display.config(state='disabled')

    def undo_last_message(self):
        if self.message_history:
            last_message = self.message_history.pop()
            start_index = self.text_display.search(last_message, "1.0", tk.END)
            if start_index:
                end_index = f"{start_index.split('.')[0]}.end"
                self.text_display.config(state='normal')
                self.text_display.delete(start_index, end_index)
                self.text_display.config(state='disabled')

    def clear_messages(self):
        self.text_display.config(state='normal')
        self.text_display.delete("1.0", tk.END)
        self.text_display.config(state='disabled')
        self.message_history.clear()

    def execute_system_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
            output = result.stdout if result.stdout else result.stderr
            self.add_message_to_display(f"SYS: {output.strip()}")
        except subprocess.TimeoutExpired:
            self.add_message_to_display("SYS: Command timed out.")
        except Exception as e:
            self.add_message_to_display(f"SYS: Error - {str(e)}")

    def execute_sh_command(self, command):
        try:
            subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        except subprocess.TimeoutExpired:
            self.add_message_to_display("SH: Command timed out.")
        except Exception as e:
            self.add_message_to_display(f"SH: Error - {str(e)}")

    def insert_newline(self, event=None):
        self.entry.insert(tk.END, "\n")

    def increase_font(self, event=None):
        if self.font_size < 24:
            self.font_size += 1
            self.root.option_add("*Font", f"TkDefaultFont {self.font_size}")
            self.text_display.config(font=f"TkDefaultFont {self.font_size}")
            self.entry.config(font=f"TkDefaultFont {self.font_size}")

    def decrease_font(self, event=None):
        if self.font_size > 8:
            self.font_size -= 1
            self.root.option_add("*Font", f"TkDefaultFont {self.font_size}")
            self.text_display.config(font=f"TkDefaultFont {self.font_size}")
            self.entry.config(font=f"TkDefaultFont {self.font_size}")

    def font_wheel_zoom(self, event=None):
        if event.delta > 0:
            self.increase_font()
        else:
            self.decrease_font()

    def export_messages_with_dialog(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.export_messages_to_path(file_path)

    def export_messages_to_path(self, file_path):
        try:
            # 解析路径中的快捷路径，如 ~desktop
            if "~desktop" in file_path:
                desktop_path = self.get_desktop_path()
                file_path = file_path.replace("~desktop", desktop_path)

            with open(file_path, 'w', encoding='utf-8') as file:
                for message in self.message_history:
                    file.write(message)
            self.add_message_to_display(f">>> Messages exported to {file_path}")
        except Exception as e:
            self.add_message_to_display(f">>> Error: Failed to export messages - {str(e)}")

    def get_desktop_path(self):
        if platform.system() == "Windows":
            return os.path.join(os.path.expanduser("~"), "Desktop")
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            return os.path.join(os.path.expanduser("~"), "Desktop")
        else:
            return os.path.expanduser("~")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()