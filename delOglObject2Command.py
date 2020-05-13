# -*- coding: UTF-8 -*-

from historyUtils import makeValuatedToken, getTokenValue
from delOglLinkObjectCommand import DelOglLinkObjectCommand

class DelOglObject2Command(DelOglLinkObjectCommand):
    """
    For OglNote
    """
    def __init__(self, shape=None):
        DelOglLinkObjectCommand.__init__(self, shape)
        
    def serialize(self):
        serialShape = DelOglLinkObjectCommand.serialize(self)
        basicSoftware = self._shape.getBasicSoftwareObject()
        
        serialShape += makeValuatedToken("Pattern", basicSoftware.getPattern())
        serialShape += makeValuatedToken("PollTimeout", repr(basicSoftware.getPollTimeout()))
        serialShape += makeValuatedToken("Timeout", repr(basicSoftware.getTimeout()))
        serialShape += makeValuatedToken("DataFormat", basicSoftware.getDataFormat())
        serialShape += makeValuatedToken("UnitTestInst", basicSoftware.getUnitTestInst())
        serialShape += makeValuatedToken("LogFilesList", basicSoftware.getLogFilesList())
        serialShape += makeValuatedToken("FieldsToExclude", basicSoftware.getFieldsToExclude())
        serialShape += makeValuatedToken("FieldsToCheck", basicSoftware.getFieldsToCheck())
        serialShape += makeValuatedToken("Function", basicSoftware.getFunction())
        serialShape += makeValuatedToken("Name", basicSoftware.getName())
        serialShape += makeValuatedToken("Instruction", basicSoftware.getInstruction())
        serialShape += makeValuatedToken("LogMessage", basicSoftware.getLogMessage())
        serialShape += makeValuatedToken("TxtTwo", basicSoftware.getTxtTwo())
        serialShape += makeValuatedToken("TxtTwo2", basicSoftware.getTxtTwo2())
        serialShape += makeValuatedToken("TxtThree", basicSoftware.getTxtThree())
        serialShape += makeValuatedToken("TxtThree2", basicSoftware.getTxtThree2())
        serialShape += makeValuatedToken("ccbThree", basicSoftware.getccbThree())
        serialShape += makeValuatedToken("instanceNewTitle", basicSoftware.getInstanceTitleType())
        serialShape += makeValuatedToken("Path", basicSoftware.getPath())

        return serialShape
    
    def unserialize(self, serializedInfos):
        
        DelOglLinkObjectCommand.unserialize(self, serializedInfos)
        basicSoftwareObject = self._shape.getBasicSoftwareObject()

        basicSoftwareObject.setPattern((getTokenValue("Pattern", serializedInfos)))
        basicSoftwareObject.setPollTimeout(eval(getTokenValue("PollTimeout", serializedInfos)))
        basicSoftwareObject.setTimeout(eval(getTokenValue("Timeout", serializedInfos)))
        basicSoftwareObject.setDataFormat((getTokenValue("DataFormat", serializedInfos)))
        basicSoftwareObject.setUnitTestInst((getTokenValue("UnitTestInst", serializedInfos)))
        basicSoftwareObject.setLogFilesList((getTokenValue("LogFilesList", serializedInfos)))
        basicSoftwareObject.setFieldsToExclude((getTokenValue("FieldsToExclude", serializedInfos)))
        basicSoftwareObject.setFieldsToCheck((getTokenValue("FieldsToCheck", serializedInfos)))
        basicSoftwareObject.setFunction((getTokenValue("Function", serializedInfos)))
        basicSoftwareObject.setName((getTokenValue("Name",serializedInfos)))
        basicSoftwareObject.setInstruction((getTokenValue("Instruction", serializedInfos)))
        basicSoftwareObject.setLogMessage((getTokenValue("LogMessage", serializedInfos)))
        basicSoftwareObject.setTxtTwo((getTokenValue("TxtTwo", serializedInfos)))
        basicSoftwareObject.setTxtTwo2((getTokenValue("TxtTwo2", serializedInfos)))
        basicSoftwareObject.setTxtThree((getTokenValue("TxtThree", serializedInfos)))
        basicSoftwareObject.setTxtThree2((getTokenValue("TxtThree2", serializedInfos)))
        basicSoftwareObject.setccbThree((getTokenValue("ccbThree", serializedInfos)))
        basicSoftwareObject.setInstanceTitleType((getTokenValue("instanceNewTitle", serializedInfos)))
        basicSoftwareObject.setPath((getTokenValue("Path", serializedInfos)))

    def undoUpDate(self, serializedInfos):
        
        DelOglLinkObjectCommand.undoUpDate(self, serializedInfos)


        self._shape.getself._shape.getBasicSoftwareObject()().setPattern((getTokenValue("Pattern", serializedInfos)))
        self._shape.getBasicSoftwareObject().setPollTimeout(eval(getTokenValue("PollTimeout", serializedInfos)))
        self._shape.getBasicSoftwareObject().setTimeout(eval(getTokenValue("Timeout", serializedInfos)))
        self._shape.getBasicSoftwareObject().setDataFormat((getTokenValue("DataFormat", serializedInfos)))
        self._shape.getBasicSoftwareObject().setUnitTestInst((getTokenValue("UnitTestInst", serializedInfos)))
        self._shape.getBasicSoftwareObject().setLogFilesList((getTokenValue("LogFilesList", serializedInfos)))
        self._shape.getBasicSoftwareObject().setFieldsToExclude((getTokenValue("FieldsToExclude", serializedInfos)))
        self._shape.getBasicSoftwareObject().setFieldsToCheck((getTokenValue("FieldsToCheck", serializedInfos)))
        self._shape.getBasicSoftwareObject().setFunction((getTokenValue("Function", serializedInfos)))
        self._shape.getBasicSoftwareObject().setName((getTokenValue("Name",serializedInfos)))
        self._shape.getBasicSoftwareObject().setInstruction((getTokenValue("Instruction", serializedInfos)))
        self._shape.getBasicSoftwareObject().setLogMessage((getTokenValue("LogMessage", serializedInfos)))
        self._shape.getBasicSoftwareObject().setTxtTwo((getTokenValue("TxtTwo", serializedInfos)))
        self._shape.getBasicSoftwareObject().setTxtTwo2((getTokenValue("TxtTwo2", serializedInfos)))
        self._shape.getBasicSoftwareObject().setTxtThree((getTokenValue("TxtThree", serializedInfos)))
        self._shape.getBasicSoftwareObject().setTxtThree2((getTokenValue("TxtThree2", serializedInfos)))
        self._shape.getBasicSoftwareObject().setccbThree((getTokenValue("ccbThree", serializedInfos)))
        self._shape.getBasicSoftwareObject().setInstanceTitleType(eval(getTokenValue("instanceNewTitle", serializedInfos)))
        self._shape.getBasicSoftwareObject().setPath((getTokenValue("Path", serializedInfos)))
       
    def upDate(self, serializedInfos):
        
        umlFrame =self.getGroup().getHistory().getFrame()
        if not umlFrame: return
        
        DelOglLinkObjectCommand.upDate(self, serializedInfos)
        
        self._shape.getself._shape.getBasicSoftwareObject()().setPattern((getTokenValue("Pattern", serializedInfos)))
        self._shape.getBasicSoftwareObject().setPollTimeout(eval(getTokenValue("PollTimeout", serializedInfos)))
        self._shape.getBasicSoftwareObject().setTimeout(eval(getTokenValue("Timeout", serializedInfos)))
        self._shape.getBasicSoftwareObject().setDataFormat((getTokenValue("DataFormat", serializedInfos)))
        self._shape.getBasicSoftwareObject().setUnitTestInst((getTokenValue("UnitTestInst", serializedInfos)))
        self._shape.getBasicSoftwareObject().setLogFilesList((getTokenValue("LogFilesList", serializedInfos)))
        self._shape.getBasicSoftwareObject().setFieldsToExclude((getTokenValue("FieldsToExclude", serializedInfos)))
        self._shape.getBasicSoftwareObject().setFieldsToCheck((getTokenValue("FieldsToCheck", serializedInfos)))
        self._shape.getBasicSoftwareObject().setFunction((getTokenValue("Function", serializedInfos)))
        self._shape.getBasicSoftwareObject().setName((getTokenValue("Name",serializedInfos)))
        self._shape.getBasicSoftwareObject().setInstruction((getTokenValue("Instruction", serializedInfos)))
        self._shape.getBasicSoftwareObject().setLogMessage((getTokenValue("LogMessage", serializedInfos)))
        self._shape.getBasicSoftwareObject().setTxtTwo((getTokenValue("TxtTwo", serializedInfos)))
        self._shape.getBasicSoftwareObject().setTxtTwo2((getTokenValue("TxtTwo2", serializedInfos)))
        self._shape.getBasicSoftwareObject().setTxtThree((getTokenValue("TxtThree", serializedInfos)))
        self._shape.getBasicSoftwareObject().setTxtThree2((getTokenValue("TxtThree2", serializedInfos)))
        self._shape.getBasicSoftwareObject().setccbThree((getTokenValue("ccbThree", serializedInfos)))
        self._shape.getBasicSoftwareObject().setInstanceTitleType(eval(getTokenValue("instanceNewTitle", serializedInfos)))
        self._shape.getBasicSoftwareObject().setPath((getTokenValue("Path", serializedInfos)))
       
        self._shape.UpdateFromModel()
        umlFrame.Refresh()