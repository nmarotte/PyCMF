import PyQt5.QtWidgets as QtWidgets


class AggregationWidget(QtWidgets.QWidget):
    model_name: str = None

    def __init__(self, model_instance, parent: QtWidgets.QWidget = None):
        self.model_instance = model_instance
        super().__init__(parent=parent)
        self.layout = QtWidgets.QVBoxLayout()
        for key, value in self.model_instance.__dict__.items():
            vertical_layout = QtWidgets.QVBoxLayout()
            vertical_layout.addWidget(QtWidgets.QLabel(key, parent=self))
            line_edit = QtWidgets.QLineEdit(str(value), parent=self)
            line_edit.setReadOnly(True)
            line_edit.show()
            vertical_layout.addWidget(line_edit)
            self.layout.addLayout(vertical_layout)
        self.setLayout(self.layout)
        self.show()
