from typing import TYPE_CHECKING

from a_views.ToolbarArea.select_component_widget import SelectComponentWidget
from controller.ToolbarArea.subcontrollers.SelectComponent.popup_controller import SelectComponentPopupController
from exceptions import NoComponentBrushSelected

if TYPE_CHECKING:
    from controller.ToolbarArea.toolbar_area_controller import ToolbarController
    from controller.main_controller import MainController


class SelectComponentController:
    __component_ratios: list[float] = None

    def __init__(self, parent_controller: "ToolbarController", main_controller: "MainController"):
        self.parent_controller = parent_controller
        self.main_controller = main_controller
        self.view = SelectComponentWidget(controller=self)
        self.popup_controller = SelectComponentPopupController()

    def button_pressed(self):
        self.popup_controller.view.exec_()
        if self.popup_controller.value:
            if self.__component_ratios is None:
                self.__component_ratios = [0] * len(self.popup_controller.value)
            summed = sum(self.popup_controller.value)
            for i, elem in enumerate(self.popup_controller.value):
                if elem is not None:
                    self.__component_ratios[i] = self.popup_controller.value[i] / summed
        print("done")
        if self.__component_ratios:
            print("changed")
            self.main_controller.finish_process_exception(NoComponentBrushSelected)

    def get_component_ratios(self):
        return self.__component_ratios

    def get_brush_width(self):
        return self.view.spinbox.value()
