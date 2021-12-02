from typing import TYPE_CHECKING

import PyQt5.QtWidgets as QtWidgets

from universe import Universe
if TYPE_CHECKING:
    from sun import Sun
    from models.Earth.earth import Earth
from views.EarthWidget import EarthWidget
from views.SunWidget import SunWidget


class UniverseWidget(QtWidgets.QWidget):
    def __init__(self, model_instance: "Universe", parent: QtWidgets.QWidget = None):
        super().__init__(parent=parent)
        self.setMinimumHeight(400)
        self.setMinimumWidth(400)
        self.tabs = QtWidgets.QTabWidget(self)
        self.__add_sun_tab(model_instance.sun)
        self.__add_earth_tab(model_instance.earth)
        self.show()

    def __add_sun_tab(self, model_instance: "Sun"):
        sun = SunWidget(model_instance, parent=self)
        self.tabs.addTab(sun, sun.model_name)

    def __add_earth_tab(self, model_instance: "Earth"):
        sun = EarthWidget(model_instance, parent=self)
        self.tabs.addTab(sun, sun.model_name)