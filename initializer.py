import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import sys

def install_requirements():
    """安装所需的Python包"""
    requirements = ["requests"]
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"成功安装: {package}")
        except subprocess.CalledProcessError:
            print(f"安装失败: {package}")
            return False
    return True

def select_directory():
    """选择安装目录"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    # 选择目录
    install_dir = filedialog.askdirectory(title="选择Fuck安装目录")
    if not install_dir:
        messagebox.showinfo("信息", "安装已取消")
        return None
    
    # 确认选择
    confirm = messagebox.askyesno("确认", f"确定选择以下目录吗?\n{install_dir}")
    if not confirm:
        return None
    
    return install_dir

def create_root_file(install_dir):
    """创建root.txt文件"""
    core_path = os.path.join(install_dir, "core.py")
    
    # 检查core.py是否存在
    if not os.path.exists(core_path):
        messagebox.showerror("错误", f"在选定目录中找不到core.py文件\n{core_path}")
        return False
    
    # 创建root.txt文件
    root_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "root.txt")
    try:
        with open(root_file_path, "w") as f:
            f.write(core_path)
        messagebox.showinfo("成功", f"root.txt文件已创建\n路径: {root_file_path}")
        return True
    except Exception as e:
        messagebox.showerror("错误", f"创建root.txt文件时出错: {str(e)}")
        return False

def main():
    """主函数"""
    print("Fuck初始化程序")
    print("==============")
    
    # 选择安装目录
    install_dir = select_directory()
    if not install_dir:
        return
    
    # 安装所需包
    print("正在安装所需的Python包...")
    if not install_requirements():
        messagebox.showwarning("警告", "部分包安装失败，程序可能无法正常工作")
    
    # 创建root.txt文件
    if create_root_file(install_dir):
        messagebox.showinfo("完成", "初始化完成! 您现在可以使用fuck命令了")
    else:
        messagebox.showerror("错误", "初始化失败")

if __name__ == "__main__":
    main()