# -*- coding: utf-8 -*-

import wx
from BasicSoftwareUtils  import displayError
from BasicSoftwareDocument import BasicSoftwareDocument
import os

def shorterFilename(filename):
    return os.path.split(filename)[1]

DefaultFilename=("Untitled.xml")

class BasicSoftwareProject:
    def __init__(self, filename, parentFrame, tree, treeroot):
        import mediator
        self._parentFrame = parentFrame
        self._ctrl = mediator.get_mediator()
        self._documents = []
        self._filename = filename
        self._modified = False
        self._treeRootParent = treeroot
        self._tree = tree
        self._treeRoot = None
        self._codePath = ""
        self.addToTree()
        
    def setFilename(self, filename):
        self._filename = filename
        self.updateTreeText()
        
    def getFilename(self):
        return self._filename
    
    def getDocuments(self):
        return self._documents
    
    def setModified(self, value=True):
        self._modified = value
        
    def getModified(self):
        return self._modified
    
    def addToTree(self):
        self._treeRoot = self._tree.AppendItem(self._treeRootParent, shorterFilename(self._filename), data=self)
        self._tree.Expand(self._treeRoot)
        
        for document in self._documents:
            document.addToTree(self, self._tree, self._treeRoot)
    
    def removeToTree(self):
        self._tree.Delete(self._treeRoot)
        
    def loadFromFile(self, filename):
        
        import IoFile
        wx.BeginBusyCursor()
        io = IoFile.IoFile()
        
        self._filename = filename
        try:
            io.open(filename, self)
            self._modified = False
        except:
            msg = "Error loading project file [%s]" %filename
            wx.EndBusyCursor()
            displayError(msg, 'Loading Error')
            return False
        wx.EndBusyCursor()
        
        self.updateTreeText()
        
        if len(self._documents) > 0:
            self._ctrl.getFileHandling().showFrame(self._documents[0].getFrame())
            self._documents[0].getFrame().Refresh()
            return True
        else:
            msg = "Errpr while loading a project from file [%s] into the mediator"%filename
            displayError(msg, 'Load Error')
            return False
        
    def loadFromText(self, xmlString):
        import IoText
        io = IoText.IoText()
        
        try:
            io.open(xmlString, self)
            self._modified = False
        except:
            msg = "Error loading project string [%s]" %xmlString
            wx.EndBusyCursor()
            displayError(msg, 'Loading Error')
            return False
        
        self.updateTreeTxt()

        if len(self._documents) > 0:
            self._ctrl.getFileHandling().showFrame(self._documents[0].getFrame())
            self._documents[0].getFrame().Refresh()
            return True
        else:
            msg = "Errpr while loading a project from string [%s] into the mediator"%xmlString
            displayError(msg, 'Load Error')
            return False            
        
    def insertProject(self, filename):
        
        import IoFile
        wx.BeginBusyCursor()
        io = IoFile.IoFile()
        
        try:
            io.open(filename, self)
            self._modified = False
        except:
            msg = "Error inserting file project [%s] into current one" %filename
            wx.EndBusyCursor()
            displayError(msg, 'Insert Error')
            return False

        wx.EndBusyCursor()
        self.updateTreeTxt()

        if len(self._documents) > 0:
            frame = self._documents[0].getFrame()
            self._ctrl.getFileHandling().registerUmlFrame(frame)
        
        return True
    
    def newDocument(self, Type):
        
        document = BasicSoftwareDocument(self._parentFrame, self, Type)
        self._documents.append(document)
        document.addToTree(self._tree, self._treeRoot)
        frame = document.getFrame()
        self._ctrl.getFileHandling().registerUmlFrame(frame)
        return document
    
    def getFrames(self):
        return[document.getFrame() for document in self._documents]
        
    def saveXmlBasicSoftware(self):
        import IoFile
        io = IoFile.IoFile()
        wx.BeginBusyCursor()
        try:
            io.save(self)
            self._modified = False
            self.updateTreeTxt()
        except:
            msg = "Error saving project"
            wx.EndBusyCursor()
            displayError(msg, 'Saving Error')
            return False       
        wx.EndBusyCursor()
        
    def updateTreeTxt(self):
        self._tree.SetItemText(self._treeRoot, shorterFilename(self._filename))
        for document in self._documents:
            document.updateTreeText()
            
    def removeDocument(self, document, confirmation=True):
        frame = document.getFrame()
        
        if confirmation:
            self._ctrl.getFileHandling().showFrame(frame)
            dlg = wx.MessageDialog(self._parentFrame, 'Are you sure to remove the document ?', 'Remove a document from a project', wx.YES_NO)
            if dlg.ShowModal() == wx.NO:
                dlg.Destroy()
                return
            dlg.Destroy()
        
        filehandling = self._ctrl.getFileHandling()
        filehandling.removeAllReferencesToUmlFrame(frame)
        
        document.removeFromTree()
        self._documents.remove(document)
        