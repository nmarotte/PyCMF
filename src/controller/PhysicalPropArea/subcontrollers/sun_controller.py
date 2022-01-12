from typing import TYPE_CHECKING

from controller.PhysicalPropArea.subcontrollers.sun_popup_controller import SunPopupController
from views.Widgets.sun_widget import SunWidget

if TYPE_CHECKING:
    from controller.PhysicalPropArea.physical_prop_area_controller import PhysicalPropAreaController
    from controller.main_controller import MainController


class SunController:
    def __init__(self, parent_controller: "PhysicalPropAreaController", main_controller: "MainController"):
        self.parent_controller = parent_controller
        self.main_controller = main_controller
        self.popup_controller = SunPopupController(parent_controller=self)
        self.view = SunWidget(self)

    def button_pressed(self):
        self.popup_controller.view.exec_()
