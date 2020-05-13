# -*- coding: utf-8 -*-

from BasicSoftwareLinkedObject import BasicSoftwareLinkedObject

class BasicSoftwareModify(BasicSoftwareLinkedObject):
    def __init__(self, name= "", isWait = False, waitTime=0):
        BasicSoftwareLinkedObject.__init__(self, name)
        self.isWait=isWait
        self.waitTime = waitTime
        
    def setIsWait(self, w):
        self.isWait = w
        
    def getIsWait(self):
        return self.isWait
    
    def setWaitingTime(self, timer):
        self.waitTime = timer
        
    def getWaitingTime(self):
        return self.waitTime
    