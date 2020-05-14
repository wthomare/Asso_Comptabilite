# -*- coding: utf-8 -*-

from MiniOgl.RectangleShapeModel import RectangleShapeModel

class TextShapeModel(RectangleShapeModel):
    """
    This class is the model of a TextShape ('view' in a
    MVC pattern).
    """
    def __init__(self):
        """
        Constructor.
        Used when the model is created first without any view.
        We have to use AddShape() and UpdateModel from the shape before
        we can use the model.
        """

        # set the coords and size to 0 and a empty list of associated
        # shapes (views)
        RectangleShapeModel.__init__(self)

        self._fontSize = 0

    #>------------------------------------------------------------------------

    def GetFontSize(self):
        return self._fontSize

    def SetFontSize(self, fontSize):
        self._fontSize = fontSize
    
