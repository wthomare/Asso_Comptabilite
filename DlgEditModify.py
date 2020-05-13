# -*- coding: utf-8 -*-

from BasicSoftwareLink import BasicSoftwareLink
from BasicSoftwareConst import expected, orderWay, restriction, prcMode, validity, account

import wx
from wx.lib import masked

[TXT_RELATIONSHIP, BTN_REMOVE, TXT_PRICE, TXT_QTY, TXT_CLTY, TXT_HC, TXT_WAIT] = range(7)

class DlgEditModify(wx.Dialog):
    
    def __init__(self, parent, ID, basicSoftwareLink):
        
        wx.Dialog.__init__(self, parent, ID, ("Modify Order"), style = wx.RESIZE_BORDER|wx.CAPTION)
        
        self._basicSoftwareLink = basicSoftwareLink
        
        self._relationship = self._basicSoftwareLink.getRelationship()
        self._price = self._basicSoftwareLink.getPrice()
        self._Qty = self._basicSoftwareLink.getQty()
        self._Way = self._basicSoftwareLink.getWay()
        self._Account = self._basicSoftwareLink.getAccount()
        self._Restriction = self._basicSoftwareLink.getRestriction()
        self._CltType = self._basicSoftwareLink.getCltType()
        self._Validity = self._basicSoftwareLink.getValidity()
        self._PrcMode = self._basicSoftwareLink.getPrcMode()
        self._WaitTime = self.basicSoftwareLink.getWaitingTime()
        self.df_cb = self._basicSoftwareLink.getDataFrame()
        
        self.expected_selection_state = self._basicSoftwareLink.getExpectAnswer()
        self._src = self._basicSoftwareLink.getSource()
        self._dst = self._basicSoftwareLink.getDestination()
        self._returnAction = wx.ID_CANCEL
        
        self.Expected_behavior = expected
        self.choice_way = orderWay
        self.choice_restriction = restriction
        self.choice_prcMode = prcMode
        self.choice_validity = validity
        self.choice_account = account
        self._need_action = [False, '']
        
        lblRela = wx.StaticText(self, wx.ID_ANY, ("Name of the Order"), style=wx.ALIGN_LEFT)
        
        lblQty = wx.StaticText(self, wx.ID_ANY, ("Qty"))
        self._cbQty = wx.CheckBox(self, id=wx.ID_ANY, label='Display')
        self._cbQty.SetValue(self.df_cb['cbQty'].iloc[0])
        self._txtQty = wx.TextCtrl(self, TXT_QTY, value=self._Qty)
        
        lblPrice = wx.StaticText(self, wx.ID_ANY, ("Price"))
        self._cbPrice = wx.CheckBox(self, id=wx.ID_ANY, label='Display')
        self._cbPrice.SetValue(self.df_cb['cbPrice'].iloc[0])
        self._txtPrice = wx.TextCtrl(self, TXT_PRICE, value=self._Price) 
        
        lblAccount = wx.StaticText(self, wx.ID_ANY, ("Account"))
        self._cbAccount = wx.CheckBox(self, id=wx.ID_ANY, label='Display')
        self._cbAccount.SetValue(self.df_cb['cbAccount'].iloc[0])
        self._ccbAccount = wx.ComboBox(self, wx.ID_ANY, size=(120, -1), choices=self.choice_account, style=wx.CB_DROPDOWN, value=self._Account)        
        
        lblRestriction = wx.StaticText(self, wx.ID_ANY, ("Restriction"))
        self._cbRestriction = wx.CheckBox(self, id=wx.ID_ANY, label='Display')
        self._cbRestriction.SetValue(self.df_cb['cbRestriction'].iloc[0])
        self._ccbRestriction = wx.ComboBox(self, wx.ID_ANY, size=(120, -1), choices=self.choice_restriction, style=wx.CB_DROPDOWN, value=self._Restriction)        
        
        lblClientType = wx.StaticText(self, wx.ID_ANY, ("Client Type"))
        self._cbClientType = wx.CheckBox(self, id=wx.ID_ANY, label='Display')
        self._cbClientType.SetValue(self.df_cb['cbClientType'].iloc[0])
        self._txtClientType = wx.TextCtrl(self, TXT_CLTY, value=self._Price)         
        
        lblValidity = wx.StaticText(self, wx.ID_ANY, ("Validity"))
        self._cbValidity = wx.CheckBox(self, id=wx.ID_ANY, label='Display')
        self._cbValidity.SetValue(self.df_cb['cbValidity'].iloc[0])
        self._ccbValidity = wx.ComboBox(self, wx.ID_ANY, size=(120, -1), choices=self.choice_validity, style=wx.CB_DROPDOWN, value=self._Validity)

        lblPriceMode = wx.StaticText(self, wx.ID_ANY, ("Price Mode"))
        self._cbPrcMode = wx.CheckBox(self, id=wx.ID_ANY, label='Display')
        self._cbPrcMode.SetValue(self.df_cb['cbPrcMode'].iloc[0])
        self._ccbPrcMode = wx.ComboBox(self, wx.ID_ANY, size=(120, -1), choices=self.choice_prcMode, style=wx.CB_DROPDOWN, value=self._PrcMode)
        
        lblHC = wx.StaticText(self, wx.ID_ANY, ("HC"))
        self._cbHC = wx.CheckBox(self, id=wx.ID_ANY, label='Display')
        self._txtHC = wx.TxtCtrl(self, TXT_HC, '')
        
        hboxWaiting = wx.BoxSizer(wx.HORIZONTAL)
        self.cbWait = wx.CheckBox(self, id=wx.ID_ANY, label='Would delay the modification')
        hboxWaiting.Add(self.cbWait, 1)
        self._txtWait = masked.NumCtrl(self, TXT_WAIT, value = self._WaitTime, min=0, max=1000000)
        hboxWaiting.Add(self._txtWait, 1, wx.ALIGN_LEFT, 0)
        
        self._txtRelationship = wx.TextCtrl(self, TXT_RELATIONSHIP, self._relationship)
        
        lblWay = wx.StaticText(self, wx.ID_ANY, ("Way"))
        self.ccWay = wx.ComboBox(self, wx.ID_ANY, size=(120, -1), choices=self.choice_way, style=wx.CB_DROPDOWN, value=self._Way)
        self._cbWay = wx.CheckBox(self, id=wx.ID_ANY, label='Display')
        self._cbWay.SetValue(self.df_cb['cbWay'].iloc[0])
        
        self.Bind(wx.EVT_TXT, self._onTxtRelationshipChange, id=TXT_RELATIONSHIP)
        self.Bind(wx.EVT_TXT, self._onTxtPriceChange, id=TXT_PRICE)
        self.Bind(wx.EVT_TXT, self._onTxtQtyChange, id=TXT_QTY)
        self.Bind(wx.EVT_TXT, self._onTxtClientTypeChange, id=TXT_CLTY)
        self.Bind(wx.EVT_TXT, self._onTxtWaitChange, id=TXT_WAIT)
        
        self.ccWay.Bind(wx.EVT_TEXT, self._onSelect2)
        self.ccRestriction.Bind(wx.EVT_TEXT, self._onSelectRestriction)
        self.ccPrcMode.Bind(wx.EVT_TEXT, self._onSelectPrcMode)
        self.ccValidity.Bind(wx.EVT_TEXT, self._onSelectValidity)
        self.ccAccount.Bind(wx.EVT_TEXT, self._onSelectAccount)
        
        self.cbWait.Bind(wx.EVT_CHECKBOX, self._onCmdWait)
        self.cbWay.Bind(wx.EVT_CHECKBOX, self._onCmdWay)
        self.cbQty.Bind(wx.EVT_CHECKBOX, self._onCmdQty)
        self.cbPrice.Bind(wx.EVT_CHECKBOX, self._onCmdPrice)
        self.cbAccount.Bind(wx.EVT_CHECKBOX, self._onCmdAccount)
        self.cbRestriction.Bind(wx.EVT_CHECKBOX, self._onCmdRestriction)
        self.cbClientType.Bind(wx.EVT_CHECKBOX, self._onCmdClientType)
        self.cbValidity.Bind(wx.EVT_CHECKBOX, self._onCmdValidity)
        self.cbPrcMode.Bind(wx.EVT_CHECKBOX, self._onCmdPrcMode)
        self.cbHC.Bind(wx.EVT_CHECKBOX, self._onCmdHC)
        
        
        
        btnOk = wx.button(self, wx.OK, ('&OK'))
        btnOk.SetDefault()
        btnCancel = wx.Button(self, wx.CANCEL, ('&Cancel'))
        btnRemove = wx.Button(self, BTN_REMOVE, ('&Remove'))
        
        self.Bind(wx.EVT_BUTTON, self._onCmdOk, id=wx.OK)
        self.Bind(wx.EVT_BUTTON, self._onCmdCancel, id=wx.CANCEL)
        self.Bind(wx.EVT_BUTTON, self._onCmdRemove, id=BTN_REMOVE)
        
        szr1 = wx.FlexGridSizer(cols=1, hgap=30, vgap=10)
        szr1.AddMany([(lblRela, 0, wx.ALIGN_CENTER_HORIZONTAL),
                      (self._txtRelationship, 0, wx.ALIGN_CENTER_HORIZONTAL),
                      (wx.StaticLine(self, wx.ID_ANY, size=(1,-1), style=wx.LI_HORIZONTAL), 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP),
                      (hboxWaiting, 0, wx.ALIGN_LEFT),
                      (wx.StaticLine(self, wx.ID_ANY, size=(1,-1), style=wx.LI_HORIZONTAL), 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP)])
    
        szr1.AddGrowableCol(0)
        
        szr2 = wx.GridSizer(cols = 3, rows=9, hgap=5, vgap=5)
        szr2.AddMany([
                
                (lblWay, 0, wx.ALIGN_LEFT),
                (self.ccWay, 0, wx.EXPAND)
                (self._cbWay, 0, wx.ALIGN_LEFT),
                
                (lblQty, 0, wx.ALIGN_LEFT),
                (self.ccQty, 0, wx.EXPAND)
                (self._cbQty, 0, wx.ALIGN_LEFT),

                (lblPrice, 0, wx.ALIGN_LEFT),
                (self.ccPrice, 0, wx.EXPAND)
                (self._cbPrice, 0, wx.ALIGN_LEFT),
                
                (lblHC, 0, wx.ALIGN_LEFT),
                (self.ccHC, 0, wx.EXPAND)
                (self._cbHC, 0, wx.ALIGN_LEFT),
        
                (lblAccount, 0, wx.ALIGN_LEFT),
                (self.ccAccount, 0, wx.EXPAND)
                (self._cbAccount, 0, wx.ALIGN_LEFT),

                (lblRestriction, 0, wx.ALIGN_LEFT),
                (self.ccRestriction, 0, wx.EXPAND)
                (self._cbRestriction, 0, wx.ALIGN_LEFT),

                (lblValidity, 0, wx.ALIGN_LEFT),
                (self.ccValidity, 0, wx.EXPAND)
                (self._cbValidity, 0, wx.ALIGN_LEFT),

                (lblClientType, 0, wx.ALIGN_LEFT),
                (self.ccClientType, 0, wx.EXPAND)
                (self._cbClientType, 0, wx.ALIGN_LEFT),
                
                (lblPriceMode, 0, wx.ALIGN_LEFT),
                (self.ccPrcMode, 0, wx.EXPAND)
                (self._cbPrcMode, 0, wx.ALIGN_LEFT)])
    
    
        szr4 = wx.BoxSizer(wx.HORIZONTAL)
        szr4.Add(btnRemove, 0, wx.ALL, 5)
        szr4.Add(btnOk, 0, wx.ALL, 5)
        szr4.add(btnCancel, 0, wx.ALL, 5)
        
        szr5 = wx.BoxSizer(wx.VERTICAL)
        szr5.Add(szr1, 0, wx.GROW|wx.ALL, 10)
        szr5.Add(szr2, 0, wx.GROW|wx.ALL, 10)
        szr5.Add(szr4, 0, wx.ALIGN_RIGHT|wx.ALL, 10)
            
        self.SetSizer(szr5)
        self.SetAutoLayout(True)
        szr5.Fit(self)
        
    def _onTxtRelationshipChange(self, event):
        self._relationship = event.GetString().strip()
        
    def _onTxtWaitChange(self, event):
        self._WaitTime = event.GetString().strip()
    
    def _onTxtPriceChange(self, event):
        self.SetPrice(event.GetString().strip())
        
    def SetPrice(self, price):
        self._price = price
    
    def _onSelectAccount(self, event):
        self._Account = self._ccbAccount.GetStringSelection()
        
    def _onSelectRestriction(self, event):
        self._Restriction = self._ccbAccount.GetStringSelection()

    def _onCmdWay(self, event):
        
        if self._cbWay.Value == False:
            self.df_cb['cbWay'].iloc[0] = False
        else:
            self.df_cb['cbWay'].iloc[0] = True
        event.skip()
        
    def _onCmdQty(self, event):
        
        if self._cbQty.Value == False:
            self.df_cb['cbQty'].iloc[0] = False
        else:
            self.df_cb['cbQty'].iloc[0] = True
        event.skip()        
        
    def _onCmdPrice(self, event):
        
        if self._cbPrice.Value == False:
            self.df_cb['cbPrice'].iloc[0] = False
        else:
            self.df_cb['cbPrice'].iloc[0] = True
        event.skip()
        
    def _onCmdAccount(self, event):
        
        if self._cbAccount.Value == False:
            self.df_cb['cbAccount'].iloc[0] = False
        else:
            self.df_cb['cbAccount'].iloc[0] = True
        event.skip()
                
    def _onCmdRestriction(self, event):
        
        if self._cbRestriction.Value == False:
            self.df_cb['cbRestriction'].iloc[0] = False
        else:
            self.df_cb['cbRestriction'].iloc[0] = True
        event.skip()
        
    def _onCmdClientType(self, event):
        
        if self._cbClientType.Value == False:
            self.df_cb['cbClientType'].iloc[0] = False
        else:
            self.df_cb['cbClientType'].iloc[0] = True
        event.skip()
        
    def _onCmdValidity(self, event):
        
        if self._cbValidity.Value == False:
            self.df_cb['cbValidity'].iloc[0] = False
        else:
            self.df_cb['cbValidity'].iloc[0] = True
        event.skip()

    def _onCmdPrcMode(self, event):
        
        if self._cbPrcMode.Value == False:
            self.df_cb['cbPrcMode'].iloc[0] = False
        else:
            self.df_cb['cbPrcMode'].iloc[0] = True
        event.skip()

    def _onCmdHC(self, event):
        
        if self._cbHC.Value == False:
            self.df_cb['cbHC'].iloc[0] = False
        else:
            self.df_cb['cbHC'].iloc[0] = True
        event.skip()

    def _onTxtClientTypeChange(self, event):
        self._CltType = event.GetString().strip()
        
    def _onSelectValidity(self, event):
        self._Validity = self._ccbValidity.GetStringSelection()
        
    def _onSelectPrcMode(self, event):
        self._PrcMode = self._ccbPrcMode.GetStringSelection()
             
    def getPrice(self):
        try:
            return self._price
        except AttributeError:
            self._price= 0
            return self._price
        
    def _onTxtQtyChange(self, event):
        self._Qty = event.GetString().strip()    

    def _onCmdOk(self, event):
        self._basicSoftwareLink.setName('Modify :' + self._relationship)
        self._basicSoftwareLink.setPrice(self._price)
        self._basicSoftwareLink.setQty(self._Qty)
        self._basicSoftwareLink.setWay(self._Way)
        self._basicSoftwareLink.setAccount(self._Account)
        self._basicSoftwareLink.setRestriction(self._Restriction)
        self._basicSoftwareLink.setCltType(self._CltType)
        self._basicSoftwareLink.setValidity(self._Validity)
        self._basicSoftwareLink.setPrcMode(self._PrcMode)
        self._basicSoftwareLink.setRelationshu(self._relationship)
        self._returnAction = wx.ID_OK
        self.Close()
        
        self.df_cb['cbWay'].iloc[1] = self._Way
        self.df_cb['cbQty'].iloc[1] = self._Qty
        self.df_cb['cbPrice'].iloc[1] = self._Price
        self.df_cb['cbAccount'].iloc[1] = self._Account
        self.df_cb['cbRestriction'].iloc[1] = self._Restriction
        self.df_cb['cbClientType'].iloc[1] = self._ClientType
        self.df_cb['cbValidity'].iloc[1] = self._Validity
        self.df_cb['cbPrcMode'].iloc[1] = self._PrcMode
        self._basicSoftwareLink.setDataFrame(self.db_cb)
        
        OutputTitle = ""
        for column in self.df_cb:
            if self.df_cb[column].iloc[0] == True:
                OutputTitle += str(self.df_cb[column].iloc[1]).lower() + " "
        
        self._basicSoftwareLink.setName('Modify : ' + self._relationship + " " + OutputTitle)
        if self.cbWait.Value == True:
            self._basicSoftwareLink.setWaiting(self._WaitTime)
        else:
            self._basicSoftwareLink.setWaiting(0)
            
    def _onCmdCancel(self, event):
        self._returnAction = wx.ID_CANCEL
        self.Close()
    
    def _onRemove(self):
        self._returnAction = wx.ID_NO
        self.Close()
        
    def _onCmdWait(self, event):
        if self._cbWait.Value == False:
            self._txtWait.Enable(False)
        else:
            self._txtWait.Enable(True)
        event.skip()        

    def _onSelect2(self, event):
        self._Way = self.ccWay.GetStringSelection()
        
    def setRelationship(self, rela):
        self._relationship = rela
        
    def getRelationShip(self):
        return self._relationship
    
    def getReturnAction(self):
        return self._returnAction
    
    def getObject(self):
        return(self._src, self.dest)

    def getName(self):
        return self._basicSoftwareLink.getName()



















