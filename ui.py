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
        assert button is not None
        button.clicked.connect(self.close_ui)

        button = self.findChild(QtWidgets.QPushButton, "pushButton_Refresh")
        assert button is not None
        button.clicked.connect(self.refresh)

        pushButton_leg1_move = self.findChild(QtWidgets.QPushButton, "pushButton_leg1_move")
        assert pushButton_leg1_move is not None
        pushButton_leg1_move.clicked.connect(self.move_leg)

        pushButton_leg1_instantaneous = self.findChild(QtWidgets.QPushButton, "pushButton_leg1_instantaneous")
        assert pushButton_leg1_instantaneous is not None
        pushButton_leg1_instantaneous.clicked.connect(self.set_instantaneous_mode)

        pushButton_leg1_constant_speed = self.findChild(QtWidgets.QPushButton, "pushButton_leg1_constant_speed")
        assert pushButton_leg1_constant_speed is not None
        pushButton_leg1_constant_speed.clicked.connect(self.set_constant_speed_mode)

        comboBox_command_leg_id = self.findChild(QtWidgets.QComboBox, "comboBox_command_leg_id")
        assert comboBox_command_leg_id is not None
        comboBox_command_leg_id.addItem("all")
        comboBox_command_leg_id.addItems([str(i + 1) for i in range(6)])

        self.refresh()

    def set_instantaneous_mode(self):
        self.robot.serial.set_leg_mode("INSTANTANEOUS")
        self.refresh()

    def set_constant_speed_mode(self):
        self.robot.serial.set_leg_mode("CONSTANT_SPEED")

        lineEdit_leg1_speed = self.findChild(QtWidgets.QLineEdit, "lineEdit_leg1_speed")
        assert lineEdit_leg1_speed is not None
        self.robot.serial.set_legs_speed(float(lineEdit_leg1_speed.text()))

        self.refresh()

    def move_leg(self):
        try:
            lineEdit_leg1_x = self.findChild(QtWidgets.QLineEdit, "lineEdit_leg1_x")
            lineEdit_leg1_y = self.findChild(QtWidgets.QLineEdit, "lineEdit_leg1_y")
            lineEdit_leg1_z = self.findChild(QtWidgets.QLineEdit, "lineEdit_leg1_z")
            comboBox_command_leg_id = self.findChild(QtWidgets.QComboBox, "comboBox_command_leg_id")

            assert lineEdit_leg1_x is not None
            assert lineEdit_leg1_y is not None
            assert lineEdit_leg1_z is not None
            assert comboBox_command_leg_id is not None

            x = float(lineEdit_leg1_x.text())
            y = float(lineEdit_leg1_y.text())
            z = float(lineEdit_leg1_z.text())
            leg_id = comboBox_command_leg_id.currentText()

            if leg_id == "all":
                self.robot.serial.disable_auto_send()
                for leg in self.robot.legs:
                    leg.move_to(x, y, z)
                self.robot.serial.send_commands()
                self.robot.serial.enable_auto_send()

                self.refresh()
            else:
                self.robot.legs[int(leg_id)].move_to(x, y, z)
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

            leg1_id_label = ui.findChild(QtWidgets.QLabel, "leg1_id_label")
            leg1_position_label = ui.findChild(QtWidgets.QLabel, "leg1_position_label")
            leg1_target_position_label = ui.findChild(QtWidgets.QLabel, "leg1_target_position_label")
            leg1_final_position_label = ui.findChild(QtWidgets.QLabel, "leg1_final_position_label")
            leg1_angles_label = ui.findChild(QtWidgets.QLabel, "leg1_angles_label")
            leg1_error_label = ui.findChild(QtWidgets.QLabel, "leg1_error_label")
            leg1_tolerance_label = ui.findChild(QtWidgets.QLabel, "leg1_tolerance_label")
            leg1_speed_label = ui.findChild(QtWidgets.QLabel, "leg1_speed_label")
            leg1_mode_label = ui.findChild(QtWidgets.QLabel, "leg1_mode_label")

            assert leg1_id_label is not None
            assert leg1_position_label is not None
            assert leg1_target_position_label is not None
            assert leg1_final_position_label is not None
            assert leg1_angles_label is not None
            assert leg1_error_label is not None
            assert leg1_tolerance_label is not None
            assert leg1_speed_label is not None
            assert leg1_mode_label is not None

            leg1_id_label.setText(str(robot.legs[1].leg_id))
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
