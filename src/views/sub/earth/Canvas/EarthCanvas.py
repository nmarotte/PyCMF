from typing import TYPE_CHECKING

import PyQt5.QtWidgets as QtWidgets
from PyQt5 import QtGui

import views.earth_view as earth_view


class EarthCanvas(QtWidgets.QWidget):
    CANVAS_SIZE = (400, 400)  # W, H
    CLEAR_COLOR = QtGui.QColor("black")

    def __init__(self, parent: earth_view.EarthView = None):
        super().__init__(parent)
        self.setLayout(QtWidgets.QGridLayout())
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(*EarthCanvas.CANVAS_SIZE)
        self.label.setPixmap(canvas)
        self.layout().addWidget(self.label)

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        pen.setColor(self.parent().get_brush_color())
        pen.setWidth(self.parent().get_brush_width())
        painter.setPen(pen)
        painter.drawPoint(e.x(), e.y())
        painter.end()
        self.update()

    def clear(self):
        self.label.pixmap().fill(EarthCanvas.CLEAR_COLOR)
        self.update()