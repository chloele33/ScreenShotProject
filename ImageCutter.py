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
        self.resizeOK = False
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
        # Booleans for drawing
        self.drawOK = False
        self.drawing = False
        self.drawingEnd = False
        self.drawLines = []
        self.tempDrawLines = []
        self.destination = None
        #List for all drawings
        self.allDrawings = []
        self.deleted = []
        # Create path and file name
        self.savePath = ""
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
        self.openMenuBtn.setAttribute(Qt.WA_TranslucentBackground)
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
        self.menu.drawBtn.clicked.connect(self.drawBtnFunc)
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
        for draw in self.drawLines:
            if draw in self.allDrawings:
                for miniLine in draw:
                    painter.drawLines(miniLine)
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
            normal.setLength(normal.length() * 0.4) #width of arrow head
            normal2 = normal.normalVector().normalVector() #Get the normal on the other side of the arrow
            normalHalf = unitVec.normalVector()
            normalHalf.setLength(normalHalf.length() * 0.12)
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
        elif self.drawing or self.drawingEnd:
            line=QLine(QPoint(0,0),QPoint(self.width(),self.height()))
            if self.destination:
                for line in self.tempDrawLines:
                    painter.drawLine(line)
            if self.drawingEnd:
                self.drawLines.append(self.tempDrawLines)
                self.allDrawings.append(self.tempDrawLines)
                self.tempDrawLines = []
                self.drawingEnd = False
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
        try: 
            with open('pathLog.txt','r') as txtFile:
                curPath = txtFile.readline()
        except:
            with open('pathLog.txt','w+') as txtFile:
                curPath = txtFile.readline()
        name = QFileDialog.getSaveFileName(self.menu, caption="Please select a path",directory = curPath, filter ="*.png;;*.xpm;;*.jpg",options=QFileDialog.ShowDirsOnly)
        path = os.path.split(unicode(name))[0]
        if path:
            with open('pathLog.txt','w') as txtFile:
                txtFile.writelines(path)
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
    def drawBtnFunc(self):
        self.drawArrowOK = False
        self.drawingArrow = False
        self.drawArrowHead = False
        self.underlineOK = False
        self.underlining = False
        self.underlineEnd = False
        self.resizeOK = False
        self.initialShiftWindow = False
        self.underlineOK = False
        self.drawOK = True
    def underlineBtnFunc(self):
        self.drawArrowOK = False
        self.drawingArrow = False
        self.drawArrowHead = False
        self.resizeOK = False
        self.initialShiftWindow = False
        self.drawOK = False
        self.drawing = False
        self.drawingEnd = False
        self.underlineOK = True
    def arrowBtnFunc(self):
        self.underlineOK = False
        self.underlining = False
        self.underlineEnd = False
        self.initialShiftWindow = False
        self.resizeOK = False
        self.drawOK = False
        self.drawing = False
        self.drawingEnd = False
        self.drawArrowOK = True
    def openMenuFunc(self):
        if (self.height() - self.selectRect.bottomLeft().y()) < 50:
            self.menu.move(QPoint(self.selectRect.bottomLeft().x(), self.selectRect.bottomLeft().y() - 40)) 
        else:
            self.menu.move(QPoint(self.selectRect.bottomLeft().x(), self.selectRect.bottomLeft().y() + 12))
        self.menu.show()
    def mousePressEvent(self,event):
        if not self.cutok:
            self.helpWin.close()
            if event.button()==Qt.LeftButton:
                self.startPos=event.globalPos()
                self.startx=self.startPos.x()
                self.starty=self.startPos.y()
                self.selectRect.setTopLeft(self.startPos)
                self.selectionExists = True
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
                self.drawLines = []
                self.tempDrawLines = []
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
                if self.resizeOK:
                    self.initialStartX = float(event.globalPos().x())
                    self.initialStartY = float(event.globalPos().y())
                if self.drawArrowOK:
                    if self.rectLabel.underMouse():
                        self.drawingArrow = True
                        self.currentPos = event.globalPos()
                        self.arrowStartPos = event.globalPos()
                        self.drawArrowOK = False
                elif self.drawOK:
                    if self.rectLabel.underMouse():
                        self.drawing = True
                        self.currentPos = event.globalPos()
                        self.drawStartPos = event.globalPos()
                        self.origin = event.globalPos()
                        self.drawOK = False 
                elif self.underlineOK:
                    if self.rectLabel.underMouse():
                        self.underlining = True
                        self.currentPos = event.globalPos()
                        self.lineStartPos = event.globalPos()
                        self.underlineOK = False
    def mouseMoveEvent(self,event):
        if not self.cutok:
            QApplication.setOverrideCursor(Qt.CrossCursor)
        else:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
        if self.drawingArrow and event.buttons() == Qt.LeftButton:
            self.currentPos = event.globalPos()
        elif self.drawing and event.buttons() == Qt.LeftButton:
            self.destination=event.globalPos()
            lineStartX = float(self.currentPos.x()) - self.rectLabel.pos().x()
            lineStartY = float(self.currentPos.y()) - self.rectLabel.pos().y()
            lineEndX = float(self.destination.x()) - self.rectLabel.pos().x()
            lineEndY = float(self.destination.y()) - self.rectLabel.pos().y()
            currLine = QLine(QPoint(lineStartX, lineStartY), QPoint(lineEndX, lineEndY))
            self.tempDrawLines.append(currLine)
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
            self.menu.hide()
            QApplication.setOverrideCursor(Qt.SizeVerCursor)
            prevx = self.selectRect.x()
            cury = event.globalPos().y()
            self.selectRect.setTopLeft(QPoint(prevx, cury))
            self.update()
            return
        elif self.bottomResizeOK and event.buttons() == Qt.LeftButton:
            self.menu.hide()
            QApplication.setOverrideCursor(Qt.SizeVerCursor)
            prevx = self.selectRect.x()
            cury = event.globalPos().y()
            self.selectRect.setBottomLeft(QPoint(prevx, cury))
            self.update()
            return
        elif self.rightResizeOK and event.buttons() == Qt.LeftButton:
            self.menu.hide()
            QApplication.setOverrideCursor(Qt.SizeHorCursor)
            prevy = self.selectRect.y()
            curx = event.globalPos().x()
            self.selectRect.setTopRight(QPoint(curx, prevy))
            self.update()
            return
        elif self.leftResizeOK and event.buttons() == Qt.LeftButton:
            self.menu.hide()
            QApplication.setOverrideCursor(Qt.SizeHorCursor)
            prevy = self.selectRect.y()
            curx = event.globalPos().x()
            self.selectRect.setTopLeft(QPoint(curx, prevy))
            self.update()
            return
        elif self.topLeftResizeOK and event.buttons() == Qt.LeftButton:
            self.menu.hide()
            QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
            curx = event.globalPos().x()
            cury = event.globalPos().y()
            self.selectRect.setTopLeft(QPoint(curx, cury))
            self.update()
            return
        elif self.topRightResizeOK and event.buttons() == Qt.LeftButton:
            self.menu.hide()
            QApplication.setOverrideCursor(Qt.SizeBDiagCursor)
            curx = event.globalPos().x()
            cury = event.globalPos().y()
            self.selectRect.setTopRight(QPoint(curx, cury))
            self.update()
            return
        elif self.bottomLeftResizeOK and event.buttons() == Qt.LeftButton:
            self.menu.hide()
            QApplication.setOverrideCursor(Qt.SizeBDiagCursor)
            curx = event.globalPos().x()
            cury = event.globalPos().y()
            self.selectRect.setBottomLeft(QPoint(curx, cury))
            self.update()
            return
        elif self.bottomRightResizeOK and event.buttons() == Qt.LeftButton:
            self.menu.hide()
            QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
            curx = event.globalPos().x()
            cury = event.globalPos().y()
            self.selectRect.setBottomRight(QPoint(curx, cury))
            self.update()
            return
        elif self.initialShiftWindow and event.buttons() == Qt.LeftButton and self.rectLabel.underMouse():
            self.menu.hide()
            QApplication.setOverrideCursor(Qt.SizeAllCursor)
            curx = float(event.globalPos().x())
            cury = float(event.globalPos().y())
            xDiff = float(self.initialStartX) - float(curx)
            yDiff = float(self.initialStartY) - float(cury)
            if (self.selectRect.x() - xDiff) < 0 or (self.selectRect.y() - yDiff) < 0:
                return
            self.selectRect.moveTo(QPoint(self.selectRect.x() - xDiff, self.selectRect.y() - yDiff))
            self.initialStartX = curx
            self.initialStartY = cury
            self.update()
            return
        #---------Detect if Ready to Resize
        elif self.cutok:
            if not self.resizeOK:
                QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.topRightResizeOK = False
            self.topLeftResizeOK = False
            self.bottomRightResizeOK = False
            self.bottomLeftResizeOK = False
            self.topResizeOK = False
            self.leftResizeOK = False
            self.bottomResizeOK = False
            self.rightResizeOK = False
            if self.resizeOK:
    #             if self.initialShiftWindow and self.rectLabel.underMouse():
    #                 QApplication.setOverrideCursor(Qt.SizeAllCursor)
                curPos = event.globalPos()
                curx = curPos.x()
                cury = curPos.y()
                #top left corner
                rectTopLeftx = self.selectRect.topLeft().x()
                rectTopLefty = self.selectRect.topLeft().y()
                rectTopLeftxMax = rectTopLeftx + 8
                rectTopLeftxMin = rectTopLeftx - 8
                rectTopLeftyMax = rectTopLefty + 8
                rectTopLeftyMin = rectTopLefty - 8
                if curx < rectTopLeftxMax and curx > rectTopLeftxMin and cury < rectTopLeftyMax and cury > rectTopLeftyMin:
                    QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
                    self.topLeftResizeOK = True
                    return
                #top right corner
                rectTopRightx = self.selectRect.topRight().x()
                rectTopRighty = self.selectRect.topRight().y()
                rectTopRightxMax = rectTopRightx + 8
                rectTopRightxMin = rectTopRightx - 8
                rectTopRightyMax = rectTopRighty + 8
                rectTopRightyMin = rectTopRighty - 8
                if curx < rectTopRightxMax and curx > rectTopRightxMin and cury < rectTopRightyMax and cury > rectTopRightyMin:
                    QApplication.setOverrideCursor(Qt.SizeBDiagCursor)
                    self.topRightResizeOK = True
                    return
                #bottom left corner
                rectBottomLeftx = self.selectRect.bottomLeft().x()
                rectBottomLefty = self.selectRect.bottomLeft().y()
                rectBottomLeftxMax = rectBottomLeftx + 8
                rectBottomLeftxMin = rectBottomLeftx - 8
                rectBottomLeftyMax = rectBottomLefty + 8
                rectBottomLeftyMin = rectBottomLefty - 8
                if curx < rectBottomLeftxMax and curx > rectBottomLeftxMin and cury < rectBottomLeftyMax and cury > rectBottomLeftyMin:
                    QApplication.setOverrideCursor(Qt.SizeBDiagCursor)
                    self.bottomLeftResizeOK = True
                    return
                #bottom right corner
                rectBottomRightx = self.selectRect.bottomRight().x()
                rectBottomRighty = self.selectRect.bottomRight().y()
                rectBottomRightxMax = rectBottomRightx + 8
                rectBottomRightxMin = rectBottomRightx - 8
                rectBottomRightyMax = rectBottomRighty + 8
                rectBottomRightyMin = rectBottomRighty - 8
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
                #Center
                if self.rectLabel.underMouse():
                    QApplication.setOverrideCursor(Qt.SizeAllCursor)
                    self.initialShiftWindow = True
    def mouseReleaseEvent(self,event):
        #self.selectRect = self.selectRect.normalized()
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        if event.button()==Qt.LeftButton and self.selectionExists:
            self.resizeOK = True
            self.cutok=True
            self.selectionExists = False
            self.openMenuBtn.show()
            self.openMenuFunc()
        if event.button()==Qt.LeftButton and self.resizeOK:
            self.openMenuFunc()
        if self.drawingArrow and self.rectLabel.underMouse():
            self.drawArrowOK = True
            self.drawingArrow = False
            self.drawArrowHead = True
        elif self.drawing and self.rectLabel.underMouse():
            self.drawOK = True
            self.drawing = False
            self.drawingEnd = True
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
            #try to get path from previous log
            try:
                with open('pathLog.txt','r') as txtFile:
                    self.savePath = txtFile.readline()
                    print self.savePath
            except:
                with open('pathLog.txt','w+') as txtFile:
                    self.savePath = txtFile.readline()
            #get path to save the file at
            if not self.savePath:
                self.openMenuBtn.hide()
                tarPath = QFileDialog.getExistingDirectory(self.menu, caption="Please select a path",options=QFileDialog.ShowDirsOnly)
                self.savePath = tarPath
                with open('pathLog.txt','w') as txtFile:
                    txtFile.writelines(tarPath)
            if not self.savePath:
                return
            rectPixmap.save(self.savePath + "\%s.png" % (name),None,100)
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