import math
import threading
from typing import Optional

from PyQt5 import QtWidgets

from a_views.main_view import MainView
from constants import CANVAS_SIZE
from controller.CanvasArea.canvas_area_controller import CanvasAreaController
from controller.controllers import StartButtonController, PauseButtonController, StopButtonController, \
    ResumeButtonController, ClearButtonController
from controller.ToolbarArea.toolbar_area_controller import ToolbarController
from controller.exception_controller import ExceptionController
from exceptions import ExceptionToProcess
from models.Earth.Components.chunk_component import ChunkComponent
from models.Earth.Components.grid_chunk import GridChunk
from universe import Universe


class MainController(StartButtonController, PauseButtonController, StopButtonController,
                     ResumeButtonController, ClearButtonController):
    model: Universe = Universe()
    simulation_thread: Optional[threading.Thread] = None

    def __init__(self):
        self.exception_controller = ExceptionController(parent_controller=self)
        self.toolbar_controller = ToolbarController(parent_controller=self)
        self.canvas_controller = CanvasAreaController(parent_controller=self)
        self.view = MainView(controller=self)
        self.model.setup(shape=CANVAS_SIZE)

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
        # self.model.earth = Earth.from_qimage(self.canvas_controller.get_canvas_as_qimage(), self.get_components_data())
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
        temperatures = self.toolbar_controller.select_component_controller.get_temperatures()
        ratios = self.toolbar_controller.select_component_controller.get_ratios()
        masses = self.toolbar_controller.select_component_controller.get_masses()
        ratioed_masses = [m * r for m, r in zip(masses, ratios)]
        for x, y in set(positions):
            components = []
            if not math.isclose(ratios[0], 0):
                components.append(ChunkComponent(component_type="WATER", mass=ratioed_masses[0], temperature=temperatures[0]))
            if not math.isclose(ratios[1], 0):
                components.append(ChunkComponent(component_type="AIR", mass=ratioed_masses[1], temperature=temperatures[1]))
            if not math.isclose(ratios[2], 0):
                components.append(ChunkComponent(component_type="LAND", mass=ratioed_masses[2], temperature=temperatures[2]))
            chunk = GridChunk(components=components, volume=1, parent=self.model.earth,  index=x + y * self.model.earth.shape[1])
            self.model.earth.set_component_at(chunk, x, y)

    def get_ratios(self):
        return self.toolbar_controller.select_component_controller.get_ratios()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    controller = MainController()
    uni = Universe()
    uni.setup(shape=CANVAS_SIZE)
    controller.model = uni

    controller.view.show()
    app.exec_()
