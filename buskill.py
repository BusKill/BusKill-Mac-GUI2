import PyQt5.QtWidgets as Qt
from PyQt5 import *
from PyQt5.QtCore import QThread
import sys
import os
import fnmatch
import subprocess
import datetime
from pathlib import Path

class MainWindow(Qt.QMainWindow):

    def __init__(self):
        super().__init__()

        self.VERSION_NO = "V1.0"
        self.setWindowTitle("BusKill Mac")
        self.setFixedSize(500,250)
        
        self.APP_CTRL = Controller()
        self.APP_CONF = Configuration(self.APP_CTRL.CONFIGLOCATION)

        self.Triggers = self.APP_CTRL._getTriggers()
        self.Devices = self.APP_CTRL._getDevices()
        self.Configs = self.APP_CTRL._getConfig()

        self.Master = Qt.QWidget()
        self.MasterLayout = Qt.QVBoxLayout()
        self.Master.setLayout(self.MasterLayout)
        self.setCentralWidget(self.Master)

        #Tabs
        self.Tabs = Qt.QTabWidget(self)
        self.Tabs.setFixedSize(500,200)
        self.MainTab = Qt.QWidget(self)

        self.MainTab.layout = Qt.QGridLayout()
        self.MainTab.setLayout(self.MainTab.layout)

        #Left Pane Code
        self.RunWithOptionLabel = Qt.QLabel("Run with Options")
        self.RunWithOptionLabel.setFixedSize(175, 30)
        self.MainTab.layout.addWidget(self.RunWithOptionLabel, 0, 0)

        self.MainTriggerMenu = self._triggerDropDown(self.Triggers)
        self.MainTab.layout.addWidget(self.MainTriggerMenu, 1, 0)

        self.MainDeviceMenu = self._deviceDropDown(self.Devices)
        self.MainTab.layout.addWidget(self.MainDeviceMenu, 2, 0)

        if len(self.Devices) != 0 and len(self.Triggers) != 0:
            self.RunWithOption = Qt.QPushButton("Go!")
            self.RunWithOption.setFixedSize(179, 30)
            self.RunWithOption.clicked.connect(self._runBusKill)
            self.MainTab.layout.addWidget(self.RunWithOption, 3, 0)

        #Right Pane Code
        self.RunWithConfigLabel = Qt.QLabel("Run With Config")
        self.RunWithConfigLabel.setFixedSize(175, 30)
        self.MainTab.layout.addWidget(self.RunWithConfigLabel, 0, 2)

        self.MainConfigMenu = Qt.QComboBox(self)
        self.MainConfigMenu.setFixedSize(175, 30)
        if self.Configs is None:
            self.Configs = list()
        if len(self.Configs) != 0:
            self.MainConfigMenu.addItem("--config--")
            for entry in self.Configs:
                self.MainConfigMenu.addItem(entry)
        else:
            self.MainConfigMenu.addItem("No Config Found!")
        self.MainTab.layout.addWidget(self.MainConfigMenu, 1, 2)

        if len(self.Configs) != 0:
            self.RunWithConfig = Qt.QPushButton("Go!")
            self.RunWithConfig.setFixedSize(179, 30)
            self.RunWithConfig.clicked.connect(self._runBusKillWithConf)
            self.MainTab.layout.addWidget(self.RunWithConfig, 3, 2)

        self.Tabs.addTab(self.MainTab, "Main")

        self.ConfigTab = Qt.QWidget(self)
        self.ConfigTab.layout = Qt.QGridLayout()
        self.ConfigTab.layout.setContentsMargins(0, 10, 0, 10)
        self.ConfigTab.setLayout(self.ConfigTab.layout)

        self.ConfigureBusKillLabel = Qt.QLabel("Configure BusKill")
        self.ConfigureBusKillLabel.setFixedSize(175, 15)
        self.ConfigTab.layout.addWidget(self.ConfigureBusKillLabel, 1, 0)

        self.ConfigTriggerMenu = self._triggerDropDown(self.Triggers)
        self.ConfigTab.layout.addWidget(self.ConfigTriggerMenu, 2, 0)

        self.ConfigDeviceMenu = self._deviceDropDown(self.Devices)
        self.ConfigTab.layout.addWidget(self.ConfigDeviceMenu, 3, 0)

        self.ConfigSaveAs = Qt.QLineEdit(self)
        self.ConfigSaveAs.setFixedSize(175, 20)
        self.ConfigSaveAs.placeholderText()
        self.ConfigTab.layout.addWidget(self.ConfigSaveAs, 4, 0)

        self.SaveConfig = Qt.QPushButton("Save Configuration")
        self.SaveConfig.setFixedSize(175, 25)
        self.SaveConfig.clicked.connect(self._createBusKillConf)
        self.ConfigTab.layout.addWidget(self.SaveConfig, 5, 0)

        self.Tabs.addTab(self.ConfigTab, "Config")

        self.MasterLayout.addWidget(self.Tabs)

        #Dock
        self.Dock = Qt.QWidget()
        self.DockContainer = Qt.QHBoxLayout()
        self.Dock.setLayout(self.DockContainer)

        self.VersionNumberLabel = Qt.QLabel("Version: " + self.VERSION_NO)
        self.DockContainer.addWidget(self.VersionNumberLabel)

        self.RefreshButton = Qt.QPushButton("Refresh")
        self.RefreshButton.setFixedSize(100, 25)
        self.RefreshButton.clicked.connect(self._refreshPage)
        self.DockContainer.addWidget(self.RefreshButton)

        self.MasterLayout.addWidget(self.Dock)

    def _triggerDropDown(self, Trigger_List):
        TriggerDropDown = Qt.QComboBox()
        TriggerDropDown.setFixedSize(175, 30)
        if len(Trigger_List) != 0:
            TriggerDropDown.addItem("--Trigger--")
            for entry in Trigger_List:
                TriggerDropDown.addItem(entry)
        else:
            TriggerDropDown.addItem("No Triggers Found!")
            self.APP_CTRL._errorHandling("Critical", "No Triggers Found!")

        return TriggerDropDown

    def _deviceDropDown(self, Device_List):
        DeviceDropDown = Qt.QComboBox()
        DeviceDropDown.setFixedSize(175, 30)
        if len(Device_List) != 0:
            DeviceDropDown.addItem("--Device--")
            for entry in Device_List:
                DeviceDropDown.addItem(entry)
        else:
            DeviceDropDown.addItem("No Devices Found!")
            self.APP_CTRL._errorHandling("Crtitcal", "No Usable Devices Found")

        return DeviceDropDown

    def _refreshPage(self):
        self.APP_CTRL._refreshView(self)

    def _runBusKill(self):
        self.Trigger = self.MainTriggerMenu.currentText()
        self.Device = self.MainDeviceMenu.currentText()
        if self.APP_CTRL._validation(self.Trigger, self.Device) == True:
            self.hide()
            self.runpage = BusKill_Run(self.Trigger, self.Device)
            self.runpage.show()
        else:
            return

    def _runBusKillWithConf(self):
        Vars = self.APP_CONF._getConf(self.MainConfigMenu.currentText())
        try:
            if self.APP_CTRL._validation(Vars[0], Vars[1]) == True:
                self.hide()
                self.runpage = BusKill_Run(Vars[0], Vars[1])
                self.runpage.show()
        except TypeError:
            self.APP_CTRL._errorHandling("Info", "You must select a config file")

    def _createBusKillConf(self):
        if self.APP_CTRL._validation(self.ConfigTriggerMenu.currentText(), self.ConfigDeviceMenu.currentText()) == True:
            self.APP_CONF._createConfig(self.ConfigSaveAs.text(), self.ConfigDeviceMenu.currentText(), self.ConfigTriggerMenu.currentText())
            self.update()
        else:
            self.APP_CTRL._errorHandling("Critical", "Validation Failed, Configuration not saved")

