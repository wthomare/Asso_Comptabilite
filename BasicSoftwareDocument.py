# -*- coding: utf-8 -*-

from UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame
from BasicSoftwareConst import DiagramLabels

def shorterFilename(filename):
    import os
    return os.path.split(filename)[1]

class BasicSoftwareDocument:
    def __init__(self, parentFrame, project, Type):
        self._parentFrame = parentFrame
        self._project = project
        self._treeRoot =None
        self._treeRootParent = None
        self._tree = None
        self._type = Type
        self._title = DiagramLabels[self._type]
        self._frame = UmlSequenceDiagramsFrame(parentFrame)
        
    def getType(self):
        return self._type
    
    def getDiagramTitle(self):
        return self._project.getFilename() + "/" + self._title
    
    def getFrame(self):
        return self._frame
    
    def addToTree(self, tree, root):
        self._tree = tree
        self._treeRootParent = root
        self._treeRoot = tree.AppendItem(self._treeRootParent, self._title)
        self._tree.SetItemData(self._treeRoot, self._frame)
        
    def updateTreeText(self):
        self._tree.SetItemText(self._treeRoot, self._title)
        
    def removeFromTree(self):
        self._tree.Delete(self._treeRoot)
    
    