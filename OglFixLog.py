# -*- coding: utf-8 -*-
from OglObject import OglObject
from BasicSoftwareSuperObject import BasicSoftwareSuperObject
from LineSplitter import LineSplitter

import wx

class OglFixLog(OglObject):
    def __init__(self, basicSoftwareFixLog=None, w=160.0, h=120.0):
        if basicSoftwareFixLog is None:
            basicSoftwareObject = BasicSoftwareSuperObject()
        else:
            basicSoftwareObject = basicSoftwareFixLog
        
        OglObject.__init__(self, basicSoftwareObject, w, h)
        self._drawFrame = False
        
    def Draw(self, dc):
        dc.SetFont(self._defaultFont)
        dc.SetPen(wx.Pen('PLUM', 3, wx.PENSTYLE_SOLID))
        dc.SetBrush(wx.Brush("#FFEFFD"))
                             
        width, height = self.GetPosition()
        x, y = self.GetPosition()
        y = y +(1.0/2.0)*height
        ListPoints = [(x, y)]
        
        ListPoints.append((x + (1.0/6.0)*width, y + (1.0/2.0)*height))
        ListPoints.append((x + (5.0/6.0)*width, y + (1.0/2.0)*height))
        ListPoints.append((x + (6.0/6.0)*width, y + (0.0/2.0)*height))
        ListPoints.append((x + (5.0/6.0)*width, y + (-1.0/2.0)*height))
        ListPoints.append((x + (1.0/6.0)*width, y + (-1.0/2.0)*height))
        
        dc.DrawPolygon(ListPoints)
        
        x += 1.0/6.0 * width
        y += -2.0/6.0 * height
        
        textWidth = 4.0/6.0 * width
        space = 1.0 * dc.GetCharHeight()
        
        dc.SetClippingRegion(x, y, textWidth, 0.6*height)
        
        lines = LineSplitter().split(self.getBasicSoftwareObject().getName(), dc, textWidth)
        
        for line in lines:
            dc.DrawText(line, x, y)
            y += space
            
        dc.DestroyClippingRegion()
        