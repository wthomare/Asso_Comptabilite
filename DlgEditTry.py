# -*- coding: utf-8 -*-

from BasicSoftwareConst import try_type, states
from wx.lib import masked

import wx

[TXT_RELATIONSHIP, BTN_REMOVE, TXT_WAIT] = range(3)

class DlgEditTry(wx.Dialog):
    def __init__(self, parent, ID, basicSoftwareLink):
        wx.Dialog.__init__(self, parent, ID, 'Apply a try function', style=wx.RESIZE_BORDER|wx.CAPTION)
        
        self._basicSoftwareLink = basicSoftwareLink
        
        self._returnAction= wx.ID_CANCEL
        self._relationship = self._basicSoftwareLink.getRelationship()
        self._WaitingTime = self._basicSoftwareLink.getWaitingTime()
        self._expected_relation_state = self._basicSoftwareLink.getCltType()
        self._function = self._basicSoftwareLink.getExpectedAnswer()
        self._src = self._basicSoftwareLink.getSource()
        self._dst = self._basicSoftwareLink.getDestination()
        self.Expected_sates = states
        self.Try = try_type
        
        lblFunction = wx.StaticText(self, wx.ID_ANy, "Choice of an function", style=wx.ALIGN_LEFT)
        self._ccbFunction = wx.ComboBox(self, wx.ID_ANY, size=(120, -1), choices=self.Try, style=wx.CB_DROPDOWN, value=self._function)
        lblRela = wx.StaticText(self, wx.ID_ANY, "Name of the order", style=wx.ALIGN_LEFT)
        
        hboxWaiting = wx.BoxSizer(wx.VERTICAL)
        self.cbWait = wx.CheckBox(self, id = wx.ID_ANY, label="Time out")
        hboxWaiting.Add(self.cbWait,1)
        self._txtWait = masked.NumCtrl(self, TXT_WAIT, value=self._WaitingTime, min=0, max=9999999999)
        hboxWaiting.Add(self._txtWait, 1, wx.ALIGN_LEFT, 0)

        self._txtRelationship= wx.TextCtrl(self, TXT_RELATIONSHIP, self._relationship, size=wx.Size(100,20))

        self.Bind(wx.EVT_TEXT, self._onTxtRelationshipChange, id=TXT_RELATIONSHIP)
        self.Bind(wx.EVT_TEXT, self._onTxtWaitChange, id=TXT_WAIT)
        self.cbWait.Bind(wx.EVT_CHECKBOX, self._onCmdWait)
        
        lblStates = wx.StaticText(self, wx.ID_ANY, 'Expected states')
        self._ccbStates = wx.ComboBox(self, wx.ID_ANY, size=(120, -1), choices=self.Expected_sates, style=wx.CB_DROPDOWN, value=self._expected_relation_state)

        btnOk = wx.Button(self, wx.OK, ("&OK"))
        btnCancel = wx.Button(self, wx.CANCEL, ("&Cancel"))
        btnRemove = wx.Button(self, BTN_REMOVE, ("Remove"))
        btnOk.SetDefault()
        
        self.Bind(wx.EVT_BUTTON, self._onCmdOk, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self._onCmdCancel, id=wx.CANCEL)
        self.Bind(wx.EVT_BUTTON, self._onCmdRemove, id=BTN_REMOVE)
        
        szr1 = wx.FlexGridSizer(cols=1, hgap=30, vgap=10)
        szr1.AddMany([(lblFunction, 0, wx.ALIGN_CENTER_HORIZONTAL),
                      (self._ccbFunction, 0, wx.ALIGN_CENTER_HORIZONTAL),
                     (lblRela, 0, wx.ALIGN_CENTER_HORIZONTAL),
                     (self._txtRelationship, 0, wx.ALIGN_CENTER_HORIZONTAL),
                     (wx.StaticLine(self, wx.ID_ANY, size=(1,-1), style=wx.LI_HORIZONTAL), 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP),
                     (hboxWaiting, 0, wx.ALIGN_LEFT)
                     (wx.StaticLine(self, wx.ID_ANY, size=(1,-1), style=wx.LI_HORIZONTAL), 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP),
                     ])
        szr1.AddGrowableCol(0)

        szr2 = wx.FlexGridSizer(cols=1, hgap=30, vgap=10)
        szr2.AddMany([
                (lblStates, 0, wx.ALIGN_CENTER_HORIZONTAL),
                (self._ccbStates, 0, wx.ALIGN_CENTER_HORIZONTAL),
                (wx.StaticLine(self, wx.ID_ANY, size=(1,-1), style=wx.LI_HORIZONTAL), 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP)                
                ])
        szr2.AddGrowableCol(0)
        
        
        szr3=wx.BoxSizer(wx.HORIZONTAL)    
        szr3.Add(btnRemove, 0, wx.RIGHT, 10)
        szr3.Add(btnOk, 0, wx.RIGHT, 10)
        szr3.Add(btnCancel, 0)
        
        szr4 = wx.BoxSizer(wx.VERTICAL)
        szr4.Add(szr1, 0, wx.GROW|wx.ALL, 10)
        szr4.Add(szr2, 0, wx.GROW|wx.ALL, 10)
        szr4.Add(szr3, 0, wx.ALIGN_RIGHT|wx.ALL, 10)
        
        self.SetSizer(szr4)
        self.SetAutoLayout(True)
        
        szr4.Fit()

    def _onTxtRelationshipChange(self, event):
        self._relationship = event.GetString()
        
    def _onCmdOk(self, event):
        self._basicSoftwareLink.setName("try " + self._function + ' : ' +self._relationship)
        self._basicSoftwareLink.setRelationship(self._relationship)
        self._returnAction = wx.ID_OK
        self._basicSoftwareLink.setWaitingValue(self._WaitingTime)
        self._basicSoftwareLink.setExpectedAnswer(self._function)
        self._basicSoftwareLink.setCltType(self._expected_relation_state)
        self.Close()
        
    def _onCmdCancel(self, event):
        self._returnAction = wx.ID_CANCEL
        self.Close()
        
    def _onCmdRemove(self, event):
        self._returnAction = wx.ID_NO
        self.Close()
                   
    def getReturnAction(self):
        return self._returnAction
    
    def _onTxtWaitChange(self, event):
        self._WaitingTime = event.GetString().strip()
    
    def _onCmdWait(self, event):
        if self.cbWait.Value == False:
            self._txtWait.Enable(False)
        else:
            self._txtWait.Enable(True)
        event.Skip()
    
    def setRelationship(self, rela):
        self._relationship = rela
    
    def getRelationship(self):
        return self._relationship
    
    def _onSelectState(self, event):
        self._expected_relation_state = self._ccbStates.GetStringSelection()
        
    def _onSelectFunction(self, event):
        self._function = self._ccbFunction.GetStringSelection()
        
        if self._function == "cmd_states":
            self._ccbStates.Disable()
        else:
            self._ccbStates.Enable()
