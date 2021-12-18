from typing import TYPE_CHECKING
import qtawesome as qta
from PyQt5.QtGui import QPixmap

from a_views.CanvasArea.title_widget import Title
from constants import ICON_SIZE
from exceptions import *

if TYPE_CHECKING:
    from controller.main_controller import MainController


class ExceptionController:
    def __init__(self, parent_controller: "MainController"):
        self.parent_controller = parent_controller
        self.exception_stack = []
        self.view = Title(controller=self)

    def set_text(self, value: str):
        self.view.label.setText(value)

    def set_icon(self, name: str, color: str):
        self.view.icon.setPixmap(qta.icon(name, color=color).pixmap(*ICON_SIZE))

    def push_exception(self, exception: type[ExceptionToProcess]):
        if len(self.exception_stack) and self.exception_stack[-1] == exception:
            return
        print(f"pushing {exception}")
        self.exception_stack.append(exception)
        self.set_text_for_top_exception()

    def reset_exception_info(self):
        self.view.icon.setPixmap(None)
        self.set_text("")

    def pop_exception(self, exception: type[ExceptionToProcess]):
        if not len(self.exception_stack):
            return
        if self.exception_stack[-1] == exception:
            self.exception_stack.pop()
        else:
            for i in range(len(self.exception_stack)-1, 0, -1):  # Look from the top of the stack
                if self.exception_stack[i] == exception:
                    self.exception_stack.pop(i)
        self.set_text_for_top_exception()

    def set_text_for_top_exception(self):
        if not len(self.exception_stack):
            self.view.icon.setPixmap(QPixmap())
            self.set_text("")
            return
        if self.exception_stack[-1] == NoComponentBrushSelected:
            self.set_icon("fa.warning", color="#eed202")
            self.set_text("You cannot paint without first selecting a component")
        else:
            self.set_icon("ei.error", color="#ff0033")
            self.set_text("There is an unexpected error")

