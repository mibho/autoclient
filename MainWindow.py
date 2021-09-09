from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QGridLayout, QMainWindow, QFileDialog, QApplication, QPushButton, QWidget)
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        startAQbtn = QPushButton('Start AQ', self)
        startAQbtn.setCheckable(True)
    
    def toggle(self, pressed):
        inputsrc = self.sender()


def main():

    app = QApplication([])
    tetris = MainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()