import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
from PyQt5.QtCore import Qt

import views.sub.earth.Canvas.EarthCanvas as EarthCanvas
from views.sub.earth.TopLayout.TopLayout import TopLayout


class EarthView(QtWidgets.QWidget):
    button_labels = ("Add Water", "Add Air", "Add Land")

    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        self.top_layout = TopLayout()
        self.canvas = EarthCanvas.EarthCanvas(parent=self)

        self.layout().addWidget(self.top_layout)
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

    def clear_canvas(self):
        self.canvas.clear()
        print("cleareing canvas")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    uni = EarthView()
    uni.show()
    app.exec()
