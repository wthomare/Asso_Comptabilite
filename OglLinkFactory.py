# -*- coding: utf-8 -*-

from OglCreateOrder import OglCreateOrder
from OglNoteLink import OglNoteLink
from OglExpectedState import OglExpectedState
from OglModify import OglModify
from OglCancel import OglCancel
from OglTry    import OglTry
from OglProcess import OglProcess

from singleton import Singleton
from BasicSoftwareConst import OGL_INTERFACE, OGL_NOTELINK, OGL_EXPECTED_STATE, OGL_MODIFY, OGL_CANCEL, OGL_TRY, OGL_PROCESS
from BasicSoftwareUtils import displayWarning

def getOglLinkFactory():
    return OglLinkFactory()


def getLinkType(link):
   if isinstance(link, OglNoteLink):
       return OGL_NOTELINK
   elif isinstance(link, OglCreateOrder):
       return OGL_INTERFACE
   elif isinstance(link, OglExpectedState):
       return OGL_EXPECTED_STATE
   elif isinstance(link, OglModify):
       return OGL_MODIFY
   elif isinstance(link, OglCancel):
       return OGL_CANCEL
   elif isinstance(link, OglTry):
       return OGL_TRY
   elif isinstance(link, OglProcess):
       return OGL_PROCESS
   
   else:
        displayWarning("[%s] unknow type of link"%(type(link)),"getlinkType error")
        return None
    
class OglLinkFactory(Singleton):
    def getOglLink(self, srcShape, basicSoftwareLink, dstShape, linkType, srcPos=None, dstPos=None):
        if linkType == OGL_INTERFACE:
            return OglCreateOrder(srcPos=srcPos, basicSoftwareLink=basicSoftwareLink, dstPos=dstPos, srcShape=srcShape, dstShape=dstShape)
        elif linkType == OGL_NOTELINK:
            return OglNoteLink(basicSoftwareLink=basicSoftwareLink, srcShape=srcShape, dstShape=dstShape)
        elif linkType == OGL_EXPECTED_STATE:
            return OglExpectedState(srcPos=srcPos, basicSoftwareLink=basicSoftwareLink, dstPos=dstPos, srcShape=srcShape, dstShape=dstShape)
        elif linkType == OGL_MODIFY:
            return OglModify(srcPos=srcPos, basicSoftwareLink=basicSoftwareLink, dstPos=dstPos, srcShape=srcShape, dstShape=dstShape)
        elif linkType == OGL_CANCEL:
            return OglCancel(srcPos=srcPos, basicSoftwareLink=basicSoftwareLink, dstPos=dstPos, srcShape=srcShape, dstShape=dstShape)
        elif linkType == OGL_TRY:
            return OglTry(srcPos=srcPos, basicSoftwareLink=basicSoftwareLink, dstPos=dstPos, srcShape=srcShape, dstShape=dstShape)
        elif linkType == OGL_PROCESS:
            return OglProcess(srcPos=srcPos, basicSoftwareLink=basicSoftwareLink, dstPos=dstPos, srcShape=srcShape, dstShape=dstShape)
        else:
            displayWarning("Unknown linkType of OglLink :", repr(linkType), "OglLinkFactory.getOglLink Error")
            return None