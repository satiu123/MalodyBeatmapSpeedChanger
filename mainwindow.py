from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QSplitter, QTextEdit,
                               QPushButton,QGridLayout,QToolTip)
from PySide6.QtCore import Qt
from PySide6.QtGui import  QIcon,QCursor
from Module.Gui.SelectWindow import SelectWindow
from Module.Process.map import info_signal
from main import getinfo_signal,addQueue,startQueue
import threading
from Module.Gui.MyListWidget import MyListWidget
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.rate_dict={}

        self.setWindowTitle("SoundChanger by satiu")
        self.setWindowIcon(QIcon("wife.jpg"))
        self.createInputAndOutputPart()
        self.unitUi()
        getinfo_signal.signal2.connect(self.openSelectWindow)
        info_signal.signal1.connect(self.outputInfo.append)
        self.resize(1000,600)  
    def createInputAndOutputPart(self):
        #right part
        self.outputInfo = QTextEdit()
        self.outputInfo.setPlaceholderText("There will be Output information")
        self.outputInfo.setReadOnly(True)
        #left part
        self.leftlayout=QGridLayout()
        #create a list widget
        self.listWidget = MyListWidget()
        self.listWidget.itemClicked.connect(slot=self.onItemSelected)
        self.widget=QWidget()
        self.widget.setLayout(self.leftlayout)

        self.rate_text=QTextEdit()
        self.rate_text.setPlaceholderText("Enter the rate of the sound file here,split by space eg:1.1 1.2")

        self.add_button=QPushButton("AddtoQueue")
        self.add_button.setFixedHeight(50)
        self.start_button=QPushButton("Start")
        self.start_button.setFixedHeight(50)
        self.clear_rate_button=QPushButton("Clear Rate")
        self.clear_input_button=QPushButton("Clear Input")
        self.clear_output_button=QPushButton("Clear Output")
        self.open_folder_button=QPushButton("Open Output Folder")

        self.add_button.clicked.connect(self.addQueue)
        self.clear_input_button.clicked.connect(self.listWidget.clear)
        self.clear_output_button.clicked.connect(self.outputInfo.clear)
        self.clear_rate_button.clicked.connect(self.rate_text.clear)
        self.start_button.clicked.connect(self.start)
        self.open_folder_button.clicked.connect(self.openFolder)

        self.leftlayout.setSpacing(0)
        self.leftlayout.setHorizontalSpacing(0)
        self.leftlayout.setVerticalSpacing(0)
        self.leftlayout.setContentsMargins(0,0,0,0)
        self.leftlayout.addWidget(self.clear_rate_button,0,0)
        self.leftlayout.addWidget(self.clear_input_button,0,1)
        self.leftlayout.addWidget(self.clear_output_button,0,2)
        self.leftlayout.addWidget(self.rate_text,1,0,3,0)
        self.leftlayout.addWidget(self.add_button,4,0,1,3)
        self.leftlayout.addWidget(self.start_button,4,3,1,1)
        self.leftlayout.addWidget(self.open_folder_button,0,3)

        self.leftsplitter=QSplitter(Qt.Orientation.Vertical)
        self.leftsplitter.addWidget(self.listWidget)
        self.leftsplitter.addWidget(self.widget)
        self.leftsplitter.setStretchFactor(0, 6)
        self.leftsplitter.setStretchFactor(1, 4)
    def unitUi(self):
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.leftsplitter)
        self.splitter.addWidget(self.outputInfo)
        self.splitter.setStretchFactor(0, 4)
        self.splitter.setStretchFactor(1, 6)
        self.setCentralWidget(self.splitter)
    def show_tooltip(self,text):
        QToolTip.showText(QCursor.pos(), text)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            self.listWidget.addItem(url.toLocalFile())
            self.outputInfo.append(f"File imported: {url.toLocalFile()}")

    def onItemSelected(self):
        item = self.listWidget.currentItem()
        if item is not None:
            self.outputInfo.append(f"Current selected item: {item.text()}")
        else:
            self.outputInfo.append(f"No item selected")

    def openSelectWindow(self,version,title):
        self.select_window = SelectWindow(self)
        self.select_window.version=version
        self.select_window.setWindowTitle(title)
        self.select_window.creatButtom()
        self.select_window.show()

    def addQueue(self):
        if self.rate_text.toPlainText()!='':
            self.rate_dict[self.listWidget.currentItem().text()]=list(map(float,self.rate_text.toPlainText().split(" ")))
            self.show_tooltip("Add to queue successfully!")
        else:
            self.show_tooltip("Please enter the rate!")
        
    def start(self):
        self.outputInfo.clear()
        addQueue(self.rate_dict)
        self.rate_dict.clear()
        thread1=threading.Thread(target=startQueue)
        thread1.start()
    def openFolder(self):
        import os
        os.startfile("out")
if __name__ == "__main__":
    app = QApplication([])
    w=MainWindow()
    w.show()
    app.exec()

