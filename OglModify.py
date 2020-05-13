# -*- coding: utf-8 -*-
from OglLink import OglLink

import wx

[CENTER] = range(1)

class OglModify(OglLink):
    
    def __init__(self, srcShape, basicSoftwareLink, dstShape, srcPos, dstPos):
        OglLink.__init__(self, srcShape=srcShape, basicSoftwareLink=basicSoftwareLink, dstShape=dstShape, srcPos=srcPos, dstPos=dstPos)
        
        self.SetPen(wx.Pen('BLUE', 3, wx.PENSTYLE_VERTICAL_HATCH))
        self.SetBrush(wx.BLUE_BRUSH)
        self._labels = {}
        self._labels[CENTER] = self.AddText(0, 0, "")
        self.updateLabels()
        self.SetDrawArrow(True)
        
    def updateLabels(self):
        
        def preparedLabel(textShape, text):
            if repr(text).strip() != "":
                textShape.SetText(text)
                textShape.SetVisible(True)
            else:
                textShape.SetVisible(False)
                
        preparedLabel(self._labels[CENTER], self._link.getName())
        
    def getLabels(self):
        return self._labels
    
    def Draw(self, dc):
        self.updateLabels()
        OglLink.Draw(self, dc)

                
                