import random

import pyperclip
from PyQt5 import QtGui
from PyQt5 import QtWidgets as qtw

from gui_parts import main

import utils
import sys

class MouseEventLable(qtw.QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._image = QtGui.QPixmap()
        self.mouse_inputs = []
        self.finished = False

    def setup_callbacks(self, c1):
        self.show_progress_cl = c1

    def paintEvent(self, paint_event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self._image)  # FIXME: what this line do?
        pen = QtGui.QPen()
        pen.setWidth(2)
        pen.setColor(QtGui.QColor("#F00"))
        painter.setPen(pen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        for _ in range(5000):
            x, y = random.choice(range(0, self.width())), random.choice(range(0, self.height()))
            painter.drawPoint(x, y)
        
    def flush(self):
        self.mouse_inputs = []

    def mouseMoveEvent(self, event) -> None:
        if 0 <= event.x() <= self.width() and \
            0 <= event.y() <= self.height():
            if self.finished is True:
                self.flush()
                self.finished = False
            self.mouse_inputs.append((event.x(), event.y()))
            self.show_progress_cl(len(self.mouse_inputs))
        super().mouseMoveEvent(event)


class MainWindow(qtw.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = main.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.cp_clipboard.clicked.connect(self.copy_password)
        self.ui.save_file.clicked.connect(self.save_password)
        self.ui.pushButton_2.clicked.connect(self.copy_passphrase)
        self.ui.pushButton_3.clicked.connect(self.save_passphrase)
        self.ui.pushButton.clicked.connect(self.copy_passpoint)
        self.ui.pushButton_4.clicked.connect(self.save_passpoint)

        self.setup_mouse_recorder()

    def setup_callbacks(self, c1, c2, c3):
        self.create_password_cl = c1
        self.create_passphrase_cl = c2
        self.create_passpoint_cl = c3

    def setup_mouse_recorder(self):
        self.lbl = MouseEventLable()
        self.lbl.setStyleSheet("background-color: #000;")
        self.lbl.setFixedHeight(300)
        self.lbl.setFixedWidth(400)
        self.ui.mouse_lbl_box.addWidget(self.lbl)
        self.lbl.setup_callbacks(self.show_progress)

    def generate_password(self):
        length = self.ui.password_len_spin.value()
        if length <= 0:
            qtw.QMessageBox.warning(self, "Unsuccessful", f"Invalid length for password: {length}")
            return None
        return self.create_password_cl(length)

    def generate_passphrase(self):
        length = self.ui.passphrase_len_spin.value()
        if length <= 0:
            qtw.QMessageBox.warning(self, "Unsuccessful", f"Invalid length for passphrase: {length}")
            return None
        return self.create_passphrase_cl(length)

    def show_progress(self, value):

        # NOTE: this func recieves length of input list. we convert it to precent in here!
        value = int(value/1)
        self.ui.progressBar.setValue(value)
        if value == 100:
            self.finish_progress()

    def finish_progress(self):
        qtw.QMessageBox.information(self, "Good", "Mouse input successfully retrived.")
        self.lbl.finished = True

    def generate_passpoint(self):
        if len(self.lbl.mouse_inputs) == 0:
            qtw.QMessageBox.warning(self, "BAD", "Please record your mouse movement before doing this.")
            return
        passwd = self.create_passpoint_cl(self.lbl.mouse_inputs)
        self.lbl.flush()
        self.show_progress(0)
        return passwd

    def copy_password(self):
        passwd = self.generate_password()
        if passwd is None:
            return
        pyperclip.copy(passwd)
        qtw.QMessageBox.information(self, "Successfull", "Your password is now in your clipboard")

    def save_to_file(self, text: str, msg: str, format: str):
        filename, _ = qtw.QFileDialog.getSaveFileName(self, msg, "", format)
        if filename:
            with open(filename, "w") as f:
                f.write(text + "\n")

    def save_password(self):
        passwd = self.generate_password()
        if passwd is None:
            return
        self.save_to_file(passwd, "Save your password...", "Text Files (*.txt)")

    def copy_passphrase(self):
        passwd = self.generate_passphrase()
        if passwd is None:
            return
        pyperclip.copy(passwd)
        qtw.QMessageBox.information(self, "Successfull", "Your passphrase is now in your clipboard")

    def save_passphrase(self):
        passwd = self.generate_passphrase()
        if passwd is None:
            return
        self.save_to_file(passwd, "Save your passphrase...", "Text Files (*.txt)")

    def copy_passpoint(self):
        passwd = self.generate_passpoint()
        if passwd is None:
            return
        pyperclip.copy(passwd)
        qtw.QMessageBox.information(self, "Successfull", "Your passpoint is now in your clipboard")

    def save_passpoint(self):
        passwd = self.generate_passpoint()
        if passwd is None:
            return
        self.save_to_file(passwd, "Save your passpoint...", "Text Files (*.txt)")


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    win = MainWindow()
    win.setup_callbacks(
        utils.PassGenerator.new_password,
        utils.PassGenerator.new_pass_phrase,
        utils.PassGenerator.new_pass_point,
    )
    win.show()
    sys.exit(app.exec())

