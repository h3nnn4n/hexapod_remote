import sys

from PyQt5 import QtWidgets, uic


class Ui(QtWidgets.QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.setup_ui()
        self.show()

    def setup_ui(self):
        uic.loadUi("ui/main_window.ui", self)

        button = self.findChild(QtWidgets.QPushButton, "quitPushButton")
        button.clicked.connect(self.close_ui)  # type:ignore

        # button = self.findChild(QtWidgets.QAction, "actionExit")
        # button.clicked.connect(self.close_ui)  # type:ignore

        # button = self.findChild(QtWidgets.QAction, "actionQuit")
        # button.clicked.connect(self.close_ui)  # type:ignore

    def close_ui(self):
        self.app.exit(0)


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = Ui(app=app)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
