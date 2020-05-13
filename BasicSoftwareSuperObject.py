# -*- coding: utf-8 -*-

from BasicSoftwareLinkedObject import BasicSoftwareLinkedObject
from BasicSoftwareConst import OGL_FIXLOG, OGL_TITLEEND

class BasicSoftwareSuperObject(BasicSoftwareLinkedObject):
    
    def __init__(self, Type="", logMessage="", TxtTwo="", TxtTwo2="", TxtThree="",
                 TxtThree2="", ccbThree="", statement="", instruction="", unitTestInst='self',
                 dataFormat='\\1{0}={1}\\1', pollTimeout=0.0, timeout=5.0, name="", path="",
                 logFilesList='', fieldsToCheck='', fieldsToExclude="", function="",
                 pattern="", objectType=''):
        if objectType == OGL_FIXLOG:
            name='fix_logs'
        elif objectType == OGL_TITLEEND:
            name = 'dump name'
        BasicSoftwareLinkedObject.__init__(self, name)
        
        self._Type = Type
        self._logMessage = logMessage
        self._function = function
        self.TxtTwo = TxtTwo
        self.TxtTwo2 = TxtTwo2
        self.TxtThree = TxtThree
        self.TxtThree2= TxtThree2
        self.ccbThree = ccbThree
        self.statemenent = statement
        self.instruction = instruction
        self._pollTimeout = pollTimeout
        self._timeout = timeout
        self._dataformat = dataFormat
        self._unitTestInst = unitTestInst
        self._logFilesList = logFilesList
        self._fieldsToCheck = fieldsToCheck
        self._fieldsToExclude = fieldsToExclude
        self._pattern = pattern
        self._path = path
        self._objectType = objectType
            
    def setPath(self, param):
        self._path = param
    
    def getPath(self):
        return self._path
    
    def setType(self, value):
        self._Type = value
        
    def getType(self):
        return self._Type
    
    def getInstanceTitleType(self):
        return self._objectType
    
    def setInstanceTitleType(self, value):
        self._objectType = value
        
    def getLogMessage(self):
        return self._logMessage
    
    def setLogMessage(self, value):
        self._logMessage = value
        
    def getFunction(self):
        return self._function
    
    def setFunction(self, value):
        self._function = value
        
    def getTxtTwo(self):
        return self.TxtTwo
    
    def setTxtTwo(self, value):
        self.TxtTwo = value
        
    def getTxtTwo2(self):
        return self.TxtTwo2
    
    def setTxtTwo2(self, value):
        self.TxtTwo2 = value
        
    def getTxtThree(self):
        return self.TxtThree
    
    def setTxtThree(self, value):
        return self.TxtThree
    
    def getTxtThree2(self):
        return self.TxtThree2
    
    def setTxtThree2(self, value):
        self.TxtThree2 = value
        
    def getccbThree(self):
        return self.ccbThree
    
    def setccbThree(self, value):
        self.ccbThree = value
        
    def getStatement(self):
        return self.statemenent
    
    def setStatement(self, value):
        self.statemenent = value
        
    def getInstruction(self):
        return self.instruction
    
    def setInstruction(self, value):
        self.instruction = value
    
    def getPollTimeout(self):
        return self._pollTimeout
    
    def setPollTimeout(self, value):
        self._pollTimeout = value
        
    def getTimeout(self):
        return self._timeout
    
    def setTimeout(self, value):
        self._timeout = value
        
    def getDataFormat(self):
        return self._dataformat
    
    def setDataFormat(self, value):
        self._dataformat = value

    def getUnitTestInst(self):
        return self._unitTestInst

    def setUnitTestInst(self, value):
        self._unitTestInst = value
    
    def getLogFilesList(self):
        return self._logFilesList
    
    def setLogFilesList(self, value):
        self._logFilesList = value
    
    def getFieldsToExclude(self):
        return self._fieldsToExclude
    
    def setFieldsToExclude(self, value):
        self._fieldsToExclude = value
        
    def getFieldsToCheck(self):
        return self._fieldsToCheck
    
    def setFieldsToCheck(self, value):
        self._fieldsToCheck = value
        
    def getPattern(self):
        return self._pattern
    
    def setPattern(self, value):
        self._pattern = value