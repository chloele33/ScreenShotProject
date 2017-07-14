# -*- coding: utf-8 -*-
import sys,time,os, datetime
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from menu import Menu
from Tkconstants import SOLID
from rectLabel import RectLabel
from Background import Background


class CutImage(QWidget):
    def __init__(self):
        super(CutImage,self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(0.01)

        #set background
        self.background = Background()
        self.background.showFullScreen()
        #set initial screen shot
        self.cutok=False
        self.fullPixmap=QPixmap.grabWindow(QApplication.desktop().winId())
        self.setMouseTracking(True)
        # Create rectLabel
        self.rectLabel=QLabel(self)
        self.rectLabel.hide()
        self.rectLabel.setMouseTracking(True)
        # Create second layer of rectLabel
        self.opaqueRectLabel = RectLabel()
        self.opaqueRectLabel.showFullScreen()
        # Create buttons for dragging
        self.topRightResize = QPushButton()
        self.topLeftResize = QPushButton()
        self.bottomRightResize = QPushButton()
        self.bottomLeftResize = QPushButton()
        self.topRightResize.setObjectName("resizeBtn")
        self.topLeftResize.setObjectName("resizeBtn")
        self.bottomRightResize.setObjectName("resizeBtn")
        self.bottomLeftResize.setObjectName("resizeBtn")
        # Create selectRect
        self.selectRect=QRect()
        # Boolean to see if selection exists
        self.selectionExists = False
        # Booleans for resizing
        self.initialShiftWindow = True
        self.topRightResizeOK = False
        self.topLeftResizeOK = False
        self.bottomRightResizeOK = False
        self.bottomLeftResizeOK = False
        self.topResizeOK = False
        self.leftResizeOK = False
        self.bottomResizeOK = False
        self.rightResizeOK = False
        # Booleans for drawing arrows
        self.drawArrowOK = False
        self.drawingArrow = False
        self.drawArrowHead = False
        self.allArrows = []
        # Booleans for underlining
        self.underlineOK = False
        self.underlining = False
        self.underlineEnd = False
        self.allLines = []
        #List for all drawings
        self.allDrawings = []
        self.deleted = []
        # Create path and file name
        self.savePath = ""
        self.saveName = ""
        # Create helpWidget
        helpText=u'''
    ��קѡ��
    ˫������
    �Ҽ��˳�
        '''
        self.helpWin=QLabel()
        self.helpWin.setText(helpText)
        self.helpWin.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.helpWin.setFixedSize(QSize(96,87))
        self.helpWin.setStyleSheet("background:rgb(69,119,170)")
        screen=QDesktopWidget().screenGeometry()
        screenWidth=screen.width()
        screenHeight=screen.height()
        helpWin=self.helpWin.geometry()
        helpWidth=helpWin.width()
        helpHeight=helpWin.height()
        self.helpWin.move(screenWidth-helpWidth,0)
        self.helpWin.show()
        #menu widgets
        self.openMenuBtn = QPushButton("Menu")
        self.openMenuBtn.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.openMenuBtn.setObjectName("openMenuBtn")
        stylesheetFile=QFile("stylesheet.qss")
        stylesheetFile.open(QFile.ReadOnly)
        self.openMenuBtn.setStyleSheet(QLatin1String(stylesheetFile.readAll()))
        self.openMenuBtn.clicked.connect(self.openMenuFunc)
        self.menu = Menu()
        self.menu.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.menu.setMouseTracking(True)
        #menu button functions
        self.menu.arrowBtn.clicked.connect(self.arrowBtnFunc)
        self.menu.underlineBtn.clicked.connect(self.underlineBtnFunc)
        self.menu.undoBtn.clicked.connect(self.undoBtnFunc)
        self.menu.redoBtn.clicked.connect(self.redoBtnFunc)
        self.menu.saveBtn.clicked.connect(self.saveBtnFunc)
        #create painter
    def paintEvent(self,QPaintEvent):
        # Enable the paintEvent function
        super(CutImage,self).paintEvent(QPaintEvent)
        rectx=self.selectRect.x()
        recty=self.selectRect.y()
        rectWidth=self.selectRect.width()
        rectHeight=self.selectRect.height()
        rectPixmap=self.fullPixmap.copy(rectx,recty,rectWidth,rectHeight)
        self.rectLabel.setPixmap(rectPixmap)
        self.rectLabel.resize(self.selectRect.size())
        self.rectLabel.move(self.selectRect.topLeft())
        self.rectLabel.show()
        self.opaqueRectLabel.label.setPixmap(rectPixmap)
        self.opaqueRectLabel.label.resize(self.selectRect.size())
        self.opaqueRectLabel.label.move(self.selectRect.topLeft())
        self.opaqueRectLabel.label.show()
        self.openMenuBtn.move(QPoint(rectx, recty))
        painter = QPainter(self.opaqueRectLabel.label.pixmap())
        pen = QPen(QColor(255, 50, 50), 3, Qt.SolidLine, Qt.RoundCap)
        brush = QBrush()
        brush.setColor(QColor(255, 50, 50))
        brush.setStyle(Qt.SolidPattern)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)  
        for line in self.allLines:
            if line in self.allDrawings:
                painter.drawLine(line)
        for poly in self.allArrows:
            if poly in self.allDrawings:
                painter.setBrush(brush)
                painter.drawPolygon(poly)
        if self.drawingArrow or self.drawArrowHead:
            painter.setBrush(brush)
            arrowStartX = float(self.arrowStartPos.x()) - self.rectLabel.pos().x()
            arrowStartY = float(self.arrowStartPos.y()) - self.rectLabel.pos().y()
            arrowEndX = float(self.currentPos.x()) - self.rectLabel.pos().x()
            arrowEndY = float(self.currentPos.y()) - self.rectLabel.pos().y()
            currLine = QLineF(QPoint(arrowStartX, arrowStartY), QPoint(arrowEndX, arrowEndY))
            #calculate arrow head direction and draw arrow head
            unitVec = currLine.unitVector()
            unitVec.setLength(currLine.length() / 4.0) #length of the arrow head
            unitVec.translate(QPointF(currLine.dx() * 0.75, currLine.dy()* 0.75))
            normal = unitVec.normalVector() 
            normal.setLength(normal.length() * 0.5) #width of arrow head
            normal2 = normal.normalVector().normalVector() #Get the normal on the other side of the arrow
            normalHalf = unitVec.normalVector()
            normalHalf.setLength(normalHalf.length() * 0.2)
            normalHalf2 = normalHalf.normalVector().normalVector()
            p1 = unitVec.p2()
            p2 = normal.p2()
            p3 = normal2.p2()
            p4 = normalHalf.p2()
            p5 = normalHalf2.p2()
            currPoly  = QPolygonF([currLine.p1(), p4, p2, p1, p3, p5])
            painter.drawPolygon(currPoly)
            if self.drawArrowHead:
                self.allDrawings.append(currPoly)
                self.allArrows.append(currPoly)
                self.drawArrowHead = False
        elif self.underlining or self.underlineEnd:
            lineStartX = float(self.lineStartPos.x()) - self.rectLabel.pos().x()
            lineStartY = float(self.lineStartPos.y()) - self.rectLabel.pos().y()
            lineEndX = float(self.currentPos.x()) - self.rectLabel.pos().x()
            lineEndY = float(self.currentPos.y()) - self.rectLabel.pos().y()
            currLine = QLine(QPoint(lineStartX, lineStartY), QPoint(lineEndX, lineEndY))
            if self.underlineEnd:
                self.allDrawings.append(currLine)
                self.allLines.append(currLine)
                self.underlineEnd = False
            #calculate arrow head direction and draw arrow head
            painter.drawLine(currLine)
    def saveBtnFunc(self):
        #self.menu.hide()
        rectPixmap=self.opaqueRectLabel.label.pixmap()
        clipboard=QApplication.clipboard()
        mineDate=QMimeData()
        mineDate.setImageData(rectPixmap)
        clipboard.clear()
        clipboard.setMimeData(mineDate)
        date = datetime.datetime.now().date()
        nowTime = time.strftime("%H.%M.%S")
        name = "Screen Shot %d-%d-%d at %s %s" %(date.year, date.month, date.day, nowTime, time.strftime("%p"))
        name = QFileDialog.getSaveFileName(self.menu, caption="Please select a path",filter ="*.png;;*.xpm;;*.jpg",options=QFileDialog.ShowDirsOnly)
        rectPixmap.save(name,None,100)
        #self.menu.show()
    def undoBtnFunc(self):
        if not self.allDrawings:
            return
        self.deleted.append(self.allDrawings.pop())
    def redoBtnFunc(self):
        if not self.deleted:
            return
        self.allDrawings.append(self.deleted.pop())
    def underlineBtnFunc(self):
        self.drawArrowOK = False
        self.drawingArrow = False
        self.drawArrowHead = False
        self.underlineOK = True
    def arrowBtnFunc(self):
        self.underlineOK = False
        self.underlining = False
        self.underlineEnd = False
        self.drawArrowOK = True
    def openMenuFunc(self):
        self.menu.move(QPoint(self.selectRect.bottomLeft().x() + 5, self.selectRect.bottomLeft().y() - 60))
        self.menu.show()
    def mousePressEvent(self,event):
        if not self.cutok:
            self.helpWin.close()
            if event.button()==Qt.LeftButton:
                self.startPos=event.globalPos()
                self.startx=self.startPos.x()
                self.starty=self.startPos.y()
                self.selectRect.setTopLeft(self.startPos)
            elif event.button()==Qt.RightButton:
                QApplication.closeAllWindows()
                self.close()
        elif self.cutok:
            if event.button()==Qt.RightButton:
                self.drawArrowOK = False
                self.drawArrowHead = False
                self.underlineOK = False
                self.underlineEnd = False
                self.allLines = []
                self.allArrows = []
                self.allDrawings = []
                self.deleted = []
                self.openMenuBtn.hide()
                self.menu.hide()
                self.startPos=event.globalPos()
                self.startx=self.startPos.x()
                self.starty=self.startPos.y()
                self.selectRect.setTopLeft(self.startPos)
                self.selectRect.setSize(QSize(0,0))
                self.opaqueRectLabel.label.hide()
                self.rectLabel.hide()
                self.cutok=False
            elif event.button() == Qt.LeftButton:
                if self.drawArrowOK:
                    if self.rectLabel.underMouse():
                        self.drawingArrow = True
                        self.currentPos = event.globalPos()
                        self.arrowStartPos = event.globalPos()
                        self.drawArrowOK = False
                elif self.underlineOK:
                    if self.rectLabel.underMouse():
                        self.underlining = True
                        self.currentPos = event.globalPos()
                        self.lineStartPos = event.globalPos()
                        self.underlineOK = False
    def mouseMoveEvent(self,event):
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        if self.drawingArrow and event.buttons() == Qt.LeftButton:
            self.currentPos = event.globalPos()
        elif self.underlining and event.buttons() == Qt.LeftButton:
            self.currentPos = event.globalPos()
        if not self.cutok and event.buttons() == Qt.LeftButton:
            QApplication.setOverrideCursor(Qt.CrossCursor)
            curPos=event.globalPos()
            curx=curPos.x()
            cury=curPos.y()
            rectWidth=curx-self.startx
            rectHeight=cury-self.starty
            self.selectRect.setSize(QSize(rectWidth,rectHeight))
            if rectWidth < 0 or rectHeight < 0:
                return
            self.update()
            self.selectionExists = True;
            return
        #----------Resizing-----------------
        elif self.topResizeOK and event.buttons() == Qt.LeftButton:
            QApplication.setOverrideCursor(Qt.SizeVerCursor)
            prevx = self.selectRect.x()
            cury = event.globalPos().y()
            self.selectRect.setTopLeft(QPoint(prevx, cury))
            self.update()
            return
        elif self.bottomResizeOK and event.buttons() == Qt.LeftButton:
            QApplication.setOverrideCursor(Qt.SizeVerCursor)
            prevx = self.selectRect.x()
            cury = event.globalPos().y()
            self.selectRect.setBottomLeft(QPoint(prevx, cury))
            self.update()
            return
        elif self.rightResizeOK and event.buttons() == Qt.LeftButton:
            QApplication.setOverrideCursor(Qt.SizeHorCursor)
            prevy = self.selectRect.y()
            curx = event.globalPos().x()
            self.selectRect.setTopRight(QPoint(curx, prevy))
            self.update()
            return
        elif self.leftResizeOK and event.buttons() == Qt.LeftButton:
            QApplication.setOverrideCursor(Qt.SizeHorCursor)
            prevy = self.selectRect.y()
            curx = event.globalPos().x()
            self.selectRect.setTopLeft(QPoint(curx, prevy))
            self.update()
            return
        elif self.topLeftResizeOK and event.buttons() == Qt.LeftButton:
            QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
            curx = event.globalPos().x()
            cury = event.globalPos().y()
            self.selectRect.setTopLeft(QPoint(curx, cury))
            self.update()
            return
        elif self.topRightResizeOK and event.buttons() == Qt.LeftButton:
            QApplication.setOverrideCursor(Qt.SizeBDiagCursor)
            curx = event.globalPos().x()
            cury = event.globalPos().y()
            self.selectRect.setTopRight(QPoint(curx, cury))
            self.update()
            return
        elif self.bottomLeftResizeOK and event.buttons() == Qt.LeftButton:
            QApplication.setOverrideCursor(Qt.SizeBDiagCursor)
            curx = event.globalPos().x()
            cury = event.globalPos().y()
            self.selectRect.setBottomLeft(QPoint(curx, cury))
            self.update()
            return
        elif self.bottomRightResizeOK and event.buttons() == Qt.LeftButton:
            QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
            curx = event.globalPos().x()
            cury = event.globalPos().y()
            self.selectRect.setBottomRight(QPoint(curx, cury))
            self.update()
            return
        #---------Detect if Ready to Resize
        elif self.cutok:
            self.topRightResizeOK = False
            self.topLeftResizeOK = False
            self.bottomRightResizeOK = False
            self.bottomLeftResizeOK = False
            self.topResizeOK = False
            self.leftResizeOK = False
            self.bottomResizeOK = False
            self.rightResizeOK = False
            QApplication.setOverrideCursor(Qt.ArrowCursor)
