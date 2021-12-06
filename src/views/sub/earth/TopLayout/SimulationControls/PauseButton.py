import PyQt5.QtWidgets as QtWidgets
import qtawesome as qta

from controller.controllers import PauseButtonController


class PauseButton(QtWidgets.QPushButton):
    def __init__(self, controller: PauseButtonController):
        super().__init__(qta.icon("fa5s.pause", color="#4169E1"), "Pause Simulation")
        self.clicked.connect(controller.pause_pressed)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setEnabled(False)
        self.setMinimumWidth(150)
