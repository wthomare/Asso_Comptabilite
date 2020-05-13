# -*- coding: utf-8 -*-

from OglObject import OglObject
from BasicSoftwareSuperObject import BasicSoftwareSuperObject
from LineSplitter import LineSplitter

import wx

class OglLog(OglObject):
    
    def __init__(self, basicSoftwareLog=None, w=560.0, h=40.0):
        if not basicSoftwareLog:
            basicSoftwareObject = BasicSoftwareSuperObject
        else:
            basicSoftwareObject = basicSoftwareLog
            
        OglObject.__init__(self, basicSoftwareObject, w, h)

    def Draw(self, dc):
        dc.SetFont(self._defaultFont)
        dc.SetPen(wx.Pen('PALE GREEN'), 3, wx.PENSTYLE_SOLID)
        dc.SetBrush(wx.Brush('PALE GREEN'))        
        
        width, height = self.GetSize()
        x, y = self.GetPosition()
        
        y = y+(1.0/2.0)*height
        ListPoints = []
        ListPoints.append((x,y))
        
        ListPoints.append((x+(1.0/6.0)*width, y+ (1.0/2.0)*height))
        ListPoints.append((x+(5.0/6.0)*width, y+ (1.0/2.0)*height))
        ListPoints.append((x+(6.0/6.0)*width, y+ (0.0/2.0)*height))
        ListPoints.append((x+(5.0/6.0)*width, y+ (-1.0/2.0)*height))
        ListPoints.append((x+(1.0/6.0)*width, y+ (-1.0/2.0)*height))
        
        dc.DrawPolygon(ListPoints)
        
        x += 1.0/6.0 * width
        y += -2.0/6.0 * height
        
        textWidth = 4.0/6.0*width
        space = 1.0 * dc.GetCharHeight()
        dc.SetClippingRegion(x, y, textWidth, 0.6*height)
        
        lines = LineSplitter().split(self.GetBasicSoftwareObject().getName(), dc, textWidth)
        
        for line in lines:
            dc.DrawText(line, x, y)
            y += space

        dc.DestroyClippingRregion()
        