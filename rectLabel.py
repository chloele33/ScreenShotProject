# -*- coding: utf-8 -*-
import sys
import MySQLdb as ms
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from BaseWindow import MoveWidget
from roundButton import RoundButton

class RectLabel(QWidget):
    def __init__(self):
        super(RectLabel, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        #widget
        self.label = QLabel(self)
    def backBtnFunc(self):
        self.hide()
    def keyPressEvent(self,event):
        if event.key()==Qt.Key_Escape:
            self.close()

if __name__ == "__main__":
    app=QApplication(sys.argv)
    rectlabel=RectLabel()
    rectlabel.showNormal()
    sys.exit(app.exec_())