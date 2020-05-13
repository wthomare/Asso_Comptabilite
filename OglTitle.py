# -*- coding: utf-8 -*-

import wx

from OglObject import OglObject
from BasicSoftwareSuperObject import BasicSoftwareSuperObject
from LineSplitter import LineSplitter

class OglTitle(OglObject):
    def __init__(self, basicSoftwareTitle = None, w =100.0, h=50.0):
        if not basicSoftwareTitle:
            basicSoftawareObject = BasicSoftwareSuperObject()
        else:
            basicSoftawareObject = basicSoftwareTitle
        
        OglObject.__init__(self, basicSoftawareObject, w, h)
        self._drawFrame = False
        
    def Draw(self, dc):
        
        OglObject.Draw(self, dc)
        dc.SetFont(self._defaultFont)
        pen = wx.Pen('#4c4c4c', 5, wx.SOLID)
        pen.SetJoin(wx.JOIN_BEVEL)
        dc.SetPen(pen)
        dc.SetBrush(wx.Brush('blue', wx.TRANSPARENT))
        
        
        width, height = self.GetSize()
        x, y = self.GetPosition()
        dc.DrawRectangle(x,y, width, height)
        
        x += 0.25*width
        y += 0.4*height
        textWidth = 0.8*width
        space = 1.1*dc.GetCharHeight()
        dc.SetClippingRegion(x, y, textWidth, 0.8*height)
        
        lines = LineSplitter().split(self.getBasicSoftwareObject().getName(), dc, textWidth)
        
        for line in lines:
            dc.DrawText(line, x, y)
            y += space

        dc.DestroyClippingRegion()        
        