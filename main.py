import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QDialog, QHBoxLayout)
from response import ui

class ApplicationWindow(QDialog):
    def __init__(self, ):
        super().__init__()
        self.setupUi()
        self.initUI()


    def setupUi(self):
        self.layout = QHBoxLayout()
        self.layout.addWidget(ui.stackResponse())
        self.setLayout(self.layout)

    
    def initUI(self):
        self.setWindowTitle("Control Theory Plot")
        self.resize(700, 850)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = ApplicationWindow()
    main.show()
    sys.exit(app.exec_())