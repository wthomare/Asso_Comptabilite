# -*- coding: utf-8 -*-
import wx

[TxtTwo_RELATIONSHIP, TxtTwo2_RELATIONSHIP] = range(2)

class DlgEditFOR(wx.Dialog):
    def __init__(self, parent, ID, basicSoftwareUseCase):
        wx.Dialog.__init__(self, parent, ID, ('Loop declaration'), style=wx.RESIZE_BORDER|wx.CAPTION)
        self._basicSoftwareUseCase = basicSoftwareUseCase
        self._returnAction = wx.ID_CANCEL
        
        self.TxtTwo = self._basicSoftwareUseCase.getTxtTwo()
        self.TxtTwo2 = self._basicSoftwareUseCase.getTxtTwo2()
        
        self.SetAutoLayout(True)
        
        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16,16))
        titleIco = wx.StaticBitmap(self, wx.ID_ANY, bmp)
        title = wx.StaticText(self, wx.ID_ANY, 'Loop definition')
        
        labelTwo1 = wx.StaticText(self, wx.ID_ANY, 'for')
        self.inputTxtTwo = wx.TextCtrl(self, TxtTwo_RELATIONSHIP, self.TxtTwo)
        labelTwo2 = wx.StaticText(self, wx.ID_ANY, 'in')
        self.inputTxtTwo2 = wx.TextCtrl(self, TxtTwo2_RELATIONSHIP, self.TxtTwo2)
        
        btnOk = wx.Button(self, wx.OK, ('&OK'))
        btnOk.SetDefault()
        btnCancel = wx.Button(self, wx.CANCEL, ('&Cancel'))

        self.Bind(wx.EVT_BUTTON, self._onCmdOk, id=wx.OK)
        self.Bind(wx.EVT_BUTTON, self._onCmdCancel, id=wx.CANCEL)
        
        topSizer = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        gridSizer = wx.GridSizer(rows=1, cols=4, hgap=5, vgap=5)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        titleSizer.Add(titleIco, 0, wx.ALL, 5)
        titleSizer.Add(title, 0, wx.ALL, 5)
        
        gridSizer.Add(labelTwo1, 0, wx.ALIGN_RIGHT)
        gridSizer.Add(self.inputTxtTwo, 0, wx.EXPAND)
        gridSizer.Add(labelTwo2, 0, wx.ALIGN_RIGHT)
        gridSizer.Add(self.inputTxtTwo2, 0, wx.EXPAND)
        
        btnSizer.Add(btnOk, 0, wx.ALL, 5)
        btnSizer.Add(btnCancel, 0, wx.ALL, 5)
        
        topSizer.Add(titleSizer, 0, wx.CENTER)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(gridSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btnSizer, 0, wx.ALL|wx.CENTER, 5)
        
        self.Bind(wx.EVT_TEXT, self._onTxtTwoChange, id=TxtTwo_RELATIONSHIP)
        self.Bind(wx.EVT_TEXT, self._onTxtTwo2Change, id=TxtTwo2_RELATIONSHIP)
        
        self.SetSizeHints(200,250,1000,800)
        self.SetSizer(topSizer)
        topSizer.Fit(self)
        
        self.Centre()
        self.ShowModal()
        
    def _onTxtTwoChange(self, event):
        self.TxtTwo = event.GetString().strip()
        
    def _onTxtTwo2Change(self, event):
        self.TxtTwo2 = event.GetString().strip()
        
    def _onCmdOk(self, event):
        self._basicSoftwareUseCase.setName('for ' + self.TxtTwo + ' in ' + self.TxtTwo2 + ' :')
        self._basicSoftwareUseCase.setTxtTwo(self.TxtTwo)
        self._basicSoftwareUseCase.setTxtTwo2(self.TxtTwo2)
        self._returnAction = wx.ID_OK
        self.Close()
        
    def _onCmdCancel(self, event):
        self._returnAction = wx.ID_CANCEL
        self.Close()
        
    def getReturnAction(self):
        return self._returnAction