from typing import TYPE_CHECKING

from a_views.ToolbarArea.simulation_time_widget import SimulationTimeWidget

if TYPE_CHECKING:
    from controller.main_controller import MainController
    from controller.ToolbarArea.toolbar_area_controller import ToolbarController


class SimulationTimeController:
    def __init__(self, parent_controller: "ToolbarController", main_controller: "MainController"):
        self.parent_controller = parent_controller
        self.main_controller = main_controller
        self.view = SimulationTimeWidget(controller=self)

    def start_pressed(self):
        return self.main_controller.start_pressed()

    def pause_pressed(self):
        return self.main_controller.pause_pressed()

    def resume_pressed(self):
        return self.main_controller.resume_pressed()

    def stop_pressed(self):
        return self.main_controller.stop_pressed()
