import json

import wx

import wxM


class FindSoftware():
    def __init__(self, sOS):
        fileDonationInfo = open("./Donations.json")
        recognition = fileDonationInfo.read()
        recognitionJSON = json.loads(recognition)
        self.software = []

        # if we're on Ubuntu, load the cache
        if sOS == "UBUNTU":
            cache = apt.Cache()

        for software in recognitionJSON:
            print "Looking for software package: " + software["name"]
            if "signatures" in software:
                for key in software["signatures"]:
                    # UBUNTU
                    if sOS == "UBUNTU":
                        try:
                            searchTarget = cache[key["apt-cache"]]
                            if key["apt-cache"] in searchTarget.fullname:
                                print "FOUND APT CACHE: " + key["apt-cache"]
                                print "Software " + software["name"] + " is likely on this computer."
                                self.software.append(dict(name = software["name"], bitcoinAddress = software["bitcoinAddress"], url = software["url"]))

                        except KeyError:
                            print "Ubuntu searching for " + software["name"] + " is unavailable."
                    else:
                        try:
                            if self.searchReg(key["regKey"]):
                                print "FOUND REG KEY:" + key["regKey"]
                                print "Software " + software["name"] + " is likely on this computer."
                                self.software.append(dict(name = software["name"], bitcoinAddress = software["bitcoinAddress"], url = software["url"]))
                        except KeyError:
                            # if no regKey was specified by the JSON, it does not apply.
                            pass

    def searchReg(self, regKey):
        keyPath = regKey.split("\\")[0]
        key = "\\".join(regKey.split("\\")[1:])

        # so far all software has been found in HKEY_CLASSES_ROOT
        if keyPath == "HKEY_CLASSES_ROOT":
            mask = _winreg.HKEY_CLASSES_ROOT
        elif keyPath == "HKEY_LOCAL_MACHINE":
            mask = _winreg.HKEY_LOCAL_MACHINE
        elif keyPath == "HKEY_CURRENT_USER":
            mask = _winreg.HKEY_CURRENT_USER

        try:
            keyFound = _winreg.OpenKey(mask, key)
            name, value, type = _winreg.EnumValue(keyFound, 0)
        except WindowsError:
            # keyFound = _winreg.KEY_WOW64_64KEY
            # working on a way to use 32-bit python to read from a 64-bit registry
            value = False
            pass

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
    import platform

    # Init'd as windows until mac time
    osType = "WINDOWS"
    osType = platform.platform()
    if "Linux" in osType:
        osType = "UBUNTU"

    # if they are not using windows, they are using ubuntu
    # at current writing. I don't have any macs, but that's next.
    try:
        import _winreg
    except ImportError:
        import apt

    app = wx.PySimpleApp()

    searcher = FindSoftware(osType)
    softwareList = searcher.software

    frame = wxM.MainForm(softwareList)
    frame.donations = softwareList
    frame.draw()
    frame.Show()

    app.MainLoop()
