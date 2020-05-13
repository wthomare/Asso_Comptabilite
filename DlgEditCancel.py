# -*- coding: utf-8 -*-
from copy import deepcopy
from wx.lib import masked
import wx

[TXT_RELATIONSHIP, BTN_REMOVE, TXT_WAIT] = range(3)

class DlgEditCancel(wx.Dialog):
    def __init__(self, parent, ID, basicSoftwareLink):
        wx.Dialog.__init__(self, parent, ID, "Cancel an order with or without delay,", wx.RESIZE_BORDER|wx.CAPTION)
        
        self._basicSoftwareLink = basicSoftwareLink
        
        self._returnAction= wx.ID_CANCEL
        self._relationship = self._basicSoftwareLink.getRelationship()
        self._WaitingTime = self._basicSoftwareLink.getWaitingTime()
        
        lblRela = wx.StaticText(self, wx.ID_ANY, "Name of the Order", style=wx.ALIGN_CENTER)
        
        hboxWaiting = wx.BoxSizer(wx.VERTICAL)
        self.cbWait = wx.CheckBox(self, id = wx.ID_ANY, label="Would you delayed the cancel")
        hboxWaiting.Add(self.cbWait,1)
        self._txtWait = masked.NumCtrl(self, TXT_WAIT, value=self._WaitingTime, min=0, max=9999999999)
        hboxWaiting.Add(self._txtWait, 1, wx.ALIGN_LEFT, 0)
        
        self._txtRelationship= wx.TextCtrl(self, TXT_RELATIONSHIP, self._relationship, size=wx.Size(100,20))
        
        self.cbWait.Bind(wx.EVT_CHECKBOX, self._onCmdWait)
        
        self.Bind(wx.EVT_TEXT, self._onTxtRelationshipChange, id=TXT_RELATIONSHIP)
        self.Bind(wx.EVT_TEXT, self._onTxtWaitChange, id=TXT_WAIT)
        
        btnOk = wx.Button(self, wx.OK, ("&OK"))
        btnCancel = wx.Button(self, wx.CANCEL, ("&Cancel"))
        btnRemove = wx.Button(self, BTN_REMOVE, ("Remove"))
        btnOk.SetDefault()
        
        self.Bind(wx.EVT_BUTTON, self._onCmdOk, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self._onCmdCancel, id=wx.CANCEL)
        self.Bind(wx.EVT_BUTTON, self._onCmdRemove, id=BTN_REMOVE)

        szr1 = wx.FlexGridSizer(cols=1, hgap=30, vgap=10)
        szr1.AddMany([(lblRela, 0, wx.ALIGN_CENTER_HORIZONTAL),
                     (self._txtRelationship, 0, wx.ALIGN_CENTER_HORIZONTAL),
                     (wx.StaticLine(self, wx.ID_ANY, size=(1,-1), style=wx.LI_HORIZONTAL), 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL),
                     (hboxWaiting, 0, wx.ALIGN_LEFT)
                     (wx.StaticLine(self, wx.ID_ANY, size=(1,-1), style=wx.LI_HORIZONTAL), 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL),
                     ])
        szr1.AddGrowableCol(0)
        
        szr2=wx.BoxSizer(wx.HORIZONTAL)    
        szr2.Add(btnRemove, 0, wx.RIGHT, 10)
        szr2.Add(btnOk, 0, wx.RIGHT, 10)
        szr2.Add(btnCancel, 0)
        
        szr3 = wx.BoxSizer(wx.VERTICAL)
        szr3.Add(szr1, 0, wx.GROW|wx.ALL, 10)
        szr3.Add(szr2, 0, wx.ALIGN_RIGHT|wx.ALL, 10)
        
        self.SetSizer(szr3)
        self.SetAutoLayout(True)
        
        szr3.Fit(self)
        
    def _copyLink(self):
        self._basicSoftwareLinkCopy = deepcopy(self._basicSoftwareLink)
        
    def _onTxtRelationshipChange(self, event):
        self._relationship = event.GetString()
        
    def _onCmdOk(self, event):
        
        self._basicSoftwareLink.setName("Cancel Order : " + self._relationship)
        self._basicSoftwareLink.setRelationship(self._relationship)

        if self.cbWait.Value:
            self._basicSoftwareLink.setWaitingValue(self._WaitingTime)
        else:
            self._basicSoftwareLink.setWaitingValue(0)

        
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
    
    def _onTxtWaitChange(self, event):
        self._WaitingTime = event.GetString().strip()
    
    def _onCmdWait(self, event):
        if self.cbWait.Value == False:
            self._txtWait.Enable(False)
        else:
            self._txtWait.Enable(True)
        event.Skip()
        
