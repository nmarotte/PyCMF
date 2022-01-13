from typing import TYPE_CHECKING

from views.Widgets.sun_popup_widget import SunPopupWidget
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
        self.view = SunWidget(self)
        self.popup = SunPopupWidget(self)

    def confirmed(self):
        self.popup.accept()
        self.popup.close()

    def cancelled(self):
        self.popup.reject()
        self.popup.close()

    def button_pressed(self):
        result = self.popup.exec_()
        if result:
            self.energy_per_second = float(self.popup.output.text())
            self.earth_radiation_ratio = float(self.popup.ratio.text())
            self.main_controller.set_sun_energy_per_second(self.energy_per_second)
            self.main_controller.set_earth_radiation_ratio(self.earth_radiation_ratio)
