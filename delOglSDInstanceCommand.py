# -*- coding: utf-8 -*-

from historyUtils import makeValuatedToken, getTokenValue
from delOglLinkObjectCommand import DelOglLinkObjectCommand
import re

class DelOglSDInstanceCommand(DelOglLinkObjectCommand):
    
    def __init__(self, shape=None):
        DelOglLinkObjectCommand.__init__(self, shape)
    
    def serialize(self):
        serialShape = DelOglLinkObjectCommand.serialize(self)
        
        basicSoftwareSDInstance = self._shape.getBasicSoftwareObject()
        
        serialShape += makeValuatedToken("instanceName", re.sub('\n', '',basicSoftwareSDInstance.getInstanceName()))
        serialShape += makeValuatedToken("instanceLifeLength", repr(basicSoftwareSDInstance.getInstanceLifeLength()))
        serialShape += makeValuatedToken("instanceType", basicSoftwareSDInstance.getInstanceType())
        return serialShape
    
    def unserialize(self, serializedInfos):
        DelOglLinkObjectCommand.unserialize(self, serializedInfos)
        
        basicSoftwareSDInstance = self._shape.getBasicSoftwareObject()
        basicSoftwareSDInstance.SetInstanceName(getTokenValue("instanceNane", serializedInfos).replace(': ', ':\n',1))
        basicSoftwareSDInstance.SetInstanceLifeLength(eval(getTokenValue("instanceLifeLength", serializedInfos)))
        basicSoftwareSDInstance.SetInstanceType(getTokenValue("instanceType", serializedInfos))
        
    def undoUpDate(self, serializedInfos):
        DelOglLinkObjectCommand.undoUpDate(self, serializedInfos)
        
        self._shape.getBasicSoftware().SetInstanceName(getTokenValue("instanceNane", serializedInfos).replace(': ', ':\n',1))
        self._shape.getBasicSoftware().SetInstanceLifeLength(eval(getTokenValue("instanceLifeLength", serializedInfos)))
        self._shape.getBasicSoftware().SetInstanceType(getTokenValue("instanceType", serializedInfos))
        
    def upDate(self, serializedInfos):
        umlFrame = self.getGroup().getHistory().getFrame()
        if not umlFrame: return
        
        DelOglLinkObjectCommand.upDate(self, serializedInfos)
        
        self._shape.getBasicSoftware().SetFilename(getTokenValue("fileName", serializedInfos))        
        self._shape.getBasicSoftware().SetInstanceName(getTokenValue("instanceNane", serializedInfos).replace(': ', ':\n',1))
        self._shape.getBasicSoftware().SetInstanceLifeLength(eval(getTokenValue("instanceLifeLength", serializedInfos)))
        self._shape.getBasicSoftware().SetInstanceType(getTokenValue("instanceType", serializedInfos))
        
        self._shape.UpdateFromModel()
        umlFrame.Refresh()