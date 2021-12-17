import PyQt5.QtWidgets as QtWidgets
from PyQt5 import QtGui

import a_views.earth_view as EarthView
from constants import CANVAS_SIZE


class EarthCanvas(QtWidgets.QWidget):
    CLEAR_COLOR = QtGui.QColor("black")

    def __init__(self, controller: "EarthView" = None):
        self.controller = controller
        super().__init__()
        self.setLayout(QtWidgets.QGridLayout())
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(*CANVAS_SIZE)
        self.label.setPixmap(canvas)
        self.layout().addWidget(self.label)

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        brush_color = self.controller.get_brush_color()
        if not brush_color:
            return
        pen.setColor(brush_color)
        pen.setWidth(self.controller.get_brush_width())
        painter.setPen(pen)
        painter.drawPoint(e.x(), e.y())
        painter.end()
        self.update()

    def clear(self):
        self.label.pixmap().fill(EarthCanvas.CLEAR_COLOR)
        self.update()
