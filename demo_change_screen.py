#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      JJ
#
# Created:     08/03/2014
# Copyright:   (c) JJ 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import wx

class MainfForm(wx.Frame):
    def __init__(self):
        self.n = 0
        wx.Frame.__init__(self, None, wx.ID_ANY, "HW")
        self.button = wx.Button(self, -1, "Next")
        self.button.Bind(wx.EVT_BUTTON, self.nextScreen)

        self.txtCounter = wx.TextCtrl(self, -1, str(self.n), size = (125, 110), pos = (100, 100))

    def nextScreen(self, e):
        self.n = self.n + 1
        self.txtCounter = wx.TextCtrl(self, -1, str(self.n), size = (125, 110), pos = (100, 100))
        pass

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MainfForm()
    frame.Show()
    app.MainLoop()
