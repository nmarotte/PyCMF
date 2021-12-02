import PyQt5.QtWidgets as QtWidgets


class PaintComponentSelector(QtWidgets.QWidget):
    __value: str = "Water"

    class Button(QtWidgets.QPushButton):
        def __init__(self, component_type: str, *, parent: "PaintComponentSelector" = None):
            super().__init__(f"Paint {component_type}", parent=parent)
            self.clicked.connect(lambda: parent.set_value(component_type))

    def __init__(self, components: tuple[str, str, str]):
        self.components = components
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.setMaximumWidth(100)
        for i, b_l in enumerate(self.components):
            button = PaintComponentSelector.Button(b_l, parent=self)
            self.layout().addWidget(button)

    def get_value(self) -> str:
        return self.__value

    def set_value(self, value: str):
        self.__value = value
