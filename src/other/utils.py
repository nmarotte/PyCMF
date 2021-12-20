from typing import Union

from PyQt5 import QtGui

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
