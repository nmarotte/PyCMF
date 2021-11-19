import PyQt5.QtWidgets as QtWidgets

from Earth.Components.grid_component import GridComponent
from views.AggregationWidget import AggregationWidget


class EarthWidget(AggregationWidget):
    model_name = "Earth"

    def __init__(self, model_instance, parent: QtWidgets.QWidget = None):
        super().__init__(model_instance, parent=parent)
        if len(model_instance.shape) < 3:
            button = QtWidgets.QPushButton("Components", parent=self)
            button.clicked.connect(self.show_components)
            self.layout.addWidget(button)
        else:
            label = QtWidgets.QLabel("3D View not available", parent=self)
            self.layout.addWidget(label)

    def show_components(self):
        popup = QtWidgets.QDialog()
        layout = QtWidgets.QHBoxLayout()
        tabs = QtWidgets.QTabWidget(parent=popup)

        shape = self.model_instance.shape
        temperature_table = QtWidgets.QTableWidget(shape[0], shape[1], parent=self)
        volume_table = QtWidgets.QTableWidget(shape[0], shape[1], parent=self)
        mass_table = QtWidgets.QTableWidget(shape[0], shape[1], parent=self)

        for elem in self.model_instance:
            i, j = elem.index // shape[0], elem.index % shape[1]

            temperature_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(elem.temperature)))
            volume_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(elem.volume)))
            mass_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(elem.mass)))

        tabs.addTab(temperature_table, "Temperature")
        tabs.addTab(volume_table, "Volume")
        tabs.addTab(mass_table, "Mass")
        layout.addWidget(tabs)
        popup.setLayout(layout)
        popup.exec_()
