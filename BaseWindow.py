# -*- coding: utf-8 -*-
import sys
import MySQLdb as ms
from PyQt4.QtCore import *
from PyQt4.QtGui import *

PADDING=4
sys.setrecursionlimit(10000)
class MoveWidget(QWidget):
    def __init__(self):
        super(MoveWidget,self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        # Load styleSheet
        stylesheetFile=QFile("stylesheet.qss")
        stylesheetFile.open(QFile.ReadOnly)
        self.setStyleSheet(QLatin1String(stylesheetFile.readAll()))
    def mousePressEvent(self,event):
        if event.button()==Qt.LeftButton:
            self.dragPosition=event.globalPos()-self.frameGeometry().topLeft()
            event.accept()
    def mouseMoveEvent(self,event):
        if event.buttons()==Qt.LeftButton: 
            self.move(event.globalPos()-self.dragPosition)
            event.accept()
    def keyPressEvent(self,event):
        if event.key()==Qt.Key_Escape:
            self.closeButtonFunc()
    def closeButtonFunc(self):
        opacity_anim = QPropertyAnimation(self, "windowOpacity")
        opacity_anim.setStartValue(1.0)
        opacity_anim.setEndValue(0.0)
        opacity_anim.setDuration(620)
        opacity_anim_curve = QEasingCurve()
        opacity_anim_curve.setType(QEasingCurve.OutQuad)
        opacity_anim.setEasingCurve(opacity_anim_curve)
        
        size =  self.geometry()
        self.winWidth=size.width()
        self.winHeight=size.height()
        self.x, self.y, _, _ = size.getCoords()
        
        size_anim = QPropertyAnimation(self, "geometry")
        size_start = QRect(self.x, self.y, self.winWidth, self.winHeight)
        size_end   = QRect(self.x, self.y, self.winWidth, 0.0)
        size_anim.setStartValue(size_start)
        size_anim.setEndValue(size_end)
        size_anim.setDuration(620)      
        size_anim_curve = QEasingCurve()
        size_anim_curve.setType(QEasingCurve.OutQuad)
        size_anim.setEasingCurve(size_anim_curve)
        
        size_anim.start(QAbstractAnimation.DeleteWhenStopped)
        opacity_anim.start(QAbstractAnimation.DeleteWhenStopped)
    
        self._animation = QSequentialAnimationGroup()
        self._animation.addAnimation(opacity_anim)
        self._animation.addAnimation(size_anim)
        self._animation.finished.connect(self._animation.clear)
        self.setWindowOpacity(1.0)
        QTimer.singleShot(620, self.close)
        
if __name__=='__main__':
    app=QApplication(sys.argv)
    aboutUS=MoveWidget()
    aboutUS.showNormal()
    sys.exit(app.exec_())