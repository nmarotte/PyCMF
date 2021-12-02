import PyQt5.QtWidgets as QtWidgets

class MainView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.__add_button("Earth (None)")
        self.__add_button("Sun (None)")
        self.setMinimumSize(300, 485)

    def __add_button(self, label: str):
        button = QtWidgets.QPushButton(label)
        button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.layout().addWidget(button)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    uni = MainView()
    uni.show()
    app.exec()
