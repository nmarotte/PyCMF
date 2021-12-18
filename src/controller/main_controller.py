from typing import TYPE_CHECKING

from PyQt5 import QtWidgets

from a_views.main_view import MainView
from constants import CANVAS_SIZE
from controller.CanvasArea.canvas_area_controller import CanvasAreaController
from controller.controllers import StartButtonController, PauseButtonController, StopButtonController, \
    ResumeButtonController, ClearButtonController
from controller.ToolbarArea.toolbar_area_controller import ToolbarController
from controller.CanvasArea.simulation_view_controller import SimulationViewController
from universe import Universe


class MainController(StartButtonController, PauseButtonController, StopButtonController,
                     ResumeButtonController, ClearButtonController):
    def __init__(self):
        self.toolbar_controller = ToolbarController(parent_controller=self)
        self.simulation_view_controller = SimulationViewController(parent_controller=self)
        self.canvas_controller = CanvasAreaController(parent_controller=self)
        self.view = MainView(controller=self)

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

    def get_brush_color(self):
        return self.toolbar_controller.get_brush_color()

    def get_brush_width(self):
        return self.toolbar_controller.get_brush_width()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    controller = MainController()
    uni = Universe()
    uni.setup(shape=CANVAS_SIZE)
    controller.model = uni

    controller.view.show()
    app.exec_()
