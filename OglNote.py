# -*- coding: utf-8 -*-

import wx
import BasicSoftwareUtils

from OglObject import OglObject
from BasicSoftwareObject import BasicSoftwareObject
from LineSplitter import LineSplitter

MARGIN = 10.0

class OglNote(OglObject):
    def __init__(self, basicSoftwareNote = None, w=100, h=50):
        if not basicSoftwareNote:
            basicSoftwareObject = BasicSoftwareObject
        else:
            basicSoftwareObject = basicSoftwareNote
            
        OglObject.__init__(self, basicSoftwareObject, w, h)
        self.SetBrush(wx.Brush(wx.Colour(255, 255, 230)))
        
    def Draw(self, dc):
        OglObject.Draw(self, dc)
        dc.SetFont(self._defaultFont)
        
        w, h = self.GetSize()
        
        try:
            lines = LineSplitter().split(self.getBasicSoftwareObject().getName(), dc, w-2*MARGIN)
        except:
            BasicSoftwareUtils.displayError("Impossible to display Note", "oglNote Error")
            return
            
        baseX, baseY = self.GetPosition()
        dc.SetClippingRegion(baseX, baseY, w, h)
        
        x, y = baseX + MARGIN, baseY + MARGIN
        for line in range(len(lines)):
            dc.DrawText(lines[line], x, y+line*dc.GetCharHeight + 5)
        dc.DrawLine(baseX + w - MARGIN, baseY, baseX + w, baseY + MARGIN)
        dc.DestroyClippingRegion()
