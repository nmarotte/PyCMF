from a_views.select_component_widget import SelectComponentWidget
from controller.ToolbarArea.subcontrollers.SelectComponent.popup_controller import SelectComponentPopupController


class SelectComponentController:
    __component_ratios: list[float] = None

    def __init__(self):
        self.view = SelectComponentWidget(controller=self)
        self.sub_controller = SelectComponentPopupController()

    def button_pressed(self):
        self.sub_controller.view.exec_()
        if self.sub_controller.value:
            if self.__component_ratios is None:
                self.__component_ratios = [0] * len(self.sub_controller.value)
            summed = sum(self.sub_controller.value)
            for i, elem in enumerate(self.sub_controller.value):
                if elem is not None:
                    self.__component_ratios[i] = self.sub_controller.value[i] / summed
