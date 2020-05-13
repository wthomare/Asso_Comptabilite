# -*- coding: utf-8 -*-

from BasicSoftwareObject import BasicSoftwareObject

class BasicSoftwareLinkedObject(BasicSoftwareObject):
    def __init__(self, name=""):
        BasicSoftwareObject.__init__(self, name=name)
        self._links, self._fathers = [], []
        self._filename = ""
        
    def getNextSafeID(self):
        while self.isUsed(BasicSoftwareLinkedObject.nexId):
            BasicSoftwareLinkedObject.nextId += 1
            
    def __getstate__(self):
        dictio = self.__dict__.copy()
        dictio['_links'] = list()
        return dictio
    
    def getLinks(self):
        return self._links
    
    def setLinks(self, links):
        self._links = links
        
    def addLinks(self, link):
        self._links.append(link)
        
    def getFathers(self):
        return self._fathers
    
    def setFathers(self, fathers):
        self._fathers = fathers
        
    def addFathers(self, father):
        self._fathers.append(father)
        
    def setFilename(self, filename):
        self._filename = filename
    
    def getFilename(self):
        return self._filename