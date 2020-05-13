# -*- coding: utf-8 -*-

import wx, os
import pandas as pd

import ErrorManager
import mediatorParameter

from singleton                import Singleton
from MiniOgl                  import Constants
from MiniOgl.ControlPoint     import ControlPoint
from MiniOgl.LinePoint        import LinePoint


import BasicSoftwareUtils
from BasicSoftwareConst      import OBJECT_NAME

from basicSoftwareXML.main import BasicSoftwareXML

from DlgEditNote import DlgEditNote
from DlgEditTitle import DlgEditTitle
from DlgEditFOR import DlgEditFOR
from DlgEditWHILE import DlgEditWHILE
from DlgEditLink import DlgEditLink
from DlgEditState import DlgEditState
#from DlgInstance import DlgInstance
from DlgEditStatement import DlgEditStatement
from DlgEditModify import DlgEditModify
from DlgEditCancel import DlgEditCancel
from DlgEditTry import DlgEditTry
from DlgEditFixInit import DlgEditFixInit
from DlgEditFixStart import DlgEditFixStart
from DlgEditFixSetup import DlgEditFixSetup
from DlgEditFixFlush import DlgEditFixFlush
from DlgEditFixExpect import DlgEditFixExpect
from DlgEditFixAdd import DlgEditFixAdd
from DlgEditFixRemove import DlgEditFixRemove
from DlgEditFixWait import DlgEditFixWait
from DlgEditLog import DlgEditLog
from DlgEditProcess import DlgEditProcess

def get_mediator():
    return Mediator()

__BasicSoftwareVersion__ = 1