#             if self.initialShiftWindow and self.rectLabel.underMouse():
#                 QApplication.setOverrideCursor(Qt.SizeAllCursor)
            curPos = event.globalPos()
            curx = curPos.x()
            cury = curPos.y()
            #top left corner
            rectTopLeftx = self.selectRect.topLeft().x()
            rectTopLefty = self.selectRect.topLeft().y()
            rectTopLeftxMax = rectTopLeftx + 10
            rectTopLeftxMin = rectTopLeftx - 10
            rectTopLeftyMax = rectTopLefty + 10
            rectTopLeftyMin = rectTopLefty - 10
            if curx < rectTopLeftxMax and curx > rectTopLeftxMin and cury < rectTopLeftyMax and cury > rectTopLeftyMin:
                QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
                self.topLeftResizeOK = True
                return
            #top right corner
            rectTopRightx = self.selectRect.topRight().x()
            rectTopRighty = self.selectRect.topRight().y()
            rectTopRightxMax = rectTopRightx + 10
            rectTopRightxMin = rectTopRightx - 10
            rectTopRightyMax = rectTopRighty + 10
            rectTopRightyMin = rectTopRighty - 10
            if curx < rectTopRightxMax and curx > rectTopRightxMin and cury < rectTopRightyMax and cury > rectTopRightyMin:
                QApplication.setOverrideCursor(Qt.SizeBDiagCursor)
                self.topRightResizeOK = True
                return
            #bottom left corner
            rectBottomLeftx = self.selectRect.bottomLeft().x()
            rectBottomLefty = self.selectRect.bottomLeft().y()
            rectBottomLeftxMax = rectBottomLeftx + 10
            rectBottomLeftxMin = rectBottomLeftx - 10
            rectBottomLeftyMax = rectBottomLefty + 10
            rectBottomLeftyMin = rectBottomLefty - 10
            if curx < rectBottomLeftxMax and curx > rectBottomLeftxMin and cury < rectBottomLeftyMax and cury > rectBottomLeftyMin:
                QApplication.setOverrideCursor(Qt.SizeBDiagCursor)
                self.bottomLeftResizeOK = True
                return
            #bottom right corner
            rectBottomRightx = self.selectRect.bottomRight().x()
            rectBottomRighty = self.selectRect.bottomRight().y()
            rectBottomRightxMax = rectBottomRightx + 10
            rectBottomRightxMin = rectBottomRightx - 10
            rectBottomRightyMax = rectBottomRighty + 10
            rectBottomRightyMin = rectBottomRighty - 10
            if curx < rectBottomRightxMax and curx > rectBottomRightxMin and cury < rectBottomRightyMax and cury > rectBottomRightyMin:
                QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
                self.bottomRightResizeOK = True
                return
            #top
            if curx < rectTopRightxMax and curx > rectTopLeftxMin and cury < rectTopRightyMax and cury > rectTopRightyMin:
                QApplication.setOverrideCursor(Qt.SizeVerCursor)
                self.topResizeOK = True
                return
            #right
            if curx < rectTopRightxMax and curx > rectTopRightxMin and cury > rectTopRightyMax and cury < rectBottomRightyMin:
                QApplication.setOverrideCursor(Qt.SizeHorCursor)
                self.rightResizeOK = True
                return
            #left
            if curx < rectTopLeftxMax and curx > rectTopLeftxMin and cury < rectBottomLeftyMax and cury > rectTopRightyMin:
                QApplication.setOverrideCursor(Qt.SizeHorCursor)
                self.leftResizeOK = True
                return
            #bottom
            if curx < rectBottomRightxMax and curx > rectBottomLeftxMin and cury < rectBottomRightyMax and cury > rectBottomRightyMin:
                QApplication.setOverrideCursor(Qt.SizeVerCursor)
                self.bottomResizeOK = True
                return
    def mouseReleaseEvent(self,event):
        #self.selectRect = self.selectRect.normalized()
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        if event.button()==Qt.LeftButton and self.selectionExists:
            self.cutok=True
            self.selectionExists = False
            self.openMenuBtn.show()
            self.openMenuFunc()
        if self.drawingArrow and self.rectLabel.underMouse():
            self.drawArrowOK = True
            self.drawingArrow = False
            self.drawArrowHead = True
        elif self.underlining and self.rectLabel.underMouse():
            self.underlineOK = True
            self.underlining = False
            self.underlineEnd = True
    def mouseDoubleClickEvent(self,event):
        if self.cutok:
            rectPixmap=self.opaqueRectLabel.label.pixmap()
            clipboard=QApplication.clipboard()
            mineDate=QMimeData()
            mineDate.setImageData(rectPixmap)
            clipboard.clear()
            clipboard.setMimeData(mineDate)
            date = datetime.datetime.now().date()
            nowTime = time.strftime("%H.%M.%S")
            name = "Screen Shot %d-%d-%d at %s %s" %(date.year, date.month, date.day, nowTime, time.strftime("%p"))
            #get path to save the file at
            if not self.savePath:
                self.openMenuBtn.hide()
                tarPath = QFileDialog.getExistingDirectory(self.menu, caption="Please select a path",options=QFileDialog.ShowDirsOnly)
                self.savePath = tarPath
            if not tarPath:
                return
            rectPixmap.save(tarPath + "\%s.png" % (name),None,100)
            QApplication.closeAllWindows()
            self.close()
    def keyPressEvent(self,event):
        if event.key()==Qt.Key_Escape:
            QApplication.closeAllWindows()
            self.close()
            
        
        
if __name__ == "__main__":
    app=QApplication(sys.argv)
    cutimage=CutImage()
    cutimage.showFullScreen()
    sys.exit(app.exec_())