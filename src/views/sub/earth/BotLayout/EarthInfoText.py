from typing import TYPE_CHECKING

import PyQt5.QtWidgets as QtWidgets
from PyQt5 import QtGui


if TYPE_CHECKING:
    from views.earth_view import EarthView


class EarthInfoText(QtWidgets.QTextEdit):
    def __init__(self, controller: "EarthView" = None):
        self.controller = controller
        super().__init__()
        self.setReadOnly(True)
        self.setText(controller.model.__str__())
