import threading
from typing import Optional

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
from PyQt5 import QtCore

import views.sub.earth.TopLayout.TopLayout as TopLayout
import views.sub.earth.BotLayout.BotLayout as BotLayout
from controller.controllers import *
from models.Earth.earth import Earth
from universe import Universe


class EarthView(QtWidgets.QWidget, StartButtonController, PauseButtonController, StopButtonController,
                ResumeButtonController, ClearButtonController):
    MODEL_SHAPE = (400, 400)

    def clear_pressed(self):
        self.bot_layout.clear_canvas()

    def start_pressed(self):
        self.bot_layout.set_canvas_enabled(False)
        self.__rebuild_simulation()
        self.__start_simulation()
        self.__update_loop_earth_info()

    def pause_pressed(self):
        self.bot_layout.set_canvas_enabled(True)
        self.__pause_simulation()

    def resume_pressed(self):
        self.bot_layout.set_canvas_enabled(False)
        self.__resume_simulation()

    def stop_pressed(self):
        self.bot_layout.set_canvas_enabled(True)
        self.__stop_simulation()

    def is_simulation_running(self):
        return self.model.running

    def __init__(self, model: Earth = None):
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
        self.bot_layout = BotLayout.BotLayout(controller=self)
        self.layout().addWidget(self.bot_layout)

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

    def __rebuild_simulation(self):
        self.model = Earth.from_qimage(self.bot_layout.get_canvas_as_qimage(), color_dict_ratio=self.color_to_ratios)

    def __start_simulation(self):
        self.simulation_thread = threading.Thread(target=self.model.start_simulation, args=())
        self.simulation_thread.start()

    def __pause_simulation(self):
        self.model.pause_updating()

    def __resume_simulation(self):
        self.simulation_thread = threading.Thread(target=self.model.resume_updating, args=())
        self.simulation_thread.start()

    def __stop_simulation(self):
        self.model.stop_updating()
        self.simulation_thread = None

    def __update_loop_earth_info(self):
        self.update_earth_info_thread = QtCore.QTimer()
        self.update_earth_info_thread.timeout.connect(self.bot_layout.update_earth_info)
        self.update_earth_info_thread.start(1000)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    uni = Earth(shape=EarthView.MODEL_SHAPE)
    earth_view = EarthView(model=uni)
    earth_view.show()
    app.exec()
