# -*- coding: utf-8 -*-
import sys
import MySQLdb as ms
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from BaseWindow import MoveWidget
from roundButton import RoundButton

class Background(QWidget):
    def __init__(self):
        super(Background, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(0.2)
        self.setStyleSheet("background:rgb(0,0,50)")
        #widget
        self.label = QLabel(self)
    def backBtnFunc(self):
        self.hide()
    def keyPressEvent(self,event):
        if event.key()==Qt.Key_Escape:
            self.close()

if __name__ == "__main__":
    app=QApplication(sys.argv)
    background=Background()
    background.showNormal()
    sys.exit(app.exec_())