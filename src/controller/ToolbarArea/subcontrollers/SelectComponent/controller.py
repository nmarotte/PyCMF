from typing import TYPE_CHECKING

from models.Earth.Components.chunk_component import ChunkComponent
from modelsv2.physical_class.grid_chunk import GridChunk
from views.Widgets.select_component_widget import SelectComponentWidget
from controller.ToolbarArea.subcontrollers.SelectComponent.popup_controller import SelectComponentPopupController
from messages import NoComponentBrushSelected

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
        result = self.popup_controller.view.exec_()
        if result:
            self.main_controller.finish_process_message(NoComponentBrushSelected)
            components = []
            ratios = self.get_ratios()
            if all(not r for r in ratios):  # If all ratios are 0
                return
            ratios = [x/sum(ratios) for x in ratios]  # Normalize
            for i, controller in enumerate(self.popup_controller.sub_controllers):
                components.append(ChunkComponent(self.get_mass() * ratios[i], self.get_temperature(),
                                                 component_type=controller.type))
            self.__grid_chunk = GridChunk(components, volume=self.get_volume_each())

    def get_ratios(self) -> list[float]:
        return [x.get_ratio() for x in self.popup_controller.sub_controllers]

    def get_mass(self) -> float:
        return self.popup_controller.get_mass()

    def get_temperature(self) -> float:
        return self.popup_controller.get_temperature()

    def get_brush_width(self):
        return self.view.spinbox.value()

    def get_grid_chunk(self) -> GridChunk:
        return self.__grid_chunk

    def get_volume_each(self) -> float:
        return 1000
