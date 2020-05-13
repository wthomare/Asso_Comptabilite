# -*- coding: utf-8 -*-

from OglObject import OglObject
from BasicSoftwareSuperObject import BasicSoftwareSuperObject
from LineSplitter import LineSplitter

import wx

class OglFor(OglObject):
    def __init__(self, basicSoftwareUseCase=None, w=160.0, h=120.0):
        if basicSoftwareUseCase is None:
            basicSoftwareObject = BasicSoftwareSuperObject()
        else:
            basicSoftwareObject = basicSoftwareUseCase
        
        OglObject.__init__(self, basicSoftwareObject, w, h)
        self._drawFrame = False
    
    def Draw(self, dc):
        OglObject.Draw(self, dc)
        dc.SetFont(self._defaultFont)
        dc.SetPen(wx.Pen((0,0,0), 2, wx.PENSTYLE_LONG_DASH))
        dc.SetBrush(wx.Brush('blue', wx.TRANSPARENT))
        
        width, height = self.GetSize()
        x, y = self.GetPosition()
        
        dc.DrawRoundedRectangle(x, y, width, height, 10)
        
        x += 0.03*width
        y += 0.03*height
        textWidth = 0.8*width
        space = 1.1 * dc.GetCharHeight()
        dc.SetClippingRegion(x, y, textWidth, 0.6*height)
        
        lines = LineSplitter().split(self.getBasicSoftwareObject().getName(), dc, textWidth)
        
        for line in lines:
            dc.DrawText(line, x, y)
            y+=space
        dc.DestroyClippingRegion()