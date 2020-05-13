# -*- coding: utf-8 -*-

import wx

[TXT_MSG] = range(1)

class DlgEditLog(wx.Dialog):
    
    def __init__(self, parent, ID, basicSoftwareLog):
        wx.Dialog.__init__(self, parent, ID, "Define the logging message", style=wx.RESIZE_BORDER|wx.CAPTION)
        
        self._basicSoftwareLog = basicSoftwareLog
        self._message = self._basicSoftwareLog.getLogMessage()
        self._function = self._basicSoftwareLog.getFunction()
        self._returnAction = wx.CANCEL
        
        lblMsg = wx.StaticText(self, wx.ID_ANY, 'Logging message')
        self._txtMsg = wx.TextCtrl(self, TXT_MSG, value=self._message, size=(300,200))
        
        btnOk = wx.Button(self, wx.OK, ("&OK"))
        btnCancel = wx.Button(self, wx.CANCEL, ("&Cancel"))
        btnOk.SetDefault()
        
        self.Bind(wx.EVT_BUTTON, self._onCmdOk, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self._onCmdCancel, id=wx.CANCEL)
        self.Bind(wx.EVT_TEXT, self._onTxtMSGChange, id=TXT_MSG)
        
        szrParam = wx.FlexGridSizer(cols=1, hgap=30, vgap=10)
        szrParam.AddMany([
                            (lblMsg, 0, wx.ALIGN_CENTER_HORIZONTAL),
                            (self._txtMsg, 0, wx.ALIGN_CENTER_HORIZONTAL)
                            ])
    
        szrParam.AddGrowableCol(0)
        
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrButtons.Add(wx.StaticLine(self, wx.ID_ANY, size=(1,-1), style=wx.LI_HORIZONTAL), 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.RIGHT|wx.TOP)
        szrButtons.Add(btnOk, 0, wx.RIGHT, 10)
        szrButtons.Add(btnCancel, 0, wx.ALIGN_CENTER, 10)
        
        szrMain = wx.BoxSizer(wx.VERTICAL)
        szrMain.Add(szrParam, 0, wx.GROW|wx.ALL, 10)
        szrMain.Add(szrButtons, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        
        self.SetSizer(szrMain)
        self.SetAutoLayout(True)
        szrMain.Fit(self)
        
        self.ShowModal()
        
    def _onCmdOk(self, event):
        self._basicSoftwareLog.setLogMessage(self._message)
        __text = 'logging.' + self._function + '.(' + self._message + ')'
        self._basicSoftwareLog.setName(__text)
        self._returnAction = wx.ID_OK
        self.Close()
        
    def _onCmdCancel(self, event):
        self._returnAction = wx.ID_CANCEL
        self.Close()
        
    def getReturnAction(self):
        return self._returnAction
    
    def _onTxtMSGChange(self, event):
        self._message = event.GetString().strip()
        
    