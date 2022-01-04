from typing import TYPE_CHECKING

from PyQt5 import QtWidgets

from views.CanvasArea.canvas_widget import CanvasWidget

if TYPE_CHECKING:
    from controller.CanvasArea.canvas_area_controller import CanvasAreaController
    from controller.main_controller import MainController


class CanvasArea(QtWidgets.QWidget):
    def __init__(self, controller: "CanvasAreaController", main_controller: "MainController"):
        self.controller = controller
        self.main_controller = main_controller
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.title = self.main_controller.exception_controller.view

        sub_layout = QtWidgets.QHBoxLayout()
        self.canvas = self.controller.canvas_controller.view
        self.earth_info = self.controller.text_edit_controller.view
        sub_layout.addWidget(self.canvas)
        sub_layout.addWidget(self.earth_info)

        self.layout().addWidget(self.title)
        self.layout().addLayout(sub_layout)

    def clear_canvas(self):
        self.canvas.clear()

    def set_canvas_enabled(self, value: bool):
        self.canvas.setEnabled(value)