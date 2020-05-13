# -*- coding: utf-8 -*-
import wx

[TXT_LFL] = range(1)

class DlgEditFixRemove(wx.Dialog):
    
    def __init__(self, parent, ID, basicSoftwareFix):
        wx.Dialog.__init__(self, parent, ID, ("Remove file to logAnalyzer"), style=wx.RESIZE_BORDER|wx.CAPTION)
        self._basicSoftwareFix = basicSoftwareFix
        self.SetAutoLayout(True)
        self._returnAction = wx.ID_CANCEL
        
        self._logFilesList = self._basicSoftwareFix.getLogFilesList()
        self._function = self._basicSoftwareFix.getFunction()
        
        lblLFL = wx.StaticText(self, wx.ID_ANY, ('List of file to record'))
        self._txtLFL = wx.TextCtrl(self, TXT_LFL, value=self._pattern)

        btnOk = wx.button(self, wx.OK, ('&OK'))
        btnOk.SetDefault()
        btnCancel = wx.Button(self, wx.CANCEL, ('&Cancel'))

        self.Bind(wx.EVT_BUTTON, self._onCmdOk, id=wx.OK)
        self.Bind(wx.EVT_BUTTON, self._onCmdCancel, id=wx.CANCEL)
        
        self.Bind(wx.EVT_TEXT, self._onTxtLFLChange, id=TXT_LFL)
      
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(btnOk, 0, wx.RIGHT, 10)
        btnSizer.Add(btnCancel, 0, wx.ALL)
        
        szrParam = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        szrParam.AddMany([(lblLFL, 0, wx.ALIGN_LEFT),
                          (self._txtLFL, 0, wx.EXPAND)])
    
        szrMain = wx.BoxSizer(wx.VERTICAL)
        szrMain.Add(szrMain, 0, wx.GROW|wx.ALL, 10)
        szrMain.Add(btnSizer, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        
        self.SetSizer(szrMain)
        self.Centre()
        self.ShowModal()

    def _onCmdOk(self, event):
        self._basicSoftwareFix.setLogFilesList(self._logFilesList)
        _text = self._function + "(files list : " + str(self._logFilesList) + ")"
        self._basicSoftwareFix(_text)
        self._returnAction = wx.ID_OK
        self.Close()
    
    def getReturnAction(self):
        return self._returnAction
    
    def _onTxtLFLChange(self, event):
        self._logFilesList = event.GetString().strip()