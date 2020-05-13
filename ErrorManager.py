# -*- coding: utf-8 -*-
from singleton import Singleton
import wx

[GRAPHIC_ERROR_VIEW, TEXT_ERROR_VIEW, RAISE_ERROR_VIEW] = range(1,4)

def getErrorManager():
    """
    Get the error manager
    """
    return ErrorManager()


class GraphicErrorView:
    """
    This class is an error view which will display error as
    wx message dialogs.

    To use it, use the mediator methods :
     - mediator = Mediator.getMediator()
     - mediator.registerErrorManager(GraphicErrorManager())
     - ...
     - errorManager = mediator.getErrorManager()
     - errorManager.newFatalError("This is a message", "...")
     - errorManager.newWarning("This is a message", "...")
     - errorManager.newInformation("This is a message", "...")
     - ...
    """

    #>------------------------------------------------------------------------

    def newFatalError(self, msg, title=None, parent=None):
        import sys, traceback
        if title is None:
            title=("An error occured...")
        errMsg = msg + "\n\n"
        errMsg +=("The following error occured : %s") % str(sys.exc_info()[1])
        errMsg += "\n\n---------------------------\n"
        if sys.exc_info()[0] is not None:
            errMsg += "Error : %s" % sys.exc_info()[0] + "\n"
        if sys.exc_info()[1] is not None:
            errMsg += "Msg   : %s" % sys.exc_info()[1] + "\n"
        if sys.exc_info()[2] is not None:
            errMsg += "Trace :\n"
            for el in traceback.extract_tb(sys.exc_info()[2]): 
                errMsg = errMsg + str(el) + "\n"

        print(errMsg)
        try:
            dlg=wx.MessageBox(errMsg,  title, wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            dlg = None
        except:
            pass

    #>------------------------------------------------------------------------

    def newWarning(self, msg, title=None, parent=None):
        if title is None:
            title=("WARNING...")
        print(msg)
        try:
            dlg = wx.MessageBox(msg, title, wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            dlg = None
        except:
            pass

    #>------------------------------------------------------------------------

    def newInformation(self, msg, title=None, parent=None):
        if title is None:
            title=("WARNING...")
        print(msg)
        try:
            dlg = wx.MessageBox(parent, msg, title, wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            dlg = None
        except:
            pass

class TextErrorView:
    """
    This class is an error view which will display error as
    text message box.

    To use it, use the mediator methods :
     - mediator = Mediator.getMediator()
     - mediator.registerErrorManager(GraphicErrorManager())
     - ...
     - errorManager = mediator.getErrorManager()
     - errorManager.newFatalError("This is a message", "...")
     - errorManager.newWarning("This is a message", "...")
     - errorManager.newInformation("This is a message", "...")
     - ...
    """

    #>------------------------------------------------------------------------

    def newFatalError(self, msg, title=None, parent=None):
        import sys, traceback
        if title is None:
            title=("An error occured...")
        errMsg = msg + "\n\n" + \
                  ("The following error occured : %s") %sys.exc_info()[1] + \
                 "\n\n---------------------------\n"
        if sys.exc_info()[0] is not None:
            errMsg += "Error : %s" % sys.exc_info()[0] + "\n"
        if sys.exc_info()[1] is not None:
            errMsg += "Msg   : %s" % sys.exc_info()[1] + "\n"
        if sys.exc_info()[2] is not None:
            errMsg += "Trace :\n"
            for el in traceback.extract_tb(sys.exc_info()[2]): 
                errMsg = errMsg + str(el) + "\n"

        print("FATAL ERROR : ", errMsg)

    #>------------------------------------------------------------------------

    def newWarning(self, msg, title=None, parent=None):
        print("WARNING : ", title, " - ", msg)

    #>------------------------------------------------------------------------

    def displayInformation(self, msg, title=None, parent=None):
        print("INFORMATION : ", title , " - ", msg)
        
class RaiseErrorView:
    """
    This class is an error view which will raise all errors as
    text message box.

    To use it, use the mediator methods :
     - mediator = Mediator.getMediator()
     - mediator.registerErrorManager(GraphicErrorManager())
     - ...
     - errorManager = mediator.getErrorManager()
     - errorManager.newFatalError("This is a message", "...")
     - errorManager.newWarning("This is a message", "...")
     - errorManager.newInformation("This is a message", "...")
     - ...

    """

    #>------------------------------------------------------------------------

    def newFatalError(self, msg, title=None, parent=None):
        raise "FATAL ERROR : "+ title+ " - "+ msg

    #>------------------------------------------------------------------------

    def newWarning(self, msg, title=None, parent=None):
        raise "WARNING : "+ title+ " - "+ msg

    #>------------------------------------------------------------------------

    def displayInformation(self, msg, title=None, parent=None):
        raise "INFORMATION : "+ title + " - "+ msg
        
def addToLogFile(title, msg):
    import time, codecs, sys, traceback
    title = u"" + title
    msg = u"" + msg
    with codecs.open('errors.log', encoding='utf-8', mode='a') as f:
        f.write("===========================")
        f.write(str(time.ctime(time.time())))
        errMsg = msg + "\n\n" + \
                  ("The following error occured : %s") %sys.exc_info()[1] + \
                 "\n\n---------------------------\n"
        if sys.exc_info()[0] is not None:
            errMsg += "Error : %s" % sys.exc_info()[0] + "\n"
        if sys.exc_info()[1] is not None:
            errMsg += "Msg   : %s" % sys.exc_info()[1] + "\n"
        if sys.exc_info()[2] is not None:
            errMsg += "Trace :\n"
            for el in traceback.extract_tb(sys.exc_info()[2]): 
                errMsg = errMsg + str(el) + "\n"
        f.write(title + u": " + msg)
        f.write(errMsg)

class ErrorManager(Singleton):
    """
    This class handle all errors.
    """

    #>------------------------------------------------------------------------

    def init(self, view = GRAPHIC_ERROR_VIEW):
        """
        Singleton constructor
        """
        self.changeType(view)

    #>------------------------------------------------------------------------

    def changeType(self, view):
        if view == GRAPHIC_ERROR_VIEW:
            self._view = GraphicErrorView()
        elif view == TEXT_ERROR_VIEW:
            self._view = TextErrorView()
        elif view == RAISE_ERROR_VIEW:
            self._view = RaiseErrorView()
        else:
            self._view = GraphicErrorView()
    
    #>------------------------------------------------------------------------

    def newFatalError(self, msg, title=None, parent=None):
        if msg is None:
            msg = u""
        if title is None:
            title = u""
        title = u"" + title
        msg = u"" + msg
        addToLogFile("Fatal error : " + title, msg)
        self._view.newFatalError(msg, title, parent)

    #>------------------------------------------------------------------------

    def newWarning(self, msg, title=None, parent=None):
        title = u"" + title
        msg = u"" + msg
        addToLogFile("Warning : " + title, msg)
        self._view.newWarning(msg, title, parent)

    #>------------------------------------------------------------------------

    def displayInformation(self, msg, title=None, parent=None):
        title = u"" + title
        msg = u"" + msg
        addToLogFile("Info : " + title, msg)
        self._view.displayInformation(msg, title, parent)  