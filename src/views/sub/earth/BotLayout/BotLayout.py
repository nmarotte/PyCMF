from typing import TYPE_CHECKING

import PyQt5.QtWidgets as QtWidgets

import views.sub.earth.BotLayout.EarthCanvas as EarthCanvas
import views.sub.earth.BotLayout.EarthInfoText as EarthInfoText

if TYPE_CHECKING:
    from a_views.earth_view import MainView


class BotLayout(QtWidgets.QWidget):
    def __init__(self, controller: "MainView"):
        self.controller = controller
        super().__init__()
        self.setLayout(QtWidgets.QHBoxLayout())
        self.canvas = EarthCanvas.EarthCanvas(controller=controller)
        self.earth_info = EarthInfoText.EarthInfoText(controller=controller)

        self.layout().addWidget(self.canvas)
        self.layout().addWidget(self.earth_info)

    def clear_canvas(self):
        self.canvas.clear()

    def set_canvas_enabled(self, value: bool):
        self.canvas.setEnabled(value)

    def get_canvas_as_qimage(self):
        return self.canvas.label.pixmap().toImage()
