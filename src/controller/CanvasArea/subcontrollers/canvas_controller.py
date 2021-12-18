from typing import TYPE_CHECKING

from a_views.CanvasArea.canvas_widget import CanvasWidget
if TYPE_CHECKING:
    from controller.CanvasArea.canvas_area_controller import CanvasAreaController


class CanvasController:
    def __init__(self, parent_controller: "CanvasAreaController"):
        self.parent_controller = parent_controller
        self.view = CanvasWidget(controller=self)

    def get_brush_color(self):
        return self.parent_controller.get_brush_color()

    def get_brush_width(self):
        return self.parent_controller.get_brush_width()

    def clear_canvas(self):
        self.view.clear()
