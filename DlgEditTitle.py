# -*- coding: utf-8 -*-

import wx
import BasicSoftwareUtils

[TXT_TITLE] = range(1)

class DlgEditTitle(wx.Dialog):
    def __init__(self, parent, ID, basicSoftwareTitle):
        wx.Dialog.__init__(self, parent, ID, ('Title Edit'), style=wx.RESIZE_BORDER|wx.CAPTION)
        self._basicSoftwareTitle = basicSoftwareTitle
        
        self._text = self._basicSoftwareTitle.getName()
        self._returnAction = wx.ID_CANCEL
        self._Type = self._basicSoftwareTitle.getInstanceTitleType()
        
        self._txtCtrl = wx.TextCtrl(self, TXT_TITLE, self._text, size = (240, 120), style=wx.TE_MULTILINE)
        self._txtCtrl.SetFocus()
        
        self.Bind(wx.EVT_TEXT, self._onTxtTitleChange, id=TXT_TITLE)
        
        btnOk = wx.Button(self, wx.OK, ('&OK'))
        btnOk.SetDefault()
        btnCancel = wx.Button(self, wx.CANCEL, ('&Cancel'))

        self.Bind(wx.EVT_BUTTON, self._onCmdOk, id=wx.OK)
        self.Bind(wx.EVT_BUTTON, self._onCmdCancel, id=wx.CANCEL)
        
        szrBtn = wx.BoxSizer(wx.HORIZONTAL)
        szrBtn.Add(btnOk, 0, wx.RIGHT, 10)
        szrBtn.Add(btnCancel, 0, wx.ALL)
        
        szrMain = wx.BoxSizer(wx.VERTICAL)
        szrMain.Add(self._txtCtrl, 0, wx.GROW|wx.ALL, 10)
        szrMain.Add(szrBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 10)
        
        self.SetSizer(szrMain)
        self.SetAutoLayout(True)
        
        szrMain.Fit(self)
        
        self.Centre()
        self.ShowModal()
        
    def _onTxtTitleChange(self, event):
        self._text = event.GetString()
        
    def _onCmdOk(self, event):
        
        if self._text[:5] != 'test_':
            msg = 'The title of a test must start by test_ otherwise basicSoftware will not handle your test \n' + 'Your title will be consider has a function declaration'
            BasicSoftwareUtils.displayWarning(msg, "Warning in title definition")
        self._basicSoftwareTitle.setName(self._text)
        self._basicSoftwareTitle.setInstanceTitleType('Start')
        self._returnAction = wx.ID_OK
        self.Close()
        
    def _onCmdCancel(self, event):
        self._returnAction = wx.ID_CANCEL
        self.Close()
        
    def getReturnAction(self):
        return self._returnAction