class BusKill_Run(Qt.QMainWindow):

    def __init__(self, Trigger, Device):

        super().__init__()
        self.APP_CTRL = Controller()

        self.setWindowTitle("BusKill Mac - running")
        self.setFixedSize(200, 200)

        wid = Qt.QWidget(self)
        self.setCentralWidget(wid)
        self.Layout = Qt.QGridLayout(self)
        wid.setLayout(self.Layout)

        self.IsRunningLabel = Qt.QLabel("BusKill is running")
        self.IsRunningLabel.setFixedSize(175, 30)
        self.Layout.addWidget(self.IsRunningLabel, 0, 0)

        self.TriggerLabel1 = Qt.QLabel("Trigger:")
        self.TriggerLabel1.setFixedSize(175, 30)
        self.Layout.addWidget(self.TriggerLabel1, 1, 0)

        self.TriggerLabel2 = Qt.QLabel(Trigger)
        self.TriggerLabel2.setFixedSize(175, 30)
        self.Layout.addWidget(self.TriggerLabel2, 1, 1)

        self.DeviceLabel1 = Qt.QLabel("Device:")
        self.DeviceLabel1.setFixedSize(175, 30)
        self.Layout.addWidget(self.DeviceLabel1, 2, 0)

        self.DeviceLabel2 = Qt.QLabel(Device)
        self.DeviceLabel2.setFixedSize(175, 30)
        self.Layout.addWidget(self.DeviceLabel2, 2, 1)

        self.CloseButton = Qt.QPushButton("Stop BusKill")
        self.CloseButton.setFixedSize(175, 30)
        self.CloseButton.clicked.connect(self._backToMain)
        self.Layout.addWidget(self.CloseButton, 3, 0, 1, 0)

        self.show()
        self.run = Runtime(Trigger, Device)
        self.run.start()

    def _backToMain(self):
        self.run.stop()
        self.close()
        self.Main = MainWindow()
        self.Main.show()

