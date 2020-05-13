# -*- coding: utf-8 -*-

from UmlDiagramsFrame import UmlDiagramsFrame

class UmlSequenceDiagramsFrame(UmlDiagramsFrame):
    def __init__(self, parent):
        UmlDiagramsFrame.__init__(self, parent)
        self.newDiagram()
        self._cdInstances = []