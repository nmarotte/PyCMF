from typing import TYPE_CHECKING

from a_views.CanvasArea.text_edit_widget import TextEdit
if TYPE_CHECKING:
    from controller.CanvasArea.canvas_area_controller import CanvasAreaController


class TextEditController:
    def __init__(self, parent_controller: "CanvasAreaController"):
        self.parent_controller = parent_controller
        self.view = TextEdit(controller=self)