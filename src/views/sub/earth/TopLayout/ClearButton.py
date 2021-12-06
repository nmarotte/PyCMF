from typing import TYPE_CHECKING

import PyQt5.QtWidgets as QtWidgets

from controller.controllers import ClearButtonController


class ClearButton(QtWidgets.QPushButton):
    def __init__(self, controller: ClearButtonController):
        super().__init__("Clear Canvas")
        self.clicked.connect(controller.clear_pressed)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
