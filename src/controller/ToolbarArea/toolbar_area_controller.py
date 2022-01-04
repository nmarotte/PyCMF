from typing import TYPE_CHECKING

from views.toolbar_area import ToolbarArea
from controller.ToolbarArea.subcontrollers.SelectComponent.controller import SelectComponentController
from controller.ToolbarArea.subcontrollers.clear_canvas_controller import ClearCanvasController
from controller.ToolbarArea.subcontrollers.simulation_time_controller import SimulationTimeController
from exceptions import NoComponentBrushSelected

if TYPE_CHECKING:
    from controller.main_controller import MainController


class ToolbarController:
    def __init__(self, parent_controller: "MainController"):
        self.parent_controller = parent_controller
        self.clear_canvas_controller = ClearCanvasController(parent_controller=self, main_controller=parent_controller)
        self.select_component_controller = SelectComponentController(parent_controller=self, main_controller=parent_controller)
        self.simulation_time_controller = SimulationTimeController(parent_controller=self, main_controller=parent_controller)
        self.view = ToolbarArea(self)

    def get_selected_component_dict(self) -> dict:
        value = self.select_component_controller.get_component_ratios()
        if value is None:
            raise NoComponentBrushSelected
        return value

    def get_brush_width(self):
        return self.select_component_controller.get_brush_width()
