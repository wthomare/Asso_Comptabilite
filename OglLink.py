# -*- coding: utf-8 -*-

from BasicSoftwareConst import WEST, NORTH, SOUTH, EAST, deltaAnchor
from mediator import get_mediator
from MiniOgl.LineShape import LineShape
from MiniOgl.ShapeEventHandler import ShapeEventHandler

import wx

def getOrient(srcX, srcY, dstX, dstY):
    """
    Return where the destination is, given the position of the source
    """
    
    deltaX = srcX - dstX
    deltaY = srcY - dstY
    
    if deltaX >0:
        if deltaX > abs(deltaY):
            return WEST
        elif deltaY > 0:
            return NORTH
        else:
            return SOUTH
    else:
        if -deltaX > abs(deltaY):
            return EAST
        elif deltaY > 0:
            return NORTH
        else:
            return SOUTH


class OglLink(LineShape, ShapeEventHandler):
    def __init__(self, srcShape, basicSoftwareLink, dstShape, srcPos=None, dstPos=None):
        self._srcShape, self._dstShape = srcShape, dstShape
        
        if not srcPos and not dstPos:
            srcX, srcY = self._srcShape.GetPosition()
            dstX, dstY = self._dstShape.GetPosition()
            orient = getOrient(srcX, srcY, dstX, dstY)
            
            sw, sh = self._srcShape.GetSize()
            dw, dh = self._dstShape.GetSize()
            if orient == NORTH:
                srcX, srcY = sw/5, 0
                dstX, dstY = dw/5, dh
            elif orient == SOUTH:
                srcX, srcY = sw/5, sh
                dstX, dstY = dw/5, 0
            elif orient == EAST:
                srcX, srcY = sw/5, 0
                dstX, dstY = 0, dh/5
            elif orient == WEST:
                srcX, srcY = 0, sh/5
                dstX, dstY = dw, dh/5
        else:
            print(srcPos)
            print(dstPos)
            (srcX, srcY) = srcPos
            (dstX, dstY) = dstPos
        
        #========== Avoid Underlying ====================#
        lstAnchorPoints = {anchor.GetRelativePosition() for anchor in srcShape.GetAnchors()}
        while (srcX, srcY) in lstAnchorPoints:
            if orient == NORTH or orient == SOUTH:
                srcX+=deltaAnchor
            else:
                srcY += deltaAnchor
                
        lstAnchorPoints = {anchor.GetRelativePosition() for anchor in dstShape.GetAnchors()}
        while (srcX, srcY) in lstAnchorPoints:
            if orient == NORTH or orient == SOUTH:
                dstX+=deltaAnchor
            else:
                dstY += deltaAnchor                
        #========== End Underlying ====================#
        
        src = self._srcShape.AddAnchor(srcX, dstX)
        dst = self._dstShape.AddAnchor(dstX, dstY)
        dst.SetPosition(dstX, dstY)
        src.SetPosition(srcX, dstY)
        src.SetVisible(False)
        dst.SetVisible(False)
        src.SetDraggable(True)
        dst.SetDraggable(True)        
        
        LineShape.__init__(self, src, dst)
        self.SetPen(wx.BLACK_PEN)
        
        if basicSoftwareLink:
            self._link = basicSoftwareLink
        else:
            self._link = basicSoftwareLink()
            
    def getSourceShape(self):
        return self._srcShape

    def getDestinationShape(self):
        return self._dstShape
    
    def getBasicSoftwareObject(self):
        return self._link
    
    def setBasicSoftwareObject(self, basicSoftwareLink):
        self._link = basicSoftwareLink
        
    def Detach(self):
        if self._diagram and not self._protected:
            LineShape.Detach()
            self._protected = True
            self._src.SetProtected(False)
            self._dst.SetProtected(False)
            self._src.Detach()
            self._dst.Detach()
            
            