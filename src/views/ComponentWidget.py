import PyQt5.QtWidgets as QtWidgets


class ComponentWidget(QtWidgets.QWidget):
    model_name: str = None

    def __init__(self, model_instance=None, parent: QtWidgets.QWidget = None):
        self.model_instance = model_instance
        super().__init__(parent=parent)
        self.layout = QtWidgets.QVBoxLayout()
        for key, value in self.model_instance.__dict__.items():
            line_edit = QtWidgets.QLineEdit(str(value), parent=self)
            line_edit.setReadOnly(True)
            line_edit.setToolTip(key)
            line_edit.show()
            self.layout.addWidget(line_edit)
        self.setLayout(self.layout)
        self.show()

    def as_table_widget_item(self):
        if self.model_instance is None:
            return None, None, None
        temperature = QtWidgets.QTableWidgetItem(str(self.model_instance.temperature))
        volume = QtWidgets.QTableWidgetItem(str(self.model_instance.volume))
        mass = QtWidgets.QTableWidgetItem(str(self.model_instance.mass))
        return temperature, volume, mass
