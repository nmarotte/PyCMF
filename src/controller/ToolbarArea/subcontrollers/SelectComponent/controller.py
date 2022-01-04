from typing import TYPE_CHECKING

from models.Earth.Components.chunk_component import ChunkComponent
from models.Earth.Components.grid_chunk import GridChunk
from views.Widgets.select_component_widget import SelectComponentWidget
from controller.ToolbarArea.subcontrollers.SelectComponent.popup_controller import SelectComponentPopupController
from exceptions import NoComponentBrushSelected

if TYPE_CHECKING:
    from controller.ToolbarArea.toolbar_area_controller import ToolbarController
    from controller.main_controller import MainController


class SelectComponentController:
    __grid_chunk: GridChunk = None

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

    def get_grid_chunk(self) -> GridChunk:
        if self.__grid_chunk is None:
            components = []
            for controller in self.popup_controller.sub_controllers:
                print(controller.get_temperature())
                components.append(ChunkComponent(controller.get_mass(), controller.get_temperature(), component_type=controller.component_type))
            self.__grid_chunk = GridChunk(components, volume=self.get_volume_each())
        return self.__grid_chunk

    def get_volume_each(self) -> float:
        return 1000
