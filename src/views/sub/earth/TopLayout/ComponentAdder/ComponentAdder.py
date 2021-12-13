import PyQt5.QtWidgets as QtWidgets


class ComponentAdder(QtWidgets.QWidget):
    class Button(QtWidgets.QPushButton):
        def __init__(self, component_type: str, *, parent: "ComponentAdder" = None):
            super().__init__(f"Add {component_type.capitalize()}", parent=parent)
            # self.clicked.connect(lambda: parent.set_value(component_type))

    def __init__(self, components: tuple[str, str, str]):
        self.components = components
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.setMaximumWidth(100)
        for i, b_l in enumerate(self.components):
            button = ComponentAdder.Button(b_l, parent=self)
            self.layout().addWidget(button)
