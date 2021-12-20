import threading

from PyQt5 import QtWidgets

from a_views.main_view import MainView
from constants import CANVAS_SIZE
from controller.CanvasArea.canvas_area_controller import CanvasAreaController
from controller.controllers import StartButtonController, PauseButtonController, StopButtonController, \
    ResumeButtonController, ClearButtonController
from controller.ToolbarArea.toolbar_area_controller import ToolbarController
from controller.exception_controller import ExceptionController
from exceptions import ExceptionToProcess
from models.Earth.earth import Earth
from universe import Universe


class MainController(StartButtonController, PauseButtonController, StopButtonController,
                     ResumeButtonController, ClearButtonController):
    def __init__(self):
        self.model = Universe()
        self.exception_controller = ExceptionController(parent_controller=self)
        self.toolbar_controller = ToolbarController(parent_controller=self)
        self.canvas_controller = CanvasAreaController(parent_controller=self)
        self.view = MainView(controller=self)

    def clear_pressed(self):
        self.canvas_controller.clear_canvas()

    def start_pressed(self):
        self.canvas_controller.set_canvas_enabled(False)
        self.__rebuild_simulation()
        self.__start_simulation()

    def pause_pressed(self):
        self.canvas_controller.set_canvas_enabled(True)
        self.__pause_simulation()

    def resume_pressed(self):
        self.canvas_controller.set_canvas_enabled(False)
        self.__resume_simulation()

    def stop_pressed(self):
        self.canvas_controller.set_canvas_enabled(True)
        self.__stop_simulation()

    def __rebuild_simulation(self):
        self.model = Earth.from_qimage(self.canvas_controller.get_canvas_as_qimage())

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

    def get_brush_color(self):
        return self.toolbar_controller.get_brush_color()

    def get_brush_width(self):
        return self.toolbar_controller.get_brush_width()

    def finish_process_exception(self, exception: type[ExceptionToProcess]):
        self.exception_controller.pop_exception(exception)

    def process_exception(self, exception: ExceptionToProcess):
        self.exception_controller.push_exception(exception)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    controller = MainController()
    uni = Universe()
    uni.setup(shape=CANVAS_SIZE)
    controller.model = uni

    controller.view.show()
    app.exec_()
