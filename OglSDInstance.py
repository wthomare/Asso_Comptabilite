# -*- coding: utf-8 -*-

from MiniOgl.TextShape import TextShape
from MiniOgl.ShapeEventHandler import ShapeEventHandler
from MiniOgl.LineShape import LineShape
from OglObject import OglObject
import wx
from MiniOgl.AnchorPoint import AnchorPoint
from MiniOgl.RectangleShape import RectangleShape


import BasicSoftwareUtils

DEFAULT_X, DEDAULT_Y = 0,0
DEFAULT_WIDTH = 120
DEFAULT_HEIGHT = 600

class OglInstanceName(TextShape, ShapeEventHandler):
    def __init__(self, basicSoftwareObject, x, y, text, parent=None):
        self._basicSoftwareObject = basicSoftwareObject
        TextShape.__init__(self, x, y, text, parent)
        
    def getBasicSoftwareObject(self):
        return self._basicSoftwareObject
    
class OglInstanceRectangleShape(RectangleShape):
    def __init__(self, x, y, w, z):
        RectangleShape.__init__(x,y,w,z)
        
        
class OglSDInstance(OglObject):
    def __init__(self, parentFrame, basicSoftwareObject=None, redo=False, xPos=0, yPos=0):
        self._parentFrame = parentFrame
        self._redo = redo
        self._xPos = xPos
        self._yPos = yPos
        
        self._instanceYPosition = 50 
        
        diagram = self._parentFrame.GetDiagram()
        
        OglObject.__init__(self, basicSoftwareObject, DEFAULT_WIDTH, DEFAULT_HEIGHT)
        diagram.AddShape(self)
        self.SetDraggable(True)
        self.SetVisible(True)
        pen = wx.Pen(wx.Colour('#9e4757'), 5, wx.SOLID)
        pen.SetJoin(wx.JOIN_BEVEL)
        self.SetPen(pen)
        self.SetBrush(wx.Brush("blue", wx.TRANSPARENT))
        
        if self._redo:
            self.SetPosition(self._xPos, self._yPos)
        else:
            self.SetPosition(self.GetPosition()[0], self._instanceYPosition)
        
        (srcX, srcY, dstX, dstY) = (DEFAULT_WIDTH/2, 0, DEFAULT_WIDTH/2, DEFAULT_HEIGHT)
        src, dst = (AnchorPoint(srcX, srcY, self), AnchorPoint(dstX, dstY, self))
        
        for el in [src, dst]:
            el.SetVisible(False)
            el.SetDraggable(False)
            
        self._LineShape = LineShape(src, dst)
        self.AppendChild(self._LineShape)
        self._LineShape.SetParent(self)
        self._LineShape.SetDrawArrow(True)
        self._LineShape.SetDraggable(True)
        self._LineShape.SetPen(wx.BLACK_DASHED_PEN)
        self._LineShape.SetVisible(True)
        diagram.AddShape(self._LineShape)
        
        
        self._instanceBox = OglInstanceRectangleShape(0, 0, DEFAULT_WIDTH, 60)
        self._instanceBox.basicSoftwareObject = self._basicSoftwareObject
        self.AppendChilds(self._instanceBox)
        self._instanceBox.SetDraggable(False)
        self._instanceBox.Resize = self.OnInstanceBoxResize
        self._instanceBox.SetResizable(True)
        self._instanceBox.SetParent(self)
        diagram.AddShape(self._instanceBox)
        
        text = self._basicSoftwareObject.getInstanceName
        self._instanceBoxText = OglInstanceName(basicSoftwareObject, 10, 10, text, self._instanceBox)
        self.AppendChild(self._instanceBoxText)
        diagram.AddShape(self._instanceBoxText)

    def getLifeLineShape(self):
        return self._LineShape
    
    def OnInstanceBoxResize(self, sizer, width, height):
        RectangleShape.Resize(sizer, width, height)
        size = self._instanceBox.GetSize()
        self.SetSize(size)
        
    def Resize(self, sizer, width, height):
        OglObject.Resize(sizer, width, height)
        
    def SetSize(self, width, height):
        OglObject.SetSize(self, width, height)
        
        (myX, myY) = self.GetPosition()
        (w, h) = self.GetSize()
        lineDst = self._LineShape.GetDestination()
        lineSrc = self._LineShape.GetSource()
        lineSrc.SetDraggable(True)
        lineDst.SetDraggable(True)
        lineSrc.SetPosition(w/2+myX, 0+myY)
        lineDst.SetPosition(w/2+myX, height+myY)
        lineSrc.SetDraggable(False)
        lineDst.SetDraggable(False)
        
        for link in self._oglLinks:
            try:
                link.updatePosition()
            except:
                BasicSoftwareUtils.displayWarning("Failed to set sized of SD Instance", 'OglSDInstance.SetSize error')
                pass

    def SetPosition(self, x, y):
        if self._redo:
            OglObject.SetPosition(self, self._xPos, self._yPos)
        else:
            y = self._instanceYPosition
            OglObject.SetPosition(self, x, y)
    
    def Draw(self, dc):
        self._instanceBoxText.SetText(self._basicSoftwareObject.getInstanceName())
        
        if self.IsSelected():
            self.SetVisible(True)
            pen = wx.Pen(wx.Colour("#9e4757"), 5, wx.SOLID)
            pen.SetJoin(wx.JOIN_BEVEL)
            self.SetPen(pen)
        OglObject.Draw(self, dc)
    
    def OnLeftUp(self, event):
        if self._redo:
            self.SetPosition(self._xPos, self._yPos)
            self._redo = False
        else:
            self.SetPosition(self.GetPosition()[0], self._instanceYPosition)
            
    def GetXPos(self):
        return self._xPos
    
    def GetYPos(self):
        return self._yPos
    
    def GetRedo(self):
        return self._redo
    
    def SetYPos(self, value):
        self._yPos = value
        
    def SetXPos(self, value):
        self._xPos = value
        
    def SetRedo(self, value):
        self._redo=value
    
    def GetBasicSoftwareObject(self):
        return self._basicSoftwareObject
    
    def SetBasicSoftwareObject(self, value):
        self._basicSoftwareObject = value
        
    def GetInstanceBox(self):
        return self._instanceBox
        
        
        