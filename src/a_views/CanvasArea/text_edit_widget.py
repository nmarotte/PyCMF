from typing import TYPE_CHECKING

from PyQt5 import QtWidgets

if TYPE_CHECKING:
    from controller.CanvasArea.subcontrollers.text_edit_controller import TextEditController


class TextEdit(QtWidgets.QTextEdit):
    def __init__(self, controller: "TextEditController"):
        self.controller = controller
        super().__init__()
        self.setReadOnly(True)
