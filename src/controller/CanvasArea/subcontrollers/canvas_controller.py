from typing import TYPE_CHECKING

from a_views.CanvasArea.canvas_widget import CanvasWidget
from exceptions import ExceptionToProcess

if TYPE_CHECKING:
    from controller.CanvasArea.canvas_area_controller import CanvasAreaController
    from controller.main_controller import MainController


class CanvasController:
    painting_enabled: bool = True

    def __init__(self, parent_controller: "CanvasAreaController", main_controller: "MainController"):
        self.main_controller = main_controller
        self.parent_controller = parent_controller
        self.view = CanvasWidget(controller=self)

    def get_brush_width(self):
        return self.main_controller.get_brush_width()

    def clear_canvas(self):
        self.view.clear()

    def is_painting_enabled(self):
        return self.painting_enabled

    def set_painting_enabled(self, value: bool):
        self.painting_enabled = value
