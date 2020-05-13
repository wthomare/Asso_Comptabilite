# -*- coding: utf-8 -*-
import wx


class DlgImport(wx.FileDialog):
    def __init__(self, parent):
        wx.FileDialog.__init__(self, parent, "Load", "", "", "xml files (*.xml)|*.xml", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        self.ShowModal()
        