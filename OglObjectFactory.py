# -*- coding: utf-8 -*-

from OglNote import OglNote
from OglTitle import OglTitle
from OglTitleEnd import OglTitleEnd
from OglStatement import OglStatement
from OglLog import OglLog
from OglFixLog import OglFixLog
from OglFor import OglFor
from OglWhile import OglWhile
from OglImport import OglImport

from singleton import Singleton
from BasicSoftwareConst import OGL_NOTE, OGL_TITLE, OGL_TITLEEND, OGL_STATEMENT, OGL_LOG, OGL_FIXLOG, OGL_FOR, OGL_WHILE, OGL_IMPORT, OBJECT_NAME
from BasicSoftwareUtils import displayWarning, displayError

def getOglObjectFactory():
    return OglObjectFactory()

def getObjectType(Object):
    if isinstance(Object, OglNote):
        return OGL_NOTE
    elif isinstance(Object, OglTitle):
        return OGL_TITLE
    elif isinstance(Object, OglTitleEnd):
        return OGL_TITLEEND
    elif isinstance(Object, OglStatement):
        return OGL_STATEMENT
    elif isinstance(Object, OglLog):
        return OGL_LOG
    elif isinstance(Object, OglFixLog):
        return OGL_FIXLOG
    elif isinstance(Object, OglFor):
        return OGL_FOR
    elif isinstance(Object, OglWhile):
        return OGL_WHILE
    elif isinstance(Object, OglImport):
        return OGL_IMPORT
    else:
        displayWarning("Unknown ObjectType of OglObject into factory", "OglObjectFactory.getLinkType Error")
        return None

def getName(BasicSoftwareSuperObject):
    if BasicSoftwareSuperObject.getType() in [OGL_NOTE, OGL_TITLE, OGL_TITLEEND, OGL_STATEMENT, OGL_LOG, OGL_FIXLOG, OGL_FOR, OGL_WHILE, OGL_IMPORT]:
        return OBJECT_NAME[BasicSoftwareSuperObject.getType()]
    else:
        displayError("Unknown BasicSoftwareSuperObject", "OglObjectFactory.getName Error")

class OglObjectFactory(Singleton):
    def getOglObject(self, basicSoftwareObject, Type, w=None, h=None):
        if not w and not h:
            basicSoftwareObject.setType(Type)
            if Type == OGL_NOTE:
                return OglNote(basicSoftwareObject, w, h)
            elif Type == OGL_TITLE:
                return OglTitle(basicSoftwareObject, w, h)
            elif Type == OGL_TITLEEND:
                return OglTitleEnd(basicSoftwareObject, w, h)
            elif Type == OGL_LOG:
                return OglLog(basicSoftwareObject, w, h)
            elif Type == OGL_FIXLOG:
                return OglFixLog(basicSoftwareObject, w, h)
            elif Type == OGL_FOR:
                return OglFor(basicSoftwareObject, w, h)
            elif Type == OGL_WHILE:
                return OglWhile(basicSoftwareObject, w, h)
            elif Type == OGL_IMPORT:
                return OglImport(basicSoftwareObject, w, h)
            elif Type == OGL_STATEMENT:
                return OglStatement(basicSoftwareObject, w, h)
            else:
                displayWarning("Unknown type of OglObject into factory : %s" %Type, "getOglObject Error")
                return None
        else:
            basicSoftwareObject.setType(Type)
            if Type == OGL_NOTE:
                return OglNote(basicSoftwareObject)
            elif Type == OGL_TITLE:
                return OglTitle(basicSoftwareObject)
            elif Type == OGL_TITLEEND:
                return OglTitleEnd(basicSoftwareObject)
            elif Type == OGL_LOG:
                return OglLog(basicSoftwareObject)
            elif Type == OGL_FIXLOG:
                return OglFixLog(basicSoftwareObject)
            elif Type == OGL_FOR:
                return OglFor(basicSoftwareObject)
            elif Type == OGL_WHILE:
                return OglWhile(basicSoftwareObject)
            elif Type == OGL_IMPORT:
                return OglImport(basicSoftwareObject)
            elif Type == OGL_STATEMENT:
                return OglStatement(basicSoftwareObject, w, h)
            else:
                displayWarning("Unknown type of OglObject into factory : %s" %repr(Type), "getOglObject Error")
                return None            