class Mediator(Singleton):
    """
    This class is the link between the parts of the GUI of pyut. It receives
    commands from the modules, and dispatch them to the right receiver.
    See the Model-View-Controller pattern and the Mediator pattern.
    There's just one instance of it, and it's global. You get the only
    instance by instanciating it. See the `singleton.py` file for more
    information about this.

    Each part of the GUI must register itself to the mediator. This is done
    with the various `register...` methods.

    The mediator contains a state machine. The different states are
    represented by integer constants, declared at the beginning of the
    `mediator.py` file. These are the `ACTION_*` constants.

    The `NEXT_ACTION` dictionary gives the next action based on the given
    one. For example, after an `ACTION_NEW_NOTE_LINK`, you get an
    `ACTION_DEST_NOTE_LINK` this way::
        
        nextAction = NEXT_ACTION[ACTION_NEW_NOTE_LINK]

    The state is kept in `self._currentAction`.

    The `doAction` is called whenever a click is received by the uml diagram
    frame.

    """
    # ------------------------------------------------------------------------- 
    def init(self):
        self._errorManager = ErrorManager.getErrorManager()
        self._currentAction = mediatorParameter.ACTION_SELECTOR
        self._currentActionPersistent = False

        self._toolBar  = None # toolbar
        self._tools    = None # toolbar tools
        self._status   = None # application status bar
        self._src      = None # source of a two-objects action
        self._dst      = None # destination of a two-objects action
        self._appFrame = None # Application's main frame
        self._appPath  = None # Application files' path
        self._toolboxOwner = None # toolbox owner, created when appframe is passed
        self._fileHandling = None # File Handler
    
        self._modifyCommand = None  # command for undo/redo a modification on a shape.
        
    # ------------------------------------------------------------------------- 
    def getErrorManager(self):
        return self._errorManager
        
    # ------------------------------------------------------------------------- 
    def registerFileHandling(self, fh):
        self._fileHandling = fh
        
    # ------------------------------------------------------------------------- 
    def registerAppPath(self, path):
        self._appPath = path
        
    # ------------------------------------------------------------------------- 
    def getAppPath(self):
        return self._appPath
    
    # ------------------------------------------------------------------------- 
    def notifyTitleChanged(self):
        if not self._appFrame is None:
            self._appFrame.notifyTitleChanged()
            
    # ------------------------------------------------------------------------- 
    def registerAppFrame(self, appFrame):
        self._appFrame=appFrame
    
    # ------------------------------------------------------------------------- 
    def getAppFrame(self):
        return self._appFrame

    # ------------------------------------------------------------------------- 
    def registerToolBar(self, tb):
        self._toolBar = tb

    # ------------------------------------------------------------------------- 
    def registerToolBarTools(self, tools):
        self._tools = tools
        
    # ------------------------------------------------------------------------- 
    def registerStatusBar(self, statusBar):
        self._status = statusBar
        
    # ------------------------------------------------------------------------- 
    def setCurrentAction(self, action):
        """
        Set the new current atction.
        This tells the mediator which action to do for the next doAction call.
        @param int action : the action from ACTION constants
        """
        if self._currentAction==action:
            self._currentActionPersistent = True
        else:
            self._currentAction = action
            self._currentActionPersistent = False
    
    # ------------------------------------------------------------------------- 
    def doAction(self, x, y):
        """
        Do the current action at coordinate x, y. Pass through history manager
        to allow the undo/redo event. 
        @param int x : x coord where the action must take place
        @param int y : y coord where the action must take place

        """        
        
        SuperObject = [mediatorParameter.ACTION_NEW_IMPORTATION, 
                       mediatorParameter.ACTION_SELECTOR,
                       mediatorParameter.ACTION_NEW_STATEMENT,
                       mediatorParameter.ACTION_NEW_NOTE,
                       mediatorParameter.ACTION_NEW_TITLE,
                       mediatorParameter.ACTION_END_TITLE,
                       mediatorParameter.ACTION_NEW_FOR,
                       mediatorParameter.ACTION_NEW_WHILE,
                       mediatorParameter.ACTION_NEW_IMPORTATION]
        umlFrame = self._fileHandling.getCurrentFrame()
        if not umlFrame: return
        
        from commandGroup import CommandGroup
        if self._currentAction == mediatorParameter.ACTION_SELECTOR:
            return Constants.SKIP_EVENT
        
        elif self._currentAction in SuperObject:
            from createOglObjectCommand import CreateOglObjectCommand
            if self._currentAction in mediatorParameter.df_LOG.columns:
                function = mediatorParameter.df_LOG[self._currentAction].iloc[0]
            elif self._currentAction in mediatorParameter.df_FIXLOG.columns:
                function = mediatorParameter.df_FIXLOG[self._currentAction].iloc[0]
            elif self._currentAction == mediatorParameter.ACTION_NEW_WHILE:
                function = "WHILE"
            elif self._currentAction == mediatorParameter.ACTION_NEW_FOR:
                function = "FOR"
            else:
                function = ""
            cmd = CreateOglObjectCommand(x=x, y=y, forExecute = True, Type=mediatorParameter.OBJECT_LINK[self._currentAction], function = function)
            if cmd.dlg_state in {wx.ID_ANY, 404}:
                cmdGroup = CommandGroup("Create %s" %(OBJECT_NAME[mediatorParameter[self._currentAction]]))
                cmdGroup.addCommand(cmd)
                umlFrame.getHistory().addCommandGroup(cmdGroup)
            self._currentAction = mediatorParameter.ACTION_SELECTOR
            
        elif self._currentAction == mediatorParameter.ACTION_NEW_SD_INSTANCE:
            from createOglSDInstanceCommand import CreateOglSDInstanceCommand
            cmd = CreateOglSDInstanceCommand(x, y, True)
            if cmd.dlg_state in {wx.ID_ANY, 404}:
                cmdGroup = CommandGroup("Create SDInstance")
                cmdGroup.addGroup(cmd)
                umlFrame.getHistory().addCommandGroup(cmdGroup)
            self._currentAction = mediatorParameter.ACTION_SELECTOR
        elif self._currentAction == mediatorParameter.ACTION_ZOOM_IN:
            return Constants.SKIP_EVENT
        elif self._currentAction == mediatorParameter.ACTION_ZOOM_OUT:
            umlFrame.DoZoomOut(x, y)
            umlFrame.Refresh()
            self.updateTitle()
        else:
            return Constants.SKIP_EVENT
        return Constants.EVENT_PROCESSED
        
    # ------------------------------------------------------------------------- 
    def shapeSelected(self, shape, position=True):
        """
        Do action when a shape is selected
        """
        
        umlFrame = self._fileHandling.getCurrentFrame()
        if not umlFrame : return
        
        if self._currentAction in mediatorParameter.SOURCE_ACTIONS:
            
            self._oldAction = self._currentAction
            self._currentAction = mediatorParameter.NEXT_ACTIONS[self._currentAction]
            
            if not shape:
                BasicSoftwareUtils.displayError('Action cancelled \nno source')
                self._currentAction = mediatorParameter.ACTION_SELECTOR
            else:
                self._src = shape
                self.srcPos = position
                
        elif self._currentAction in mediatorParameter.DEST_ACTIONS:
            self._dst = shape
            self._dstPos = position
            if not self._dst:
                BasicSoftwareUtils.displayError('Action cancelled \nno destination', 'mediator.doAction')
                self._currentAction = mediatorParameter.ACTION_SELECTOR
                return
            
            from createOglLinkCommand import CreateOglLinkCommand
            from commandGroup import CommandGroup
            print("test createLink call")
            cmd = CreateOglLinkCommand(self._src, self._dst, True, mediatorParameter.LINK_TYPE[self._currentAction])
            
            if cmd.dlg_state in {wx.ID_ANY, 404}:
                cmdGroup = CommandGroup("Create link")
                cmdGroup.addCommand(cmd)
                umlFrame.getHistory().addCommandGroup(cmdGroup)
                
            if cmd._expected_shapes:
                try:
                    from createOglLinkCommand import CreateOglLinkCommand
                    cmd_expected = CreateOglLinkCommand(self._src, self._dst, True, mediatorParameter.LINK_TYPE[mediatorParameter.ACTION_AUTO_EXPECTED])
                    df = pd.read_csv(os.path.join(os.getcwd(), 'current_expected_link.csv'))
                    state, relation = df['state'].iloc[0], df['relation'].iloc[0]
                    cmd_expected._shape.getBasicSoftwareObject().setRelationship(relation)
                    cmd_expected._shape.getBasicSoftwareObject().setName('Expected %s' %(state))
                    os.remove(os.path.join(os.getcwd(), 'current_expected_link.csv'))
                    
                    cmdGroup = CommandGroup("Create link")
                    cmdGroup.addCommand(cmd_expected)
                    umlFrame.getHistory().addCommandGroup(cmdGroup)
                    umlFrame.Refresh()
                except:
                    msg = "Failed to create link or to register it in the history manager"
                    BasicSoftwareUtils.displayError(msg, 'mediator.shapeSelected error')
                    
            self._src, self._dst = None, None
            
            if self._currentActionPersitent:
                self._currentAction = self._oldAction
                del self._oldAction
            else:
                self._currentAction = mediatorParameter.ACTION_SELECTOR
            return


    # ------------------------------------------------------------------------- 
    def actionWaiting(self):
        """
        Return True if there's an action waiting to be completed.

        """
        return self._currentAction != mediatorParameter.ACTION_SELECTOR                
                
    # ------------------------------------------------------------------------- 
    def editObject(self, x, y):
        """
        Edit the object at x, y.

        """           
                
        umlFrame = self._fileHandling.getCurrentFrame()
        if not umlFrame: return

        from OglNote import OglNote
        from OglTitle import OglTitle
        from OglFor import OglFor
        from OglWhile import OglWhile
        from OglCreateOrder import OglCreateOrder
        from OglExpectedState import OglExpectedState
        from OglStatement import OglStatement
        from OglModify import OglModify
        from OglCancel import OglCancel
        from OglTry import OglTry
        from OglFixLog import OglFixLog
        from OglImport import OglImport
        from OglLog import OglLog
        from OglSDInstance import OglSDInstance, OglInstanceRectangleShape, OglInstanceName
        from OglProcess import OglProcess
        from OglNoteLink import OglNoteLink
        from OglTitleEnd import OglTitleEnd
        from MiniOgl.SizerShape import SizerShape
        
        Object = umlFrame.FindShape(x, y)
        if not Object: return
        rep = None
        
        if isinstance(Object, (OglInstanceRectangleShape)):
            BasicSoftwareObject = Object.basicSoftwareObject()
        else:
            BasicSoftwareObject = Object.getBasicSoftwareObject()
            
        if isinstance(Object, OglNote):
            dlg = DlgEditNote(umlFrame, wx.ID_ANY, BasicSoftwareObject)
            rep = dlg.getReturnAction()
            if rep == wx.ID_NO:
                Object.Detach()
        elif isinstance(Object, OglTitle):
            dlg = DlgEditTitle(umlFrame, wx.ID_ANY, BasicSoftwareObject)
            rep = dlg.getReturnAction()
            if rep == wx.ID_NO:
                Object.Detach()           
        elif isinstance(Object, OglFor):
            dlg = DlgEditFOR(umlFrame, wx.ID_ANY, BasicSoftwareObject)
            rep = dlg.getReturnAction()
            if rep == wx.ID_NO:
                Object.Detach()              
        elif isinstance(Object, OglWhile):
            dlg = DlgEditWHILE(umlFrame, wx.ID_ANY, BasicSoftwareObject)
            rep = dlg.getReturnAction()
            if rep == wx.ID_NO:
                Object.Detach()              
        elif isinstance(Object, OglExpectedState):
            dlg = DlgEditState(umlFrame, wx.ID_ANY, BasicSoftwareObject)
            dlg.ShowModal()
            rep = dlg.getReturnAction()
            if rep == wx.ID_NO:
                Object.Detach()
        elif isinstance(Object, OglProcess):
            dlg = DlgEditProcess(umlFrame, wx.ID_ANY, BasicSoftwareObject)
            dlg.ShowModal()
            rep = dlg.getReturnAction()
            if rep == wx.ID_NO:
                Object.Detach()   
        elif isinstance(Object, OglCreateOrder):
            dlg = DlgEditLink(umlFrame, wx.ID_ANY, BasicSoftwareObject)
            dlg.ShowModal()
            rep = dlg.getReturnAction()
            if rep == wx.ID_NO:
                Object.Detach()                 
        elif isinstance(Object, OglStatement):
            dlg = DlgEditStatement(umlFrame, wx.ID_ANY, BasicSoftwareObject)
            rep = dlg.getReturnAction()
            if rep == wx.ID_NO:
                Object.Detach()                 
        elif isinstance(Object, OglModify):
            dlg = DlgEditModify(umlFrame, wx.ID_ANY, BasicSoftwareObject)
            dlg.ShowModal()
            rep = dlg.getReturnAction()
            if rep == wx.ID_NO:
                Object.Detach()
        elif isinstance(Object, OglCancel):
            dlg = DlgEditCancel(umlFrame, wx.ID_ANY, BasicSoftwareObject)
            dlg.ShowModal()
            rep = dlg.getReturnAction()
            if rep == wx.ID_NO:
                Object.Detach()    
        elif isinstance(Object, OglTry):
            dlg = DlgEditTry(umlFrame, wx.ID_ANY, BasicSoftwareObject)
            dlg.ShowModal()
            rep = dlg.getReturnAction()
            if rep == -1:
                Object.Detach()    
        elif isinstance(Object, OglFixLog):
            function = BasicSoftwareObject.getFunction()
            if function == 'Init':
                dlg = DlgEditFixInit(umlFrame, wx.ID_ANY, BasicSoftwareObject)
                rep = dlg.getReturnAction()
                dlg.Destroy()
                if rep == wx.ID_NO:
                    Object.Detach()
            elif function == 'Start':
                dlg = DlgEditFixStart(umlFrame, wx.ID_ANY, BasicSoftwareObject)
                rep = dlg.getReturnAction()
                dlg.Destroy()
                if rep == wx.ID_NO:
                    Object.Detach()            
            elif function == 'Setup':
                dlg = DlgEditFixSetup(umlFrame, wx.ID_ANY, BasicSoftwareObject)
                rep = dlg.getReturnAction()
                dlg.Destroy()
                if rep == wx.ID_NO:
                    Object.Detach()   
            elif function == 'Stop':
                pass
            elif function == 'Flush':
                dlg = DlgEditFixFlush(umlFrame, wx.ID_ANY, BasicSoftwareObject)
                rep = dlg.getReturnAction()
                dlg.Destroy()
                if rep == wx.ID_NO:
                    Object.Detach()           
            elif function == 'Expect':
                dlg = DlgEditFixExpect(umlFrame, wx.ID_ANY, BasicSoftwareObject)
                dlg.Destroy()
            elif function == 'Add':
                dlg = DlgEditFixAdd(umlFrame, wx.ID_ANY, BasicSoftwareObject)
                rep = dlg.getReturnAction()
                dlg.Destroy()
                if rep == wx.ID_NO:
                    Object.Detach()                       
            elif function == 'Remove':
                dlg = DlgEditFixRemove(umlFrame, wx.ID_ANY, BasicSoftwareObject)
                rep = dlg.getReturnAction()
                dlg.Destroy()
                if rep == wx.ID_NO:
                    Object.Detach()   
            elif function == 'Wait':
                dlg = DlgEditFixWait(umlFrame, wx.ID_ANY, BasicSoftwareObject)
                rep = dlg.getReturnAction()
                dlg.Destroy()
                if rep == wx.ID_NO:
                    Object.Detach()
            else:
                BasicSoftwareUtils.displayError('Not a fixlog function', 'Edit Object warning')
        elif isinstance(Object, OglLog):
            dlg = DlgEditLog(umlFrame, wx.ID_ANY, BasicSoftwareObject)
            rep = dlg.getReturnAction()
            if rep == wx.ID_NO:
                Object.Detach()               
        elif isinstance(Object, OglImport):
            xml_path = BasicSoftwareObject.getPath()
            app = wx.App(redirect=False)
            BasicSoftwareXML(default_xml_path=xml_path)
            app.MainLoop()
        elif isinstance(Object, OglSDInstance):
            #dlg = DlgInstance(umlFrame, wx.ID_ANY, BasicSoftwareObject)
            #dlg.ShowModal()
            #rep = dlg.getReturnAction()
            #if rep == wx.ID_NO:
            #    Object.Detach()
            pass
        elif isinstance(Object, (OglInstanceRectangleShape, OglInstanceName)):
            #dlg = DlgInstance(umlFrame, wx.ID_ANY, BasicSoftwareObject)
            #dlg.ShowModal()
            #rep = dlg.getReturnAction()
            #if rep == wx.ID_NO:
            #    parentObject = self.getOglSDInstance(BasicSoftwareSDInstance = BasicSoftwareObject)
            #    parentObject.Detach()
            pass
        elif isinstance(Object, (OglNoteLink, OglTitleEnd, SizerShape)):
            rep=-1
        else:
            BasicSoftwareUtils.displayWarning('[%s] is an unknow Ogl Object' %Object, 'Edit Object Error')
        
        self.upDateHistoryManager(Object, rep)
        umlFrame.Refresh()
        
        
    # ------------------------------------------------------------------------- 
    def getUmlObjects(self):
        """
        Return the list of UmlObjects in the diagram.

        """
        if self._fileHandling is None:
            return []
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame:
            return umlFrame.getUmlObjects()
        else: 
            return []

    # ------------------------------------------------------------------------- 
    def getSelectedShapes(self):
        """
        Return the list of selected OglObjects in the diagram.
        """
        umlObjects = self.getUmlObjects()
        if umlObjects:
            return [obj for obj in self.getUmlObjects() if obj.IsSelected()]
        else:
            return []

    # ------------------------------------------------------------------------- 
    def getDiagram(self):
        """
        Return the uml diagram.

        """
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None:
            return None
        return umlFrame.getDiagram()
    
    
    # ------------------------------------------------------------------------- 
    def getUmlFrame(self):
        """
        Return the active uml frame.
        """
        return self._fileHandling.getCurrentFrame()
    
    # ------------------------------------------------------------------------- 
    def deselectAllShapes(self):
        """
        Deselect all shapes in the diagram.
        """
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame:
            shapes = umlFrame.GetDiagram().GetShapes()
            for shape in shapes:
                shape.SetSelected(False)
            umlFrame.Refresh()
            
            
    # ------------------------------------------------------------------------- 
    def getCurrentDir(self):
        """
        Return the application's current directory

        @return String : application's current directory
        """
        return self._appFrame.getCurrentDir()


    # ------------------------------------------------------------------------- 
    def setCurrentDir(self, directory):
        """
        Set the application's current directory

        @param String directory : New appliation's current directory
        """
        return self._appFrame.updateCurrentDir(directory)

    # ------------------------------------------------------------------------- 
    def processChar(self, event):
        """
        Process keyboard events
        """

        c = event.GetKeyCode()
        func = {wx.WXK_DELETE : self.deleteSelectedShape,
                wx.WXK_INSERT : self.insertSelectedShape,
                ord('i')      : self.insertSelectedShape,
                ord('I')      : self.insertSelectedShape,
                ord('Ļ')      : self.moveOglObjUp,
                ord('Ľ')      : self.moveOglObjectDown,
                ord('ĺ')      : self.moveOglObjectLeft,
                ord('ļ')      : self.moveOglObjectRigth
                }
        
        if c in func:
            func(c)()
        else:
            BasicSoftwareUtils.displayWarning("Not Supported : [%s]"%c, 'mediator.processChar error')
            event.Skip()
            
    # ------------------------------------------------------------------------- 
    def moveOglObjectUp(self):
        umlFrame = self._fileHandling.getCurrentFrame()
        if not umlFrame: return
        
        self.moveOglObject(umlFrame, 'North')
        
    # ------------------------------------------------------------------------- 
    def moveOglObjectDown(self):
        umlFrame = self._fileHandling.getCurrentFrame()
        if not umlFrame: return
        
        self.moveOglObject(umlFrame, 'South')        
        
    # ------------------------------------------------------------------------- 
    def moveOglObjectLeft(self):
        umlFrame = self._fileHandling.getCurrentFrame()
        if not umlFrame: return
        
        self.moveOglObject(umlFrame, 'West')  
        
    # ------------------------------------------------------------------------- 
    def moveOglObjectRigth(self):
        umlFrame = self._fileHandling.getCurrentFrame()
        if not umlFrame: return
        
        self.moveOglObject(umlFrame, 'East')  
        
    # ------------------------------------------------------------------------- 
    def moveOglObject(self, umlFrame = None, azimut = ""):
        import OglObject

        selected = umlFrame.GetSelectedShapes()
        if len(selected) > 0:
            for shape in selected:
                if isinstance(shape, OglObject.OglObject):
                    x, y = shape.GetPosition
                    if azimut == "North":
                        shape.SetPosition(x, y-10)
                    elif azimut == "South":
                        shape.SetPosition(x, y+10)
                    elif azimut == "West":
                        shape.SetPosition(x-10, y)
                    elif azimut == "East":
                        shape.SetPosition(x+10,y)
                    else:
                        BasicSoftwareUtils.displayError("Error in the azimut value", "moveOglObject error")
        umlFrame.Refresh()
        
    # ------------------------------------------------------------------------- 
    def deleteSelectedShape(self):
        from delOglObjectCommand import DelOglObjectCommand

        from OglLink import OglLink
        from OglObject import OglObject
        from commandGroup import CommandGroup
        from BasicSoftwareSuperObject import BasicSoftwareSuperObject
        from BasicSoftwareSDInstance import BasicSoftwareSDInstance
        from createOglSDInstanceCommand import CreateOglSDInstanceCommand
        from createOglLinkCommand import CreateOglLinkCommand
        from createOglObjectCommand import CreateOglObjectCommand

        umlFrame = self._fileHandling.getCurrentFrame()
        selected = umlFrame.GetSelectedShapes()
        cmdGroup = CommandGroup("Delete UML object(s)")
        cmdGroupInit = False
        
        for shape in selected:
            cmd = None
            try:
                basicSoftwareObject = shape.getBasicSoftwareObject()
                if isinstance(basicSoftwareObject, BasicSoftwareSuperObject):
                    cmd = CreateOglObjectCommand(shape = shape, forExecute = False)
                elif isinstance(basicSoftwareObject, BasicSoftwareSDInstance):
                    cmd = CreateOglSDInstanceCommand(shape = shape)
            except AttributeError:
                if isinstance(shape, OglLink):
                    cmd = CreateOglLinkCommand(shape = shape, src = shape.getSourceShape(), dst = shape.getDestinationShape(), linType = shape.getBasicSoftwareObject().getType(),
                                               srcId = shape.getSourceShape().getBasicSoftwareObject.getId(), dstId = shape.getDestinationShape.getBasicSoftwareObject.getId())
                elif isinstance(shape, OglObject):
                    cmd = DelOglObjectCommand(shape)
            except Exception:
                BasicSoftwareUtils.displayError("Failed to delete the shape : [%s]" %shape, "mediator.deleteSelectedShape error")
                
            if cmd:
                cmdGroup.addCommand(cmd)
                cmdGroupInit = True
            else:
                shape.Detach()
                umlFrame.Refresh()
                
            if cmdGroupInit:
                shape.Detach()
                umlFrame.getHistory().addCommandGroup(cmdGroup)
                self._fileHandling.getCurrentFrame().getHistory()._groupToUndo -=1
                umlFrame.Refresh()
                
    # ------------------------------------------------------------------------- 
    def insertSelectedShape(self):
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None: return
        selected = umlFrame.GetSelectedShapes()
        if len(selected) != 1:
            return
        selected = selected.pop()
        if isinstance(selected, LinePoint):
            px, py = selected.GetPosition()
            line = selected.GetLines()[0]
            if line.GetSource().GetParent() is \
                line.GetDestination().GetParent():
                cp = ControlPoint(0, 0, line.GetSource().GetParent())
                cp.SetPosition(px + 20, py + 20)
            else:
                cp = ControlPoint(px + 20, py + 20)
            line.AddControl(cp, selected)
            umlFrame.GetDiagram().AddShape(cp)
            umlFrame.Refresh()
            
    # ------------------------------------------------------------------------- 
    def getOglSDInstance(self, basicSoftwareSDInstance):
        from OglSDInstance import OglSDInstance
        po = [po for po in self.getUmlObjects() if isinstance(po, OglSDInstance) and po.getBasicSoftwareObject() is basicSoftwareSDInstance]
        return po[0]
    
    # ------------------------------------------------------------------------- 
    def getOglNote(self, basicSoftwareNote):
        from OglNote import OglNote
        po = [po for po in self.getUmlObjects() if isinstance(po, OglNote) and po.getBasicSoftwareObject() is basicSoftwareNote]
        return po[0]
    

    # ------------------------------------------------------------------------- 
    def getFileHandling(self):
        return self._fileHandling

    # ------------------------------------------------------------------------- 
    def updateTitle(self):
        """
        Set the application title, fonction of version and current filename
        """
        
        # Get filename
        project = self._fileHandling.getCurrentProject()
        if project is not None:
            filename = project.getFilename()
        else:
            filename = ""

        #Set text
        txt = "BasicProphet v" + str(__BasicSoftwareVersion__) + " - " + filename
        if (project is not None) and (project.getModified()):
            if self._fileHandling.getCurrentFrame() is not None:
                zoom = self._fileHandling.getCurrentFrame().GetCurrentZoom()
            else:
                zoom = 1
                
            txt=txt + " (" + ((int)(zoom * 100)).__str__() + "%)" + " *"
        self._appFrame.SetTitle(txt)  
        
        
    # ------------------------------------------------------------------------- 
    def loadByFilename(self, filename):
        """
        Load a file from its filename
        """
        self._appFrame.loadByFilename(filename)
                
    # ------------------------------------------------------------------------- 
    def cutSelectedShapes(self):
        self._appFrame.cutSelectedShapes()
        
    # ------------------------------------------------------------------------- 
    def getCurrentAction(self):
        return self._currentAction
    
    def upDateHistoryManager(self, oglObject, rep):
        from OglSDInstance import OglSDInstance, OglInstanceRectangleShape, OglInstanceName
        from commandGroup import CommandGroup
        from OglLink import OglLink
        from BasicSoftwareSuperObject import BasicSoftwareSuperObject
        
        umlFrame = self._fileHandling.getCurrentFrame()
        action = None
        if rep == wx.ID_NO:
            action = 'Delete'
        elif rep in [wx.ID_OK, None]:
            action = 'UpDate'
        elif rep == wx.ID_PASTE:
            action = 'Copy'
            
        if not umlFrame or not action : return
        if isinstance(oglObject, OglSDInstance):
            from createOglSDInstanceCommand import CreateOglSDInstanceCommand
            cmd = CreateOglSDInstanceCommand(shape = oglObject)
            cmdGroup = CommandGroup("%s SDInstance" %action)
            cmdGroup.addCommand(cmd)
            umlFrame.getHistory().addCommandGroup(cmdGroup)
            self._fileHandling.getCurrentFrame().getHistory()._groupToUndo -=1
            return
        elif isinstance(oglObject, OglInstanceRectangleShape):
            basicSoftwareObject = oglObject.basicSoftwareObject
            upObject = self.getOglSDInstance(basicSoftwareObject)
            from createOglSDInstanceCommand import CreateOglSDInstanceCommand
            cmd = CreateOglSDInstanceCommand(shape = upObject)
            cmdGroup = CommandGroup("%s SDInstance" %action)
            cmdGroup.addCommand(cmd)
            umlFrame.getHistory().addCommandGroup(cmdGroup)
            self._fileHandling.getCurrentFrame().getHistory()._groupToUndo -=1
            return                        
        elif isinstance(oglObject, OglInstanceName):
            basicSoftwareObject = oglObject.getbasicSoftwareObject()
            upObject = self.getOglSDInstance(basicSoftwareObject)
            from createOglSDInstanceCommand import CreateOglSDInstanceCommand
            cmd = CreateOglSDInstanceCommand(shape = upObject)
            cmdGroup = CommandGroup("%s SDInstance" %action)
            cmdGroup.addCommand(cmd)
            umlFrame.getHistory().addCommandGroup(cmdGroup)
            self._fileHandling.getCurrentFrame().getHistory()._groupToUndo -=1                        
            
        basicSoftwareObject = oglObject.getBasicSoftwareObject()
        if isinstance(basicSoftwareObject, BasicSoftwareSuperObject):
            from createOglObjectCommand import CreateOglObjectCommand   
            cmd = CreateOglObjectCommand(shape = oglObject)
            Type = basicSoftwareObject.getType()
            cmdGroup = CommandGroup("%s %s" %(action, OBJECT_NAME[Type]))
            cmdGroup.addCommand(cmd)
            umlFrame.getHistory().addCommandGroup(cmdGroup)
            self._fileHandling.getCurrentFrame().getHistory()._groupToUndo -=1
            return
        elif isinstance(oglObject, OglLink):
            src = oglObject.getSourceShape()
            dst = oglObject.getDestinationShape()
            linkType = oglObject.getBasicSoftwareObject().getType()
            from createOglLinkCommand import CreateOglLinkCommand
            cmd = CreateOglLinkCommand(shape = oglObject, src=src, dst=dst, linkType=linkType)
            cmdGroup = CommandGroup("%s Link" %action)
            cmdGroup.addCommand(cmd)
            umlFrame.getHistory.addCommandGroup(cmdGroup)
            self._fileHandling.getCurrentFrame().getHistory._groupToUndo -=1
            return
        else:
            BasicSoftwareUtils.displayWarning("This Ogl Object can't be modify", 'upDateHistoryManager warning')
            
            
            
            
            
            