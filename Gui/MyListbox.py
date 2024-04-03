from tkinter import Listbox
from tkinter.filedialog import askopenfilenames
from Process.MySignal import signal1
import os

class MyListbox(Listbox):
    def __init__(self,master):
        super().__init__(master)
        self.bind('<Button-1>', self.open_file_dialog)
        self.bind('<BackSpace>', self.delete_selected_item)
        self.bind('<<ListboxSelect>>', 
                  func=lambda _:signal1.emit("Current selected item: "+self.get(self.curselection())))
        
        self.selection_set(0)
        # 在Listbox中添加提示文本
        self.insert('end', '点击选择或者拖入文件')
    def clear(self):
        self.delete(0,'end')
        self.insert('end', '点击选择或者拖入文件')
    def selection_set(self, first: str | int, last: str | int | None = None) -> None:
        if self.get(0) == '点击选择或者拖入文件':
            return
        return super().selection_set(first, last)
    def drop(self,filepath):
        self.delete(0)
        for path in filepath:
            try:
                path=str(path,encoding='utf-8')
            except UnicodeDecodeError:
                signal1.emit("The file path contains illegal characters!,please try rename the file and try again!")
            
            self.insert('end', path)
            signal1.emit("File imported: "+path)

    def open_file_dialog(self, event=None):
        if self.size() == 1 and self.get(0) == '点击选择或者拖入文件':
            # 打开文件选择对话框并获取选定的文件路径
            filepath = askopenfilenames()
            # 如果用户取消选择文件，则返回
            if not filepath:
                return
            # 删除提示文本
            self.delete(0)

            # 将文件路径添加到Listbox组件中
            for path in filepath:
                self.insert('end', path)
                signal1.emit("File imported: "+path)

    def delete_selected_item(self, event=None):
        # 获取选中的元素的索引
        selected = self.curselection()

        # 删除选中的元素
        if selected:
            self.delete(selected)
        # 如果Listbox中没有元素，则添加提示文本
        if self.size() == 0:
            self.insert('end', '点击选择或者拖入文件')