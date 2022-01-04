from PyQt5 import QtWidgets

import threading
from typing import Optional, TYPE_CHECKING

from models.Earth.earth import Earth
from universe import Universe
if TYPE_CHECKING:
    from controller.main_controller import MainController


class MainView(QtWidgets.QWidget):
    model: Universe

    def __init__(self, controller: "MainController"):
        self.controller = controller
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        # Creates the connection to the model, and its thread for smooth parallel execution
        self.simulation_thread: Optional[threading.Thread] = None

        self.toolbar_area_view = self.controller.toolbar_controller.view
        self.layout().addWidget(self.toolbar_area_view)

        self.canvas_area_view = self.controller.canvas_controller.view
        self.layout().addWidget(self.canvas_area_view)

