'''
Py-Notebook
一个基于Python的本地笔记本应用，支持Markdown语法编辑与实时预览，提供直观的文件夹管理功能。
version:v1.0
By HelloWorld05 in 20250402
'''

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
from datetime import datetime
import markdown2
import webbrowser
import tempfile
import shutil

class NotebookApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Py-Notebook")
        self.root.geometry("1000x600")
        
        # 当前文件路径和标题跟踪
        self.current_file_path = None
        self.title_var = tk.StringVar()
        self.title_var.set("未命名笔记")
        
        # 创建界面组件
        self.setup_top_bar()
        self.setup_sidebar()
        self.setup_editor()
        
        # 初始化树形结构右键菜单
        self.context_menu = None
        
        # 绑定树形结构展开事件
        self.tree.bind("<<TreeviewOpen>>", self.on_folder_expand)

    def setup_top_bar(self):
        """创建顶部工具栏"""
        top_frame = tk.Frame(self.root, height=30, bg="#f0f0f0")
        top_frame.pack(fill=tk.X, side=tk.TOP)
        
        # 保存按钮
        save_btn = tk.Button(top_frame, text="保存", command=self.save_current_note)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # 标题显示
        title_label = tk.Label(top_frame, textvariable=self.title_var, bg="#f0f0f0")
        title_label.pack(side=tk.LEFT, expand=True)
        
        # 预览按钮
        preview_btn = tk.Button(top_frame, text="预览", command=self.preview_markdown)
        preview_btn.pack(side=tk.RIGHT, padx=5)
        
        # 帮助按钮
        help_btn = tk.Button(top_frame, text="帮助", command=self.show_help)
        help_btn.pack(side=tk.RIGHT, padx=5)
        
        # 关于按钮
        about_btn = tk.Button(top_frame, text="介绍", command=self.show_about)
        about_btn.pack(side=tk.RIGHT, padx=5)

    def setup_sidebar(self):
        """创建左侧边栏树形结构"""
        self.left_frame = tk.Frame(self.root, width=200)
        self.left_frame.pack(fill=tk.Y, side=tk.LEFT)
        
        self.tree = ttk.Treeview(self.left_frame, show="tree")
        self.tree.pack(expand=True, fill=tk.BOTH)
        
        # 绑定右键事件
        self.tree.bind("<Button-3>", self.show_context_menu)

    def setup_editor(self):
        """创建右侧文本编辑器"""
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(expand=True, fill=tk.BOTH)
        
        # 文本编辑器
        self.text_editor = tk.Text(self.right_frame, wrap=tk.WORD)
        self.text_editor.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(self.right_frame, command=self.text_editor.yview)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.text_editor.config(yscrollcommand=scrollbar.set)

    def show_context_menu(self, event):
        """显示右键菜单"""
        item = self.tree.identify_row(event.y)
        menu = tk.Menu(self.root, tearoff=0)
        
        if item:
            tags = self.tree.item(item, "tags")
            if "folder" in tags:
                menu.add_command(label="新建文件夹", command=lambda: self.create_new_folder(item))
                menu.add_command(label="新建笔记", command=lambda: self.create_new_note(item))
                menu.add_command(label="删除文件夹", command=lambda: self.delete_folder(item))
                menu.add_command(label="重命名", command=lambda: self.rename_item(item))
            elif "note" in tags:
                menu.add_command(label="删除笔记", command=lambda: self.delete_note(item))
                menu.add_command(label="重命名", command=lambda: self.rename_item(item))
        else:
            menu.add_command(label="打开文件夹", command=self.add_root_folder)
        
        menu.post(event.x_root, event.y_root)

    def add_root_folder(self):
        """添加根文件夹"""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.tree.insert("", "end", iid=folder_path, 
                           text=os.path.basename(folder_path), tags=("folder",))
            self.load_child_items(folder_path)

    def load_child_items(self, parent_path):
        """加载子项到树形结构"""
        try:
            for entry in os.listdir(parent_path):
                entry_path = os.path.join(parent_path, entry)
                if os.path.isdir(entry_path):
                    self.tree.insert(parent_path, "end", iid=entry_path, 
                                  text=entry, tags=("folder",))
                elif entry.endswith(".txt"):
                    self.tree.insert(parent_path, "end", iid=entry_path, 
                                  text=entry, tags=("note",))
        except Exception as e:
            messagebox.showerror("错误", f"无法加载目录: {e}")

    def on_folder_expand(self, event):
        """处理文件夹展开事件"""
        item = self.tree.focus()
        self.load_child_items(item)

    def create_new_folder(self, parent_item):
        """创建新文件夹"""
        parent_path = self.tree.item(parent_item)["iid"]
        folder_name = simpledialog.askstring("新建文件夹", "输入文件夹名称:")
        if folder_name:
            new_path = os.path.join(parent_path, folder_name)
            try:
                os.makedirs(new_path, exist_ok=True)
                self.tree.insert(parent_item, "end", iid=new_path, 
                              text=folder_name, tags=("folder",))
            except Exception as e:
                messagebox.showerror("错误", f"创建失败: {e}")

    def create_new_note(self, parent_item):
        """创建新笔记"""
        parent_path = self.tree.item(parent_item)["iid"]
        default_name = datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"
        new_path = os.path.join(parent_path, default_name)
        try:
            with open(new_path, "w") as f:
                f.write("")
            self.tree.insert(parent_item, "end", iid=new_path, 
                           text=default_name, tags=("note",))
        except Exception as e:
            messagebox.showerror("错误", f"创建失败: {e}")

    def delete_folder(self, item):
        """删除文件夹"""
        path = self.tree.item(item)["iid"]
        if messagebox.askyesno("确认", f"删除整个文件夹 {os.path.basename(path)} 及其所有内容？"):
            try:
                shutil.rmtree(path)
                self.tree.delete(item)
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {e}")

    def delete_note(self, item):
        """删除笔记"""
        path = self.tree.item(item)["iid"]
        if messagebox.askyesno("确认", f"删除笔记 {os.path.basename(path)}？"):
            try:
                os.remove(path)
                self.tree.delete(item)
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {e}")

    def rename_item(self, item):
        """重命名项目"""
        old_path = self.tree.item(item)["iid"]
        old_name = os.path.basename(old_path)
        new_name = simpledialog.askstring("重命名", "输入新名称:", initialvalue=old_name)
        
        if new_name:
            parent_dir = os.path.dirname(old_path)
            new_path = os.path.join(parent_dir, new_name)
            
            try:
                os.rename(old_path, new_path)
                self.tree.item(item, iid=new_path, text=new_name)
                if self.current_file_path == old_path:
                    self.current_file_path = new_path
                    self.title_var.set(new_name)
            except Exception as e:
                messagebox.showerror("错误", f"重命名失败: {e}")

    def save_current_note(self):
        """保存当前笔记"""
        if self.current_file_path:
            content = self.text_editor.get("1.0", tk.END)
            try:
                with open(self.current_file_path, "w") as f:
                    f.write(content)
                messagebox.showinfo("保存成功", "笔记已保存！")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {e}")
        else:
            messagebox.showwarning("警告", "请先选择或创建笔记")

    def on_tree_select(self, event):
        """处理树形结构选择事件"""
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            if "note" in self.tree.item(item, "tags"):
                self.current_file_path = item
                try:
                    with open(item, "r") as f:
                        content = f.read()
                    self.text_editor.delete("1.0", tk.END)
                    self.text_editor.insert("1.0", content)
                    self.title_var.set(os.path.basename(item))
                except Exception as e:
                    messagebox.showerror("错误", f"无法打开文件: {e}")

    def preview_markdown(self):
        """预览Markdown内容"""
        content = self.text_editor.get("1.0", tk.END)
        if content.strip():
            html = markdown2.markdown(content)
            with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as f:
                f.write(html)
                webbrowser.open(f"file://{f.name}")
        else:
            messagebox.showwarning("预览", "当前没有内容可预览")

    def show_help(self):
        """显示帮助信息"""
        help_text = """Markdown快速参考：
        # 标题1
        ## 标题2
        
        **粗体**
        *斜体*  
        ~~删除线~~  
        `内联代码`  
        **_粗斜体组合_**  
        ==高亮文本==
        
        - 无序列表项
        * 另一种无序列表
        1. 有序列表项
        - [x] 任务列表（已完成）
        - [ ] 任务列表（未完成）
        
        [文本链接](https://example.com)  
        <https://自动链接.com>  
        ![图片描述](image.jpg)  
        [引用式链接][1]
        [1]: https://example.com
        
        ```python
        # 代码块（指定语言）
        print("Hello World")
        ```
        
        > 块引用
        >> 嵌套引用
        脚注示例[^1]
        [^1]: 这里是脚注内容
        
        表格示例：
        | 左对齐 | 居中对齐 | 右对齐 |
        | :----- | :------: | -----: |
        | 单元格 |  单元格  | 单元格 |
        """
        top = tk.Toplevel()
        top.title("帮助")
        tk.Label(top, text=help_text, justify=tk.LEFT).pack(padx=10, pady=10)

    def show_about(self):
        """显示关于信息"""
        about_text = """
        Py-Notebook 
        开发者：HelloWorld05
        版本：v1.0
        功能：支持Markdown的笔记本程序，提供文件夹管理、笔记编辑和实时预览功能。"""
        top = tk.Toplevel()
        top.title("关于")
        tk.Label(top, text=about_text, justify=tk.LEFT).pack(padx=10, pady=10)

if __name__ == "__main__":
    app = NotebookApp()
    app.root.mainloop()
