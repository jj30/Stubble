import os
import wxModule
import wx
import json
import _winreg
import re

class FoundSoftware():
    def __init__(self):
        fileDonationInfo = open("./Donations.json")
        recognition = fileDonationInfo.read()
        recognitionJSON = json.loads(recognition)
        self.software = []

        for software in recognitionJSON:
            print "Looking for software package: " + software["name"]
            if "signatures" in software:
                for key in software["signatures"]:
                    if self.searchReg(key["regKey"]):
                        print "FOUND REG KEY:" + key["regKey"]
                        print "Software " + software["name"] + " is likely on this computer."
                        self.software.append(dict(name = software["name"], bitcoinAddress = software["bitcoinAddress"]))

    def searchReg(self, regKey):
        keyPath = regKey.split("\\")[0]
        key = "\\".join(regKey.split("\\")[1:])

        # so far all software has been found in HKEY_CLASSES_ROOT
        if keyPath == "HKEY_CLASSES_ROOT":
            mask = _winreg.HKEY_CLASSES_ROOT

        keyFound = _winreg.OpenKey(mask, key)
        name, value, type = _winreg.EnumValue(keyFound, 0)
        return value

    """
    #This will be uncommented if and when the filesystem is used
    # Usage:
        #if search("/", "cover.lpx"):
        #    print "FOUND"
    def search(start_path, match):
        for root, subFolder, files in os.walk(start_path):
            bFound = False
            regex = re.compile(match, re.IGNORECASE)

            for elem in files:
                m = regex.match(elem)
                if m:
                    if m.group():
                        if len(m.group()):
                            bFound = True
                            return bFound
    """

if __name__ == '__main__':
    app = wx.PySimpleApp()

    software = FoundSoftware().software
    frame = wxModule.MainForm(software)
    frame.donations = software
    frame.draw()
    frame.Show()

    app.MainLoop()
