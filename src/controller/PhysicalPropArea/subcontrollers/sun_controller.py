from typing import TYPE_CHECKING

from controller.PhysicalPropArea.subcontrollers.sun_popup_controller import SunPopupController
from views.Widgets.sun_widget import SunWidget

if TYPE_CHECKING:
    from controller.PhysicalPropArea.physical_prop_area_controller import PhysicalPropAreaController
    from controller.main_controller import MainController


class SunController:
    energy_per_second: float = None
    earth_radiation_ratio: float = None

    def __init__(self, parent_controller: "PhysicalPropAreaController", main_controller: "MainController"):
        self.parent_controller = parent_controller
        self.main_controller = main_controller
        self.popup_controller = SunPopupController(parent_controller=self)
        self.view = SunWidget(self)

    def button_pressed(self):
        self.popup_controller.view.exec_()
        if self.popup_controller.view.accepted:
            self.energy_per_second = float(self.popup_controller.view.output.text())
            self.earth_radiation_ratio = float(self.popup_controller.view.ratio.text())
