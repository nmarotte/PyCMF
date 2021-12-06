import PyQt5.QtWidgets as QtWidgets
import qtawesome as qta

from controller.controllers import StartButtonController


class StartButton(QtWidgets.QPushButton):
    def __init__(self, controller: StartButtonController):
        super().__init__(qta.icon("fa.check", color="#228B22"), "Start Simulation")
        self.clicked.connect(controller.start_pressed)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