class Controller:

    def __init__(self):
        self.APPROOT = self._getAppRoot()
        self.LOGLOCATION = self.APPROOT + "/Logging/"
        self.TRIGLOCATION = self.APPROOT + "/Triggers/"
        self.RESOURCELOCATION = self.APPROOT + "/Reosurces/"
        self.CONFIGLOCATION = self.APPROOT + "/Config/"

    def _refreshView(self, Main):
        Main.hide()
        self.New = MainWindow()
        self.New.show()
        
    def _getAppRoot(self): 
        self.path = os.path.abspath(__file__).split("/")
        del self.path[len(self.path) - 1]
        return "/".join(self.path)

    def _getTriggers(self):
        try:
            self.Triggers = list()
            self.dirlist = os.listdir(self.TRIGLOCATION)
            for dir in self.dirlist:
                if os.path.isdir(os.path.join(self.TRIGLOCATION, dir)) == True:
                    self.Triggers.append(dir)
            return self.Triggers
        except FileNotFoundError:
            self._errorHandling("Critical", "No Triggers Found")
            return ["0"]

    def _getDevices(self):
        self.Devices = os.listdir("/dev")
        self.Disk_Devices = list()
        for Device in self.Devices:
            if fnmatch.fnmatch(Device, "*disk*"):
                if Device.startswith("r") == False:
                    if fnmatch.fnmatch(Device, "*isk*s*") == False:
                        if Device.endswith("1") == False:
                            if Device.endswith("0") == False:
                                self.Disk_Devices.append(Device)
        return self.Disk_Devices

    def _getConfig(self):
        try:
            self.Config = list()
            self.dirlist = os.listdir(self.CONFIGLOCATION)
            for File in self.dirlist:
                if File.endswith("BSConf"):
                    self.Config.append(File)
            return self.Config
        except FileNotFoundError:
            self._writeLog("INFO", "Check for config... None Found")

    def _executeTrigger(self, Trigger):
        subprocess.call("python " + self.TRIGLOCATION + Trigger + "/Trigger.py", shell = True)

    def _checkDevice(self, Device):
        if os.path.exists("/dev/"+Device) == True:
            return True
        else:
            return False

    def _validation(self, Trigger ,Device):
        Dev = False
        if Device is not None:
            if Device != "--Device--":
                if Device != "No Devices Found!":
                    if self._checkDevice(Device) != False:
                        Dev = True
                    else:
                        self._errorHandling("info", "Device Could not be found, may have been prematurely removed")
                else:
                    self._errorHandling("Info", "This placeholder cannot be used, but no devices were found")
            else:
                Dev = False
                self._errorHandling("Info", "Device Cannot be placeholder")
        else:
            Dev = False 
            self._errorHandling("Critical", "Device Cannot be None")

        Trig = False
        if Trigger is not None:
            if Trigger != "No Triggers Found!":
                if Trigger != "--Trigger--":
                    if os.path.exists(self.APPROOT + "/Triggers/" + Trigger + "/Trigger.py"):
                        Trig = True
                    else:
                        self._errorHandling("critical", "Trigger.py could not be found in selected Trigger")
                else:
                    self._errorHandling("Info", "This placeholder cannot be used, but no triggers were found")
            else:
                self._errorHandling("Info", "Trigger Cannot be placeholder")
        else:
            self._errorHandling("Critical", "Device Cannot be None")
        return Dev & Trig
    #unsupported
    #def _exportLog(self):
        #function = None
    #unsupported
    #def _selectLogSaveLocation(self):
        #function = None
    #unsupported
    #def _selectTriggerInstaller(self):
        #function = None
    
    def _writeLog(self, Severity, Message):
        log = self.LOGLOCATION + "Log - " + str(datetime.date.today())
        attempt = 0
        while attempt != 2:
            try:
                with open(log, "a") as Log:
                    Log.write(str(datetime.datetime.now().ctime()) + " - " + Severity + " - " + Message + "\n")  
                    attempt = 2
            except FileNotFoundError:
                Path(log).touch()
                attempt+=1
                if attempt == 2:
                    BusKill_CritMessage("Log File could not be created/Found")

    def _errorHandling(self, Severity, Message):
        if Severity.lower() == "critical":
            BusKill_CritMessage(Message)
        elif Severity.lower() == "info":
            BusKill_InfoMessage(Message)

        self._writeLog(Severity, Message)

