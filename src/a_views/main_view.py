from PyQt5 import QtWidgets

import threading
from typing import Optional, TYPE_CHECKING

from a_views.CanvasArea.canvas_area import CanvasArea
from a_views.toolbar_widget import ToolbarWidget
from controller.controllers import *
from models.Earth.earth import Earth
from other.utils import color_from_ratio
from universe import Universe
if TYPE_CHECKING:
    from controller.main_controller import MainController


class MainView(QtWidgets.QWidget, StartButtonController, PauseButtonController, StopButtonController,
               ResumeButtonController, ClearButtonController):
    model: Universe

    def clear_pressed(self):
        self.bot_layout.clear_canvas()

    def start_pressed(self):
        self.bot_layout.set_canvas_enabled(False)
        self.__rebuild_simulation()
        self.__start_simulation()

    def pause_pressed(self):
        self.bot_layout.set_canvas_enabled(True)
        self.__pause_simulation()

    def resume_pressed(self):
        self.bot_layout.set_canvas_enabled(False)
        self.__resume_simulation()

    def stop_pressed(self):
        self.bot_layout.set_canvas_enabled(True)
        self.__stop_simulation()

    def is_simulation_running(self):
        return self.model.running

    def __init__(self, controller: "MainController"):
        self.controller = controller
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        # Creates the connection to the model, and its thread for smooth parallel execution
        self.simulation_thread: Optional[threading.Thread] = None

        # Creates the top tool bar
        self.top_layout = ToolbarWidget(controller=self.controller.toolbar_controller)
        self.layout().addWidget(self.top_layout)

        # Create the bottom drawing canvas/simulation view
        self.bot_layout = CanvasArea(controller=self.controller.canvas_controller)
        self.layout().addWidget(self.bot_layout)

    def get_brush_width(self):
        return self.top_layout.get_brush_width()

    def get_brush_color(self):
        value = self.top_layout.paint_component_selector.get_component_ratios()
        if value is not None:
            return color_from_ratio(value)
        return None

    def __rebuild_simulation(self):
        self.model = Earth.from_qimage(self.bot_layout.get_canvas_as_qimage())

    def __start_simulation(self):
        self.simulation_thread = threading.Thread(target=self.model.start_simulation, args=())
        self.simulation_thread.start()

    def __pause_simulation(self):
        self.model.pause_updating()

    def __resume_simulation(self):
        self.simulation_thread = threading.Thread(target=self.model.resume_updating, args=())
        self.simulation_thread.start()

    def __stop_simulation(self):
        self.model.stop_updating()
        self.simulation_thread = None
