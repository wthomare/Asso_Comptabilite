# -*- coding: utf-8 -*-

from command import Command
from OglObjectFactory import getOglObjectFactory
from BasicSoftwareConst import OGL_FOR
from mediator import get_mediator
from delOglObject2Command import DelOglObject2Command
from BasicSoftwareSuperObject import BasicSoftwareSuperObject
from BasicSoftwareUtils import displayWarning, displayError


from DlgEditNote import DlgEditNote
from DlgEditStatement import DlgEditStatement
from DlgEditLog import DlgEditLog
from DlgEditFixAdd import DlgEditFixAdd
from DlgEditFixExpect import DlgEditFixExpect
from DlgEditFixFlush import DlgEditFixFlush
from DlgEditFixInit import DlgEditFixInit
from DlgEditFixRemove import DlgEditFixRemove
from DlgEditFixSetup import DlgEditFixSetup
from DlgEditFixStart import DlgEditFixStart
from DlgEditFixWait import DlgEditFixWait
from DlgEditFOR import DlgEditFOR
from DlgEditWHILE import DlgEditWHILE
from DlgEditTitle import DlgEditTitle
from DlgImport import DlgImport

import wx, os

class CreateOglObjectCommand(Command):
    def __init__(self,x=0, y=0, forExecute=False, shape=None, function="", Type=OGL_FOR):
        Command.__init__(self)
        
        self._x = x
        self._y = y
        self._forExecute = forExecute
        self._shape = shape
        self._function = function
        self._Type = Type
        
        self.dlg_state = None
        
        if forExecute:
            self._shape = self._createObject(self._x, self._y, self._Type)
        else:
            DelOglObject2Command.__init__(self, self._shape)
            
    def serialize(self):
        return DelOglObject2Command.serialize(self)
    
    def unserialize(self, serializedInfos):
        DelOglObject2Command.unserialize(self, serializedInfos)
        
    def redo(self):
        DelOglObject2Command.undo(self)
        
    def redoUpdate(self, serializedInfos):
        DelOglObject2Command.undoUpDate(self, serializedInfos)
         
        umlFrame = self.getGroup().getHistory().getFrame()
        umlFrame.addShape(self._shape, 0, 0, withModelUpdate=False)
        self._shape.UpdateFromModel(False)
        umlFrame.Refresh()
        
    def undo(self):
        DelOglObject2Command.redo(self)
        
    def upDate(self, serializedInfos):
        DelOglObject2Command.upDate(self, serializedInfos)
        
    def execute(self):
        pass
    
    def _createObject(self, x, y, Type=OGL_FOR):
        
        from OglNote import OglNote
        from OglTitle import OglTitle
        from OglTitleEnd import OglTitleEnd
        from OglStatement import OglStatement
        from OglLog import OglLog
        from OglFixLog import OglFixLog
        from OglFor import OglFor
        from OglWhile import OglWhile
        from OglImport import OglImport
        
        umlFrame = get_mediator().getFileHandling().getCurrentFrame()
        basicSoftwareSuperObject = BasicSoftwareSuperObject(Type=Type)
        
        oglObjectFactory = getOglObjectFactory()
        oglObject = oglObjectFactory.getOglObject(basicSoftwareObject=basicSoftwareSuperObject, Type=Type)
        
        if isinstance(oglObject, OglNote):
            dlg=DlgEditNote(umlFrame, wx.ID_ANY, basicSoftwareSuperObject)
            self.dlg_state = dlg.getReturnAction()
            
            if self.dlg_state == wx.ID_OK:
                dlg.Destroy()
                oglSuperObjet = OglNote(basicSoftwareSuperObject=basicSoftwareSuperObject)
                umlFrame.addShape(oglSuperObjet, x, y, withModelUpdate=True)
                umlFrame.Refresh()
                return oglSuperObjet
            elif self.dlg_state in [wx.ID_NO, wx.ID_CANCEL]:
                dlg.Destroy()
                
        elif isinstance(oglObject, OglTitle):
            dlg = DlgEditTitle(umlFrame, wx.ID_ANY, basicSoftwareSuperObject)
            self.dlg_state = dlg.getReturnAction()
            
            if self.dlg_state == wx.ID_OK:
                dlg.Destroy()
                oglSuperObjet = OglTitle(basicSoftwareTitle=basicSoftwareSuperObject)
                umlFrame.addShape(oglSuperObjet, x, y, withModelUpdate=True)
                umlFrame.Refresh()
                return oglSuperObjet
            elif self.dlg_state in [wx.ID_NO, wx.ID_CANCEL]:
                dlg.Destroy()            
                return False

        elif isinstance(oglObject, OglTitleEnd):
            basicSoftwareSuperObject.setInstanceTitleType('End')
            oglSuperObjet = OglTitleEnd(basicSoftwareSuperObject)
            umlFrame.addShape(oglSuperObjet, x, y, withModelUpdate=True)
            umlFrame.Refresh()
            return oglSuperObjet

        elif isinstance(oglObject, OglStatement):
            
            dlg = DlgEditStatement(umlFrame, wx.ID_ANY, basicSoftwareSuperObject)
            self.dlg_state = dlg.getReturnAction()
            
            if self.dlg_state == wx.ID_OK:
                dlg.Destroy()
                oglSuperObjet = OglStatement(basicSoftwareSuperObject)
                umlFrame.addShape(oglSuperObjet, x, y, withModelUpdate=True)
                umlFrame.Refresh()
                return oglSuperObjet
            elif self.dlg_state in [wx.ID_NO, wx.ID_CANCEL]:
                dlg.Destroy()            
                return False    

        elif isinstance(oglObject, OglLog):
            
            dlg = DlgEditLog(umlFrame, wx.ID_ANY, basicSoftwareSuperObject)
            self.dlg_state = dlg.getReturnAction()
            
            if self.dlg_state == wx.ID_OK:
                dlg.Destroy()
                oglSuperObjet = OglLog(basicSoftwareSuperObject=basicSoftwareSuperObject)
                umlFrame.addShape(oglSuperObjet, x, y, withModelUpdate=True)
                umlFrame.Refresh()
                return oglSuperObjet
            elif self.dlg_state in [wx.ID_NO, wx.ID_CANCEL]:
                dlg.Destroy()            
                return False
        elif isinstance(oglObject, OglFixLog):
            basicSoftwareSuperObject.setFunction(self._function)
            
            if self._function =='Init':
                dlg = DlgEditFixInit(umlFrame, wx.ID_ANY, basicSoftwareSuperObject)
                self.dlg_state = dlg.getReturnAction()
                dlg.Destroy()
            elif self._function == 'Start':
                dlg = DlgEditFixStart(umlFrame, wx.ID_ANY, basicSoftwareSuperObject)
                self.dlg_state = dlg.getReturnAction()
                dlg.Destroy() 
            elif self._function == 'Setup':
                dlg = DlgEditFixSetup(umlFrame, wx.ID_ANY, basicSoftwareSuperObject)
                self.dlg_state = dlg.getReturnAction()
                dlg.Destroy()  
            elif self._function == 'Stop':
                pass
            elif self._function == 'Flush':
                dlg = DlgEditFixFlush(umlFrame, wx.ID_ANY, basicSoftwareSuperObject)
                self.dlg_state = dlg.getReturnAction()
                dlg.Destroy() 
            elif self._function == 'Expect':
                dlg = DlgEditFixExpect(umlFrame, wx.ID_ANY, basicSoftwareSuperObject)
                self.dlg_state = dlg.getReturnAction()
                dlg.Destroy() 
            elif self._function == 'Add':
                dlg = DlgEditFixAdd(umlFrame, wx.ID_ANY, basicSoftwareSuperObject)
                self.dlg_state = dlg.getReturnAction()
                dlg.Destroy()      
            elif self._function == 'Remove':
                dlg = DlgEditFixRemove(umlFrame, wx.ID_ANY, basicSoftwareSuperObject)
                self.dlg_state = dlg.getReturnAction()
                dlg.Destroy()
            elif self._function == 'Wait':
                dlg = DlgEditFixWait(umlFrame, wx.ID_ANY, basicSoftwareSuperObject)
                self.dlg_state = dlg.getReturnAction()
                dlg.Destroy()
            else:
                displayWarning("Unkown Fixlog function", "CreateOglObjectommand._createObject")
            
            if self.dlg_state == wx.ID_OK:
                oglSuperObjet = OglFixLog(basicSoftwareSuperObject)
                umlFrame.addShape(oglSuperObjet, x, y, withModelUpdate=True)
                umlFrame.Refresh()
                return oglSuperObjet
            elif self.dlg_state in [wx.ID_NO, wx.ID_CANCEL]:
                return False
        elif isinstance(oglObject, (OglFor, OglWhile)):
            if self._function == 'FOR':
                dlg = DlgEditFOR(umlFrame, wx.ID_ANY, basicSoftwareSuperObject)
                self.dlg_state = dlg.getReturnAction()
            elif self._function == 'WHILE':
                dlg = DlgEditWHILE(umlFrame, wx.ID_ANY, basicSoftwareSuperObject)
                self.dlg_state = dlg.getReturnAction()
            else:
                displayError('UNknow type of Loop [%s]'%(self._function),'CreateOglObjectommand()._createObject')

            if self.dlg_state == wx.ID_OK:
                dlg.Destroy()
                if self._function =="FOR":
                    oglSuperObjet = OglFor(basicSoftwareSuperObject)
                elif self._function == "WHILE":
                    oglSuperObjet = OglWhile(basicSoftwareSuperObject)
                umlFrame.addShape(oglSuperObjet, x, y, withModelUpdate=True)
                umlFrame.Refresh()
                return oglSuperObjet
            elif self.dlg_state in [wx.ID_NO, wx.ID_CANCEL]:
                dlg.Destroy()
                return False

        elif isinstance(oglObject, OglImport):
            oldPath = os.getcwd()
            dlg =  DlgImport(umlFrame)
            xml_path = os.path.dirname(dlg.GetPath())
            filename = os.path.basename(dlg.GetPath())
            dlg.Destroy()
            if xml_path == None and filename == None:
                basicSoftwareSuperObject.setPath('\\')
                basicSoftwareSuperObject.setName("No file\n selected")
                oglSuperObjet = OglImport(basicSoftwareSuperObject)
                umlFrame.addShape(oglSuperObjet, x, y, withModelUpdate=True)
                umlFrame.Refresh()
                return oglSuperObjet
            else:
                os.chdir(oldPath)
                basicSoftwareSuperObject.setPath(xml_path)
                basicSoftwareSuperObject.setName(filename) 
                oglSuperObjet = OglImport(basicSoftwareSuperObject)
                umlFrame.addShape(oglSuperObjet, x, y, withModelUpdate=True)
                umlFrame.Refresh()
                return oglSuperObjet                                   