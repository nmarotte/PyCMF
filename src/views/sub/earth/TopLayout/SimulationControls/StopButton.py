import PyQt5.QtWidgets as QtWidgets
import qtawesome as qta

from controller.controllers import StopButtonController


class StopButton(QtWidgets.QPushButton):
    def __init__(self, controller: StopButtonController):
        super().__init__(qta.icon("fa.hand-stop-o", color="#B22222"), "Stop Simulation")
        self.clicked.connect(controller.stop_pressed)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setHidden(True)
