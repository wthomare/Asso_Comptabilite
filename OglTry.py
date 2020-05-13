# -*- coding: utf-8 -*-

from OglLink import OglLink
import wx

[CENTER] = range(1)

class OglTry(OglLink):
    
    def __init__(self, srcShape, basiSoftwareLink, dstShape, srcPos, dstPos):
        OglLink.__init__(self, srcShape=srcShape, basiSoftwareLink=basiSoftwareLink, dstShape=dstShape, srcPos=srcPos, dstPos=dstPos)
        
        self.Pen(wx.Pen("#FF7700", 3, wx.PENSTYLE_DOT_DASH))
        self.SetBrush(wx.Brush("#FF7700"))
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
        self.updateLabels
        OglLink.Draw(self, dc)