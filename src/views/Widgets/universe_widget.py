from typing import TYPE_CHECKING

from PyQt5 import QtWidgets

if TYPE_CHECKING:
    from controller.PhysicalPropArea.subcontrollers.universe_controller import UniverseController


class UniverseWidget(QtWidgets.QPushButton):
    def __init__(self, controller: "UniverseController"):
        self.controller = controller
        super().__init__("Universe properties")
        self.clicked.connect(self.controller.button_pressed)
