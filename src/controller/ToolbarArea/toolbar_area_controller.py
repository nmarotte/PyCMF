from typing import TYPE_CHECKING

from a_views.ToolbarArea.toolbar_area import ToolbarArea
from controller.ToolbarArea.subcontrollers.SelectComponent.controller import SelectComponentController
from controller.ToolbarArea.subcontrollers.simulation_time_controller import SimulationTimeController
from exceptions import NoComponentBrushSelected
from other.utils import color_from_ratio

if TYPE_CHECKING:
    from controller.main_controller import MainController


class ToolbarController:
    def __init__(self, parent_controller: "MainController"):
        self.parent_controller = parent_controller
        self.select_component_controller = SelectComponentController()
        self.simulation_time_controller = SimulationTimeController()
        self.view = ToolbarArea(self)

    def get_brush_color(self):
        value = self.select_component_controller.get_component_ratios()
        if value is None:
            raise NoComponentBrushSelected
        return color_from_ratio(value)

    def get_brush_width(self):
        return self.select_component_controller.get_brush_width()
