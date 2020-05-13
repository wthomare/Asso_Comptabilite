# -*- coding: utf-8 -*-

from OglObject import OglObject
from BasicSoftwareSuperObject import BasicSoftwareSuperObject
from LineSplitter import LineSplitter

import wx

class OglImport(OglObject):
    
    def __init__(self, basicSoftwareImport, w=120, h=80):
        if not basicSoftwareImport:
            basicSoftwareObject = BasicSoftwareSuperObject()
        else:
            basicSoftwareObject = basicSoftwareImport
            
        OglObject.__init__(self, basicSoftwareObject, w, h)
        self._drawFrame = False

    def Draw(self, dc):
        OglObject.Draw(self, dc)
        dc.SetFont(self._defaultFont)
        dc.SetPen(wx.Pen('BLACK', 2, wx.PENSTYLE_SOLID))
        
        x, y = self.GetPosition()
        w, h = self.GetSize()
        dc.DrawRoundedRectangle(x, y, w, h, 10)
        
        x += (1.0/12.0)*w
        y += (1.0/8.0)*h
        
        dc.SetPen(wx.Pen("BLACK", 1, wx.PENSTYLE_SHORT_DASH))
        dc.DrawRoundedRectangle(x, y, (10.0/12.0)*w, (6.0/8.0)*h, 10)

        x += (1.0/12.0)*w
        y += (2.0/8.0)*h     
        
        textWidth = 8.0/12.0 * w
        space = 1.0 * dc.GetCharHeight()
        
        dc.SetClippingRegion(x, y, textWidth, 3.0/8.0*h)
        lines = LineSplitter().split(self.getBasicSoftwareObject().getName(), dc, textWidth)
        
        for line in lines:
            dc.DrawText(line, x, y)
            y += space
        
        dc.DestroyClippingRegion()
        