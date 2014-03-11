import wx
import urllib
from cStringIO import StringIO
import urllib2

# example URL:
# https://chart.googleapis.com/chart?chs=150x150&cht=qr&chl=bitcoin:17orEh51ab8HoU7g8Ezwcp76jCpeL7PabJ?label=Blender%26amount=0.01

class MainForm(wx.Frame):
    def __init__(self, donations):
        self.donations = donations
        wx.Frame.__init__(self, None, wx.ID_ANY, "Donate to Developers", size = (325, 325))
        self.panel_one = MainPanel(self)

    def draw(self):
        self.panel_one.drawIcons()

class MainPanel(wx.Panel):
    def __init__(self, parent):
        self.donations = parent.donations
        self.panel = wx.Panel.__init__(self, parent)
        self.txtAmt = wx.TextCtrl(self, -1, "0.01", size = (125, -1), pos = (10, 10))
        self.button = wx.Button(self, -1, "Next", pos = (150, 10))
        self.redraw = wx.Button(self, -1, "Redo", pos = (230, 10))

        # init value
        self.nIconNumber = 0
        self.button.Bind(wx.EVT_BUTTON, self.drawIcons)

        # redo button redoes the icon for a different amount
        self.redraw.Bind(wx.EVT_BUTTON, self.redo)

    def drawIcons(self, e = None):
        # avoid out of range error
        if self.nIconNumber in range(0, len(self.donations)):
            self.drawIcon()
            self.nIconNumber = self.nIconNumber + 1

    def redo(self, e = None):
        self.nIconNumber = self.nIconNumber - 1
        self.drawIcon()
        self.nIconNumber = self.nIconNumber + 1

    def drawIcon(self):
        d = self.donations[self.nIconNumber]
        image = self.fetchImage(d)

        wx.StaticText(self, pos = (20, 50), label = d["name"], size = (100, 20))
        # QR code is 150 square, we're giving 25 for all-around margin, 175
        wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image), pos = (100, 50))

    def fetchImage(self, donation):
        amt = self.txtAmt.GetValue()

        # The label is for the bitcoin client
        # http://tcatm.github.io/bitcoin-js-remote/
        label = urllib.quote(donation["name"])
        imageObj = urllib2.urlopen("https://chart.googleapis.com/chart?chs=150x150&" +
            "cht=qr&chl=bitcoin:" + donation["bitcoinAddress"] +
            "?label=" + label +
            "%26amount=" + str(amt)).read()

        img = wx.ImageFromStream(StringIO(imageObj))
        return img
