import threading
from typing import TYPE_CHECKING, Optional

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import Qt

import views.sub.earth.Canvas.EarthCanvas as EarthCanvas
import views.sub.earth.TopLayout.TopLayout as TopLayout
from controller.controllers import *
from models.Earth.earth import Earth
from universe import Universe


class EarthView(QtWidgets.QWidget, StartButtonController, PauseButtonController, StopButtonController,
                ResumeButtonController, ClearButtonController):
    def clear_pressed(self):
        self.canvas.clear()

    def start_pressed(self):
        # Locks the canvas
        self.canvas.setEnabled(False)
        # Starts the simulation
        self.model.running = True
        self.model.earth = Earth.from_qimage(self.canvas.label.pixmap().toImage(),
                                             color_dict_ratio=self.color_to_ratios)
        self.simulation_thread = threading.Thread(target=self.model.start_updating, args=())
        self.simulation_thread.start()

    def pause_pressed(self):
        # Unlocks the canvas
        self.canvas.setEnabled(True)
        self.model.running = False

    def resume_pressed(self):
        self.canvas.setEnabled(False)
        self.model.running = True
        self.simulation_thread = threading.Thread(target=self.model.start_updating, args=())
        self.simulation_thread.start()

    def stop_pressed(self):
        # Unlocks the canvas
        self.canvas.setEnabled(True)
        self.model.running = False
        self.simulation_thread = None

    def is_simulation_running(self):
        return self.model.running

    def __init__(self, model: Universe = None):
        super().__init__()
        self.color_to_ratios = {}
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
        if value is None:
            return
        res = QtGui.QColor(
            (int(QtGui.QColor("blue").red() * value[0]) + int(QtGui.QColor("white").red() * value[1]) + int(
                QtGui.QColor("brown").red() * value[2])),
            (int(QtGui.QColor("blue").green() * value[0]) + int(QtGui.QColor("white").green() * value[1]) + int(
                QtGui.QColor("brown").green() * value[2])),
            (int(QtGui.QColor("blue").blue() * value[0]) + int(QtGui.QColor("white").blue() * value[1]) + int(
                QtGui.QColor("brown").blue() * value[2]))
        )
        if res.rgb() not in self.color_to_ratios:
            self.color_to_ratios[res.rgb()] = value
        return res


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    uni = Universe()
    uni.setup()
    earth_view = EarthView(model=uni)
    earth_view.show()
    app.exec()
