from typing import Union, TYPE_CHECKING

import PyQt5.QtWidgets as QtWidgets

from controller.controllers import StartButtonController, PauseButtonController, StopButtonController, \
    ResumeButtonController
if TYPE_CHECKING:
    import a_views.earth_view as earth_view
from .StartButton import StartButton
from .PauseButton import PauseButton
from .StopButton import StopButton
from .ResumeButton import ResumeButton


class SimulationControls(QtWidgets.QWidget, StartButtonController, PauseButtonController, ResumeButtonController, StopButtonController):
    def start_pressed(self):
        """
        Called when the "Start Simulation" button is pressed.
        Forwards the call to the controller (to start the simulation)
        Manipulate the buttons visibility
        :return:
        """
        self.controller.start_pressed()
        self.start_button.hide()
        self.layout().replaceWidget(self.start_button, self.stop_button)
        self.stop_button.show()

        self.pause_button.setEnabled(True)

    def pause_pressed(self):
        """
        Called when the "Pause Simulation" button is pressed.
        Forwards the call to the controller (to pause the simulation)
        Manipulate the buttons visibility
        :return:
        """
        self.controller.pause_pressed()

        self.pause_button.hide()
        self.layout().replaceWidget(self.pause_button, self.resume_button)
        self.resume_button.show()

    def resume_pressed(self):
        """
        Called when the "Resume Simulation" button is pressed.
        Forwards the call to the controller (to resume the simulation)
        Manipulate the buttons visibility
        :return:
        """
        self.controller.resume_pressed()

        self.resume_button.hide()
        self.layout().replaceWidget(self.resume_button, self.pause_button)
        self.pause_button.show()

    def stop_pressed(self):
        """
        Called when the "Stop Simulation" button is pressed.
        Forwards the call to the controller (to stop the simulation)
        Manipulate the buttons visibility
        :return:
        """
        self.controller.stop_pressed()

        self.stop_button.hide()
        self.layout().replaceWidget(self.stop_button, self.start_button)
        self.start_button.show()

        self.layout().replaceWidget(self.resume_button, self.pause_button)
        self.resume_button.hide()

        self.pause_button.show()
        self.pause_button.setEnabled(False)

    def __init__(self, controller: Union[
        "earth_view.MainView", StartButtonController, ResumeButtonController, PauseButtonController, StopButtonController]):
        self.controller = controller
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.start_button = StartButton(controller=self)
        self.pause_button = PauseButton(controller=self)
        self.resume_button = ResumeButton(controller=self)
        self.stop_button = StopButton(controller=self)

        self.layout().addWidget(self.start_button)
        self.layout().addWidget(self.pause_button)
