# -*- coding: utf-8 -*-

from historyUtils import *
from command import Command
from OglLinkFactory import getOglLinkFactory
from BasicSoftwareLink import BasicSoftwareLink
from BasicSoftwareConst import OGL_MODIFY
from delOglLinkCommand import DelOglLinkCommand
from mediator import get_mediator

import mediatorParameter
import pandas as pd
import os
import wx

class CreateOglLinkCommand(Command):
    """
    This class is a part of the history system of PyUt.
    It creates every kind of OglLink and allowds to undo/redo it.
    """
    
    def __init__(self, src = None, dst = None, forExecute = False, linkType=OGL_MODIFY, shape=None):
        """
        Constructor.
        @param src OglObject    :   object from which starts the link
        @param dst OglObject    :   object at which ends the link
        @param linkType integer :   type of the link (see OglLinkFactory)
        @param srcPos tuple     :   start position of the link
        @param dstPos tuple     :   end position of the link
        """
        print("A")
        Command.__init__(self)
        self._med = get_mediator()
        print("B")
        self._src = src
        self._dst = dst
        self._shape = shape
        self._linkType = linkType
        self.forExecute = forExecute
        self._umlFrame = self._med.getFileHandling().getCurrentFrame()
        self._expected_shape = False
        self.dlg_state = None

        if forExecute:
            print("C1")
            self._srcId = self._src.getBasicSoftwareObject().getId()
            self._dstId = self._dst.getBasicSoftwareObject().getId()
            self._shape = self._createLink(self._src, self._dst, self._linkType)
        else:
            print("C2")
            self._srcId, self._dstId = 0,0
            DelOglLinkCommand.__init__(self, self._shape, self._src, self._dst, self._srcId, self._dstId)
    #>-------------------------------------------------------------------------------
        
    def serialize(self):
        """
        serialize the data needed by the command to undo/redo the created link
        """

        return DelOglLinkCommand.serialize(self)

    #>-------------------------------------------------------------------------------

    def unserialize(self, serializedInfos):
        """
        unserialize the data needed by the command to undo/redo the created link
        @param serializedInfos string   :   string representation of the data needed
                                            by the command to undo redo a link
        """
        
        DelOglLinkCommand.unserialize(self, serializedInfos)
        
    #>-------------------------------------------------------------------------------

    def redo(self):
        """
        redo the creation of the link.
        """
        DelOglLinkCommand.undo()
        
    def redoUpDate(self, serializedGroup):
        DelOglLinkCommand.undoUpDate(self, serializedGroup)

    #>-------------------------------------------------------------------------------    
        
    def undo(self):
        """
        Undo the creation of link, what means that we destroy the link
        """

        #create the command to delete an oglLink without add it to the group, then
        #just execute the destruction of the link.
        DelOglLinkCommand.redo(self)
        
    def upDate(self, serializedGroup):
        DelOglLinkCommand.upDate(self, serializedGroup)

    #>-------------------------------------------------------------------------------

    def execute(self):
        """
        Create the ogl graphicaly by adding to the frame the oglLink created in the
        constructor.
        """
        pass
    
    #>-------------------------------------------------------------------------------        
        
    def _createLink(self, src, dst, linkType=OGL_MODIFY, srcPos = None, dstPos = None):
        from OglExpectedState import OglExpectedState
        from OglTry import OglTry
        from OglModify import OglModify
        from OglCancel import OglCancel
        from OglCreateOrder import OglCreateOrder
        from OglNoteLink import OglNoteLink
        from OglProcess import OglProcess
        from DlgEditState import DlgEditState
        from DlgEditModify import DlgEditModify
        from DlgEditCancel import DlgEditCancel
        from DlgEditTry import DlgEditTry
        from DlgEditLink import DlgEditLink
        from DlgEditProcess import DlgEditProcess
        
        self.dlg_state = 404
        basicSoftwareLink = BasicSoftwareLink(33, linkType=linkType, source=src.getBasicSoftwareObject(), destination=dst.getBasicSoftwareObject())
        
        oglLinkFactory = getOglLinkFactory()
        oglLink = oglLinkFactory.getOglLink(srcShape=src, basicSoftwareLink=basicSoftwareLink, dstShape=dst, linkType=linkType)
        x,y = oglLink.GetPosition()
        
        if isinstance(oglLink, OglExpectedState) and self._med._oldAction == mediatorParameter.ACTION_EXPECTED_STATE:
            dlg=DlgEditState(None, wx.ID_ANY, basicSoftwareLink)
            dlg.ShowModal()
            self.dlg_state=dlg.getReturnAction()
            dlg.Destroy()
            if self.dlg_state == wx.ID_NO:
                oglLink.Detach()
        elif isinstance(oglLink, OglCancel):
            dlg=DlgEditCancel(None, wx.ID_ANY, basicSoftwareLink)
            dlg.ShowModal()
            self.dlg_state=dlg.getReturnAction()
            dlg.Destroy()
            if self.dlg_state == wx.ID_NO:
                oglLink.Detach()    
        elif isinstance(oglLink, OglTry):
            dlg=DlgEditTry(None, wx.ID_ANY, basicSoftwareLink)
            dlg.ShowModal()
            self.dlg_state=dlg.getReturnAction()
            dlg.Destroy()
            if self.dlg_state == wx.ID_NO:
                oglLink.Detach()                  
        elif isinstance(oglLink, OglNoteLink):
                self.dlg_state=wx.ID_OK
        elif isinstance(oglLink, OglProcess):
            dlg=DlgEditProcess(None, wx.ID_ANY, basicSoftwareLink)
            dlg.ShowModal()
            self.dlg_state=dlg.getReturnAction()
            dlg.Destroy()
            if self.dlg_state == wx.ID_NO:
                oglLink.Detach()             
        elif isinstance(oglLink, OglExpectedState):
            pass
        else:
            print("%s unknow type of link" %type(oglLink))

        if self.dlg_state in [wx.ID_OK, 404]:
            src.addLink(oglLink)
            dst.addLink(oglLink)
            self._umlFrame.addShape(oglLink, 0,0,withModelUpdate=True)
            self._umlFrame.Refresh()
            return oglLink
        elif self.dlg_statein [wx.ID_NO, wx.ID_CANCEL]:
            return False
        else:
            print('incorrect returnAction')
            raise
                
    #>-------------------------------------------------------------------------------

    def _createInheritanceLink(self, child, father):
        """
        Add a paternity link between child and father.

        @param OglClass child : child
        @param OglClass father : father

        """
        
        basicSoftwareLink = BasicSoftwareLink("", linkType=OGL_INHERITANCE,
            source=child.getBasicSoftwareObject(),
            destination=father.getBasicSoftwareObject())
        oglLink = getOglLinkFactory().getOglLink(child, basicSoftwareLink, father,OGL_INHERITANCE)

        # Added by ND
        child.addLink(oglLink)
        father.addLink(oglLink)

        # add it to the PyutClass
        child.getBasicSoftwareObject().addFather(father.getBasicSoftwareObject())

        return oglLink
