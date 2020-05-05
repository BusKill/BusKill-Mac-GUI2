import os
import fnmatch
import sys
import subprocess
import datetime
import BusKill_GUIElements
from pathlib import Path
from PyQt5.QtCore import QThread

class Controller:

    def __init__(self):
        self.GETAPPROOT = self._getAppRoot()
        self.LOGLOCATION = self.GETAPPROOT + "/Logging/"
        self.TRIGLOCATION = self.GETAPPROOT + "/Triggers/"
        self.RESOURCELOCATION = self.GETAPPROOT + "/Reosurces/"
        self.CONFIGLOCATION = self.GETAPPROOT + "/Config/"

    def _getAppRoot(self):
        self.path = os.path.abspath(__file__).split("/")
        del self.path[len(self.path) - 1]
        del self.path[len(self.path) - 1]
        return "/".join(self.path)

    def _getTriggers(self):
        try:
            self.Triggers = []
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
        self.Disk_Devices = []
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
            self.Config = []
            self.dirlist = os.listdir(self.CONFIGLOCATION)
            for file in self.dirlist:
                if file.endswith("BSConf"):
                    self.Config.append(file)
            return self.Config
        except FileNotFoundError:
            self._writeLog("INFO", "Check for config... None Found")
            pass

    def _executeTrigger(self, Trigger):
        subprocess.call("python " + self.TRIGLOCATION + Trigger + "/Trigger.py", shell = True)

    def _checkDevice(self, Device):
        if os.path.exists("/dev/"+Device) == True:
            return True
        else:
            return False
            #add WriteLog in here

    def _validation(self, Trigger ,Device):
        Trig = True
        Dev = True
        #add some actual validation in here.
        #add some specific self._errorHandling() Messages Depending on what has failed Validation
        return Trig and Dev

    #unsupported
    def _createConfig(self):
        function = None
    #unsupported
    def _exportLog(self):
        function = None
    #unsupported
    def _selectLogSaveLocation(self):
        function = None
    #unsupported
    def _selectTriggerInstaller(self):
        function = None
    
    def _writeLog(self, Severity, Message):
        log = self.LOGLOCATION + "Log - " + str(datetime.date.today())
        attempt = 0
        while attempt != 2:
            try:
                with open(log, "a") as Log: #not sure if this will work, may require manual creation
                    Log.write(str(datetime.datetime.now().ctime()) + " - " + Severity + " - " + Message + "\n")  
                    attempt = 2
            except FileNotFoundError:
                Path(log).touch()
                attempt+=1
                if attempt == 2:
                    BusKill_GUIElements.BusKill_CritMessage("Log File could not be created/Found")

    def _errorHandling(self, Severity, Message):
        if Severity.lower() == "critical":
            BusKill_GUIElements.BusKill_CritMessage(Message)
        elif Severity.lower() == "informative":
            BusKill_GUIElements.BusKill_InfoMessage(Message)

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
        return

    def stop(self):
        self.runs = False

class Configuration: #This Class will need to be fixed

    def __init__(self, CONFIGLOCATION):
        self.APP_CTRL = Controller()
        self.CONFIGLOCATION = CONFIGLOCATION

    def _createConfig(self, name, Device, Trigger):
        config = self.CONFIGLOCATION + name + ".BSConf"
        attempt = 0 
        while attempt != 2:
            try:
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
            with open(self.CONFIGLOCATION+name+".BSConf") as Conf:
                self.values.append(Conf.readlines()[1].split(":")[1]) #Trigger
                self.values.append(Conf.readline()[2].split(":")[1]) #Device
                return self.values
        except IOError:
            self.APP_CTRL._errorHandling("Critical", "Configuration File could not be read")