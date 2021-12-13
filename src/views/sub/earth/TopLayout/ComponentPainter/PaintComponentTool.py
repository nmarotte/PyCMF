import PyQt5.QtWidgets as QtWidgets
import qtawesome as qta

from views.sub.earth.TopLayout.ComponentPainter.SelectComponentPopup import SelectComponentPopup


class PaintComponentTool(QtWidgets.QWidget):
    __value: list[float] = None

    class SelectComponentButton(QtWidgets.QPushButton):
        def __init__(self, *, parent: "PaintComponentTool" = None):
            super().__init__(f"Select Component\n Brush", parent=parent)
            self.clicked.connect(parent.select_component_button_clicked)

    class BrushSizeSelector(QtWidgets.QWidget):
        def __init__(self, parent: "PaintComponentTool" = None):
            super().__init__(parent=parent)
            self.setLayout(QtWidgets.QVBoxLayout())
            label = QtWidgets.QLabel("\uf1fc" + "Brush Size")
            label.setFont(qta.font('fa', 12))
            self.layout().addWidget(label)
            self.spinbox = QtWidgets.QSpinBox()
            self.spinbox.setValue(10)
            self.layout().addWidget(self.spinbox)
            self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        def get_value(self) -> int:
            return self.spinbox.value()

        def set_value(self, value: int):
            self.spinbox.setValue(value)

    def __init__(self, components: tuple[str, str, str]):
        self.components = components
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.layout().addWidget(PaintComponentTool.SelectComponentButton(parent=self))
        self.brush_size_selector = PaintComponentTool.BrushSizeSelector(parent=self)
        self.layout().addWidget(self.brush_size_selector)

    def get_brush_size(self):
        return self.brush_size_selector.get_value()

    def select_component_button_clicked(self):
        popup = SelectComponentPopup()
        popup.exec_()
        if popup.value:
            if self.__value is None:
                self.__value = [0] * len(popup.value)
            summed = sum(popup.value)
            for i, elem in enumerate(popup.value):
                if elem is not None:
                    self.__value[i] = popup.value[i]/summed

    def get_value(self) -> list[float]:
        if self.__value is None:
            msg = QtWidgets.QMessageBox()
            msg.setInformativeText('Please first select what component to paint')
            msg.exec_()
        return self.__value

    def set_value(self, value: list[float]):
        self.__value = value
