# -*- coding: utf-8 -*-

import wx
import mediator
import Ctrl_Manager
import mediatorParameter

from OglStatement import OglStatement
from MiniOgl.DiagramFrame import DiagramFrame
from MiniOgl.Constants import SKIP_EVENT
from historyManager import HistoryManager
from OglLink import OglLink
from OglObject import OglObject

DEFAULT_WIDTH = 3000
wx.InitAllImageHandlers()

class UmlDiagramsFrame(DiagramFrame):
    
    def __init__(self, parent, frame = None):
        DiagramFrame.__init__(self, parent)
        
        self._ctrl = mediator.get_mediator()
        self._ctrlVP = Ctrl_Manager.getController()

        self.maxWidth = DEFAULT_WIDTH
        self.maxHeight = int(self.maxWidth / 1.41)
        
        
        self.SetScrollbar(20,20, int(self.maxWidth/20), int(self.maxHeight/20))
        
        if not frame:
            self._frame = wx.ID_ANY
        else:
            self._frame = frame
            
        self._history = HistoryManager(self)
        
        self.Bind(wx.EVT_CLOSE, self.evtClose)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_CHAR, self._ctrl.processChar)
        self.SetInfinite(True)
        self._defaultCursor = self.GetCursor()
        
    def cleanUp(self):
        self._ctrl, self._frame = None, None
        
    def evtClose(self, event):
        self._history.Destroy()
        self.cleanUp()
        self.Destroy()
        
    def newDiagram(self):
        self._diagram.DeleteAllShapes()
        self.Refresh()
        
    def getDiagram(self):
        return self._diagram
    
    def OnLeftDown(self, event):
        if self._ctrl.actionWaiting():
            x, y = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
            skip = self._ctrl.doAction(x,y)
            
            if self._ctrl.getCurrentAction()== mediatorParameter.ACTION_ZOOM_IN:
                DiagramFrame.BeginSelect(self, event)
            if skip == SKIP_EVENT:
                DiagramFrame.OnLeftDown(self, event)
        else:
            DiagramFrame.OnLeftDown(self, event)
            
    def OnLeftUp(self, event):
        
        if self._ctrl.getCurrentAction() == mediatorParameter.ACTION_ZOOM_IN:
            width, heigth = self._selector.GetSize()
            x, y = self._selector.GetPosition()
            self._selector.Detach()
            self._selector = None
            self.DoZoom(x, y, width, heigth)
            self.Refresh()
            self._ctrl.updateTitle()
        else:
            DiagramFrame.OnLeftUp(self, event)
    
    def OnRigthDown(self, event):
        
        self._xRD, self._yRD = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
        self.Bind(wx.EVT_MENU, self._OnMnuEditCut, id=mediatorParameter.ID_MNUEDITCUT)
        self.Bind(wx.EVT_MENU, self._OnMnuEditCopy, id=mediatorParameter.ID_MNUEDITCOPY)
        self.Bind(wx.EVT_MENU, self.OnMnuEditPaste, id=mediatorParameter.ID_MNUEDITPASTE)
        
        menu = wx.Menu()
        menu.Append(mediatorParameter.ID_MNUEDITCOPY, "Copy")
        menu.Append(mediatorParameter.ID_MNUEDITCUT, "Cut")
        menu.Append(mediatorParameter.ID_MNUEDITPASTE, "Paste")
        
        self.PopupMenu(menu)
        menu.Destroy()
        
    def OnLeftDClick(self, event):
        x, y = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
        self._ctrl.editObject(x,y)
        DiagramFrame.OnLeftDClick(self, event)
        
    def addShape(self, shape, x=None, y=None, pen=None, brush=None, withModelUpdate=True):
        shape.SetDraggable(True)
        shape.SetPosition(x,y)
        if pen:
            shape.SetPen(pen)
        if brush:
            shape.SetBrush(brush)
        self._diagram.AddShape(shape, withModelUpdate)
        
    def addLinkShape(self, shape, x, y, pen=None, brush=None, withModelUpdate=True):
        shape.SetDraggable(True)
        shape.SetPosition(x,y)
        
        if pen:
            shape.SetPen(pen)
        if brush:
            shape.SetBrush(brush)
        self._diagram.AddLinkShape(shape, withModelUpdate)
        
    def getUmlObjects(self):
        return[s for s in self._diagram.GetShapes() if isinstance(s, (OglObject, OglLink, OglStatement))]
        
    def getWidth(self):
        return self.maxWidth
    
    def getHeight(self):
        return self.maxHeight
    
    def getObjectsBoundaries(self):
        
        infinite = 1e9
        minx, miny, maxx, maxy = infinite, infinite, infinite, infinite
        
        for object in self._diagram.GetShapes():
            ox1, oy1 = object.GetPosition()
            ox2, oy2 = object.GetSize()
            
            ox2 += ox1
            oy2 += ox1
            
            minx = min(minx, ox1)
            maxx = max(maxx, ox2)
            miny = min(miny, oy1)
            maxy = max(maxy, oy2)
            
        return (minx, miny, maxx, maxy)
    
    def getUmlObjectById(self, objectId):
        for shape in self.GetDiagram().GetShapes():
            if isinstance(shape, (OglObject, OglLink)):
                if shape.getBasicSoftwareObject().getId() == objectId or str(shape.getBasicSoftwareObject().getId())==objectId or shape.getBasicSoftwareObject()==str(objectId):
                    return shape
        return None
    
    def getHistory(self):
        return self._history
    
    def OnClose(self, force=False):
        self.cleanUp()
        self.Destroy()
        return True
    
    def _OnMnuEditCut(self, event):
        self._ctrlVP._OnMnuEditCut()
        
    def _OnMnuEditCopy(self, event):
        self._ctrlVP._OnMnuEditCopy()
        
    def _OnMnuEditPaste(self, event):
        self._ctrlVP._OnMnuEditPaste()
        