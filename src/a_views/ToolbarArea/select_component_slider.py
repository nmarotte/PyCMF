from typing import TYPE_CHECKING

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

if TYPE_CHECKING:
    from controller.ToolbarArea.subcontrollers.SelectComponent.slider_controller import SelectComponentSliderController


class AtomicSelectComponentSlider(QtWidgets.QWidget):
    slider: QtWidgets.QSlider
    spinbox: QtWidgets.QSpinBox
    lock_checkbox: QtWidgets.QCheckBox
    composition_button: QtWidgets.QPushButton

    def __init__(self, label: str, index: int, default_mass: int, controller: "SelectComponentSliderController"):
        self.controller = controller
        super().__init__()
        self.index = index
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(QtWidgets.QLabel(label.capitalize()))

        self.sub_layout = QtWidgets.QHBoxLayout()

        # Construct the slider widget
        self.slider = QtWidgets.QSlider(Qt.Horizontal)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.valueChanged.connect(self.controller.slider_changed)
        self.sub_layout.addWidget(self.slider)

        # Construct the spinbox (number text with arrows)
        self.spinbox = QtWidgets.QSpinBox()
        self.spinbox.setMinimum(0)
        self.spinbox.setMaximum(100)
        self.spinbox.valueChanged.connect(self.controller.spinbox_changed)
        self.sub_layout.addWidget(self.spinbox)

        # Construct the lock check box
        self.lock_checkbox = QtWidgets.QCheckBox("Lock")
        self.lock_checkbox.stateChanged.connect(self.controller.lock_changed)
        self.sub_layout.addWidget(self.lock_checkbox)

        self.mass_label = QtWidgets.QLabel("Mass (kg)")
        self.sub_layout.addWidget(self.mass_label)
        self.mass_spinbox = QtWidgets.QDoubleSpinBox()
        self.mass_spinbox.setMaximum(10000)
        self.mass_spinbox.setValue(default_mass)
        self.mass_spinbox.setSingleStep(default_mass//10)
        self.sub_layout.addWidget(self.mass_spinbox)
        # Add the 3 components from left to right to the layout
        self.layout().addLayout(self.sub_layout)


class SelectComponentSlider(AtomicSelectComponentSlider):
    def __init__(self, label: str, index: int, default_mass: int, controller: "SelectComponentSliderController"):
        super(SelectComponentSlider, self).__init__(label, index, default_mass, controller)
        self.composition_button = QtWidgets.QPushButton("Composition")
        self.sub_layout.insertWidget(0, self.composition_button)
