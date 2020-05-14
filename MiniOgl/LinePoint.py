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

from MiniOgl.PointShape                import PointShape

__all__ = ["LinePoint"]

class LinePoint(PointShape):
    """
    This is a point guiding a line.

    Exported methods:
    -----------------

    __init__(self, x, y, parent=None)
        Constructor.
    AddLine(self, line)
        Add a line to this point.
    Detach(self)
        Detach the point from the diagram
    GetLines(self)
        Get the lines passing through this point.
    RemoveLine(self, line)
        Remove a line from this point.
    SetMoving(self, state)
        A non-moving shape will be redrawn faster when others are moved.

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def __init__(self, x, y, parent=None):
        """
        Constructor.

        @param double x, y : position of the point
        @param Shape parent : parent shape
        """
        #print ">>>LinePoint ", x, y
        PointShape.__init__(self, x, y, parent)
        self._lines = [] # a list of LineShape passing through this point

    #>------------------------------------------------------------------------

    def AddLine(self, line):
        """
        Add a line to this point.

        @param LineShape line
        """
        self._lines.append(line)

    #>------------------------------------------------------------------------

    def Detach(self):
        """
        Detach the point from the diagram
        This also removes the point from all the lines it belongs to.
        """
        PointShape.Detach(self)
        for line in self._lines:
            line.Remove(self)
        self._lines = []

    #>------------------------------------------------------------------------

    def GetLines(self):
        """
        Get the lines passing through this point.
        Modifying the returned list won't modify the point itself.

        @return LineShape []
        """
        return self._lines[:]

    #>------------------------------------------------------------------------

    def RemoveLine(self, line):
        """
        Remove a line from this point.

        @param LineShape line
        """
        if line in self._lines:
            self._lines.remove(line)

    #>------------------------------------------------------------------------

    def SetMoving(self, state):
        """
        A non-moving shape will be redrawn faster when others are moved.
        See DiagramFrame.Refresh for more information.

        @param bool state
        """
        PointShape.SetMoving(self, state)
        for line in self._lines:
            line.SetMoving(state)

    #>------------------------------------------------------------------------
