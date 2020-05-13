# -*- coding: utf-8 -*-

import wx

from OglObject import OglObject
from BasicSoftwareSuperObject import BasicSoftwareSuperObject

class OglTitleEnd(OglObject):
    def __init__(self, basicSoftwareTitleEnd = None, w =100.0, h=50.0):
        if not basicSoftwareTitleEnd:
            basicSoftawareObject = BasicSoftwareSuperObject()
        else:
            basicSoftawareObject = basicSoftwareTitleEnd
        
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
            