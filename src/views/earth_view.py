import threading
from typing import TYPE_CHECKING, Optional

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
from PyQt5.QtCore import Qt

import views.sub.earth.Canvas.EarthCanvas as EarthCanvas
import views.sub.earth.TopLayout.TopLayout as TopLayout
from controller.controllers import *
from universe import Universe


class EarthView(QtWidgets.QWidget, StartButtonController, PauseButtonController, StopButtonController, ResumeButtonController, ClearButtonController):
    def clear_pressed(self):
        self.canvas.clear()

    def start_pressed(self):
        # Locks the canvas
        self.canvas.setDisabled(True)
        # Starts the simulation
        self.model.running = True
        self.simulation_thread = threading.Thread(target=self.model.start_updating, args=())
        self.simulation_thread.start()

    def pause_pressed(self):
        # Unlocks the canvas
        self.canvas.setDisabled(False)
        self.model.running = not self.model.running

    def resume_pressed(self):
        pass

    def stop_pressed(self):
        # Unlocks the canvas
        self.canvas.setDisabled(False)
        self.model.running = False

    def is_simulation_running(self):
        return self.model.running

    button_labels = ("Add Water", "Add Air", "Add Land")

    def __init__(self, model: Universe = None):
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        # Creates the connection to the model, and its thread for smooth parallel execution
        self.model = model
        self.simulation_thread: Optional[threading.Thread] = None

        # Creates the top tool bar
        self.top_layout = TopLayout.TopLayout(controller=self)
        self.layout().addWidget(self.top_layout)

        # Create the bottom drawing canvas/simulation view
        self.canvas = EarthCanvas.EarthCanvas(parent=self)
        self.layout().addWidget(self.canvas)

    def get_brush_width(self):
        return self.top_layout.get_brush_width()

    def get_brush_color(self):
        value = self.top_layout.paint_component_selector.get_value()
        if value == self.top_layout.COMPONENTS[0]:  # Water
            return QtGui.QColor("blue")
        elif value == self.top_layout.COMPONENTS[1]:  # Air
            return QtGui.QColor("white")
        elif value == self.top_layout.COMPONENTS[2]:  # Land
            return QtGui.QColor("brown")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    uni = Universe()
    uni.setup()
    earth_view = EarthView(model=uni)
    earth_view.show()
    app.exec()
