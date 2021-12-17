from typing import TYPE_CHECKING

import PyQt5.QtWidgets as QtWidgets
from PyQt5 import QtCore

if TYPE_CHECKING:
    from a_views.earth_view import MainView


class EarthInfoText(QtWidgets.QWidget):
    text_edit: QtWidgets.QTextEdit
    checkbox: QtWidgets.QCheckBox
    button: QtWidgets.QPushButton

    auto_update_timer: QtCore.QTimer

    def __init__(self, controller: "MainView" = None):
        self.controller = controller
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setText(controller.model.__str__())
        self.layout().addWidget(self.text_edit)

        sub_layout = QtWidgets.QHBoxLayout()
        self.checkbox = QtWidgets.QCheckBox("Auto-Refresh")
        self.checkbox.stateChanged.connect(self.__checkbox_state_changed)
        sub_layout.addWidget(self.checkbox)

        self.button = QtWidgets.QPushButton("Refresh Info")
        self.button.clicked.connect(self.refresh)
        sub_layout.addWidget(self.button)

        self.layout().addLayout(sub_layout)

        self.auto_update_timer = QtCore.QTimer()
        self.auto_update_timer.timeout.connect(self.refresh)

    def __checkbox_state_changed(self):
        if self.checkbox.isChecked():
            self.button.setEnabled(False)
            self.auto_update_timer.start(200)
        else:
            self.button.setEnabled(True)
            self.auto_update_timer.stop()

    def refresh(self):
        self.text_edit.setText(self.controller.model.__str__())
