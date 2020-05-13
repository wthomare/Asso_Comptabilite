# -*- coding: utf-8 -*-
import wx

[TXT_UTI, TXT_DAF, TXT_PTO, TXT_TMO] = range(4)

class DlgEditFixSetup(wx.Dialog):
    
    def __init__(self, parent, ID, basicSoftwareFix):
        wx.Dialog.__init__(self, parent, ID, ("Setup logAnalyzer from Prophet"), style=wx.RESIZE_BORDER|wx.CAPTION)
        self._basicSoftwareFix = basicSoftwareFix
        self.SetAutoLayout(True)
        self._returnAction = wx.ID_CANCEL
        
        self._dataFormat = self._basicSoftwareFix.getDataFormat()
        self._pollTimeout = self._basicSoftwareFix.getPollTimeout()
        self._timeout = self._basicSoftwareFix.getTimeout()
        self._function = self._basicSoftwareFix.getFunction()
        
        lblDAF = wx.StaticText(self, wx.ID_ANY, ('Key/Value format for data search'))
        self._txtDAF = wx.TextCtrl(self, TXT_DAF, value=self._dataFormat)
        
        lblPTO = wx.StaticText(self, wx.ID_ANY, ('Timeout use by poll while checkout'))
        self._txtPTO = wx.TextCtrl(self, TXT_PTO, value=self._pollTimeout)

        lblTMO = wx.StaticText(self, wx.ID_ANY, ('Timeout for the research of data'))
        self._txtTMO = wx.TextCtrl(self, TXT_TMO, value=self._timeout)
        
        btnOk = wx.button(self, wx.OK, ('&OK'))
        btnOk.SetDefault()
        btnCancel = wx.Button(self, wx.CANCEL, ('&Cancel'))

        self.Bind(wx.EVT_BUTTON, self._onCmdOk, id=wx.OK)
        self.Bind(wx.EVT_BUTTON, self._onCmdCancel, id=wx.CANCEL)
        
        self.Bind(wx.EVT_TEXT, self._onTxtDAFChange, id=TXT_DAF)
        self.Bind(wx.EVT_TEXT, self._onTxtPTOChange, id=TXT_PTO)
        self.Bind(wx.EVT_TEXT, self._onTxtTMOChange, id=TXT_TMO)
        
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(btnOk, 0, wx.RIGHT, 10)
        btnSizer.Add(btnCancel, 0, wx.ALL)
        
        szrParam = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        szrParam.AddMany([(lblDAF, 0, wx.ALIGN_LEFT),
                          (self._txtDAF, 0, wx.EXPAND),
                          (lblPTO, 0, wx.ALIGN_LEFT),
                          (self._txtPTO, 0, wx.EXPAND),
                          (lblTMO, 0, wx.ALIGN_LEFT),
                          (self._txtTMO, 0, wx.EXPAND)])
    
        szrMain = wx.BoxSizer(wx.VERTICAL)
        szrMain.Add(szrMain, 0, wx.GROW|wx.ALL, 10)
        szrMain.Add(btnSizer, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        
        self.SetSizer(szrMain)
        self.Centre()
        self.ShowModal()
        
    def _onCmdOk(self, event):
        self._basicSoftwareFix.setDataFormat(str(self._dataFormat))
        self._basicSoftwareFix.setPolTimeout(str(self._pollTimeout))
        self._basicSoftwareFix.setTimeout(str(self._timeout))
        
        _text = self._function + "(format : " + str(self._dataFormat) + ", PTO : " + str(self._pollTimeout) + ', TMO : ' + str(self._timeout) + ')'
        self._basicSoftwareFix.setName(_text)
        self._returnAction = wx.ID_OK
        self.Close()
        
    def _onCmdCancel(self, event):
        self._returnAction=wx.ID_CANCEL
        self.Close()
        
    def getReturnAction(self):
        return self._returnAction
    
    def _onTxtDAFChange(self, event):
        self._dataFormat=event.GetString().strip()
    
    def _onTxtPTOChange(self, event):
        self._pollTimeout=event.GetString().strip()
        
    def _onTxtTMOChange(self, event):
        self._timeout=event.GetString().strip()
        