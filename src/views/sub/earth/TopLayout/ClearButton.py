from typing import TYPE_CHECKING

import PyQt5.QtWidgets as QtWidgets

if TYPE_CHECKING:
    from views.sub.earth.TopLayout.TopLayout import TopLayout


class ClearButton(QtWidgets.QPushButton):
    def __init__(self, parent: "TopLayout" = None):
        super().__init__("Clear", parent=parent)
        self.clicked.connect(parent.clear_pressed)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
