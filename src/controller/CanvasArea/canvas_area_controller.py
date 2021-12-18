from typing import TYPE_CHECKING

from a_views.CanvasArea.canvas_area import CanvasArea
from controller.CanvasArea.subcontrollers.canvas_controller import CanvasController
from controller.CanvasArea.subcontrollers.text_edit_controller import TextEditController

if TYPE_CHECKING:
    from controller.main_controller import MainController


class CanvasAreaController:
    def __init__(self, parent_controller: "MainController"):
        self.parent_controller = parent_controller
        self.canvas_controller = CanvasController(parent_controller=self)
        self.text_edit_controller = TextEditController(parent_controller=self)
        self.view = CanvasArea(controller=self)

    def get_brush_color(self):
        return self.parent_controller.get_brush_color()

    def get_brush_width(self):
        return self.parent_controller.get_brush_width()