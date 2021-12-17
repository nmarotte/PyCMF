from typing import TYPE_CHECKING

from PyQt5 import QtWidgets

from a_views.select_component_widget import SelectComponentWidget
if TYPE_CHECKING:
    from controller.ToolbarArea.toolbar_controller import ToolbarController


class ToolbarWidget(QtWidgets.QWidget):
    def __init__(self, controller: "ToolbarController"):
        super().__init__()
        self.setLayout(QtWidgets.QHBoxLayout())
        self.select_component_widget = SelectComponentWidget(controller.select_component_controller)
        self.layout().addWidget(self.select_component_widget)
        self.select_time_widget = None
