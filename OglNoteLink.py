# -*- coding: utf-8 -*-

from OglLink import OglLink
import wx

class OglNoteLink(OglLink):
    def __init__(self, srcShape, basisSoftwareObject, dstShape):
        OglLink.__init__(self, srcShape, basisSoftwareObject, dstShape)
        self.SetDrawArrow(False)
        
        self.SetPen(wx.Pen("BLACK", 2, wx.LONG_DASH))
        