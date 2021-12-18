from typing import TYPE_CHECKING

import PyQt5.QtWidgets as QtWidgets

from views.sub.earth.TopLayout.ClearButton import ClearButton
from views.sub.earth.TopLayout.ComponentAdder.ComponentAdder import ComponentAdder
from views.sub.earth.TopLayout.ComponentPainter.PaintComponentToolView import PaintComponentToolView
import views.sub.earth.TopLayout.SimulationControls.SimulationControls as SimulationControls

if TYPE_CHECKING:
    from a_views.earth_view import MainView


class TopLayout(QtWidgets.QWidget):
    COMPONENTS = "WATER", "AIR", "LAND"

    def __init__(self, controller: "MainView"):
        self.controller = controller
        super().__init__()
        self.setLayout(QtWidgets.QHBoxLayout())
        self.component_adder = ComponentAdder(TopLayout.COMPONENTS)
        self.paint_component_selector = PaintComponentToolView(TopLayout.COMPONENTS)
        self.clear_button = ClearButton(controller=self.controller)
        self.simulation_controls = SimulationControls.SimulationControls(controller=self.controller)

        self.layout().addWidget(self.component_adder)
        self.layout().addWidget(self.paint_component_selector)
        self.layout().addWidget(self.clear_button)
        self.layout().addWidget(self.simulation_controls)

    def get_component_to_paint(self):
        return self.paint_component_selector.get_value()

    def get_brush_width(self):
        return self.paint_component_selector.brush_size_selector.get_component_ratios()

    def clear_pressed(self):
        self.parent().clear_canvas()

    def start_pressed(self):
        self.parent().start_simulation()
