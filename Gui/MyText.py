from ttkbootstrap import ScrolledText
class MyText(ScrolledText):
    def __init__(self,master=None):
        super().__init__(master)
    def append(self,text):
        self.config(state='normal')
        self.insert('end',text+'\n')
        self.config(state='disabled')
    def clear(self):
        self.config(state='normal')
        self.delete('1.0','end')
        self.config(state='disabled')
