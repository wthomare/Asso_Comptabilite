# -*- coding: utf-8 -*-

import wx

[TXT_NOTE] = range(1)

class DlgEditNote(wx.Dialog):
    
    def __init__(self, parent, ID, basicSoftwareNote):
        wx.Dialog.__init__(self, parent, ID, ("Edit Note"), style = wx.RESIZE_BORDER|wx.CAPTION)
        
        self._basicSoftwareNote = basicSoftwareNote
        self.SetAutoLayout(True)
        
        self._text = self._basicSoftwareNote.getName()
        self._returnAction = wx.ID_CANCEL
        
        label = wx.StaticText(self, wx.ID_ANY, ("Note text"))
        
        self._txtCtrl.SetFocus()
        
        self.Bind(wx.EVT_TEXT, self._onTxtNoteChange, id=TXT_NOTE)
        
        btnOk = wx.button(self, wx.OK, ('&OK'))
        btnOk.SetDefault()
        btnCancel = wx.Button(self, wx.CANCEL, ('&Cancel'))
        
        self.Bind(wx.EVT_BUTTON, self._onCmdOK, id = wx.OK)
        self.Bind(wx.EVT_BUTTON, self._onCmdCancel, id = wx.CANCEL)
        
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrButtons.Add(btnOk, 0, wx.RIGHT, 10)
        szrButtons.Add(btnCancel, 0, wx.ALL)
        
        szrMain = wx.BoxSizer(wx.VERTICAL)
        szrMain.Add(label, 0, wx.BOTTOM, 5)
        szrMain.Add(self._txtCtrl, 1, wx.EXPAND|wx.ALL, 10)
        szrMain.Add(szrButtons, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_BOTTOM)
        
        szrBorder = wx.BoxSizer(wx.VERTICAL)
        szrBorder.Add(szrMain, 1, wx.EXPAND|wx.ALL, 10)
        self.SetSizer(szrBorder)
        szrBorder.Fit(self)
        
        self.Centre()
        self.ShowModal()
        
    def _onTxtNoteChange(self, event):
        self._text = event.GetString()
        
    def _onCmdOk(self, event):
        self._basicSoftwareNote.setName(self._text)
        self._returnAction=wx.ID_OK
        self.Close()
        
    def _onCmdCancel(self, event):
        self._returnAction = wx.ID_CANCEL
        self.Close()
        
    def getReturnAction(self):
        return self._returnAction
        
        
        
        
        

