# -*- coding: utf-8 -*-

from BasicSoftwareLink import BasicSoftwareLink
from BasicSoftwareConst import process

import wx

[TXT_RELATIONSHIP, BTN_REMOVE, TXT_PRICE, TXT_QTY, TXT_HC] = range(5)

class DlgEditProcess(wx.Dialog):
    def __init__(self, parent, ID, basicSoftwareLink):
        wx.Dialog.__init__(self, parent, ID, "Expected State of an instance", style=wx.RESIZE_BORDER|wx.CAPTION)
        
        self._basicSotwareLink = basicSoftwareLink
        self._relationship = self._basicSotwareLink.getRelationship()
        self._expected_selection_state = self._basicSotwareLink.getExpectAnswer()
        self._returnAction = wx.ID_CANCEL
        self.Expected_state = process
        
        lblRela = wx.StaticText(self, wx.ID_ANY, "Name of the Order", style=wx.ALIGN_CENTER)
        
        hboxExpect = wx.BoxSizer(wx.HORIZONTAL)
        lblExpec = wx.StaticText(self, wx.ID_ANY, 'Expected behavior', style=wx.ALIGN_CENTER)
        hboxExpect.Add(lblExpec, 1, wx.ALIGN_LEFT, 0)
        
        self._txtRelationship= wx.TextCtrl(self, TXT_RELATIONSHIP, self._relationship, size=wx.Size(100,20))
        
        self.lb = wx.ComboBox(self, wx.ID_ANY, size=(200,-1), choices=self.Expected_state, style=wx.CB_DROPDOWN, value=self._expected_selection_state)
        
        self.Bind(wx.EVT_TXT, self._onTxtRelationshipChange, id=TXT_RELATIONSHIP)
        self.lb.Bind(wx.EVT_TEXT, self._onSelect)
        
        btnOk = wx.Button(self, wx.OK, ("&OK"))
        btnCancel = wx.Button(self, wx.CANCEL, ("&Cancel"))
        btnRemove = wx.Button(self, BTN_REMOVE, ("Remove"))
        btnOk.SetDefault()
        
        self.Bind(wx.EVT_BUTTON, self._onCmdOk, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self._onCmdCancel, id=wx.CANCEL)
        self.Bind(wx.EVT_BUTTON, self._onCmdRemove, id=BTN_REMOVE)
        
        line = wx.StaticLine(self, wx.ID_ANY, size=(1, -1), style=wx.LI_HORIZONTAL)
        
        szr1 = wx.FlexGridSizer(cols=1, hgap=30, vgap=10)
        szr1.AddMany([
                        (lblRela, 0 , wx.ALIGN_CENTER_HORIZONTAL),
                        (self._txtRelationship, 0, wx.ALIGN_CENTER_HORIZONTAL),
                        (line, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.RIGHT|wx.TOP)
                ])
        szr1.AddGrowableRow(0)
        
        szr2 = wx.BoxSizer(wx.VERTICAL)
        szr2.Add(hboxExpect, 0, wx.CENTER, 10)
        szr2.Add(self.lb, 2, wx.CENTER, 10)
        
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
        
        szr4.Fit(self)

    def _onTxtRelationshipChange(self, event):
        self._relationship = event.GetString()
        
    def _onCmdOk(self):
        self._basicSotwareLink.setName('Expected ' + self._expected_selection_state + ' state of instance : self.' + self._relationship)
        self._basicSotwareLink.setExpectAnswer(self._expected_selection_state)
        self._basicSotwareLink.setRelationship(self._relationship)
        
        self._returnAction = wx.ID_OK
        self.Close()
        
    def _onCmdCancel(self, event):
        self._returnAction = wx.ID_CANCEL
        self.Close()
        
    def _onCmdRemove(self, event):
        self._returnAction = wx.ID_NO
        self.Close()
                   
    def getReturnAction(self):
        return self._returnAction
    
    def _onSelect(self, event):
        self._expected_selection_state = self.lb.GetStringSelection()
        
    def setRelationship(self, rela):
        self._relationship = rela
        
    def getRelationship(self):
        return self._relationship
        
    