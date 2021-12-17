from typing import TYPE_CHECKING

from controller.controllers import StartButtonController, PauseButtonController, StopButtonController, \
    ResumeButtonController, ClearButtonController
from controller.ToolbarArea.toolbar_controller import ToolbarController
from controller.CanvasArea.simulation_view_controller import SimulationViewController


class MainController(StartButtonController, PauseButtonController, StopButtonController,
                     ResumeButtonController, ClearButtonController):
    def __init__(self):
        self.toolbar_controller = ToolbarController()
        # self.simulation_view_controller = SimulationViewController()

    def clear_pressed(self):
        self.simulation_view_controller.clear_canvas()

    def start_pressed(self):
        self.simulation_view_controller.set_canvas_enabled(False)
        self.__rebuild_simulation()
        self.__start_simulation()

    def pause_pressed(self):
        self.simulation_view_controller.set_canvas_enabled(True)
        self.__pause_simulation()

    def resume_pressed(self):
        self.simulation_view_controller.set_canvas_enabled(False)
        self.__resume_simulation()

    def stop_pressed(self):
        self.simulation_view_controller.set_canvas_enabled(True)
        self.__stop_simulation()
