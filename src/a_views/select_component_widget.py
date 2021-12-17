from typing import TYPE_CHECKING

from a_views.select_component_slider import AtomicSelectComponentSlider
from controller.ToolbarArea.subcontrollers.SelectComponent.slider_controller import SelectComponentSliderController

if TYPE_CHECKING:
    from controller.ToolbarArea.subcontrollers.SelectComponent.popup_controller import SelectComponentPopupController
    from controller.ToolbarArea.subcontrollers.SelectComponent.controller import SelectComponentController


import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import Qt

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


class SelectComponentWidget(QtWidgets.QPushButton):
    def __init__(self, controller: "SelectComponentController"):
        self.controller = controller
        super().__init__(f"Select Component\n Brush")
        self.clicked.connect(self.controller.button_pressed)
