# -*- coding: utf-8 -*-

from command import Command
from delOglSDInstanceCommand import DelOglSDInstanceCommand
from DlgInstance import DlgInstance
from mediator import get_mediator
from BasicSoftwareSDInstance import BasicSoftwareSDInstance
from OglSDInstance import OglSDInstance

import BasicSoftwareUtils
import wx

class CreateOglSDInstanceCommand(Command):
    def __init__(self, x=0, y=0, forExecute=False, shape=None, function = "", autoCreate=False, iterAuto=None, client='PyCaRO'):
        Command.__init__(self)
        self._x = x
        self._y = y
        self._forExecute = forExecute
        self._shape = shape
        self._function = function
        self._autoCreate = autoCreate
        self._iterAuto = iterAuto
        self._client = client
        
        self.dlg_state = None


        if forExecute == False:
            self._shape = self._createNewSDInstance(self._x, self._y)
        elif forExecute == True:
            self._shape = self._createNewAutoSDInstance(self._x, self._y, self._Type)
        else:
            DelOglSDInstanceCommand.__init__(self, self._shape)

    def serialize(self):
        return DelOglSDInstanceCommand.serialize(self)
    
    def unserialize(self, serializedInfos):
        DelOglSDInstanceCommand.unserialize(self, serializedInfos)
        
    def redo(self):
        DelOglSDInstanceCommand.undo(self)
        
    def redoUpdate(self, serializedGroup):
        
        DelOglSDInstanceCommand.undoUpDate(self, serializedGroup)
        
        umlFrame = self.getGroup().getHistory().getFrame()
        umlFrame.addShape(self._shape, 0, 0, withModelUpdate=False)
        self._shape.UpdateFromModel()
        umlFrame.Refresh()
    
    def undo(self):
        DelOglSDInstanceCommand.redo(self)
    
    def upDate(self, serializedGroup):
        DelOglSDInstanceCommand.upDate(self, serializedGroup)
        
    def execute(self):
        pass
    
    def _createNewSDInstance(self, x , y):
        med = get_mediator()
        umlFrame = med.getFileHandling().getCurrentFrame()
        
        basicSoftwareInstance = BasicSoftwareSDInstance()
        dlg = DlgInstance(umlFrame, wx.ID_ANY, basicSoftwareInstance)
        dlg.ShowModal()
        
        self.dlg_state = dlg.getReturnAction()
        if self.dlg_state == wx.ID_OK:
            dlg.Destroy()
            ogl = OglSDInstance(basicSoftwareObject=basicSoftwareInstance, parentFrame=umlFrame, redo=False)
            umlFrame.addShape(ogl, x, y, withModelUpdate=True)
            umlFrame.Refresh()
            return ogl
        else:
            dlg.Destroy()
            return False

    def _createNewAutoSDInstance(self, x, y, client="PyCaRO"):
        med = get_mediator()
        umlFrame = med.getFileHandling().getCurrentFrame()
        
        basicSoftwareInstanceClient =  BasicSoftwareSDInstance()
        
        if self._iterAuto == 'Client':
            basicSoftwareInstanceClient.setInstanceName('Client : \n' + client)
            basicSoftwareInstanceClient.setInstanceType('Client')
            basicSoftwareInstanceClient.setName(client)
            
            ogl = OglSDInstance(parentFrame=umlFrame, basicSoftwareObject=basicSoftwareInstanceClient, redo=False, xPos=100, yPos=50)
            umlFrame.addShape(ogl, x, y, withModelUpdate=True)
            umlFrame.Refresh()
            return ogl
        elif self._iterAuto == "RTGEN":
            basicSoftwareInstanceRTGEN = BasicSoftwareSDInstance()
            basicSoftwareInstanceRTGEN.setInstanceName('RTGEN : \n' + "RTGEN")
            basicSoftwareInstanceRTGEN.setInstanceType('RTGEN')
            basicSoftwareInstanceRTGEN.setName("RTGEN")

            ogl = OglSDInstance(parentFrame=umlFrame, basicSoftwareObject=basicSoftwareInstanceRTGEN, redo=False, xPos=400, yPos=50)
            umlFrame.addShape(ogl, x, y, withModelUpdate=True)
            umlFrame.Refresh()
            return ogl  
        else:
            BasicSoftwareUtils.displayError("Unknown value for _iterAuto [%s]"%self._iterAuto,"CreateOglSDInstanceCommand()._createNewAutoSDInstance")
            