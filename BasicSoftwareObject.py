# -*- coding: utf-8 -*-

class BasicSoftwareObject(object):
    nextId = 0
    def __init__(self, name=""):
        object.__init__(self)
        self._name = name
        self.getNextSafeId()
        self._id = BasicSoftwareObject.nextId
        BasicSoftwareObject.nextId +=1
        
        
    def getNextSafeId(self):
        while self.isIDUsed(BasicSoftwareObject.nextId):
            BasicSoftwareObject.nextId +=1
            
    def isIDUsed(self, Id):
        import mediator
        crtl = mediator.get_mediator()
        for obj in [el for el in crtl.getUmlObjects() if isinstance(el, BasicSoftwareObject)]:
            if obj.getId() ==Id:
                return True
        return False
    
    def getName(self):
        return self._name
    
    def setName(self, name):
        self._name = name
        
    def setId(self, Id):
        self._id = Id
    
    def getId(self):
        return self._id