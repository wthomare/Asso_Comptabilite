# -*- coding: utf-8 -*-

from OglLink import OglLink

import wx

[CENTER] = range(1)

class OglCreateOrder(OglLink):
    def __init__(self, srcShape,basicSoftwareLink, dstShape, srcPos, dstPos):
        OglLink.__init__(srcShape, basicSoftwareLink, dstShape, srcPos, dstPos)
        
        self.SetPen(wx.Pen('RED', 3, wx.LONG_DASH))
        self.SetBrush(wx.RED_BRUSH)
        self._labels = {}
        self._labels[CENTER] = self.AddText(0, 0, "")
        self.updateLabels()
        self.SetDrawArrow(True)
        
    def updateLabels(self):
        def prepareLabel(textShape, text):
            if text.strip() != "":
                textShape.SetText(text)
                textShape.SetVisible(True)
            else:
                textShape.SetVisible(False)
        
        prepareLabel(self._labels[CENTER], self._link.getName())

    def getLabels(self):
        return self._labels

    def Draw(self, dc):
        self.updateLabels()
        OglLink.Draw(self, dc)