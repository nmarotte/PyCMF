from typing import TYPE_CHECKING

from views.Widgets.universe_popup_widget import UniversePopupWidget

if TYPE_CHECKING:
    from controller.PhysicalPropArea.subcontrollers.universe_controller import UniverseController


class UniversePopupController:
    def __init__(self, parent_controller: "UniverseController"):
        self.parent_controller = parent_controller
        self.view = UniversePopupWidget(self)

    def confirmed(self):
        self.view.accept()

    def cancelled(self):
        self.view.reject()
