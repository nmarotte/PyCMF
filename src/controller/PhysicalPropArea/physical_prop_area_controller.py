from typing import TYPE_CHECKING

from controller.PhysicalPropArea.subcontrollers.sun_controller import SunController
from controller.PhysicalPropArea.subcontrollers.universe_controller import UniverseController
from views.physical_prop_area import PhysicalPropArea

if TYPE_CHECKING:
    from controller.main_controller import MainController
    from controller.ToolbarArea.toolbar_area_controller import ToolbarController


class PhysicalPropAreaController:
    def __init__(self, parent_controller: "ToolbarController", main_controller: "MainController"):
        self.parent_controller = parent_controller
        self.main_controller = main_controller
        self.universe_controller = UniverseController(parent_controller=self, main_controller=main_controller)
        self.sun_controller = SunController(parent_controller=self, main_controller=main_controller)
        self.view = PhysicalPropArea(self)
