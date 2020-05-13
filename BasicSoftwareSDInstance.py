# -*- coding: utf-8 -*-
from BasicSoftwareLinkedObject import BasicSoftwareLinkedObject

class BasicSoftwareSDInstance(BasicSoftwareLinkedObject):
    def __init__(self, name="", actor=""):
        BasicSoftwareLinkedObject.__init__(self, name)
        self._instanceName= "Unnamed"
        self._lifeLineLength = 200
        self._actor = "Unnamed actor"
        
    def getInstanceName(self):
        return self._instanceName
    
    def setInstanceName(self, value):
        self._instanceName = value
        
    def getInstanceLifeLineLength(self):
        return self._lifeLineLength
    
    def setInstanceLifeLineLength(self, value):
        self._lifeLineLength = value
        
    def setInstanceType(self, value):
        self._actor = value
        
    def getInstanceType(self):
        return self._actor
