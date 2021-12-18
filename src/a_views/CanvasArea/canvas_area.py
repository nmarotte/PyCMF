from typing import TYPE_CHECKING

from PyQt5 import QtWidgets

from a_views.CanvasArea.canvas_widget import CanvasWidget

if TYPE_CHECKING:
    from controller.CanvasArea.canvas_area_controller import CanvasAreaController


class CanvasArea(QtWidgets.QWidget):
    def __init__(self, controller: "CanvasAreaController"):
        self.controller = controller
        super().__init__()
        self.setLayout(QtWidgets.QHBoxLayout())
        self.canvas = self.controller.canvas_controller.view
        self.earth_info = self.controller.text_edit_controller.view

        self.layout().addWidget(self.canvas)
        self.layout().addWidget(self.earth_info)

    def clear_canvas(self):
        self.canvas.clear()

    def set_canvas_enabled(self, value: bool):
        self.canvas.setEnabled(value)

    def get_canvas_as_qimage(self):
        return self.canvas.label.pixmap().toImage()