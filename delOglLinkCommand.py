# -*- coding: utf-8 -*-


from historyUtils import makeValuatedToken, getTokenValue
from command import Command
from BasicSoftwareLink import BasicSoftwareLink
from OglLinkFactory import getOglLinkFactory


class DelOglLinkCommand(Command):
    """
    This class is a part of the history system of PyUt.
    Every action that needs to be redone/undone should have an associated
    command. This class is to be considered as an abstract class.
    """
    
    def __init__(self, shape=None, src=None, dst=None, srcId=None, dstId=None):

        Command.__init__(self)
        self._shape=shape
        self._src=src
        self._dst=dst
        self._srcId=srcId
        self._dstId=dstId
        
        
    def serialize(self):
        serialShape = Command.serialize(self)
        
        basicSoftwareLink = self._shape.getBasicSoftwareObject()
        
        serialShape += makeValuatedToken("oglShapeModule", self._shape.__module__)
        serialShape += makeValuatedToken("oglShapeClass", self._shape.__class__)
        serialShape += makeValuatedToken("basicSoftwareShapeModule", self._shape.getBasicSoftwareObject().__module__)
        serialShape += makeValuatedToken("basicSoftwareShapeClass", self._shape.getBasicSoftwareObject().__class__.__name__)
        serialShape += makeValuatedToken("shapeId", repr(basicSoftwareLink.getId()))
        serialShape += makeValuatedToken("shapeName", basicSoftwareLink.getName())

        model = self._shape.GetModel()
        pos = model.GetPosition()
        
        serialShape += makeValuatedToken("fileName", self._shape.getBasicSoftwareObject().getFilename())
        serialShape += makeValuatedToken("position", repr(pos))
        
        serialShape += makeValuatedToken("srcId", repr(self._srcId))
        serialShape += makeValuatedToken("dstId", repr(self._dstId))
        serialShape += makeValuatedToken("srcPos", repr(self._src.GetPosition()))
        serialShape += makeValuatedToken("dstPos", repr(self._dst.GetPosition()))
        serialShape += makeValuatedToken("Name", basicSoftwareLink.getName())
        serialShape += makeValuatedToken("Type", repr(basicSoftwareLink.getType()))
        serialShape += makeValuatedToken("ExpectAnswer", basicSoftwareLink.getExpectAnswer())
        serialShape += makeValuatedToken("Qty", basicSoftwareLink.getQty())
        serialShape += makeValuatedToken("Price", basicSoftwareLink.getPrice())
        serialShape += makeValuatedToken("Way", basicSoftwareLink.getWay())
        serialShape += makeValuatedToken("Account", basicSoftwareLink.getAccount())
        serialShape += makeValuatedToken("Restriction", basicSoftwareLink.getRestriction())
        serialShape += makeValuatedToken("CltType", basicSoftwareLink.getCltType())
        serialShape += makeValuatedToken("Validity", basicSoftwareLink.getValidity())
        serialShape += makeValuatedToken("PrcMode", basicSoftwareLink.getPrcMode())
        serialShape += makeValuatedToken("Relationship", basicSoftwareLink.getRelationship())
        serialShape += makeValuatedToken("WaitingTme", repr(basicSoftwareLink.getWaitingTme()))
        
        
        df = basicSoftwareLink.getDataFrame()
        serialShape += makeValuatedToken("cbWay", df['cbWay'].iloc[1])
        serialShape += makeValuatedToken("cbQty", df['cbQty'].iloc[1])        
        serialShape += makeValuatedToken("cbPrice", df['cbPrice'].iloc[1])        
        serialShape += makeValuatedToken("cbAccount", df['cbAccount'].iloc[1])
        serialShape += makeValuatedToken("cbRestriction", df['cbRestriction'].iloc[1])
        serialShape += makeValuatedToken("cbClientType", df['cbClientType'].iloc[1])
        serialShape += makeValuatedToken("cbValidity", df['cbValidity'].iloc[1])
        serialShape += makeValuatedToken("cbPrcMode", df['cbPrcMode'].iloc[1])
        
        return serialShape
    
    def unserialize(self, serializedInfos):
        
        Command.unserialize(self, serializedInfos)
        
        shapeId = eval(getTokenValue("shapeId", serializedInfos))
        shapePosition = eval(getTokenValue("position", serializedInfos))
        srcPosition = eval(getTokenValue("srcPos", serializedInfos))
        dstPosition = eval(getTokenValue("dstPos", serializedInfos))
        
        src = self._umlFrame.getUmlObjectById(eval(getTokenValue("srcId", serializedInfos)))
        dst = self._umlFrame.getUmlObjectById(eval(getTokenValue("dstId", serializedInfos)))
        linkType = eval(getTokenValue("Type", serializedInfos))
        
        self._shape = self.getGroup().getHistory().getFrame().getUmlObjectById(shapeId)
        umlFrame = self.getGroup().getHistory().getFrame()
        basicSoftwareLink = BasicSoftwareLink(" ", linkType=linkType, source=src.getBasicSoftwareObject(), destination= dst.getBasicSoftwareObject())
        
        if not self._shape():
            oglLinkFactory = getOglLinkFactory()
            self._shape = oglLinkFactory.getOglLink(srcShape = src, basicSoftwareLink=basicSoftwareLink, dstShpae=dst, linkType=linkType)
            self._shape.setBasicSoftwareObject(basicSoftwareLink)
            self._shape.GetModel().SetPosition(shapePosition[0], shapePosition[1])
            src.addLink(self._shape)
            dst.addLink(self._shape)
            
            if eval(getTokenValue("srcId", serializedInfos)) == eval(getTokenValue("dstId", serializedInfos)):
                src = umlFrame.FindShape(srcPosition[0], srcPosition[0])
                dst = umlFrame.FindShape(dstPosition[0], dstPosition[0])
        
        basicSoftwareLink.SetId(shapeId)
        basicSoftwareLink.SetFilename(getTokenValue("fileName", serializedInfos))
        basicSoftwareLink.SetName(getTokenValue("name", serializedInfos))
        basicSoftwareLink.SetType(eval(getTokenValue("Type", serializedInfos)))
        basicSoftwareLink.SetExpectAnswer(getTokenValue("ExpectAnswer", serializedInfos))
        basicSoftwareLink.SetQty(getTokenValue("Qty", serializedInfos))
        basicSoftwareLink.SetPrice(getTokenValue("Price", serializedInfos))
        basicSoftwareLink.SetWay(getTokenValue("Way", serializedInfos))
        basicSoftwareLink.SetAccount(getTokenValue("Account", serializedInfos))
        basicSoftwareLink.SetRestriction(getTokenValue("Restriction", serializedInfos))
        basicSoftwareLink.SetCltType(getTokenValue("CltType", serializedInfos))
        basicSoftwareLink.SetValidity(getTokenValue("Validity", serializedInfos))
        basicSoftwareLink.SetPrcMode(getTokenValue("PrcMode", serializedInfos))
        basicSoftwareLink.SetRelationship(getTokenValue("Relationship", serializedInfos))
        basicSoftwareLink.SetWaitingTime(eval(getTokenValue("WaitingTime", serializedInfos)))
        
        
        basicSoftwareLink.df_checkBox['cbWay'].iloc[1] = getTokenValue("cbWay", serializedInfos)
        basicSoftwareLink.df_checkBox['cbQty'].iloc[1] = getTokenValue("cbQty", serializedInfos)
        basicSoftwareLink.df_checkBox['cbPrice'].iloc[1] = getTokenValue("cbPrice", serializedInfos)
        basicSoftwareLink.df_checkBox['cbAccount'].iloc[1] = getTokenValue("cbAccount", serializedInfos)
        basicSoftwareLink.df_checkBox['cbRestriction'].iloc[1] = getTokenValue("cbRestriction", serializedInfos)
        basicSoftwareLink.df_checkBox['cbClientType'].iloc[1] = getTokenValue("cbClientType", serializedInfos)
        basicSoftwareLink.df_checkBox['cbValidity'].iloc[1] = getTokenValue("cbValidity", serializedInfos)
        basicSoftwareLink.df_checkBox['cbPrcMode'].iloc[1] = getTokenValue("cbPrcMode", serializedInfos)

    def redo(self):
        
        umlFrame = self.getGroup.getHistory().getFrame()
        shape = self._shape
        shape.Detach()
        umlFrame.Refresh()
        
    def undo(self):
        umlFrame = self.getGroup.getHistory().getFrame()
        umlFrame.addShape(self._shape, withModelUpdate=True)
        self._shape.UpdateFromModel()
        self._umlFrame.Refresh()

    def undoUpDate(self, serializedInfos):
        Command.unserialize(self, serializedInfos)
        shapeId = eval(getTokenValue("shapeId", serializedInfos))
        shapePosition = eval(getTokenValue("position", serializedInfos))
        srcPosition = eval(getTokenValue("srcPos", serializedInfos))
        dstPosition = eval(getTokenValue("dstPos", serializedInfos))
        
        src = self._umlFrame.getUmlObjectById(eval(getTokenValue("srcId", serializedInfos)))
        dst = self._umlFrame.getUmlObjectById(eval(getTokenValue("dstId", serializedInfos)))
        linkType = eval(getTokenValue("Type", serializedInfos))
        
        self._shape = self.getGroup().getHistory().getFrame().getUmlObjectById(shapeId)
        umlFrame = self.getGroup().getHistory().getFrame()
        basicSoftwareLink = BasicSoftwareLink(" ", linkType=linkType, source=src.getBasicSoftwareObject(), destination= dst.getBasicSoftwareObject())
              
        if not self._shape():
            oglLinkFactory = getOglLinkFactory()
            self._shape = oglLinkFactory.getOglLink(srcShape = src, basicSoftwareLink=basicSoftwareLink, dstShpae=dst, linkType=linkType)
            self._shape.setBasicSoftwareObject(basicSoftwareLink)
            self._shape.GetModel().SetPosition(shapePosition[0], shapePosition[1])
            src.addLink(self._shape)
            dst.addLink(self._shape)
            
            if eval(getTokenValue("srcId", serializedInfos)) == eval(getTokenValue("dstId", serializedInfos)):
                src = umlFrame.FindShape(srcPosition[0], srcPosition[0])
                dst = umlFrame.FindShape(dstPosition[0], dstPosition[0])
                
        basicSoftwareLink.SetId(shapeId)
        basicSoftwareLink.SetFilename(getTokenValue("fileName", serializedInfos))
        basicSoftwareLink.SetName(getTokenValue("name", serializedInfos))
        basicSoftwareLink.SetType(eval(getTokenValue("Type", serializedInfos)))
        basicSoftwareLink.SetExpectAnswer(getTokenValue("ExpectAnswer", serializedInfos))
        basicSoftwareLink.SetQty(getTokenValue("Qty", serializedInfos))
        basicSoftwareLink.SetPrice(getTokenValue("Price", serializedInfos))
        basicSoftwareLink.SetWay(getTokenValue("Way", serializedInfos))
        basicSoftwareLink.SetAccount(getTokenValue("Account", serializedInfos))
        basicSoftwareLink.SetRestriction(getTokenValue("Restriction", serializedInfos))
        basicSoftwareLink.SetCltType(getTokenValue("CltType", serializedInfos))
        basicSoftwareLink.SetValidity(getTokenValue("Validity", serializedInfos))
        basicSoftwareLink.SetPrcMode(getTokenValue("PrcMode", serializedInfos))
        basicSoftwareLink.SetRelationship(getTokenValue("Relationship", serializedInfos))
        basicSoftwareLink.SetWaitingTime(eval(getTokenValue("WaitingTime", serializedInfos)))
        
        
        basicSoftwareLink.df_checkBox['cbWay'].iloc[1] = getTokenValue("cbWay", serializedInfos)
        basicSoftwareLink.df_checkBox['cbQty'].iloc[1] = getTokenValue("cbQty", serializedInfos)
        basicSoftwareLink.df_checkBox['cbPrice'].iloc[1] = getTokenValue("cbPrice", serializedInfos)
        basicSoftwareLink.df_checkBox['cbAccount'].iloc[1] = getTokenValue("cbAccount", serializedInfos)
        basicSoftwareLink.df_checkBox['cbRestriction'].iloc[1] = getTokenValue("cbRestriction", serializedInfos)
        basicSoftwareLink.df_checkBox['cbClientType'].iloc[1] = getTokenValue("cbClientType", serializedInfos)
        basicSoftwareLink.df_checkBox['cbValidity'].iloc[1] = getTokenValue("cbValidity", serializedInfos)
        basicSoftwareLink.df_checkBox['cbPrcMode'].iloc[1] = getTokenValue("cbPrcMode", serializedInfos)
        
        umlFrame = self.getGroup().getHistory().getFrame()
        umlFrame.addShape(self._shape, 0,0, withModelUpdate=False)
        self._shape.UpdateFromModel()
        umlFrame.Refresh()
        
    def upDate(self, serializedInfos):
        umlFrame = self.getGroup().getHistory().getFrame()
        if not umlFrame : return
        
        #name of the oglObject's class to rebuild it
        oglShapeClassName = getTokenValue("oglShapeClass", serializedInfos)
        #name of the oglObject's module to rebuild it
        oglShapeModule = getTokenValue("oglShapeModule", serializedInfos)
        #name of the pyutObject's class to rebuild it
        basicSoftwareShapeClassName = getTokenValue("basicSoftwareShapeClass", serializedInfos)
        #name of the pyutObject's module to rebuild it
        basicSoftwareShapeModule = getTokenValue("basicSoftwareShapeModule", serializedInfos)
        #name of the pyutObject
        shapeName = getTokenValue("shapeName", serializedInfos)
        # id of the pyutObject
        shapeId = eval(getTokenValue("shapeId", serializedInfos))
        #oglObject's modelPosition (MVC : see miniOgl)
        shapePosition = eval(getTokenValue("position", serializedInfos))      
    
        #import the module which contains the ogl and pyut shape classes and
        #get that classes. 
        oglShapeClass = getattr(__import__(oglShapeModule), oglShapeClassName)
        basicSoftwareShapeClass = getattr(__import__(basicSoftwareShapeModule), basicSoftwareShapeClassName)

        if not self._shape:
            basicSoftwareLink = basicSoftwareShapeClass(shapeName)
            basicSoftwareLink.setId(shapeId)    
            self._shape = oglShapeClass()
            self._shape.setBasicSoftwareObject(basicSoftwareLink)
            self._shape.GetModel().SetPosition(shapePosition[0], shapePosition[1])
        else:
            self._shape.GetModel().SetPosition(shapePosition[0], shapePosition[1])
            basicSoftwareLink = self._shape.getBasicSoftwareObject()

        basicSoftwareLink.SetId(shapeId)
        basicSoftwareLink.SetFilename(getTokenValue("fileName", serializedInfos))
        basicSoftwareLink.SetName(getTokenValue("name", serializedInfos))
        basicSoftwareLink.SetType(eval(getTokenValue("Type", serializedInfos)))
        basicSoftwareLink.SetExpectAnswer(getTokenValue("ExpectAnswer", serializedInfos))
        basicSoftwareLink.SetQty(getTokenValue("Qty", serializedInfos))
        basicSoftwareLink.SetPrice(getTokenValue("Price", serializedInfos))
        basicSoftwareLink.SetWay(getTokenValue("Way", serializedInfos))
        basicSoftwareLink.SetAccount(getTokenValue("Account", serializedInfos))
        basicSoftwareLink.SetRestriction(getTokenValue("Restriction", serializedInfos))
        basicSoftwareLink.SetCltType(getTokenValue("CltType", serializedInfos))
        basicSoftwareLink.SetValidity(getTokenValue("Validity", serializedInfos))
        basicSoftwareLink.SetPrcMode(getTokenValue("PrcMode", serializedInfos))
        basicSoftwareLink.SetRelationship(getTokenValue("Relationship", serializedInfos))
        basicSoftwareLink.SetWaitingTime(eval(getTokenValue("WaitingTime", serializedInfos)))
        
        
        basicSoftwareLink.df_checkBox['cbWay'].iloc[1] = getTokenValue("cbWay", serializedInfos)
        basicSoftwareLink.df_checkBox['cbQty'].iloc[1] = getTokenValue("cbQty", serializedInfos)
        basicSoftwareLink.df_checkBox['cbPrice'].iloc[1] = getTokenValue("cbPrice", serializedInfos)
        basicSoftwareLink.df_checkBox['cbAccount'].iloc[1] = getTokenValue("cbAccount", serializedInfos)
        basicSoftwareLink.df_checkBox['cbRestriction'].iloc[1] = getTokenValue("cbRestriction", serializedInfos)
        basicSoftwareLink.df_checkBox['cbClientType'].iloc[1] = getTokenValue("cbClientType", serializedInfos)
        basicSoftwareLink.df_checkBox['cbValidity'].iloc[1] = getTokenValue("cbValidity", serializedInfos)
        basicSoftwareLink.df_checkBox['cbPrcMode'].iloc[1] = getTokenValue("cbPrcMode", serializedInfos)      
        
        self._shape.UpdateFromModel()
        umlFrame.Refresh()