from PySide6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton
from PySide6.QtGui import QCloseEvent
import main
class SelectWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.version:list=[]
        self.my_layout = QGridLayout(self)
        self.my_layout.addWidget(QLabel("Select the version"))
        self.setBaseSize(250,400)
    def select(self):
        main.version = self.sender().text() #type:ignore
        main.user_has_chosen =True
        main.stop_thread=False
        self.close()
    def creatButtom(self):
        for i in range(len(self.version)):
            button=QPushButton(self.version[i])
            button.clicked.connect(self.select)
            self.layout().addWidget(button)
    def closeEvent(self, arg__1: QCloseEvent) -> None:
        if not main.user_has_chosen:
            main.stop_thread=True
        return super().closeEvent(arg__1)

