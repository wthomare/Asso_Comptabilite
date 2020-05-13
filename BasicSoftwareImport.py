# -*- coding: utf-8 -*-

from BasicSoftwareLinkedObject import BasicSoftwareLinkedObject

class BasicSoftwareImport(BasicSoftwareLinkedObject):
    def __init__(self, name="", path=""):
        BasicSoftwareLinkedObject.__init__(name)
        self._path = path
        
    def setPath(self, path):
        self._path = path
        
    def getPath(self):
        return self._path