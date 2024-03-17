from PySide6.QtCore import QObject, Signal
#自定义信号类
class MySignal(QObject):
    
    #向文本框传递文本的信号
    signal1 = Signal(object) 

    #传递版本和标题的信号
    signal2 = Signal(object,str)
