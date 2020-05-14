# -*- coding: utf-8 -*-

# This file is part of MiniOgl.
#
# MiniOgl is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# MiniOgl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MiniOgl; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from MiniOgl.Shape                     import Shape
from MiniOgl.MiniOglUtils              import sign
from MiniOgl.SizerShape                import SizerShape
from MiniOgl.RectangleShapeModel       import RectangleShapeModel

__all__ = ["RectangleShape"]

class RectangleShape(Shape):
    """
    A rectangle shape.

    Exported methods:
    -----------------

    __init__(self, x=0.0, y=0.0, width=0.0, height=0.0, parent=None)
        Constructor.
    SetResizable(self, state)
        Set the resizable flag.
    GetResizable(self)
        Get the resizable flag.
    GetTopLeft(self)
        Get the coords of the top left point in diagram coords.
    SetTopLeft(self, x, y)
        Set the position of the top left point.
    Draw(self, dc, withChildren=False)
        Draw the rectangle on the dc.
    DrawBorder(self, dc)
        Draw the border of the shape, for fast rendering.
    SetDrawFrame(self, draw)
        Choose to draw a frame around the rectangle.
    Inside(self, x, y)
        True if (x, y) is inside the rectangle.
    GetSize(self)
        Get the size of the rectangle.
    SetSelected(self, state=True)
        Select the shape.
    Detach(self)
        Detach the shape from its diagram.
    ShowSizers(self, state=True)
        Show the four sizer shapes if state is True.
    SetSize(self, width, height)
        Set the size of the rectangle.
    Resize(self, sizer, x, y)
        Resize the rectangle according to the new position of the sizer.

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def __init__(self, x=0.0, y=0.0, width=0.0, height=0.0, parent=None):
        """
        Constructor.

        @param double x, y : position of the point
        @param double width, height : size of the rectangle
        @param Shape parent : parent shape
        """
        Shape.__init__(self, x, y, parent)
        self._width = width   # width and height can be < 0 !!!
        self._height = height
        self._drawFrame = True
        self._resizable = True

        self._topLeftSizer = None
        self._topRightSizer = None
        self._botLeftSizer = None
        self._botRightSizer = None

        #added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)
        # set the model of the shape (MVC pattern)
        self._model = RectangleShapeModel(self)

    #>------------------------------------------------------------------------

    def SetResizable(self, state):
        """
        Set the resizable flag.

        @param bool state
        """
        self._resizable = state

    #>------------------------------------------------------------------------

    def GetResizable(self):
        """
        Get the resizable flag.

        @return bool
        """
        return self._resizable

    #>------------------------------------------------------------------------

    def GetTopLeft(self):
        """
        Get the coords of the top left point in diagram coords.

        @return (double, double)
        """
        x, y = self.GetPosition()
        x -= self._ox
        y -= self._oy
        width, height = self.GetSize()
        if width < 0:
            x += width
        if height < 0:
            y += height
        return x, y

    #>------------------------------------------------------------------------

    def SetTopLeft(self, x, y):
        """
        Set the position of the top left point.

        @param double x, y : new position
        """
        x += self._ox
        y += self._oy
        width, height = self.GetSize()
        if width < 0:
            x -= width
        if height < 0:
            y -= height
        self._x, self._y = x, y

    #>------------------------------------------------------------------------

    def Draw(self, dc, withChildren=False):
        """
        Draw the rectangle on the dc.

        @param wxDC dc
        """
        if self._visible:
            # CD
            #if self._selected:
            #    self.ShowSizers(False)
            #    self.ShowSizers(True)


            Shape.Draw(self, dc, False)
            if self._drawFrame:
                sx, sy = self.GetPosition()
                sx, sy = sx - self._ox, sy - self._oy
                width, height = self.GetSize()

                dc.DrawRectangle(sx, sy, width, height)
            if withChildren:
                self.DrawChildren(dc)
            
            # CD
            if self._topLeftSizer!=None:
                self._topLeftSizer.Draw(dc, False)

    #>------------------------------------------------------------------------

    def DrawBorder(self, dc):
        """
        Draw the border of the shape, for fast rendering.
        """
        Shape.DrawBorder(self, dc)
        sx, sy = self.GetPosition()
        sx, sy = sx - self._ox, sy - self._oy
        width, height = self.GetSize()
        dc.DrawRectangle(sx, sy, width, height)

    #>------------------------------------------------------------------ 

    def SetDrawFrame(self, draw):
        """
        Choose to draw a frame around the rectangle.

        @param bool draw : True to draw the frame
        """
        self._drawFrame = draw

    #>------------------------------------------------------------------------

    def Inside(self, x, y):
        """
        True if (x, y) is inside the rectangle.

        @param double x, y
        @return bool
        """
        # this also works if width and/or height is negative.
        sx, sy = self.GetPosition()
        # take a minimum of 4 pixels for the selection
        width, height = self.GetSize()
        width = sign(width) * max(abs(width), 4.0)
        height = sign(height) * max(abs(height), 4.0)
        topLeftX = sx - self._ox
        topLeftY = sy - self._oy
        a = x > topLeftX
        b = x > topLeftX + width
        c = y > topLeftY
        d = y > topLeftY + height
        return (a + b) == 1 and (c + d) == 1

    #>------------------------------------------------------------------------

    def GetSize(self):
        """
        Get the size of the rectangle.

        @return (double, double)
        """
        return self._width, self._height

    #>------------------------------------------------------------------------

    def SetSelected(self, state=True):
        """
        Select the shape.

        @param bool state
        """
        Shape.SetSelected(self, state)
        if self._resizable:
            self.ShowSizers(state)

    #>------------------------------------------------------------------ 

    def Detach(self):
        """
        Detach the shape from its diagram.
        This is the way to delete a shape. All anchor points are also
        removed, and link lines too.
        """
        # do not detach a protected shape
        if self._diagram is not None and not self._protected:
            Shape.Detach(self)
            self.ShowSizers(False)

    #>------------------------------------------------------------------ 

    def ShowSizers(self, state=True):
        """
        Show the four sizer shapes if state is True.

        @param bool state
        """
        width, height = self.GetSize()
        if state and not self._topLeftSizer:
            self._topLeftSizer = SizerShape(-self._ox, -self._oy, self)
            self._topRightSizer = SizerShape(-self._ox + width - 1,
                self._oy, self)
            self._botLeftSizer = SizerShape(-self._ox,
                -self._oy + height - 1, self)
            self._botRightSizer = SizerShape(-self._ox + width - 1,
                -self._oy + height - 1, self)
            self._diagram.AddShape(self._topLeftSizer)
            self._diagram.AddShape(self._topRightSizer)
            self._diagram.AddShape(self._botLeftSizer)
            self._diagram.AddShape(self._botRightSizer)
        elif not state and self._topLeftSizer is not None:
            self._topLeftSizer.Detach()
            self._topLeftSizer = None
            self._topRightSizer.Detach()
            self._topRightSizer = None
            self._botLeftSizer.Detach()
            self._botLeftSizer = None
            self._botRightSizer.Detach()
            self._botRightSizer = None

    #>------------------------------------------------------------------ 

    def SetSize(self, width, height):
        """
        Set the size of the rectangle.

        @param double width, height
        """
        self._width, self._height = width, height

        #added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)
        if self.HasDiagramFrame():
            self.UpdateModel()
        
        for anchor in self._anchors:
            ax, ay = anchor.GetPosition()
            # Reset position to stick the border
            anchor.SetPosition(ax, ay)

           
    #>------------------------------------------------------------------------

    def Resize(self, sizer, x, y):
        """
        Resize the rectangle according to the new position of the sizer.
        Not used to programmaticaly resize a shape. Use `SetSize` for this.

        @param SizerShape sizer
        @param double x, y : position of the sizer
        """
        tlx, tly = self.GetTopLeft()
        w, h = self.GetSize()
        sw, sh = sign(w), sign(h)
        w, h = abs(w), abs(h)
        if sizer is self._topLeftSizer:
            nw = sw * (w - x + tlx)
            nh = sh * (h - y + tly)
            self._ox = self._ox * nw / w
            self._oy = self._oy * nh / h
            self.SetSize(nw, nh)
            self.SetTopLeft(x, y)
            self._topRightSizer.SetRelativePosition(nw - 1, 0)
            self._botLeftSizer.SetRelativePosition(0, nh - 1)
            self._botRightSizer.SetRelativePosition(nw - 1, nh - 1)
        elif sizer is self._topRightSizer:
            nw = sw * (x - tlx)
            nh = sh * (tly + h - y)
            self.SetTopLeft(tlx, y)
            self.SetSize(nw + 1, nh)
            self._topRightSizer.SetRelativePosition(nw, 0)
            self._botRightSizer.SetRelativePosition(nw, nh - 1)
            self._botLeftSizer.SetRelativePosition(0, nh - 1)
        elif sizer is self._botLeftSizer:
            nw = sw * (w - x + tlx)
            nh = sh * (y - tly)
            self.SetTopLeft(x, tly)
            self.SetSize(nw, nh + 1)
            self._botLeftSizer.SetRelativePosition(0, nh)
            self._botRightSizer.SetRelativePosition(nw - 1, nh)
            self._topRightSizer.SetRelativePosition(nw - 1, 0)
        elif sizer is self._botRightSizer:
            nw = sw * (x - tlx)
            nh = sh * (y - tly)
            self.SetSize(nw + 1, nh + 1)
            self._botLeftSizer.SetRelativePosition(0, nh)
            self._botRightSizer.SetRelativePosition(nw, nh)
            self._topRightSizer.SetRelativePosition(nw, 0)
            
    #>------------------------------------------------------------------------

    def UpdateFromModel(self):
        """
        Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)

        Updates the shape position and size from the model in the light of a
        change of state of the diagram frame (here it's only for the zoom)
        """

        #change the position of the shape from the model
        Shape.UpdateFromModel(self)

        #get the model size   
        width, height = self.GetModel().GetSize()

        #get the diagram frame ratio between the shape and the model
        ratio = self.GetDiagram().GetPanel().GetCurrentZoom()

        # set the new size to the shape.
        self._width, self._height = width * ratio, height * ratio

    #>------------------------------------------------------------------------

    def UpdateModel(self):
        """
        Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)

        Updates the model when the shape (view) is deplaced or resized.
        """

        #change the coords of model
        Shape.UpdateModel(self)

        #get the size of the shape (view)
        width, height = self.GetSize()

        #get the ratio between the model and the shape (view) from
        #the diagram frame where the shape is displayed.
        ratio = self.GetDiagram().GetPanel().GetCurrentZoom()

        # set the new size to the model.
        self.GetModel().SetSize(width/ratio, height/ratio)
        
    #>------------------------------------------------------------------------
    # Added by C.Dutoit

    #def DrawHandles(self, dc):
    #   """
    #   Draw the handles (selection points) of the shape.
    #   A shape has no handles, because it has no size.

    #   @param wxDC dc
    #   """
    #   sx, sy = self.GetPosition()
    #   dc.DrawRectangle(sx - 1 - self._ox, sy - 1 - self._oy, 3, 3)
    #   dc.DrawRectangle(sx + self._width - 2 - self._ox,
    #       sy - 1 - self._oy, 3, 3)
    #   dc.DrawRectangle(sx - 1 - self._ox,
    #       sy + self._height - 2 - self._oy, 3, 3)
    #   dc.DrawRectangle(sx + self._width - 2 - self._ox,
    #       sy + self._height - 2 - self._oy, 3, 3)
