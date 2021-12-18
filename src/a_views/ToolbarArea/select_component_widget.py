from typing import TYPE_CHECKING
import qtawesome as qta

if TYPE_CHECKING:
    from controller.ToolbarArea.subcontrollers.SelectComponent.popup_controller import SelectComponentPopupController
    from controller.ToolbarArea.subcontrollers.SelectComponent.controller import SelectComponentController


import PyQt5.QtWidgets as QtWidgets

from constants import COMPONENTS


class SelectComponentPopupView(QtWidgets.QDialog):
    def __init__(self, controller: "SelectComponentPopupController"):
        self.controller = controller
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        self.sliders = []
        for i, elem in enumerate(COMPONENTS):
            self.sliders.append(self.controller.sub_controllers[i].view)
            self.layout().addWidget(self.sliders[-1])

        self.bottom_layout = QtWidgets.QHBoxLayout()
        self.confirm = QtWidgets.QPushButton("Confirm")
        self.confirm.clicked.connect(self.controller.confirmed)
        self.bottom_layout.addWidget(self.confirm)

        self.cancel = QtWidgets.QPushButton("Cancel")
        self.cancel.clicked.connect(self.controller.cancelled)
        self.bottom_layout.addWidget(self.cancel)

        self.layout().addLayout(self.bottom_layout)


class SelectComponentWidget(QtWidgets.QWidget):
    def __init__(self, controller: "SelectComponentController"):
        self.controller = controller
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        # Button to select component
        self.button = QtWidgets.QPushButton(f"Select Component\n Brush")
        self.button.clicked.connect(self.controller.button_pressed)

        self.layout().addWidget(self.button)

        # Label and spinbox to select size
        label = QtWidgets.QLabel("\uf1fc" + "Brush Size")
        label.setFont(qta.font('fa', 12))
        label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.layout().addWidget(label)

        self.spinbox = QtWidgets.QSpinBox()
        self.spinbox.setValue(10)
        self.spinbox.setSingleStep(5)
        self.spinbox.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.layout().addWidget(self.spinbox)
