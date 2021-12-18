from typing import TYPE_CHECKING

from PyQt5 import QtWidgets
import qtawesome as qta

from constants import ICON_SIZE

if TYPE_CHECKING:
    from controller.exception_controller import ExceptionController


class Title(QtWidgets.QWidget):
    def __init__(self, controller: "ExceptionController"):
        self.controller = controller
        super().__init__()
        self.setLayout(QtWidgets.QHBoxLayout())

        self.icon = QtWidgets.QLabel()
        self.icon.setPixmap(qta.icon("fa.check", color="#00FF00").pixmap(*ICON_SIZE))
        self.icon.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.layout().addWidget(self.icon)

        self.label = QtWidgets.QLabel("Sample Text")
        self.layout().addWidget(self.label)
