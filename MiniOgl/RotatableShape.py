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

from MiniOgl.RectangleShape            import RectangleShape
from MiniOgl.VShapes                   import VShape

__all__ = ["RotatableShape"]

class RotatableShape(RectangleShape):
    """
    Canvas for shapes that can be rotated.
    The shape is defined for one orientation, using a list of VShapes which
    is a class field named SHAPES. Then, the method Rotate can be called to
    automatically rotate the shape.

    Exported methods:
    -----------------

    __init__(self, x=0.0, y=0.0, width=0.0, height=0.0, parent=None)
        Constructor.
    GetAngle(self)
        Get the actual angle, in range [0; 3].
    SetAngle(self, angle)
        Set the actual angle, in range [0; 3].
    SetScale(self, scale)
        Set the scaling of this shape.
    GetScale(self)
        Get the scaling of this shape.
    SetOrigin(self, x, y)
        Set the origin of the shape, from its upper left corner.
    Rotate(self, clockwise)
        Rotate the shape 90° clockwise or conterclockwise.
    Draw(self, dc, withChildren=True)
        Draw the shape on the dc.

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def __init__(self, x=0.0, y=0.0, width=0.0, height=0.0, parent=None):
        """
        Constructor.

        @param double x, y : position of the point
        @param double width, height : size of the rectangle
        @param Shape parent : parent shape
        """
        RectangleShape.__init__(self, x, y, width, height, parent)
        # this is the definition of the shape
        self._defineShape()
        self._angle = 0                 # angle is in [0..3], by steps of 90°
        self._vShapes = self._SHAPES[0] # currently used list of shapes
        self._InitRotations()          # create the other rotations if necessary
        self._scale = 1.0              # scale of the shape
        self._sox, self._soy = self._ox, self._oy # ox, oy with scale == 1
        self._sw, self._sh = self._width, self._height # width and height with
                                                       # scale == 1

    #>------------------------------------------------------------------------

    def _defineShape(self):
        """
        This is the definition of the graphical object.
        It uses a list of basic shapes, that support rotation and scaling.
        Define your own shapes in children classes by filling the innermost
        list with `VShape` instances.
        """
        self._SHAPES = [
            [
            ]
        ]

    #>------------------------------------------------------------------------

    def GetAngle(self):
        """
        Get the actual angle, in range [0; 3].

        @return int angle
        """
        return self._angle

    #>------------------------------------------------------------------------

    def SetAngle(self, angle):
        """
        Set the actual angle, in range [0; 3].
        0 is the initial angle. Each unit is a clockwise 90° rotation.

        @param int angle
        """
        while self._angle != angle:
            self.Rotate(1)

    #>------------------------------------------------------------------------

    def SetScale(self, scale):
        """
        Set the scaling of this shape.

        @param float scale
        """
        self._scale = scale
        self._ox, self._oy = self._sox * scale, self._soy * scale
        self._width, self._height = self._sw * scale, self._sh * scale

    #>------------------------------------------------------------------------

    def GetScale(self):
        """
        Get the scaling of this shape.

        @return float
        """
        return self._scale

    #>------------------------------------------------------------------------

    def SetOrigin(self, x, y):
        """
        Set the origin of the shape, from its upper left corner.

        @param double x, y : new origin
        """
        self._ox, self._oy = x, y
        scale = self._scale
        if scale != 0:
            self._sox, self._soy = x / scale, y / scale
        else:
            self._sox, self._soy = 0, 0

    #>------------------------------------------------------------------------

    def _InitRotations(self):
        """
        Init the rotations.
        Will be done just one time, or when the initial shape is changed.
        """
        if len(self._SHAPES) == 1:
            from copy import copy
            for i in range(1, 4):
                next = []
                for shape in self._SHAPES[0]:
                    n = copy(shape)
                    n.SetAngle(i)
                    next.append(n)
                self._SHAPES.append(next)

    #>------------------------------------------------------------------------

    def Rotate(self, clockwise):
        """
        Rotate the shape 90° clockwise or conterclockwise.

        @param bool clockwise
        """
        if clockwise:
            self._angle += 1
        else:
            self._angle -= 1
        self._angle %= 4
        self._vShapes = self._SHAPES[self._angle]
        for child in self._anchors + self._children:
            lock = False
            x, y = child.GetRelativePosition()
            if not child.IsDraggable():
                child.SetDraggable(True)
                lock = True
            x, y = VShape().Convert(1, x, y)
            child.SetRelativePosition(x, y)
            if lock:
                child.SetDraggable(False)
        self._width, self._height = \
            VShape().Convert(1, self._width, self._height)
        self._ox, self._oy= VShape().Convert(1, self._ox, self._oy)

    #>------------------------------------------------------------------------

    def Draw(self, dc, withChildren=True):
        """
        Draw the shape on the dc.

        @param wxDC dc
        """
        if self._visible:
            RectangleShape.Draw(self, dc, False)
            for shape in self._vShapes:
                shape.Draw(dc, self._x, self._y, self._scale)
            if withChildren:
                self.DrawChildren(dc)

    #>------------------------------------------------------------------------
