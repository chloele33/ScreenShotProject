# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class RoundButton(QPushButton):
    def __init__(self,normalIcon,hoverIcon,parent=None):
        super(RoundButton,self).__init__(parent)
        self.normalIcon=normalIcon
        self.hoverIcon=hoverIcon
        self.hovered=False
        self.pressed=False
        self.setIconSize(QSize(15, 15))
        self.setFixedSize(QSize(18, 18))

        
    def paintEvent(self,event):
        painter=QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        buttonRect=QRect(self.geometry())
        painter.setPen(QPen(QBrush(Qt.red),2.0))
        if self.isEnabled():
            if (self.pressed==False and self.hovered==False):
                iconSize=self.iconSize()
                iconPosition=self.calculateIconPosition(buttonRect,iconSize)
                painter.setOpacity(1.0)
                painter.drawPixmap(iconPosition, QPixmap(QIcon(self.normalIcon).pixmap(iconSize)))
            elif (self.hovered==True or self.pressed==True):
                iconSize=self.iconSize()
                iconPosition=self.calculateIconPosition(buttonRect,iconSize)
                painter.setOpacity(1.0)
                painter.drawPixmap(iconPosition,QPixmap(QIcon(self.hoverIcon).pixmap(iconSize)))
        else:
            iconSize=self.iconSize()
            iconPosition=self.calculateIconPosition(buttonRect,iconSize)
            painter.setOpacity(1.0)
            painter.drawPixmap(iconPosition, QPixmap(QIcon(self.normalIcon).pixmap(iconSize)))
    def enterEvent(self,event):
        self.hovered=True
        self.repaint()
    def leaveEvent(self,event):
        self.hovered=False
        self.repaint()
    def calculateIconPosition(self,buttonRect,iconSize):
        x=(buttonRect.width()/2)-(iconSize.width()/2)
        y=(buttonRect.height()/2)-(iconSize.height()/2)
        width=iconSize.width()
        height=iconSize.height()
        iconPosition=QRect()
        iconPosition.setX(x)
        iconPosition.setY(y)
        iconPosition.setWidth(width)
        iconPosition.setHeight(height)
        return iconPosition

if __name__=='__main__':
    import sys
    app=QApplication(sys.argv)
    aboutUS=RoundButton("close.png","close_hover.png")
    aboutUS.showNormal()
    sys.exit(app.exec_())