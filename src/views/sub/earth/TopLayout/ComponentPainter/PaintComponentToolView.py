import PyQt5.QtWidgets as QtWidgets
import qtawesome as qta
from typing import TYPE_CHECKING

from a_views.select_component_widget import SelectComponentWidget

if TYPE_CHECKING:
    from controller.ToolbarArea.subcontrollers.SelectComponent.controller import SelectComponentController


class PaintComponentToolView(QtWidgets.QWidget):
    class SelectComponentWidget(QtWidgets.QPushButton):
        # todo thesis write why its a subclass (because it is the implementation of its parent class, nobody else needs to know how it is done)
        def __init__(self, *, controller: "PainterController"):
            self.controller = controller
            super().__init__(f"Select Component\n Brush")
            self.clicked.connect(self.controller.select_component_button_clicked)

    class BrushSizeSelector(QtWidgets.QWidget):
        def __init__(self, controller: "PainterController" = None):
            self.controller = controller
            super().__init__()
            self.setLayout(QtWidgets.QVBoxLayout())

            label = QtWidgets.QLabel("\uf1fc" + "Brush Size")
            label.setFont(qta.font('fa', 12))
            self.layout().addWidget(label)

            self.spinbox = QtWidgets.QSpinBox()
            self.spinbox.setValue(10)
            self.spinbox.setSingleStep(5)
            self.layout().addWidget(self.spinbox)
            self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        def get_value(self) -> int:
            return self.spinbox.value()

        def set_value(self, value: int):
            self.spinbox.setValue(value)

    def __init__(self, controller: PainterController):
        self.controller = controller
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)

        # Add sub widgets
        self.layout().addWidget(SelectComponentWidget(controller=self.controller))
        self.layout().addWidget(PaintComponentToolView.BrushSizeSelector(controller=self.controller))

    def get_brush_size(self):
        return self.brush_size_selector.get_value()

    def get_value(self) -> list[float]:
        if self.__value is None:
            msg = QtWidgets.QMessageBox()
            msg.setInformativeText('Please first select what component to paint')
            msg.exec_()
        return self.__value

    def set_value(self, value: list[float]):
        self.__value = value
