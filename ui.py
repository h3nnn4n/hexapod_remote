import sys
import threading

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

        # button = self.findChild(QtWidgets.QAction, "actionExit")
        # button.clicked.connect(self.close_ui)  # type:ignore

        # button = self.findChild(QtWidgets.QAction, "actionQuit")
        # button.clicked.connect(self.close_ui)  # type:ignore

    def refresh(self):
        self.robot.update()

        leg1_position_label = self.findChild(QtWidgets.QLabel, "leg1_position_label")
        leg1_target_position_label = self.findChild(QtWidgets.QLabel, "leg1_target_position_label")
        leg1_final_position_label = self.findChild(QtWidgets.QLabel, "leg1_final_position_label")
        leg1_angles_label = self.findChild(QtWidgets.QLabel, "leg1_angles_label")
        leg1_error_label = self.findChild(QtWidgets.QLabel, "leg1_error_label")
        leg1_tolerance_label = self.findChild(QtWidgets.QLabel, "leg1_tolerance_label")
        leg1_speed_label = self.findChild(QtWidgets.QLabel, "leg1_speed_label")
        leg1_mode_label = self.findChild(QtWidgets.QLabel, "leg1_mode_label")

        assert leg1_position_label is not None
        assert leg1_target_position_label is not None
        assert leg1_final_position_label is not None
        assert leg1_angles_label is not None
        assert leg1_error_label is not None
        assert leg1_tolerance_label is not None
        assert leg1_speed_label is not None
        assert leg1_mode_label is not None

        leg1_position_label.setText(str(self.robot.legs[0].current_position))
        leg1_target_position_label.setText(str(self.robot.legs[0].target_position))
        leg1_final_position_label.setText(str(self.robot.legs[0].final_position))
        leg1_angles_label.setText(str(self.robot.legs[0].current_angles))
        leg1_error_label.setText(str(self.robot.legs[0].error))
        leg1_tolerance_label.setText(str(self.robot.legs[0].tolerance))
        leg1_speed_label.setText(str(self.robot.legs[0].speed))
        leg1_mode_label.setText(str(self.robot.legs[0].mode))

    def close_ui(self):
        self.app.exit(0)

        sys.exit()


def robot_thread(robot):
    robot.init()

    while True:
        pass


def main() -> None:
    robot = Robot()

    threads = [threading.Thread(target=robot_thread, args=(robot,))]
    for t in threads:
        t.start()

    app = QtWidgets.QApplication(sys.argv)
    window = Ui(app=app, robot=robot)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
