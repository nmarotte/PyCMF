import PyQt5.QtWidgets as QtWidgets
import qtawesome as qta

from controller.controllers import ResumeButtonController


class ResumeButton(QtWidgets.QPushButton):
    def __init__(self, controller: ResumeButtonController):
        super().__init__(qta.icon("fa5s.play", color="#4169E1"), "Resume Simulation")
        self.clicked.connect(controller.resume_pressed)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setMinimumWidth(150)

