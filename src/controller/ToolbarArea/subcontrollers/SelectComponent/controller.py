from typing import TYPE_CHECKING

from views.ToolbarArea.select_component_widget import SelectComponentWidget
from controller.ToolbarArea.subcontrollers.SelectComponent.popup_controller import SelectComponentPopupController
from exceptions import NoComponentBrushSelected
from other.utils import ChunkData

if TYPE_CHECKING:
    from controller.ToolbarArea.toolbar_area_controller import ToolbarController
    from controller.main_controller import MainController


class SelectComponentController:
    data: ChunkData = None

    def __init__(self, parent_controller: "ToolbarController", main_controller: "MainController"):
        self.parent_controller = parent_controller
        self.main_controller = main_controller
        self.popup_controller = SelectComponentPopupController()
        self.view = SelectComponentWidget(controller=self)

    def button_pressed(self):
        self.popup_controller.view.exec_()
        if self.popup_controller.view.accepted:
            self.main_controller.finish_process_exception(NoComponentBrushSelected)

    def get_ratios(self) -> list[float]:
        return [x.get_ratio() for x in self.popup_controller.sub_controllers]

    def get_masses(self) -> list[float]:
        return [x.get_mass() for x in self.popup_controller.sub_controllers]

    def get_temperatures(self) -> list[float]:
        return [x.get_temperature() for x in self.popup_controller.sub_controllers]

    def get_brush_width(self):
        return self.view.spinbox.value()