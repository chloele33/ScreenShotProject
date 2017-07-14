# -*- coding: utf-8 -*-
import sys
import MySQLdb as ms
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from BaseWindow import MoveWidget
from roundButton import RoundButton

class Menu(MoveWidget):
    def __init__(self):
        super(Menu, self).__init__()
        self.resize(QSize(300, 35))
        self.setObjectName("Menu")
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.setCursor(Qt.PointingHandCursor)
        self.setWindowOpacity(0.9)
        #widget
        self.innerWidget = QWidget()
        self.innerWidget.setFixedSize(QSize(480, 35))
        self.backBtn = RoundButton("images/close.png", "images/closeHover.png")
        self.backBtn.setObjectName("backBtn")
        self.arrowBtn = RoundButton("images/redArrow.png", "images/redArrowHover.png")
        self.underlineBtn = RoundButton("images/underline.png", "images/underlineHover.png")
        self.underlineBtn.setIconSize(QSize(20, 20))
        self.undoBtn = RoundButton("images/back.png", "images/backHover.png")
        self.undoBtn.setIconSize(QSize(22, 22))
        self.redoBtn = RoundButton("images/redo.png", "images/redoHover.png")
        self.redoBtn.setIconSize(QSize(22, 22))
        self.saveBtn = RoundButton("images/save.png", "images/saveHover.png")
        self.drawBtn = RoundButton("images/draw.png", "images/drawHover.png")
        self.drawBtn.setIconSize(QSize(19, 19))
        # layout
        topBtnLayout = QHBoxLayout()
        topBtnLayout.addWidget(self.drawBtn)
        topBtnLayout.addWidget(self.underlineBtn)
        topBtnLayout.addWidget(self.arrowBtn)
        topBtnLayout.addWidget(self.undoBtn)
        topBtnLayout.addWidget(self.redoBtn)
        topBtnLayout.addWidget(self.saveBtn)
        topBtnLayout.addWidget(self.backBtn)
        topBtnLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topBtnLayout)
        #self.innerWidget.setLayout(mainLayout)
        #outerLayout = QVBoxLayout()
        #outerLayout.addWidget(self.innerWidget)
        self.setLayout(mainLayout)
        #stylesheet
        stylesheetFile=QFile("stylesheet.qss")
        stylesheetFile.open(QFile.ReadOnly)
        self.setStyleSheet(QLatin1String(stylesheetFile.readAll()))
        #function
        self.backBtn.clicked.connect(self.backBtnFunc)
    def backBtnFunc(self):
        self.hide()
    def keyPressEvent(self,event):
        if event.key()==Qt.Key_Escape:
            self.close()

if __name__ == "__main__":
    app=QApplication(sys.argv)
    menu=Menu()
    menu.showNormal()
    sys.exit(app.exec_())