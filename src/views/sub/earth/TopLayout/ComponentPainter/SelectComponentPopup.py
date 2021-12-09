import random

import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import Qt

from constants import COMPONENTS


class SelectComponentPopup(QtWidgets.QDialog):
    class AtomicComponentSlider(QtWidgets.QWidget):
        slider: QtWidgets.QSlider
        spinbox: QtWidgets.QSpinBox
        lock_checkbox: QtWidgets.QCheckBox
        composition_button: QtWidgets.QPushButton

        def __init__(self, label: str, index: int, controller: "SelectComponentPopup"):
            super().__init__()
            self.index = index
            self.controller = controller
            self.setLayout(QtWidgets.QVBoxLayout())
            self.layout().addWidget(QtWidgets.QLabel(label))

            self.sub_layout = QtWidgets.QHBoxLayout()
            self.build()

        def build(self):
            self.__build_slider()
            self.__build_spinbox()
            self.__build_checkbox()
            self.layout().addLayout(self.sub_layout)

        def __build_slider(self):
            self.slider = QtWidgets.QSlider(Qt.Horizontal)
            self.slider.setTickInterval(10)
            self.slider.setSingleStep(1)
            self.slider.setMinimum(0)
            self.slider.setMaximum(100)
            self.slider.valueChanged.connect(self.update_spinbox)
            self.sub_layout.addWidget(self.slider)

        def __build_spinbox(self):
            self.spinbox = QtWidgets.QSpinBox()
            self.spinbox.valueChanged.connect(self.update_slider)
            self.sub_layout.addWidget(self.spinbox)

        def __build_checkbox(self):
            self.lock_checkbox = QtWidgets.QCheckBox("Lock")
            self.lock_checkbox.stateChanged.connect(self.lock_changed)
            self.sub_layout.addWidget(self.lock_checkbox)

        def update_spinbox(self):
            if self.slider.value() > self.controller.get_maximum():
                self.slider.setValue(self.controller.get_maximum())
            else:
                self.spinbox.setValue(self.slider.value())

        def update_slider(self):
            if self.spinbox.value() > self.controller.get_maximum():
                self.spinbox.setValue(self.controller.get_maximum())
            else:
                self.slider.setValue(self.spinbox.value())
                self.controller.balance_sliders(self.index, self.get_value())

        def lock_changed(self):
            if self.lock_checkbox.isChecked():
                self.slider.setDisabled(True)
                self.spinbox.setDisabled(True)
            else:
                self.slider.setEnabled(True)
                self.spinbox.setEnabled(True)
            self.controller.lock_changed()

        def is_locked(self):
            return self.lock_checkbox.isChecked()

        def set_locked(self, value: bool):
            self.lock_checkbox.setChecked(value)

        def get_value(self):
            return self.slider.value()

        def set_value(self, value: int):
            self.slider.setValue(value)

        def set_locking_enabled(self, value: bool):
            if not value:
                self.lock_checkbox.setChecked(False)
            self.lock_checkbox.setEnabled(value)

        def is_locking_enabled(self):
            return self.lock_checkbox.isEnabled()

    class ComponentSlider(AtomicComponentSlider):
        def __build_composition_button(self):
            self.composition_button = QtWidgets.QPushButton("Composition")
            self.sub_layout.addWidget(self.composition_button)

        def build(self):
            self.__build_composition_button()
            super().build()

    def __init__(self):
        super().__init__()
        self.balancing = False
        self.value = None
        self.sliders = []
        self.setLayout(QtWidgets.QVBoxLayout())
        for i, elem in enumerate(COMPONENTS):
            self.sliders.append(SelectComponentPopup.AtomicComponentSlider(elem, i, controller=self))
            self.layout().addWidget(self.sliders[-1])

        self.bottom_layout = QtWidgets.QHBoxLayout()
        self.confirm = QtWidgets.QPushButton("Confirm")
        self.confirm.clicked.connect(self.confirmed)
        self.bottom_layout.addWidget(self.confirm)

        self.cancel = QtWidgets.QPushButton("Cancel")
        self.cancel.clicked.connect(self.cancelled)
        self.bottom_layout.addWidget(self.cancel)

        self.layout().addLayout(self.bottom_layout)

    def balance_sliders(self, index: int, value: int):
        if self.balancing:
            return
        self.balancing = True
        # Count the remaining value to balance
        total_to_balance = 100 - value - sum(x.get_value() for x in self.sliders if x.is_locked())
        # Count the amount of sliders not locked
        count_not_locked_not_index = sum(not x.is_locked() and x.index != index for x in self.sliders)
        for slider in self.sliders:
            if slider.index != index and not slider.is_locked():
                slider.set_value(total_to_balance//count_not_locked_not_index)
        self.balancing = False

    def lock_changed(self):
        """
        Locks all "Lock" checkbox when only 2 sliders are left unlocked
        :return:
        """
        count = sum(not x.is_locked() for x in self.sliders)
        if count == 2:
            for elem in self.sliders:
                if not elem.is_locked():
                    elem.set_locking_enabled(False)
        else:
            for elem in self.sliders:
                if not elem.is_locking_enabled():
                    elem.set_locking_enabled(True)

    def get_maximum(self):
        """
        Computes the maximum value that is left to be allocated to sliders
        :return:
        """
        return 100 - sum(x.get_value() for x in self.sliders if x.is_locked())

    def confirmed(self):
        self.value = [x.get_value() for x in self.sliders]
        self.accept()

    def cancelled(self):
        self.value = [None] * len(self.sliders)
        self.reject()
