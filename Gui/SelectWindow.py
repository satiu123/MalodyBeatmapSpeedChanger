from ttkbootstrap import Window,Button,Toplevel
import main
class SelectWindow(Window):
    def __init__(self,master):
        super().__init__(master)
        self.version:list=[]
        self.minsize(200,200)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    def select(self,button):
        main.version = button["text"]
        main.user_has_chosen =True
        main.stop_thread=False
        self.destroy()
    
    def add_button(self, version):
        for v in version:
            button = Button(self, text=v)
            button.pack(fill='both', expand=True)
            button['command'] = lambda button=button: self.select(button)

    def on_close(self):
        if not main.user_has_chosen:
            main.stop_thread=True
        self.destroy()