from typing import TYPE_CHECKING

from PyQt5 import QtWidgets

from a_views.ToolbarArea.select_component_widget import SelectComponentWidget

if TYPE_CHECKING:
    from controller.ToolbarArea.toolbar_area_controller import ToolbarController


class ToolbarArea(QtWidgets.QWidget):
    def __init__(self, controller: "ToolbarController"):
        self.controller = controller
        super().__init__()
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().addWidget(SelectComponentWidget(controller=controller.select_component_controller))