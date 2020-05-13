# -*- coding: utf-8 -*-

from BasicSoftwareLinkedObject import BasicSoftwareLinkedObject
import pandas as pd

class BasicSoftwareLink(BasicSoftwareLinkedObject):
    def __init__(self, name=' ', linkType=0, source=None, destination=None, answer='', Qty='', Price='', Way='',
                 account='', restriction='', cltType='', validity='', prcMode='', relationship='', waitTime=0, df_CB=None):
        
        if not df_CB:
            df_CB = pd.DataFrame({'cbWay':[False, ""], 'cbQty':[False, ""],'cbPrice':[False, ""],
                                  'cbAccount':[False, ""],'cbRestriction':[False, ""],'cbClientType':[False, ""],
                                  'cbValidity':[False, ""],'cbPriceMode':[False, ""]})
        
        BasicSoftwareLinkedObject.__init__(self, name=name)
        self._type = linkType
        self._src = source
        self._dst = destination
        self.answer = answer
        self._Qty = Qty
        self._Price = Price
        self._Way = Way
        self._Account = account
        self._Restriction = restriction
        self._CltType = cltType
        self._Validity = validity
        self._PrcMode = prcMode
        self._relationship = relationship
        self.waitTime = waitTime
        self.df_checkBox = df_CB
        
    def __str__(self):
        return "(%s) links from %s to %s"%(self.getName, self._src, self._dst)
    
    def getSource(self):
        return self._src
    
    def setSource(self, source):
        self._src = source
        
    def getDestination(self):
        return self._dst
    
    def setDestination(self, destination):
        self._dst = destination
        
    def setType(self, theType):
        if isinstance(theType, str):
            try:
                theType = int(theType)
            except:
                theType = 0
        self._type = theType
    
    def getType(self):
        return self._type

    def getExpectAnswer(self):
        return self.answer
    
    def setExpectAnswer(self, answer):
        self.answer = answer
        
    def setQty(self, qty):
        self._Qty = qty
    
    def getQty(self):
        return self._Qty
    
    def setPrice(self, price):
        self._Price = price
    
    def getPrice(self):
        return self._Price

    def setWay(self, way):
        self._Way = way
    
    def getWay(self):
        return self._Way    
        
    def setAccount(self, account):
        self._Account = account
    
    def getAccount(self):
        return self._Account

    def setRestriction(self, restriction):
        self._Restriction = restriction
    
    def getRestriction(self):
        return self._Restriction

    def setCltType(self, cltType):
        self._CltType = cltType
    
    def getCltType(self):
        return self._CltType

    def setValidity(self, validity):
        self._Validity = validity
    
    def getValidity(self):
        return self._Validity

    def setPrcMode(self, prcMode):
        self._PrcMode = prcMode
    
    def getPrcMode(self):
        return self._PrcMode

    def setRelationship(self, rela):
        self._relationship = rela
    
    def getRelationship(self):
        return self._relationship

    def setWaitingTime(self, timer):
        self.waitTime = timer
    
    def getWaitingTime(self):
        return self.waitTime

    def setDataFrame(self, df):
        self.df_checkBox = df
    
    def getDataFrame(self):
        return self.df_checkBox
        
        