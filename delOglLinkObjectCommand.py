#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from historyUtils import getTokenValue
from delOglObjectCommand import DelOglObjectCommand

class DelOglLinkObjectCommand(DelOglObjectCommand):

    
    def __init__(self, shape = None):
        """
        Constructor.
        @param shape OglLinkedObject    : object that is destroyed
        """
        
        DelOglObjectCommand.__init__(self, shape)
       
    def serialize(self):
        """
        Serialize the data needed by the destroyed OglLinkedObject.
        @return a string representation of the data needed by the command.
        """
        
        #serialize the data common to all OglObjects
        serialShape = DelOglObjectCommand.serialize(self)

        fileName = self._shape.getBasicSoftwareObject().getFilename()
        serialShape += getTokenValue("fileName",fileName)

        return serialShape
    
    def unserialize(self, serializedInfos):
        """
        unserialize the data needed by the destroyed OglLinkedObject.
        @param serializedInfos String   :   serialized data needed by the command.
        """
        
        #unserialize the data common to all OglObjects
        DelOglObjectCommand.unserialize(self, serializedInfos)

        fileName = getTokenValue("fileName", serializedInfos)
        self._shape.getPyutObject().setFilename(fileName)

    def undoUpDate(self, serializedInfos):
        
        oglShapeClassName = getTokenValue("oglShapeClass", serializedInfos)
        oglShapeModule = getTokenValue("oglShapeModule", serializedInfos)
        basicSoftwareShapeClassName = getTokenValue("basicSoftwareShapeClass", serializedInfos)
        basicSoftwareShapeModule = getTokenValue('basicSoftwareModule', serializedInfos)
        shapeName = getTokenValue("shapeName", serializedInfos)
        shapeId = eval(getTokenValue("shapeId", serializedInfos))
        shapePosition= eval(getTokenValue("shapePosition", serializedInfos))
        shapeSize = eval(getTokenValue("shapeSize", serializedInfos))
        oglShapeClass = getattr(__import__(oglShapeModule), oglShapeClassName)
        basicSoftwareShapeClass = getattr(__import__(basicSoftwareShapeModule), basicSoftwareShapeClassName)
        
        self._shape = self.getGroup().getHistory().getFrame().getUmlObjectById(shapeId)
        if not self._shape:
            basicSoftwareShape = basicSoftwareShapeClass(shapeName)
            basicSoftwareShape.setId(shapeId)
            
            self._shape = oglShapeClass()
            self._shape.setBasicSoftwareObject(basicSoftwareShape)
            self._shape.GetModel().SetPosition(shapePosition[0], shapePosition[1])
            self._shape.GetModel().SetSize(shapeSize[0], shapeSize[1])
        
        self._shape.getBasicSoftwareObject().setFilename(getTokenValue("filename", serializedInfos))
    
    def upDate(self, serializedInfos):
        oglShapeClassName = getTokenValue("oglShapeClass", serializedInfos)
        oglShapeModule = getTokenValue("oglShapeModule", serializedInfos)
        basicSoftwareShapeClassName = getTokenValue("basicSoftwareShapeClass", serializedInfos)
        basicSoftwareShapeModule = getTokenValue('basicSoftwareModule', serializedInfos)
        shapeName = getTokenValue("shapeName", serializedInfos)
        shapeId = eval(getTokenValue("shapeId", serializedInfos))
        shapePosition= eval(getTokenValue("shapePosition", serializedInfos))
        shapeSize = eval(getTokenValue("shapeSize", serializedInfos))
        oglShapeClass = getattr(__import__(oglShapeModule), oglShapeClassName)
        basicSoftwareShapeClass = getattr(__import__(basicSoftwareShapeModule), basicSoftwareShapeClassName)
        
        self._shape = self.getGroup().getHistory().getFrame().getUmlObjectById(shapeId)
        if not self._shape:
            basicSoftwareShape = basicSoftwareShapeClass(shapeName)
            basicSoftwareShape.setId(shapeId)
            self._shape = oglShapeClass()
            self._shape.setBasicSoftwareObject(basicSoftwareShape)
            self._shape.GetModel().SetPosition(shapePosition[0], shapePosition[1])
            self._shape.GetModel().SetSize(shapeSize[0], shapeSize[1])
            
        else:
            self._shape.GetModel().SetPosition(shapePosition[0], shapePosition[1])
            self._shape.GetModel().SetSize(shapeSize[0], shapeSize[1])            