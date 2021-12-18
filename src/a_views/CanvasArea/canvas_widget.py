from typing import TYPE_CHECKING

from PyQt5 import QtWidgets, QtGui

from constants import CANVAS_SIZE
if TYPE_CHECKING:
    from controller.CanvasArea.subcontrollers.canvas_controller import CanvasController


class CanvasWidget(QtWidgets.QLabel):
    CLEAR_COLOR = QtGui.QColor("black")

    def __init__(self, controller: "CanvasController"):
        self.controller = controller
        super().__init__()
        self.setPixmap(QtGui.QPixmap(*CANVAS_SIZE))

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):
        painter = QtGui.QPainter(self.pixmap())
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
        self.pixmap().fill(CanvasWidget.CLEAR_COLOR)
        self.update()
