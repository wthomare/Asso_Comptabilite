# -*- coding: utf-8 -*-

import wx

from singleton import Singleton
from mediator import get_mediator
from BasicSoftwareUtils import displayError, displayWarning
from BasicSoftwareSuperObject import BasicSoftwareSuperObject
from BasicSoftwareSDInstance import BasicSoftwareSDInstance
from BasicSoftwareConst import OGL_NOTE, OGL_TITLE, OGL_TITLEEND, OGL_STATEMENT, OGL_LOG, OGL_FIXLOG, OGL_FOR, OGL_WHILE, OGL_IMPORT
from BasicSoftwareLink import BasicSoftwareLink

from OglNote import OglNote
from OglSDInstance import OglSDInstance
from OglTitle import OglTitle
from OglFor import OglFor
from OglWhile import OglWhile
from OglStatement import OglStatement
from OglImport import OglImport
from OglTitleEnd import OglTitleEnd
from OglLog import OglLog
from OglFixLog import OglFixLog

from copy import deepcopy

def getController():
    return Ctrl_Manager()


class Ctrl_Manager(Singleton):
    def init(self):
        self._ctrl = get_mediator()
        self._fileHandling = self._ctrl.getFileHandling()
        self._clipboard = []
        self.x, self.y = 100,100
        
    def _OnMnuEditCopy(self):
        selected = self._ctrl.getSelectedShape()
        if len(selected) > 0:
            self._clipboard = []
        else:
            return
        
        for obj in selected:
            obj = deepcopy(obj.getBasicSoftwareObject())
            if isinstance(obj, BasicSoftwareLink):
                displayError(("The copy of link is not yet supported. This Event will be skipt"), ('Copy Error'))
            else:
                self._clipboard.append(obj)
                
    def _OnMnuEditPaste(self):
        
        if len(self._clipboard) == 0:
            return
        umlFrame= self._ctrl.getUmlFrame()
        if not umlFrame:
            displayWarning(("No current Frame to paste the selection"), ("Paste error"))
            return
        
        for obj in self._clipboard:
            obj = deepcopy(obj)
            obj._id = obj.nextId
            obj.nextId +=1

            if isinstance(obj, BasicSoftwareSuperObject):
                objtype = int(obj.getType())
                if objtype == OGL_NOTE:
                    po = OglNote(obj)
                elif objtype == OGL_TITLE:
                    po= OglTitle(obj)
                elif objtype == OGL_TITLEEND:
                    po = OglTitleEnd(obj)
                elif objtype == OGL_STATEMENT:
                    po = OglStatement(obj)
                elif objtype == OGL_LOG:
                    po = OglLog(obj)
                elif objtype == OGL_FIXLOG:
                    po = OglFixLog(obj)
                elif objtype == OGL_FOR:
                    po = OglFor(obj)
                elif objtype == OGL_WHILE:
                    po = OglWhile(obj)
                elif objtype == OGL_IMPORT:
                    po = OglImport(obj)
                else:
                    displayError(("Unknown Type of BasicSoftware Object : [%s]" %(type(obj))), ("Paste Error"))
            elif isinstance(obj, BasicSoftwareSDInstance):
                po = OglSDInstance(parentFrame=umlFrame, BasicSoftwareObject=obj)
            
            else:
                displayError(("Unknow type of Ogl Object : [%s]. This event will be skipt" %type(obj)), ("Paste Error"))
                return
            
            self._ctrl.getUmlFrame().addShape(po, self.x, self.y)
            self._ctrl.upDateHistoryManager(po, wx.ID_PASTE)
            
            self.x += 20
            self.y += 20
            
        canvas = po.GetDiagram().GetPanel()
        dc = wx.ClientDF(canvas)
        canvas.PrepareDC(dc)
        
        self._fileHandling.getCurrentFrame().getHistory()._groupToUndo +=1
        self._fileHandling.setModified(True)
        self._ctrl.updateTitle()
        canvas.Refresh()
        
    def _OnMnuEditPasteRightClick(self, x, y):
        if len(self._clipboard) == 0:
            return
        umlFrame= self._ctrl.getUmlFrame()
        if not umlFrame:
            displayWarning(("No current Frame to paste the selection"), ("Paste error"))
            return
        
        for obj in self._clipboard:
            obj = deepcopy(obj)
            obj._id = obj.nextId
            obj.nextId +=1

            if isinstance(obj, BasicSoftwareSuperObject):
                objtype = int(obj.getType())
                if objtype == OGL_NOTE:
                    po = OglNote(obj)
                elif objtype == OGL_TITLE:
                    po= OglTitle(obj)
                elif objtype == OGL_TITLEEND:
                    po = OglTitleEnd(obj)
                elif objtype == OGL_STATEMENT:
                    po = OglStatement(obj)
                elif objtype == OGL_LOG:
                    po = OglLog(obj)
                elif objtype == OGL_FIXLOG:
                    po = OglFixLog(obj)
                elif objtype == OGL_FOR:
                    po = OglFor(obj)
                elif objtype == OGL_WHILE:
                    po = OglWhile(obj)
                elif objtype == OGL_IMPORT:
                    po = OglImport(obj)
                else:
                    displayError(("Unknown Type of BasicSoftware Object : [%s]" %(type(obj))), ("Paste Error"))
            elif isinstance(obj, BasicSoftwareSDInstance):
                po = OglSDInstance(parentFrame=umlFrame, BasicSoftwareObject=obj)
            
            else:
                displayError(("Unknow type of Ogl Object : [%s]. This event will be skipt" %type(obj)), ("Paste Error"))
                return
            
            self._ctrl.getUmlFrame().addShape(po, x, y)
            self._ctrl.upDateHistoryManager(po, wx.ID_PASTE)
            
            x += 20
            y += 20
            
        canvas = po.GetDiagram().GetPanel()
        dc = wx.ClientDF(canvas)
        canvas.PrepareDC(dc)
        
        self._fileHandling.getCurrentFrame().getHistory()._groupToUndo +=1
        self._fileHandling.setModified(True)
        self._ctrl.updateTitle()
        canvas.Refresh()
        
    def _OnMnuEditCut(self):
        
        selected = self._ctrl.getSelectedShapes()
        if len(selected) > 0:
            self._clipboard = []
        else:
            return

        canvas = selected[0].GetDiagram().GetPanel()
        
        from BasicSoftwareLink import BasicSoftwareLink
        for obj in selected:
            basicSoftwareObj = obj.getBasicSoftwareObject()
            if isinstance(basicSoftwareObj, BasicSoftwareLink):
                displayError(("The copy of OglLink is not yet supported. This Event will be skipt"), ("Cut Error"))
            else:
                obj.Detach()
                self._clipboard.append(basicSoftwareObj)
        
        self._fileHandling.setModified(True)
        self._ctrl.updateTitle()
        canvas.Refresh()