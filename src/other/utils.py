from typing import Union, Iterable, TypeVar

from PyQt5 import QtGui, QtWidgets

from constants import COMPONENTS


def color_from_ratio(ratios: Union[list[float], dict[str, float]]):
    if isinstance(ratios, list):
        ratios = {k: v for k, v in zip(COMPONENTS, ratios)}
    return ComponentColor(ratios)


def index_to_2D(index: int, shape: tuple[int, int]) -> tuple[int, int]:
    """
    Convert the number from unidimensional to 2 dimensional
    :param index: the index to convert
    :param shape: Rows, Column
    :return:
    """
    return index // shape[0], index % shape[1]


class ComponentColor(QtGui.QColor):
    WATER = QtGui.QColor("blue")
    AIR = QtGui.QColor("white")
    LAND = QtGui.QColor("brown")
    DICT = dict()  # Saves the ratio used for that color

    def __init__(self, ratios: dict[str, float], *args, **kwargs):
        self.ratios = ratios
        super().__init__(*args, **kwargs)
        self.setRed(int(ComponentColor.WATER.red() * ratios.get("WATER", 0)) +
                    int(ComponentColor.AIR.red() * ratios.get("AIR", 0)) +
                    int(ComponentColor.LAND.red() * ratios.get("LAND", 0)))

        self.setGreen(int(ComponentColor.WATER.green() * ratios.get("WATER", 0)) +
                      int(ComponentColor.AIR.green() * ratios.get("AIR", 0)) +
                      int(ComponentColor.LAND.green() * ratios.get("LAND", 0)))

        self.setBlue(int(ComponentColor.WATER.blue() * ratios.get("WATER", 0)) +
                     int(ComponentColor.AIR.blue() * ratios.get("AIR", 0)) +
                     int(ComponentColor.LAND.blue() * ratios.get("LAND", 0)))
        ComponentColor.DICT[self.rgb()] = ratios


class LabelledWidget(QtWidgets.QWidget):
    def __init__(self, widget_class: type[QtWidgets.QWidget], label: str, *, vertical: bool = True):
        super().__init__()
        self.widget_object = widget_class()
        self.setLayout(QtWidgets.QVBoxLayout() if vertical else QtWidgets.QHBoxLayout())
        self.layout().addWidget(QtWidgets.QLabel(label))
        self.layout().addWidget(self.widget_object)

    def __getattr__(self, item):
        """
        Redirects the attribute getting to the spinbox for abstraction
        :param item: the attribute to get (example the size, the value, the maximum value, etc ...)
        :return:
        """
        return self.widget_object.__getattribute__(item)
