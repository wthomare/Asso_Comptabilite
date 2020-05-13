# -*- coding: UTF-8 -*-

from historyUtils import makeValuatedToken, getTokenValue
from command import Command
from BasicSoftwareSDInstance import BasicSoftwareSDInstance
import BasicSoftwareUtils

class DelOglObjectCommand(Command):
    """
    This class is a part of the history system of BasicSoftware.
    It execute/undo/redo the deletion of an OglObject. It is to be considered
    as an abstract class, because OglObject is abstract.
    """
    
    def __init__(self, shape = None):

        Command.__init__(self)
        self._shape = shape
        
    #>------------------------------------------------------------------------
       
    def serialize(self):

        serialShape = Command.serialize(self)

        #serialize the class and module of the ogl and pyut shape to get the
        #constructors for the unserialization.
        oglShapeModule = self._shape.__module__
        oglShapeClass = self._shape.__class__.__name__
        basicSoftwareShapeModule = self._shape.getBasicSoftwareObject().__module__
        basicSoftwareShapeClass = self._shape.getBasicSoftwareObject().__class__.__name__
        serialShape += makeValuatedToken("oglShapeModule", oglShapeModule)
        serialShape += makeValuatedToken("oglShapeClass", oglShapeClass)
        serialShape += makeValuatedToken("basicSoftwareShapeModule", basicSoftwareShapeModule)
        serialShape += makeValuatedToken("basicSoftwareShapeClass", basicSoftwareShapeClass)
        
        model = self._shape.GetModel()
        pos = model.GetPosition()
        size = model.GetSize()
        serialShape += makeValuatedToken("position", repr(pos))
        serialShape += makeValuatedToken("size", repr(size))
        
        from delOglLinkCommand import DelOglLinkCommand
        for link in self._shape.getLinks():
            if not link.IsSelected():
                cmd = DelOglLinkCommand(link)
                self.getGroup().addCommand(cmd)
            

        #serialize data to init the associated BasicSoftwareObject        
        basicSoftwareObj = self._shape.getBasicSoftwareObject()
        shapeId = basicSoftwareObj.getId()
        shapeName = basicSoftwareObj.getName()
        serialShape += makeValuatedToken("shapeId", repr(shapeId))
        serialShape += makeValuatedToken("shapeName", shapeName)
        
        return serialShape
    
    def unserialize(self, serializedInfos):
        """
        unserialize the data needed to undo/redo a delete command and create
        a shape
        """
        try:
            #UNSERIALIZATION OF THE DATA NEEDED BY THE COMMAND :
            #name of the oglObject's class to rebuild it
            oglShapeClassName = getTokenValue("oglShapeClass", serializedInfos)
            #name of the oglObject's module to rebuild it
            oglShapeModule = getTokenValue("oglShapeModule", serializedInfos)
            #name of the BasicSoftwareObject's class to rebuild it
            basicSoftwareShapeClassName = getTokenValue("basicSoftwareShapeClass", serializedInfos)
            #name of the BasicSoftwareObject's module to rebuild it
            basicSoftwareShapeModule = getTokenValue("basicSoftwareShapeModule", serializedInfos)
            #name of the BasicSoftwareObject
            shapeName = getTokenValue("shapeName", serializedInfos)
            # id of the BasicSoftwareObject
            shapeId = eval(getTokenValue("shapeId", serializedInfos))
            #oglObject's modelPosition (MVC : see miniOgl)
            shapePosition = eval(getTokenValue("position", serializedInfos))
            #oglObject's modelSize (MVC : see miniOgl)
            shapeSize = eval(getTokenValue("size", serializedInfos))
    
            #CONSTRUCTION OF THE UML OBJECT :
            #import the module which contains the ogl and BasicSoftware shape classes and
            #get that classes. 
            oglShapeClass = getattr(__import__(oglShapeModule), oglShapeClassName)
            basicSoftwareShapeClass = getattr(__import__(basicSoftwareShapeModule), basicSoftwareShapeClassName)
    
            #build the BasicSoftwareObject : it suppose that every parameter of the
            #constructor has a default value
    
            self._shape = self.getGroup().getHistory().getFrame().getUmlObjectById(shapeId)
            umlFrame = self.getGroup().getHistory().getFrame()
            if not self._shape:
                basicSoftwareShape = basicSoftwareShapeClass(shapeName)
                basicSoftwareShape.setId(shapeId)    
                
                if isinstance(basicSoftwareShape, BasicSoftwareSDInstance):
                    self._shape = oglShapeClass(basicSoftwareObject = basicSoftwareShape, parentFrame=umlFrame, redo=True, xPos=shapePosition[0], yPos=shapePosition[1])
                    self._shape.SetSize(shapeSize[0], shapeSize[1])
                else:
                    self._shape = oglShapeClass()
                    self._shape.setBasicSoftwareObject(basicSoftwareShape)
                    self._shape.GetModel().SetPosition(shapePosition[0], shapePosition[1])
                    self._shape.GetModel().SetSize(shapeSize[0], shapeSize[1])
        except:
            msg = "Failed to unserialized a roup in the DelOglobjectCommand"
            BasicSoftwareUtils.displayError(msg, 'DelOglObjectCommand.unserialized error')
            
    
    def redo(self):
        umlFrame = self.GetGroup().getHistory().getFrame()
        umlFrame.addShape(self._shape, 0, 0, withModelUpdate=False)
        self._shape.UpdateFromModel()
        umlFrame.Refresh()
        
    def redoUpdate(self):
        umlFrame = self.GetGroup().getHistory().getFrame()
        shape = self._shape
        shape.Detach()
        umlFrame.Refresh()
        
    def undoUpdate(self):
        umlFrame = self.GetGroup().getHistory().getFrame()
        umlFrame.addShape(self._shape, 0, 0, withUpdateUpdate=False)
        self._shape.UpdateFromModel()
        umlFrame.Refresh()