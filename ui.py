import sys

from PyQt5 import QtWidgets, uic


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("ui/main_window.ui", self)
        self.show()


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    Ui()
    app.exec_()


if __name__ == "__main__":
    main()
