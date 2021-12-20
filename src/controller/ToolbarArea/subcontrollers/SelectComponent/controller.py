from typing import TYPE_CHECKING

from a_views.ToolbarArea.select_component_widget import SelectComponentWidget
from constants import COMPONENTS
from controller.ToolbarArea.subcontrollers.SelectComponent.popup_controller import SelectComponentPopupController
from exceptions import NoComponentBrushSelected

if TYPE_CHECKING:
    from controller.ToolbarArea.toolbar_area_controller import ToolbarController
    from controller.main_controller import MainController


class SelectComponentController:
    __component_ratios: list[float] = None
    __component_masses: list[float] = None

    def __init__(self, parent_controller: "ToolbarController", main_controller: "MainController"):
        self.parent_controller = parent_controller
        self.main_controller = main_controller
        self.popup_controller = SelectComponentPopupController()
        self.view = SelectComponentWidget(controller=self)

    def button_pressed(self):
        self.popup_controller.view.exec_()
        if self.popup_controller.ratios:
            summed = sum(self.popup_controller.ratios)
            if not summed:
                return 
            self.__component_ratios = [elem/summed for elem in self.popup_controller.ratios]
            self.main_controller.finish_process_exception(NoComponentBrushSelected)
            self.__component_masses = self.popup_controller.masses

    def get_component_ratios(self):
        return self.__component_ratios

    def get_component_masses(self):
        return self.__component_masses

    def get_brush_width(self):
        return self.view.spinbox.value()