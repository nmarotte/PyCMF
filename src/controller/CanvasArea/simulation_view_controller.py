from typing import TYPE_CHECKING

from controller.CanvasArea.subcontrollers.canvas_controller import CanvasController

if TYPE_CHECKING:
    from controller.main_controller import MainController


class SimulationViewController:
    def __init__(self, parent_controller: "MainController"):
        self.parent_controller = parent_controller
        # self.title_controller = title_controller
        self.canvas_controller = CanvasController(parent_controller=self)
        # self.text_edit_controller = text_edit_controller

    def clear_canvas(self):
        self.canvas_controller.clear_canvas()

    def get_brush_color(self):
        return self.parent_controller.get_brush_color()

    def get_brush_width(self):
        return self.parent_controller.get_brush_width()