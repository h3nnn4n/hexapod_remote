import sys
import threading
from time import sleep

from PyQt5 import QtWidgets, uic  # type:ignore

from hexapod_remote.robot import Robot


class Ui(QtWidgets.QMainWindow):
    def __init__(self, app, robot):
        super().__init__()
        self.app = app
        self.robot = robot

        self.setup_ui()
        self.show()

    def setup_ui(self):
        uic.loadUi("ui/main_window.ui", self)

        button = self.findChild(QtWidgets.QPushButton, "quitPushButton")
        button.clicked.connect(self.close_ui)  # type:ignore

        button = self.findChild(QtWidgets.QPushButton, "pushButton_Refresh")
        button.clicked.connect(self.refresh)  # type:ignore

        pushButton_leg1_move = self.findChild(QtWidgets.QPushButton, "pushButton_leg1_move")
        assert pushButton_leg1_move is not None
        pushButton_leg1_move.clicked.connect(self.move_leg)

        # button = self.findChild(QtWidgets.QAction, "actionExit")
        # button.clicked.connect(self.close_ui)  # type:ignore

        # button = self.findChild(QtWidgets.QAction, "actionQuit")
        # button.clicked.connect(self.close_ui)  # type:ignore

        self.refresh()

    def move_leg(self):
        try:
            lineEdit_leg1_x = self.findChild(QtWidgets.QLineEdit, "lineEdit_leg1_x")
            lineEdit_leg1_y = self.findChild(QtWidgets.QLineEdit, "lineEdit_leg1_y")
            lineEdit_leg1_z = self.findChild(QtWidgets.QLineEdit, "lineEdit_leg1_z")

            assert lineEdit_leg1_x is not None
            assert lineEdit_leg1_y is not None
            assert lineEdit_leg1_z is not None

            x = float(lineEdit_leg1_x.text())
            y = float(lineEdit_leg1_y.text())
            z = float(lineEdit_leg1_z.text())

            self.robot.legs[1].move_to(x, y, z)

            self.refresh()
        except Exception as e:
            print(f"failed to move leg with error {e}")

    def refresh(self):
        thread = threading.Thread(target=_refresh_ui, args=(self, self.robot))
        thread.start()

    def close_ui(self):
        self.app.exit(0)
        sys.exit()


def _refresh_ui(ui, robot, loop=False):
    if loop:
        sleep(1)

    while True:
        try:
            robot.legs[1].update_state()

            leg1_position_label = ui.findChild(QtWidgets.QLabel, "leg1_position_label")
            leg1_target_position_label = ui.findChild(QtWidgets.QLabel, "leg1_target_position_label")
            leg1_final_position_label = ui.findChild(QtWidgets.QLabel, "leg1_final_position_label")
            leg1_angles_label = ui.findChild(QtWidgets.QLabel, "leg1_angles_label")
            leg1_error_label = ui.findChild(QtWidgets.QLabel, "leg1_error_label")
            leg1_tolerance_label = ui.findChild(QtWidgets.QLabel, "leg1_tolerance_label")
            leg1_speed_label = ui.findChild(QtWidgets.QLabel, "leg1_speed_label")
            leg1_mode_label = ui.findChild(QtWidgets.QLabel, "leg1_mode_label")

            assert leg1_position_label is not None
            assert leg1_target_position_label is not None
            assert leg1_final_position_label is not None
            assert leg1_angles_label is not None
            assert leg1_error_label is not None
            assert leg1_tolerance_label is not None
            assert leg1_speed_label is not None
            assert leg1_mode_label is not None

            leg1_position_label.setText(str(robot.legs[1].current_position))
            leg1_target_position_label.setText(str(robot.legs[1].target_position))
            leg1_final_position_label.setText(str(robot.legs[1].final_position))
            leg1_angles_label.setText(str(robot.legs[1].current_angles))
            leg1_error_label.setText(str(robot.legs[1].error))
            leg1_tolerance_label.setText(str(robot.legs[1].tolerance))
            leg1_speed_label.setText(str(robot.legs[1].speed))
            leg1_mode_label.setText(str(robot.legs[1].mode))

            sleep(0.1)
        except Exception as e:
            print(f"failed to refresh ui with error {e}")

        if not loop:
            break


def robot_thread(robot):
    robot.init()


def main() -> None:
    robot = Robot()

    thread = threading.Thread(target=robot_thread, args=(robot,))
    thread.start()

    app = QtWidgets.QApplication(sys.argv)
    window = Ui(app=app, robot=robot)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
