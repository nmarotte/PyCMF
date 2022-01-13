from typing import TYPE_CHECKING

from views.Widgets.universe_popup_widget import UniversePopupWidget
from views.Widgets.universe_widget import UniverseWidget

if TYPE_CHECKING:
    from controller.PhysicalPropArea.physical_prop_area_controller import PhysicalPropAreaController
    from controller.main_controller import MainController


class UniverseController:
    time_delta: float = None

    def __init__(self, parent_controller: "PhysicalPropAreaController", main_controller: "MainController"):
        self.parent_controller = parent_controller
        self.main_controller = main_controller
        self.view = UniverseWidget(self)
        self.popup = UniversePopupWidget(self)

    def confirmed(self):
        self.popup.accept()
        self.popup.close()

    def cancelled(self):
        self.popup.reject()
        self.popup.close()

    def button_pressed(self):
        result = self.popup.exec_()
        if result:
            self.time_delta = self.popup.time_delta_spinbox.value()
