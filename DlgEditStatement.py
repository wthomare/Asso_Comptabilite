# -*- coding: utf-8 -*-

import wx
import BasicSoftwareUtils

[TXT_STATEMENT, BTN_REMOVE] = range(2)

class DlgEditStatement(wx.Dialog):
    def __init__(self, parent, ID, basicSoftwareStatement):
        wx.Dialog.__init__(self, parent, ID, title='Statement Declaration', style=wx.RESIZE_BORDER|wx.CAPTION)

        self._basicSoftwareStatement = basicSoftwareStatement
        self.instruction = self._basicSoftwareStatement.getInstruction()
        self.statement = self._basicSoftwareStatement.getStatement()
        self._returnAction = wx.ID_CANCEL
        self.SetAutoLayout(True)
        
        statementCBL = ['if', 'elif', 'else', 'try', 'except', 'finally']
        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16))
        titleIco = wx.StaticBitmap(self, wx.ID_ANY, bmp)
        title = wx.StaticText(self, wx.ID_ANY, "Statement definition")
        
        
        lblStat = wx.StaticText(self, wx.ID_ANY, "Type of Statement")
        self.ccbStat = wx.ComboBox(self, wx.ID_ANY, size=(50, -1), choices=statementCBL, style=wx.CB_DROPDOWN, value=self.statement)
        self.inputState = wx.TextCtrl(self, TXT_STATEMENT, self.instruction)
        lblIns = wx.StaticText(self, wx.ID_ANY, "Hard code instruction")
        
        btnOk = wx.Button(self, wx.OK, ("&OK"))
        btnCancel = wx.Button(self, wx.CANCEL, ("&Cancel"))
        btnRemove = wx.Button(self, BTN_REMOVE, ("Remove"))
        btnOk.SetDefault()
        
        self.ccbStat.Bind(wx.EVT_TEXT, self._onSelect)
        
        self.Bind(wx.EVT_BUTTON, self._onCmdOk, id=wx.OK)
        self.Bind(wx.EVT_BUTTON, self._onCmdCancel, id=wx.CANCEL)
        self.Bind(wx.EVT_BUTTON, self._onCmdRemove, id=BTN_REMOVE)
        
        self.Bind(wx.EVT_TEXT, self._onInstChange, id=TXT_STATEMENT)
        
        topSizer = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        gridSizer = wx.GridSizer(rows=4, cols=1, hgap=5, vgap=5)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        titleSizer.Add(titleIco, 0, wx.ALL, 5)
        titleSizer.Add(title, 0, wx.ALL, 5)
        
        gridSizer.Add(lblStat, 0, wx.ALIGN_RIGHT)
        gridSizer.Add(self.ccbStat, 0, wx.EXPAND)
        gridSizer.Add(lblIns, 0, wx.ALIGN_RIGHT)
        gridSizer.Add(self.inputState, 0, wx.EXPAND)
        

        btnSizer.Add(btnOk, 0, wx.ALL, 5)
        btnSizer.Add(btnCancel, 0, wx.ALL, 5)
        btnSizer.Add(btnRemove, 0, wx.ALL, 5)
        
        topSizer.Add(titleSizer, 0, wx.CENTER)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(gridSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btnSizer, 0, wx.ALL|wx.EXPAND, 5)
        
        self.SetSizeHints(250, 300, 1000, 800)
        
        self.SetSizer(topSizer)
        topSizer.Fit(self)
        self.Centre()
        self.ShowModal()
        
    def _onInstChange(self, event):
        self.instruction = event.GetString()
        
    def _onSelect(self, event):
        self.statement = self.ccbStat.GetStringSelection()
    
    def _onCmdOk(self, event):
        
        if self.statement:
            self._basicSoftwareStatement.setName(self.statement + " " + self.instruction + ' :')
            self._basicSoftwareStatement.setStatement(self.statement)
            self._basicSoftwareStatement.setInstruction(self.instruction)
            self._returnAction = wx.ID_OK
            self.Close()
        else:
            msg = 'No statement selected in combobox'
            BasicSoftwareUtils.displayError(msg, 'DlgStatement error')
            
    def _onCmdCancel(self, event):
        self._returnAction = wx.ID_CANCEL
        self.Close()
        
    def _onCmdRemove(self, event):
        self._returnAction = wx.ID_NO
        self.Close()
                   
    def getReturnAction(self):
        return self._returnAction       
