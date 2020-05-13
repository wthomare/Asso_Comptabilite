# -*- coding: utf-8 -*-

import BasicSoftwareUtils 

from BasicSoftwareProject import BasicSoftwareProject
import BasicSoftwareConst
import wx

[ALL, PARTIAL] = range(2)

def shorterFilename(filename):
    import os
    string = os.path.split(filename)[1]
    if len(string)>12:
        return string[:4] + string[-8:]
    else:
        return string
    

class FileHandling:
    
    def __init__(self, parent, mediator, projectTree, projectTreeRoot, notebook):
        self._projects = []
        self._parent = parent
        self._ctrl = mediator
        self._currentProject = None
        self._currentFrame = None
        self._projectTree = projectTree
        self._notebook = notebook
        self._projectTreeRoot = projectTreeRoot
        self._notebook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self._onNotebookPageChanged)
        self._projectTree.Bind(wx.EVT_TREE_SEL_CHANGED, self._onProjectTreeSelChanged)
        self._notebook.Bind(wx.aui.EVT_AUINOTEBOOK_BUTTON, self.onCloseCurrentPage)
        
        self._notebookCurrentPage = -1
        
    def registerUmlFrame(self, frame):
        self._currentFrame = frame
        self._currentProject = self.getProjectFromFrame(frame)
        
    class EventClone:
        def __init__(self, id):
            self._id = id
        def GetId(self):
            return self._id
        
    def showFrame(self, frame):
        self._frame = frame
        frame.Show()
        
    def getProjects(self):
        return self._projects
    
    def isProjectLoaded(self, filename):
        for project in self._projects:
            if project.getFilename == filename:
                return True
        return False
    
    def isDefaultFileName(self, filename):
        return filename == BasicSoftwareConst.DefaultFileName
    
    def openFile(self, filename, project=None):
        
        if not self.isDefaultFileName(filename) and self.isProjectLoaded(filename):
            BasicSoftwareUtils.displayError(("The selected file is already loaded"))
            return False
        
        if not project:
            project = BasicSoftwareProject(BasicSoftwareConst.DefaultFileName, self._notebook, self._projectTree, self._projectTreeRoot)
        
        try:
            if not project.loadFromFilename(filename):
                BasicSoftwareUtils.displayError(("The specified file can't be loaded !"))
                return False
            self._projects.append(project)
            self._currentProject = project
        except:
            BasicSoftwareUtils.displayError(("An error occured while loading the project"))
            return False
        
        try:
            for document in project.getDocuments():
                self._notebook.AddPafe(document.getFrame(), document.getDiagramTitle())
            self._notebookCurrentPage = self._notebook.GetPageCount() -1
            self._notebook.SetSelection(self._notebookCurrentPage)
            if len(project.getDocuments())>0:
                self._currentFrame = project.getDocuments()[0].getFrame()
        except:
            BasicSoftwareUtils.displayError(("An error occured while adding the project to the notebook"))
            
    
    def openText(self, xmlString):
        
        project = BasicSoftwareProject(BasicSoftwareConst.DefaultFileName, self._notebook, self._projectTree, self._projectTreeRoot)
        
        try:
            if not project.loadFromText(xmlString):
                BasicSoftwareUtils.displayError(("The specified file can't be loaded"))
                return False
            self._projects.append(project)
            self._currentProject = project
        except:
            BasicSoftwareUtils.displayError(("An error occured while loading the project"))
            
            
        try:
            for document in project.getDocuments():
                self._notebook.AddPage(document.getFrame(), document.getDiagramTitle())
            self._notebookCurrentPage = self._notebook.GetPageCount() -1
            self._notebook.SetSelection(self._notebookCurrentPage)
            if len(project.getDocuments()) > 0:
                self._currentFrame = project.getDocuments()[0].getFrame()
        except:
            BasicSoftwareUtils.displayError(("An error occured while adding the porject to the notebook"))
            return False
        return True
    
    def insertFile(self, filename):
        project = self._currentProject
        
        nbInitialDocuments = len(project.getDocuments())
        
        if not project.insertPorject(filename):
            BasicSoftwareUtils.displayError(("The specified file can't be loaded"))
            return False
        
        try:
            for document in project.getDocuments()[nbInitialDocuments:]:
                self._notebook.AddPage(document.getFrame(), document.getDiagramTitle())
            self._notebookCurrentPage = self._notebook.GetPageCount() -1
            self._notebook.SetSelection(self._notebookCurrentPage)
        except:
            BasicSoftwareUtils.displayError(("An error occured while adding the project to the notebook"))
            return False
        
        if len(project.getDocuments()) > nbInitialDocuments:
            self._frame = project.getDocuments()[nbInitialDocuments].getFrame()
            
    def saveFile(self):
        currentProject = self._currentProject
        if not currentProject:
            BasicSoftwareUtils.displayError(("No diagram to save"))
            return False
        
        if not currentProject.getFilename() or currentProject.getFilename()==BasicSoftwareConst.DefaultFileName:
            return self.saveFileAs()
        else:
            return currentProject.saveXmlBasicSoftware()
        
    def saveFileAs(self):
        
        if not self._ctrl.getDiagram():
            BasicSoftwareUtils.displayError(("No diagram to save"))
            return
        
        filenameOK = False
        while not filenameOK:
            dlg = wx.FileDialog(self._parent, defaultDir=self._parent.getCurrentDir(), wildcard=("BasicSoftware file (*.xml)|*.xml"), style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
            if dlg.ShowModal() != wx.ID_OK:
                dlg.Destroy()
                return False
            
            filename = dlg.GetPath()
            
            if len([project for project in self._projects if project.getFilename() == filename])>0:
                msg = ("Error! The filename %s correspond to a project which is currently opened!" %(str(filename)))
                BasicSoftwareUtils.displayError(msg, ("Save change, filename Error"))
                return
            filenameOK = True

        project = self._currentProject
        project.setFilename(filename)
        project.saveXmlBasicSoftware()

        for i in range(self._notebook.GetPageCount()):
            frame = self._notebook.GetPage()
            document = [document for document in project.getDocuments() if document.getFrame() is frame]
            if len(document)>0:
                document=document[0]
                if frame in project.getFrames():
                    self._notebook.SetPageText(i, document.getDiagramTitle())
            else:
                BasicSoftwareUtils.displayError(("Not updating notebook in FileHandling"), "Warning")
                
        self._parent.updateCurrentDir(dlg.GetPath())
        project.setModified(False)
        dlg.Destroy()
        return True
    
    def newProject(self):
        project = BasicSoftwareProject(BasicSoftwareConst.DefaultFileName, self._notebook, self._projectTree, self._projectTreeRoot)
        self._projects.append(project)
        self._currentProject = project
        self._currentFrame = None
        
    def newDocument(self, Type):
        project = self._currentProject
        if not project:
            self.newProject()
            project = self.getCurrentProject()
        
        frame = project.newDocument(Type).getFrame()
        self._currentFrame = frame
        self._currentProject = project
        self._notebook.AddPage(frame, shorterFilename(project.getFilename()))
        self._notebookCurrentPage = self._notebook.GetPageCount()-1
        self._notebook.SetSelection(self._notebookCurrentPage)
        
        
    def exportToImageFile(self, extension, imageType):
        dlg = wx.FileDialog(self._parent, ("Export to %s file format"%extension), self._parent.getCurrentDir(), "", "*." +extension, wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            self._ctrl.deselectAllShapes()
            frame = self.getCurrentFrame()
            
            (x1, y1, x2, y2) = frame.getObjectsBoundaries()
            x1+=10
            y1+=10
            x1 = max(0,x1)
            y1 = max(0, y1)
            x2 += 10
            y2 += 10
            
            out_dc = wx.MemoryDC()
            out_bitmap = wx.Bitmap(x2-x1, y2-y1)
            out_dc.SelectObject(out_bitmap)
            
            diag_dc = wx.MemoryDC()
            w, h = frame.GetVirtualSize()
            diag_dc.SelectObject(wx.Bitmap(w,h))
            diag_dc.SetBackground(wx.WHITE_BRUSH)
            diag_dc.Clear()
            
            frame.Redraw(diag_dc)
            out_dc.Blit(0, 0, x2-x1, y2-y1, diag_dc, x1, y1)
            out_dc.SelectObject(wx.NullBitmap)
            diag_dc.SelectObject(wx.NullBitmap)     
            image = out_bitmap.ConvertToImage()
            image.SaveFile(dlg.GetPath(), imageType)
        self._parent.updateCurrentDir(dlg.GetPath())
        dlg.Destroy()
        
    def exportToBmp(self, event):
        self.exportToImageFile("bmp", wx.BITMAP_TYPE_BMP)
        
    def exportToJpg(self, event):
        self.exportToImageFile("jpg", wx.BITMAP_TYPE_BMP)
         
    def exportToPng(self, event):
        self.exportToImageFile("png", wx.BITMAP_TYPE_BMP)
        
    def _onNotebookPageChanged(self, event):
        """
        Callback for notebook page changed
        """
        self._notebookCurrentPage=self._notebook.GetSelection()
        if not self._ctrl is None:
            #self._ctrl.registerUMLFrame(self._getCurrentFrame())
            self._currentFrame = self._getCurrentFrameFromNotebook()
            # self._parent.notifyTitleChanged()

        # Register the current project
        self._currentProject = self.getProjectFromFrame(self._currentFrame)

    def _onProjectTreeSelChanged(self, event):
        """
        Callback for notebook page changed
        """
        pyData = self._projectTree.GetItemData(event.GetItem())
        if isinstance(pyData, wx.ScrolledWindow):
            frame = pyData
            self._currentFrame = frame
            self._currentProject = self.getProjectFromFrame(frame)

            # Select the frame in the notebook
            for i in range(self._notebook.GetPageCount()):
                pageFrame=self._notebook.GetPage(i)
                if pageFrame is frame:
                    self._notebook.SetSelection(i)
                    return
        elif isinstance(pyData, BasicSoftwareProject):
            self._currentProject = pyData

    def _getCurrentFrameFromNotebook(self):
        """
        Get the current frame in the notebook

        @return frame Current frame in the notebook; -1 if none selected
        """
        noPage = self._notebookCurrentPage
        if noPage == -1:
            return None
        frame = self._notebook.GetPage(noPage)
        return frame

    def getCurrentFrame(self):
        """
        Get the current frame
        """
        return self._currentFrame
    
    #>-----------------------------------------------------------------------

    def getCurrentProject(self):
        """
        Get the current working project 

        @return Project : the current project or None if not found
        """
        return self._currentProject

    #>-----------------------------------------------------------------------

    def getProjectFromFrame(self, frame):
        """
        Return the project that owns a given frame

        @param wx.Frame frame : the frame to get his project
        """
        for project in self._projects:
            if frame in project.getFrames():
                return project
        return None


    #>-----------------------------------------------------------------------

    def getCurrentDocument(self):
        """
        Get the current document.
        """
        project = self.getCurrentProject()
        if project is None: return None
        for document in project.getDocuments():
            if document.getFrame() is self._currentFrame:
                return document
        return None

    def setModified(self, flag=True):
        if self._currentProject:
            self._currentProject.setModified(flag)
        self._ctrl.updateTitle()
        
        
    def onClose(self):
        for project in self._projects:
            if project.getModified()==True:
                frames = project.getFrames()
                if len(frames) != 0:
                    frame = frames[0]
                    frame.SetFocus()
                    wx.Yield()
                    self.showFrame(frame)
                dlg = BasicSoftwareUtils.displayWarning(("Your diagram has not been saved! Would you like to save it?"), ('Save changes ?'))
                if dlg == wx.CANCEL:
                    self.clearVariable(ALL)
                    return False
                elif dlg == wx.YES:
                    if not self.saveFile():
                        self.clearVariable(ALL)
                        return False

    def onCloseCurrentProject(self):
        """
        Close the current project

        @return True if everything's ok
        """
        # No frame left ?
        if self._currentProject is None and self._currentFrame is not None:
            self._currentProject = self.getProjectFromFrame(self._currentFrame)
        if self._currentProject is None:
            BasicSoftwareUtils.displayError(("No frame to close !"), ("Error..."))
            return

        # Close the file
        if self._currentProject.getModified()==True  \
           and not self._ctrl.isInScriptMode():
            # Ask to save the file
            frame = self._currentProject.getFrames()[0]
            frame.SetFocus()
            #self._ctrl.registerUMLFrame(frame)
            self.showFrame(frame)

            dlg = wx.MessageDialog(self.__parent, 
                ("Your project has not been saved. "
                  "Would you like to save it ?"),
                ("Save changes ?"),
                wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                #save
                if self.saveFile() == False:
                    return False

        # Remove the frame in the notebook
        if not self._ctrl.isInScriptMode():
            pages = range(self.__notebook.GetPageCount())
            pages.reverse()
            for i in pages:
                pageFrame=self.__notebook.GetPage(i)
                if pageFrame in self._currentProject.getFrames():
                    self.__notebook.DeletePage(i)
                    # RemovePage si erreur ??

        self._currentProject.removeFromTree()
        self._projects.remove(self._currentProject)

        self._currentProject = None
        self._currentFrame = None
        
    def onCloseCurrentPage(self, event):
        if not self._currentProject and self._currentFrame:
            self._currentProject = self.getProjectFromFrame(self._currentFrame)
        if not self._currentProject:
            BasicSoftwareUtils.displayError(('No frame to close !') ('onCloseCurrentPage error'))
            return False
        
        if self._currentProject.getModified() and len(self._currentFrame.GetDiagram().GetShapes()) !=0:
            dlg = BasicSoftwareUtils.displayWarning(('Your project has not been saved. Would you like to save it'), ('Save changes ?'))
            if dlg == wx.CANCEL:
                return False
            elif dlg==wx.YES:
                if not self.saveFile():
                    return False
                self._notebook.DeletePage(self._notebookCurrentPage)
                if self._notebook.GetPageCount() == 0:
                    self._currentProject.removeFromTree()
                    self._projects.remove(self._currentProject)
                    self.clearVariable(PARTIAL)
                return True
        else:
            self._notebook.DeletePage(self._notebookCurrentPage)
            if self._notebook.GetPageCount() == 0:
                self.projects.remove(self._currentProject)
                self.clearVariable(PARTIAL)
            return True
        
    def removeAllReferencesToUmlFrame(self, umlFrame):
        """
        Remove all my references to a given uml frame
        """
        # Current frame ?
        if self._currentFrame is umlFrame:
            self._currentFrame is None
        
        for i in range(self.__notebook.GetPageCount()):
            pageFrame = self.__notebook.GetPage(i)
            if pageFrame is umlFrame:
                self.__notebook.DeletePage(i)
                break

    def getProjectFromOglObjects(self, oglObjects):
        """
        Get a project that owns oglObjects
       
        @param oglObjects Objects to find their parents
        """
        for project in self._projects:
            for frame in project.getFrames():
                diagram = frame.getDiagram()
                shapes = diagram.GetShapes()
                for obj in oglObjects:
                    if obj in shapes:
                        return project
        return None
               
    def clearVariable(self, kind):          
        if kind ==ALL:
            self._parent = None
            self._ctrl = None
            self._splitter = None
            self._projectTree = None
            self._notebook.DeleteAllPages()
            self._notebook = None
            self._projects =None
            self._currentProject =None
            self._currentFrame = None
        elif kind == PARTIAL:
            self._currentProject = None
            self._currentFrame = None
            
            
