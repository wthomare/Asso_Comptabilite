# -*- coding: utf-8 -*-

from MiniOgl.RectangleShape import RectangleShape
from MiniOgl.ShapeEventHandler import ShapeEventHandler

import mediator
import wx

DEFAULT_FONT_SIZE = 10

class OglObject(RectangleShape, ShapeEventHandler):
    def __init__(self, basicSoftwareObject=None, width=0, height=0):
        RectangleShape.__init__(self, 0, 0, width, height)
        self._basicSoftwareObject = basicSoftwareObject
        self._defaultFont = wx.Font(DEFAULT_FONT_SIZE, wx.SWISS, wx.NORMAL, wx.NORMAL)
        
        self._oglLinks = []
        self._modifyCommand = None
        
    def setBasicSoftwareObject(self, basicSoftwareObject):
        self._basicSoftwareObject = basicSoftwareObject
    def getBasicSoftwareObject(self):
        return self._basicSoftwareObject

    def addLink(self, link):
        self._oglLinks.append(link)
    def getLinks(self):
        return self._oglLinks
     
    def OnLeftDown(self, event):
        med = mediator.get_mediator()
        if med.actionWaiting():
            print(' event.GetPosition() %s'  %event.GetPosition())
            med.shapeSelected(self, position=event.GetPosition())
            return
        event.Skip()
        
    def OnLeftUp(self, event):
        pass
    
    def autoResize(self):
        pass
    
    def SetPosition(self, x, y):
        med = mediator.get_mediator()
        fileHandling = med.getFileHandling()
        if fileHandling:
            fileHandling.setModified(True)
        RectangleShape.SetPosition(self, x, y)
        
    def SetSelected(self, state=True):
        from mediator import get_mediator
        from mediatorParameter import ACTION_ZOOM_OUT
        
        if get_mediator().getCurrentAction() !=ACTION_ZOOM_OUT:
            RectangleShape.SetSelected(self, state)
            