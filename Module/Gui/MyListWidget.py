from PySide6.QtWidgets import QListWidget, QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
class MyListWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.count() == 0:
            painter = QPainter(self.viewport())
            painter.setPen(QColor(128, 128, 128))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No files. Click to open file dialog or Drag files here.")
    def mousePressEvent(self, event):
        if self.count() == 0:
            file_dialog = QFileDialog(self)
            file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)  # 设置为可以选择多个文件
            if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
                files = file_dialog.selectedFiles()
                self.addItems(files)
                #获取父窗口
                for file in files:
                    self.window().outputInfo.append(f"File imported: {file}") #type:ignore
        else:
            super().mousePressEvent(event)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Backspace:
            # 删除当前选中的项目
            current_item = self.currentItem()
            if current_item is not None:
                row = self.row(current_item)
                item = self.takeItem(row)
                del item
        else:
            super().keyPressEvent(event)

