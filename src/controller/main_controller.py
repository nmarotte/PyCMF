import math
import threading
from typing import Optional

from PyQt5 import QtWidgets

from models.Earth.earth import Earth
from sun import Sun
from views.main_view import MainView
from constants import CANVAS_SIZE
from controller.CanvasArea.canvas_area_controller import CanvasAreaController
from controller.ToolbarArea.toolbar_area_controller import ToolbarController
from controller.exception_controller import ExceptionController
from exceptions import ExceptionToProcess
from models.Earth.Components.chunk_component import ChunkComponent
from models.Earth.Components.grid_chunk import GridChunk
from universe import Universe


class MainController:
    model: Universe
    simulation_thread: Optional[threading.Thread] = None

    def __init__(self):
        self.model = Universe()
        self.model.earth = Earth(shape=CANVAS_SIZE, parent=self.model)
        self.model.sun = Sun(parent=self.model)
        self.exception_controller = ExceptionController(parent_controller=self)
        self.toolbar_controller = ToolbarController(parent_controller=self)
        self.canvas_controller = CanvasAreaController(parent_controller=self)
        self.view = MainView(controller=self)

    def clear_pressed(self):
        self.canvas_controller.clear_canvas()

    def build_pressed(self):
        self.__rebuild_simulation()

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
        pass

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

    def get_brush_width(self):
        return self.toolbar_controller.get_brush_width()

    def finish_process_exception(self, exception: type[ExceptionToProcess]):
        self.exception_controller.pop_exception(exception)

    def process_exception(self, exception: ExceptionToProcess):
        self.exception_controller.push_exception(exception)

    def is_exception_processing(self, exception: type[ExceptionToProcess]):
        return any(isinstance(e, exception) for e in self.exception_controller.exception_stack)

    def components_painted(self, *positions: tuple[int, int]):
        for x, y in set(positions):
            chunk = self.toolbar_controller.select_component_controller.get_grid_chunk()
            chunk.index = x + y * self.model.earth.shape[1]
            chunk.parent = self.model.earth
            chunk.neighbours = chunk.parent.neighbours(chunk.index)
            self.model.earth.set_component_at(chunk, x, y)

    def get_ratios(self):
        return self.toolbar_controller.select_component_controller.get_ratios()

    def get_grid_chunk(self):
        return self.toolbar_controller.select_component_controller.get_grid_chunk()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    controller = MainController()

    controller.view.show()
    app.exec_()
