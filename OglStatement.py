# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

import wx

from OglObject import OglObject
from BasicSoftwareSuperObject import BasicSoftwareSuperObject
from LineSplitter import LineSplitter

class OglStatement(OglObject):
    def __init__(self, basicSoftwareStatement = None, w =160.0, h=120.0):
        if not basicSoftwareStatement:
            basicSoftawareObject = BasicSoftwareSuperObject()
        else:
            basicSoftawareObject = basicSoftwareStatement
        
        OglObject.__init__(self, basicSoftawareObject, w, h)
        self._drawFrame = False
        
    def Draw(self, dc):
        
        OglObject.Draw(self, dc)
        dc.SetFont(self._defaultFont)
        pen = wx.Pen('#539e47', 2, wx.PENSTYLE_SOLID)
        dc.SetPen(pen)
        dc.SetBrush(wx.Brush('blue', wx.TRANSPARENT))
        
        
        width, height = self.GetSize()
        x, y = self.GetPosition()
        dc.DrawRoundedRectangle(x,y, width, height, 8)
        
        x += 0.3*width
        y += 0.3*height
        textWidth = 0.8*width
        space = 1.1*dc.GetCharHeight()
        dc.SetClippingRegion(x, y, textWidth, 0.6*height)
        
        lines = LineSplitter().split(self.getBasicSoftwareObject().getName(), dc, textWidth)
        
        for line in lines:
            dc.DrawText(line, x, y)
            y += space

        dc.DestroyClippingRegion()        
        