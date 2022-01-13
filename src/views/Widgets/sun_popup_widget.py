from typing import TYPE_CHECKING

from PyQt5 import QtWidgets, QtGui

from other.utils import LabelledWidget, FloatValidator

if TYPE_CHECKING:
    from controller.PhysicalPropArea.subcontrollers.sun_controller import SunController


class SunPopupWidget(QtWidgets.QDialog):
    validator = FloatValidator()

    def __init__(self, controller: "SunController"):
        self.controller = controller
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        self.bottom_layout = QtWidgets.QHBoxLayout()
        self.confirm = QtWidgets.QPushButton("Confirm")
        self.confirm.clicked.connect(self.controller.confirmed)
        self.bottom_layout.addWidget(self.confirm)

        self.cancel = QtWidgets.QPushButton("Cancel")
        self.cancel.clicked.connect(self.controller.cancelled)
        self.bottom_layout.addWidget(self.cancel)

        self.output = LabelledWidget(QtWidgets.QLineEdit, "Energy(J) output per second", vertical=False)
        self.output.setText(str(self.controller.main_controller.get_energy_per_second()))
        self.output.setValidator(self.validator)
        self.output.textChanged.connect(self.verify_output)
        self.layout().addWidget(self.output)

        self.ratio = LabelledWidget(QtWidgets.QLineEdit, "Earth ratio viewed from the sun", vertical=False)
        self.ratio.setText(str(self.controller.main_controller.get_earth_radiation_ratio()))
        self.ratio.textChanged.connect(self.verify_ratio)
        self.ratio.setValidator(self.validator)
        self.layout().addWidget(self.ratio)
        self.layout().addLayout(self.bottom_layout)

    def showEvent(self, a0: QtGui.QShowEvent):
        self.ratio.setText(str(self.controller.main_controller.get_earth_radiation_ratio()))
        self.output.setText(str(self.controller.main_controller.get_energy_per_second()))
        super(SunPopupWidget, self).showEvent(a0)

    def verify_output(self):
        """
        Verify that the lineEdit is a valid float, and disables the confirm button if not
        :return:
        """
        try:
            float(self.output.text())
        except ValueError:
            self.confirm.setDisabled(True)
        else:
            self.confirm.setEnabled(True)

    def verify_ratio(self):
        """
        Verify that the lineEdit is a valid float, and disables the confirm button if not
        :return:
        """
        try:
            float(self.ratio.text())
        except ValueError:
            self.confirm.setDisabled(True)
        else:
            self.confirm.setEnabled(True)
