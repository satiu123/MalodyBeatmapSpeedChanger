from Process.MySignal import signal1,signal2
from Gui.MyText import MyText
from Gui.MyListbox import MyListbox
from Gui.SelectWindow import SelectWindow
from main import addQueue,startQueue
from ttkbootstrap import Window, Button,Entry,Frame,PhotoImage
import windnd,os,threading
class MainWindow(Window):
    def __init__(self):
        super().__init__()
        self.rate_dict={} #record the rate of each beatmap
    
        self.title("SoundChanger ttk ver.")
        self.iconphoto(True, PhotoImage(file='assets/icon.png'))
        self.minsize(1000,800)
        self.setup()
        self.protocol("WM_DELETE_WINDOW", self.quit)
        signal1.connect(self.output_text.append)
        signal2.connect(self.openSelectWindow)
        for i in range(3):
            self.left_buttom.rowconfigure(i,weight=1)
            self.left_buttom.columnconfigure(i,weight=1)
    def setup(self):
        self.left=Frame(self)
        self.right=Frame(self)
        self.left_top=Frame(self.left)
        self.left_buttom=Frame(self.left)
        self.left.pack(side='left',fill='both',expand=True)
        self.right.pack(side='right',fill='both',expand=True)
        self.left_top.pack(side='top',fill='both',expand=True)
        self.left_buttom.pack(side='bottom',fill='both',expand=True)
        self.output_text=MyText(self.right)
        # 创建一个Entry组件用于输入
        self.rate_text=Entry(self.left_buttom)
        # 创建一个MyListbox组件
        
        self.my_listbox = MyListbox(self.left_top)
        # 为MyListbox组件绑定拖拽文件事件
        windnd.hook_dropfiles(self.my_listbox, func=self.my_listbox.drop)
        
        # 创建按钮
        self.clear_rate=Button(self.left_buttom,text='Clear Rate',style='Outline.TButton',command=lambda:self.rate_text.delete('0','end'))
        self.clear_input=Button(self.left_buttom,text='Clear Input',style='Outline.TButton',command=self.my_listbox.clear)
        self.clear_output=Button(self.left_buttom,text='Clear Output',style='Outline.TButton',command=self.output_text.clear)
        self.open_folder=Button(self.left_buttom,text="Open OutPutFolder",style='Outline.TButton',command=lambda:os.startfile("out"))
        self.add_queue=Button(self.left_buttom,text='Add Queue',style='Outline.TButton',command=self.add_to_queue)
        self.start_queue=Button(self.left_buttom,text='Start Queue',style='Outline.TButton',command=self.start_to_queue)
        # 设定位置
        self.output_text.pack(fill='both',expand=True)
        
        self.my_listbox.pack(fill='both',expand=True)
        
        self.clear_rate.grid(row=0,column=0,sticky="nsew")
        self.clear_input.grid(row=0,column=1,sticky="nsew")
        self.clear_output.grid(row=0,column=2,sticky="nsew")
        self.open_folder.grid(row=0,column=4,sticky="nsew")
        self.rate_text.grid(row=1,column=0,columnspan=6,sticky="nsew")
        self.add_queue.grid(row=2,column=0,columnspan=2,sticky="nesw")
        self.start_queue.grid(row=2,column=2,columnspan=4,sticky="nesw")
    
    def openSelectWindow(self,version:list,title:str):
        
        self.select_window = SelectWindow(self)
        self.select_window.version=version
        self.select_window.title(title)
        self.select_window.add_button(version)
        self.select_window.transient(self.master)

        self.select_window.mainloop()
    def add_to_queue(self):
        rate=self.rate_text.get()
        if rate=="":
            signal1.emit("Rate is empty!")
            return
        rate=list(map(float,rate.split(" ")))
        index=self.my_listbox.curselection()
        key=self.my_listbox.get(index)
        signal1.emit("Rate added: "+os.path.basename(key)+" "+str(rate))
        self.rate_dict[key]=rate
    
    def start_to_queue(self):
        self.output_text.clear()
        addQueue(self.rate_dict)
        self.rate_dict.clear()
        thread1=threading.Thread(target=startQueue)
        thread1.start()