class Runtime(QThread):

    def __init__(self, Trigger, Device):
        QThread.__init__(self)
        self.APP_CTRL = Controller()
        self.Trigger = Trigger
        self.Device = Device
        self.runs = True

    def __del__(self):
        self.wait()

    def run(self):
        Triggered = False
        while Triggered == False and self.runs == True:
            if self.APP_CTRL._checkDevice(self.Device) == False:
                self.APP_CTRL._executeTrigger(self.Trigger)
                Triggered = True
                sys.exit()

    def stop(self):
        self.runs = False

class Configuration:

    def __init__(self, CONFIGLOCATION):
        self.APP_CTRL = Controller()
        self.CONFIGLOCATION = CONFIGLOCATION

    def _createConfig(self, name, Device, Trigger):
        config = self.CONFIGLOCATION + name + ".BSConf"
        attempt = 0 
        while attempt != 2:
            try:
                if os.path.exists(config):
                    self.APP_CTRL._errorHandling("Critical", "Configuration file already exists")
                    attempt = 2
                else:
                    with open(config,"a") as NewConfig:
                        NewConfig.write("THIS FILE CAN BE MODIFIED MANUALLY. IF IT FAILS VALIDATION PLEASE CLEAR CONFIGURATION \n")
                        NewConfig.write("Trigger:"+Trigger+"\n")
                        NewConfig.write("Device:"+Device+"\n")
                        NewConfig.write("this file was generated by buskill")
                        attempt = 2
            except FileNotFoundError:
                Path(config).touch
                attempt+=1
                if attempt == 2:
                    self.APP_CTRL._errorHandling("Critical", "Configuration File could not be generated")

    def _getConf(self, name):
        self.values = []
        try:
            with open(self.CONFIGLOCATION+name) as Conf:
                Data = Conf.readlines()
                self.values.append(Data[1].split(":")[1].rstrip())
                self.values.append(Data[2].split(":")[1].rstrip())
                return self.values
        except IOError:
            if name != "--config--":
                self.APP_CTRL._errorHandling("Critical", "Configuration File could not be read")

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

def main():
    app = Qt.QApplication(sys.argv)
    UI = MainWindow()
    UI.show()
    app.exec_()
    sys.exit(app.exec_())

main()