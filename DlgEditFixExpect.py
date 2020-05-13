# -*- coding: utf-8 -*-

import wx
from wx.lib import masked

[TXT_PAT, TXT_FTC, TXT_FTE, TXT_TMO] = range(4)

class DlgEditFixExpect(wx.Dialog):
    
    def __init__(self, parent, ID, basicSoftwareFix):
        wx.Dialog.__init__(self, parent, ID, ("Look for pattern in files"), style=wx.RESIZE_BORDER|wx.CAPTION)
        self._basicSoftwareFix = basicSoftwareFix
        self.SetAutoLayout(True)
        self._returnAction = wx.ID_CANCEL
        
        self._pattern = self._basicSoftwareFix.getPattern()
        self._fieldsToCheck = self._basicSoftwareFix.getFieldsToCheck()
        self._fieldsToExclude = self._basicSoftwareFix.getFieldsToExclude()
        self._timeout = self._basicSoftwareFix.getTimeout()
        self._function = self._basicSoftwareFix.getFunction()
        
        lblPAT = wx.StaticText(self, wx.ID_ANY, ('Pattern expected in the log'))
        self._txtPAT = wx.TextCtrl(self, TXT_PAT, value=self._pattern)
        
        lblFTC = self.StaticText(self, wx.ID_ANY, ('fieldsToCheck : List of strings\nto start method'))
        self._txtFTC = wx.TextCtrl(self, TXT_FTC, value=self._fieldsToCheck)
        
        lblFTE = wx.StaticText(self, wx.ID_ANY, ('fieldsToExclude : List of strings\nnot matching in the same line fieldsToCheck'))
        self._txtFTE = wx.TextCtrl(self, TXT_FTE, value=self._fieldsToExclude)
        
        lblTMO = wx.StaticText(self, wx.ID_ANY, ('Timeout for the research of data'))
        self._txtTMO = masked.NumCtrl(self, TXT_TMO, value =self._timeout, min=0, max=1000)
        
        btnOk = wx.button(self, wx.OK, ('&OK'))
        btnOk.SetDefault()
        btnCancel = wx.Button(self, wx.CANCEL, ('&Cancel'))

        self.Bind(wx.EVT_BUTTON, self._onCmdOk, id=wx.OK)
        self.Bind(wx.EVT_BUTTON, self._onCmdCancel, id=wx.CANCEL)
        
        self.Bind(wx.EVT_TEXT, self._onTxtPATChange, id=TXT_PAT)
        self.Bind(wx.EVT_TEXT, self._onTxtFTCChange, id=TXT_FTC)
        self.Bind(wx.EVT_TEXT, self._onTxtFTEChange, id=TXT_FTE)
        self.Bind(wx.EVT_TEXT, self._onTxtTMOChange, id=TXT_TMO)
        
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(btnOk, 0, wx.RIGHT, 10)
        btnSizer.Add(btnCancel, 0, wx.ALL)
        
        szrParam = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        szrParam.AddMany([(lblPAT, 0, wx.ALIGN_LEFT),
                          (self._txtPAT, 0, wx.EXPAND),
                          (lblFTC, 0, wx.ALIGN_LEFT),
                          (self._txtFTC, 0, wx.EXPAND),
                          (lblFTE, 0, wx.ALIGN_LEFT),
                          (self._txtFTE, 0, wx.EXPAND),
                          (lblTMO, 0, wx.ALIGN_LEFT),
                          (self._txtTMO, 0, wx.EXPAND)])
    
        szrMain = wx.BoxSizer(wx.VERTICAL)
        szrMain.Add(szrMain, 0, wx.GROW|wx.ALL, 10)
        szrMain.Add(btnSizer, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        
        self.SetSizer(szrMain)
        self.Centre()
        self.ShowModal()
        
    def _onCmdOk(self, event):
        self._basicSoftwareFix.setPattern(str(self._pattern))
        self._basicSoftwareFix.setFieldsToCheck(str(self._fieldsToCheck))
        self._basicSoftwareFix.setFieldsToExclude(str(self._fieldsToExclude))
        self._basicSoftwareFix.setTimeout(str(self._timeout))
        
        _text = self._function + "(pattern : " + str(self._pattern) + ", Check : " + str(self._fieldsToCheck) + ", Exclude : " + str(self._fieldsToExclude) + ", TMO : " + str(self._timeout) + ")"
        self._basicSoftwareFix.setName(_text)
        self._returnAction = wx.ID_OK
        self.Close()
        
    def _onCmdCancel(self, event):
        self._returnAction = wx.ID_CANCEL
        self.Close()

    def getReturnAction(self):
        return self._returnAction

    def _onTxtPATChange(self, event):
        self._pattern = event.GetString().strip()

    def _onTxtFTCChange(self, event):
        self._fieldsToCheck = event.GetString().strip()
        
    def _onTxtFTEChange(self, event):
        self._fieldsToExclude = event.GetString().strip()

    def _onTxttmoChange(self, event):
        self._timeout = event.GetString().strip()