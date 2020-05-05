import PyQt5.QtWidgets as Qt
from PyQt5 import *
import sys


class BusKill_CritMessage:

    def __init__(self, Message):
        super().__init__()

        self.msg = Qt.QMessageBox()
        self.msg.setIcon(Qt.QMessageBox.Critical)
        self.msg.setWindowTitle("oops!")
        self.msg.setStandardButtons(Qt.QMessageBox.Ok)
        self.msg.setText("BusKill has ran into a Crtitcal Error")
        self.msg.setInformativeText(Message)
        self.msg.exec_()

class BusKill_InfoMessage:

    def __init__(self, Message):

        self.msg = Qt.QMessageBox()
        self.msg.setIcon(Qt.QMessageBox.Information)
        self.msg.setWindowTitle("oops!")
        self.msg.setStandardButtons(Qt.QMessageBox.Ok)
        self.msg.setText("BusKill has encountered something weird")
        self.msg.setInformativeText(Message)
        self.msg.exec_()
