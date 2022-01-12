from typing import TYPE_CHECKING

from controller.PhysicalPropArea.subcontrollers.universe_popup_controller import UniversePopupController
from views.Widgets.universe_widget import UniverseWidget

if TYPE_CHECKING:
    from controller.PhysicalPropArea.physical_prop_area_controller import PhysicalPropAreaController
    from controller.main_controller import MainController


class UniverseController:
    def __init__(self, parent_controller: "PhysicalPropAreaController", main_controller: "MainController"):
        self.parent_controller = parent_controller
        self.main_controller = main_controller
        self.popup_controller = UniversePopupController(parent_controller=self)
        self.view = UniverseWidget(self)

    def button_pressed(self):
        self.popup_controller.view.exec_()