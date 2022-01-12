from typing import TYPE_CHECKING

from views.Widgets.sun_popup_widget import SunPopupWidget

if TYPE_CHECKING:
    from controller.PhysicalPropArea.subcontrollers.sun_controller import SunController


class SunPopupController:
    energy_per_second: float = None
    earth_radiation_ratio: float = None

    def __init__(self, parent_controller: "SunController"):
        self.parent_controller = parent_controller
        self.view = SunPopupWidget(self)

    def confirmed(self):
        self.energy_per_second = float(self.view.output.text())
        self.earth_radiation_ratio = float(self.view.ratio.text())
        self.view.accept()

    def cancelled(self):
        self.view.reject()
