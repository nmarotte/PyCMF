import PyQt5.QtWidgets as QtWidgets
import qtawesome as qta


class BrushSizeSelector(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
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
