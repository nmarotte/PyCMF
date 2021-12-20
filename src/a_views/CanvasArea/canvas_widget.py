from typing import TYPE_CHECKING

from PyQt5 import QtWidgets, QtGui

from constants import CANVAS_SIZE
from exceptions import ExceptionToProcess, CannotPaintNow, NoComponentBrushSelected
from other.utils import color_from_ratio

if TYPE_CHECKING:
    from controller.CanvasArea.subcontrollers.canvas_controller import CanvasController


class CanvasWidget(QtWidgets.QLabel):
    CLEAR_COLOR = QtGui.QColor("black")

    def __init__(self, controller: "CanvasController"):
        self.controller = controller
        super().__init__()
        self.setPixmap(QtGui.QPixmap(*CANVAS_SIZE))

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):
        if not self.controller.is_painting_enabled():
            self.controller.main_controller.process_exception(CannotPaintNow())
            return
        with QtGui.QPainter(self.pixmap()) as painter:
            pen = QtGui.QPen()
            ratios = self.controller.main_controller.get_component_ratios()
            if ratios is None:
                self.controller.main_controller.process_exception(NoComponentBrushSelected())
                return
            brush_color = color_from_ratio(ratios)
            pen.setColor(brush_color)
            pen.setWidth(self.controller.get_brush_width())
            painter.setPen(pen)
            painter.drawPoint(e.x(), e.y())
        self.update()

    def clear(self):
        self.pixmap().fill(CanvasWidget.CLEAR_COLOR)
        self.update()
