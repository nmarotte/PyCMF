from typing import TYPE_CHECKING

from PyQt5 import QtWidgets

if TYPE_CHECKING:
    from controller.PhysicalPropArea.subcontrollers.sun_controller import SunController


class SunWidget(QtWidgets.QPushButton):
    def __init__(self, controller: "SunController"):
        self.controller = controller
        super().__init__("Sun properties")
        self.clicked.connect(self.controller.button_pressed)
