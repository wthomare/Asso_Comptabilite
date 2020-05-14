# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 17:40:14 2020

@author: wilfr
"""

import wx
import wx.ribbon as RB
import wx.grid as gridlib

import images
import os

from FileHandling import FileHandling

from AssoComptaUtils import CreateBitmap, displayWarning
from AssoComptaPrintout import Printout
from AssoComptaConst import SEQUENCE_DIAGRAM

from commandGroup import CommandGroup
import mediator
import mediatorParameter
#import Ctrl_Manager


class RibbonFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.DEFAULT_FRAME_STYLE, log=None):
        wx.Frame.__init__(self, parent, id, title, pos, size)
        panel = wx.Panel(self)
        
        self._ribbon = RB.RibbonBar(panel, style=RB.RIBBON_BAR_DEFAULT_STYLE |RB.RIBBON_BAR_SHOW_PANEL_EXT_BUTTONS)
        
        self._bitmap_creation_dc = wx.MemoryDC()
        self._colour_data = wx.ColourData()
        
        home = RB.RibbonPage(self._ribbon, wx.ID_ANY, "HomePage", CreateBitmap("ribbon"))
        
        toolbar_panel = RB.RibbonPanel(home, wx.ID_ANY, "Toolbar", style = RB.RIBBON_PANEL_NO_AUTO_MINIMISE | RB.RIBBON_PANEL_EXT_BUTTON)
        toolbar = RB.RibbonToolBar(toolbar_panel, mediatorParameter.ID_MAIN_TOOLBAR)
        toolbar.AddTool(mediatorParameter.ID_MNUFILENEWSEQUENCEDIAGRAM, wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_OTHER, wx.Size(24,23)))
        toolbar.AddTool(mediatorParameter.ID_MNUUNDO, wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_OTHER, wx.Size(24,23)))
        toolbar.AddTool(mediatorParameter.ID_MNUREDO, wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_OTHER, wx.Size(24,23)))
        toolbar.AddSeparator()
        
        toolbar.AddTool(mediatorParameter.ID_MNUFILEOPEN, wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, wx.Size(24,23)))
        toolbar.AddTool(mediatorParameter.ID_MNUFILESAVE, wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, wx.Size(24,23)))
        toolbar.AddTool(mediatorParameter.ID_MNUFILESAVEAS, wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, wx.Size(24,23)))
        toolbar.AddTool(mediatorParameter.ID_MNUFILEPRINT, wx.ArtProvider.GetBitmap(wx.ART_PRINT, wx.ART_OTHER, wx.Size(24,23)))
        toolbar.AddSeparator()
        toolbar.SetRows(2, 3)
        
        view_panel = RB.RibbonPanel(home, wx.ID_ANY, style = RB.RIBBON_PANEL_NO_AUTO_MINIMISE | RB.RIBBON_PANEL_EXT_BUTTON)
        view = RB.RibbonToolBar(view_panel, wx.ID_ANY)
        view.AddTool(mediatorParameter.ID_ARROW, CreateBitmap("handle", 32, 31), "Selector")
        view.AddTool(mediatorParameter.ID_ZOOMIN, CreateBitmap("zoomin", 32, 31), "Zoom in")
        view.AddTool(mediatorParameter.ID_ZOOMOUT, CreateBitmap("zoomout", 32, 31), "Zoom out")
        
        setup_panel = RB.RibbonPanel(home, wx.ID_ANY, "Setup", style = RB.RIBBON_PANEL_NO_AUTO_MINIMISE | RB.RIBBON_PANEL_EXT_BUTTON)
        setup = RB.RibbonToolBar(setup_panel, wx.ID_ANY)
        setup.AddHybridTool(mediatorParameter.ID_BASICSETUP, CreateBitmap("config_setup", 48, 47), help_string="Default setup for a diagramm")

        tool_panel = RB.RibbonPanel(home, wx.ID_ANY, "Tools", CreateBitmap("selection_panel"))
        tool = RB.RibbonToolBar(tool_panel, wx.ID_ANY) 
        tool.AddTool(mediatorParameter.ID_SD_INSTANCE, CreateBitmap("actor", 32, 31), help_string="Create an instance")
        tool.AddHybridTool(mediatorParameter.ID_TITLE, CreateBitmap("function1", 32, 31), help_string="declare a function")
        tool.AddHybridTool(mediatorParameter.ID_USECASE, CreateBitmap("loop", 32, 31), help_string="declare a loop")
        tool.AddTool(mediatorParameter.ID_NOTE, CreateBitmap("code", 32, 31), help_string="Hard code")
        tool.AddTool(mediatorParameter.ID_STATEMENT, CreateBitmap("divergence1", 32, 31), help_string="Create a divergence")
        
        
        link_panel = RB.RibbonPanel(home, wx.ID_ANY, "Links", CreateBitmap("selection_panel"))
        link = RB.RibbonButtonBar(link_panel)
        link.AddDropdownButton(mediatorParameter.ID_LINK, "Order link", CreateBitmap("mainlink"), help_string="Create a link between two actor")
        link.AddDropdownButton(mediatorParameter.ID_OTHERLINK, "Other link", CreateBitmap("mainlink"), help_string="Create other link")
        
        logging_panel = RB.RibbonPanel(home, wx.ID_ANY, "Logging", style = RB.RIBBON_PANEL_NO_AUTO_MINIMISE | RB.RIBBON_PANEL_EXT_BUTTON)
        logging = RB.RibbonButtonBar(logging_panel)
        logging.AddDropdownButton(mediatorParameter.ID_FIXLOG, "Fix_Log", CreateBitmap("FIXLOG", 32, 31), help_string="Fix Logging function")
        logging.AddDropdownButton(mediatorParameter.ID_LOG, "Logging", CreateBitmap("log", 32, 31), help_string="Logging function")
        
        scheme = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Export/Import", CreateBitmap("eye"))
        save_panel = RB.RibbonPanel(scheme, wx.ID_ANY, "Save", CreateBitmap("selection_panel"))
        save = RB.RibbonToolBar(save_panel, wx.ID_ANY)
        save.AddTool(mediatorParameter.ID_MNUFILEOPEN, wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, wx.Size(24,23)))
        save.AddTool(mediatorParameter.ID_MNUFILESAVE, wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, wx.Size(24,23)))
        save.AddSeparator()
        save.AddTool(mediatorParameter.ID_MNUFILESAVEAS, wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, wx.Size(24,23)))        
        save.AddTool(mediatorParameter.ID_MNUFILEPRINT, wx.ArtProvider.GetBitmap(wx.ART_PRINT, wx.ART_OTHER, wx.Size(24,23)))
        save.SetRows(2, 3)

        image_panel = RB.RibbonPanel(scheme, wx.ID_ANY, "Image", CreateBitmap("selection_panel"))
        image = RB.RibbonButtonBar(image_panel, wx.ID_ANY)
        image.AddDropdownButton(mediatorParameter.ID_SAVEIMAGE, "Save \n Image", CreateBitmap("mondrian", 32, 31), help_string = "...")
        
        translate_panel = RB.RibbonPanel(scheme, wx.ID_ANY, "BasicConfig", CreateBitmap("eye"))
        translate = RB.RibbonToolBar(translate_panel, wx.ID_ANY)     
        translate.AddTool(mediatorParameter.ID_EXPORTPYTHON, CreateBitmap("python", 36, 35), help_string = "translate grphic into python")
        
        xml_panel = RB.RibbonPanel(scheme, wx.ID_ANY, "Import XML", CreateBitmap("eye"))
        xml = RB.RibbonToolBar(xml_panel, wx.ID_ANY)  
        xml.AddTool(mediatorParameter.ID_IMPORTXML, CreateBitmap("xml", 36, 35), help_string = "Incert scheme")
        
        # window splitting
        self._logwindow = wx.SplitterWindow(panel, wx.ID_ANY)
        
        # Project tree
        self._projectTree = wx.TreeCtrl(self._logwindow, wx.ID_ANY, style= wx.TR_DEFAULT_STYLE)
        self._projectTreeRoot = self._projectTree.AddRoot(("Root"))
        
        self.myGrid = gridlib.Grid(self._logwindow)
        self.myGrid.CreateGrid(12, 8)
        
        # Diagram container
        # self._notebook=AUI.AuiNotebook(self._logwindow, wx.ID_ANY, style=wx.NB_FLAT)
        
        # Set splitter
        self._logwindow.SetMinimumPaneSize(20)
        self._logwindow.SplitVertically(self._projectTree, self.myGrid, sashPosition = 230)
        
        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(self._ribbon, 0, wx.EXPAND)
        s.Add(self._logwindow, 1, wx.EXPAND)
        
        panel.SetSizer(s)
        self.panel = panel
        
        # Set events
        self._BindEvents(link, image, toolbar, translate, tool, logging, setup)

        self.SetIcon(images.mondrian.Icon)
        self.CenterOnScreen()
        self._ribbon.Realize()

        # Properties
        #self.plugMgr = PluginManager()
        #self.plugs = {}
        #plugs = self.plugMgr.getOutputPlugins()
        
        #for i in range(len(plugs)):
        #    obj = plugs[i](None, None)
        #    if obj.getOutputFormat()[1] == "py":
        #        Id = mediatorParameter.ID_EXPORTPYTHON
        #        self.plugs[Id] = plugs[i]
                
        self._lastDir = os.getcwd()
        
        # Get the mediator singleton
        self._ctrl = mediator.get_mediator()
        self._ctrl.registerAppFrame(self)
        
        # Load file Handler
        self._fileHandling = FileHandling(self, self._ctrl, self._projectTree, self._projectTreeRoot, self.myGrid)
        self._ctrl.registerFileHandling(self._fileHandling)
        self._initPrinting()
        
        # Get the Ctrl+v Ctrl+P Manager
        # self._ctrlVP = Ctrl_Manager.getController()
        
        # Accelerator init
        acc = self._createAcceleratorTable()
        accel_table = wx.AcceleratorTable(acc)
        self.SetAcceleratorTable(accel_table)
        
        # Membernvars
        self._currentDirectory = os.getcwd()
        self._ctrl.registerAppPath(self._currentDirectory)
        self.clipboard = []


        # Set application title
        self._fileHandling.newProject()
        self._ctrl.updateTitle()

    def _BindEvents(self, link, image, toolbar, translate, tool, logging, setup):    
        """
        Callbacks
        """
        toolbar.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, (lambda x:self.OnMnuFileNewSequenceDiagram(x)), id=mediatorParameter.ID_MNUFILENEWSEQUENCEDIAGRAM)
        
        #Undo / Redo
        toolbar.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, self.OnMnuUndo, id=mediatorParameter.ID_MNUUNDO)
        toolbar.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, self.OnMnuRedo, id=mediatorParameter.ID_MNUREDO)
        
        # Print
        toolbar.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, self.OnMnuFilePrint, id=mediatorParameter.ID_MNUFILEPRINT)
        
        
        # Title
        tool.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, self.OnTitle, id=mediatorParameter.ID_TITLE)
        tool.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnTitle, id=mediatorParameter.ID_TITLE)
        self.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_END_TITLE)
        self.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_END_TITLE)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_END_TITLE)        
        
        self.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_NEW_TITLE)
        self.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_NEW_TITLE)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_NEW_TITLE)        
        
        # Loop
        tool.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, self.OnLoop, id=mediatorParameter.ID_USECASE)
        tool.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnLoop, id=mediatorParameter.ID_USECASE)
        self.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_FOR)
        self.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_FOR)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_FOR)        
        self.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_WHILE)
        self.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_WHILE)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_WHILE)            
        
        
        # Logging     
        logging.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnLog, id=mediatorParameter.ID_LOG)
        logging.Bind(RB.EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED, self.OnLog, id=mediatorParameter.ID_LOG)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_LOG_DEB)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_LOG_INF)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_LOG_WAR)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_LOG_ERR)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_LOG_CRI)

        # Fix logging
        logging.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnFixLog, id=mediatorParameter.ID_FIXLOG)
        logging.Bind(RB.EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED, self.OnFixLog, id=mediatorParameter.ID_FIXLOG)    
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_FIX_INIT)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_FIX_START)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_FIX_SETUP)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_FIX_STOP)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_FIX_FLUSH)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_FIX_EXPECT)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_FIX_ADD)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_FIX_REMOVE)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_FIX_WAIT)
        
        # Basic Setup
        setup.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, self.OnSetup, id=mediatorParameter.ID_BASICSETUP)
        setup.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnSetup, id=mediatorParameter.ID_BASICSETUP)          
        setup.Bind(wx.EVT_MENU, (lambda x:self.OnMnuNewCaro(x)), id=mediatorParameter.ID_SETUPCARO)
        setup.Bind(wx.EVT_MENU, (lambda x:self.OnMnuNewSlice(x)), id=mediatorParameter.ID_SETUPSLICE)
        
        # Open / Save / Save As / Export
        self.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, (lambda x:self.OnMnuFileOpen(x)), id=mediatorParameter.ID_MNUFILEOPEN)
        self.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, (lambda x:self.OnMnuFileSave(x)), id=mediatorParameter.ID_MNUFILESAVE)
        self.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, (lambda x:self.OnMnuFileSaveAs(x)), id=mediatorParameter.ID_MNUFILESAVEAS)
        
        image.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnImage, id=mediatorParameter.ID_SAVEIMAGE)
        image.Bind(RB.EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED, self.OnImage, id=mediatorParameter.ID_SAVEIMAGE)    
        self.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, self.OnMnuFileExportBmp, id=mediatorParameter.ID_MNUFILEEXPBMP)
        self.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnMnuFileExportBmp, id=mediatorParameter.ID_MNUFILEEXPBMP)
        self.Bind(wx.EVT_MENU, self.OnMnuFileExportBmp, id=mediatorParameter.ID_MNUFILEEXPBMP)
        self.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, self.OnMnuFileExportJpg, id=mediatorParameter.ID_MNUFILEEXPJPG)
        self.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnMnuFileExportJpg, id=mediatorParameter.ID_MNUFILEEXPJPG)
        self.Bind(wx.EVT_MENU, self.OnMnuFileExportJpg, id=mediatorParameter.ID_MNUFILEEXPJPG)        
        self.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, self.OnMnuFileExportPng, id=mediatorParameter.ID_MNUFILEEXPPNG)
        self.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnMnuFileExportPng, id=mediatorParameter.ID_MNUFILEEXPPNG)
        self.Bind(wx.EVT_MENU, self.OnMnuFileExportPng, id=mediatorParameter.ID_MNUFILEEXPPNG)

        link.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnLink, id=mediatorParameter.ID_LINK)           
        link.Bind(RB.EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED, self.OnLink, id=mediatorParameter.ID_LINK) 
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_REL_REALISATION)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_EXPECTED)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_MODIFY)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_CANCEL)
        self.Bind(wx.EVT_MENU, (lambda x:self.OnNewAction(x)), id=mediatorParameter.ID_TRY)
        
        link.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnOtherLink, id=mediatorParameter.ID_OTHERLINK)           
        link.Bind(RB.EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED, self.OnOtherLink, id=mediatorParameter.ID_OTHERLINK) 
                
        
        for ID in {mediatorParameter.ID_SD_INSTANCE, mediatorParameter.ID_ZOOMOUT, mediatorParameter.ID_ZOOMIN, mediatorParameter.ID_ARROW, mediatorParameter.ID_NEW_TITLE, mediatorParameter.ID_END_TITLE, mediatorParameter.ID_USECASE,
                   mediatorParameter.ID_NOTE, mediatorParameter.ID_STATEMENT, mediatorParameter.ID_EXPECTED, mediatorParameter.ID_MODIFY, mediatorParameter.ID_REL_NOTE, mediatorParameter.ID_REL_REALISATION,
                   mediatorParameter.ID_FIX_INIT, mediatorParameter.ID_FIX_START, mediatorParameter.ID_FIX_SETUP, mediatorParameter.ID_FIX_STOP, mediatorParameter.ID_FIX_FLUSH, mediatorParameter.ID_FIX_EXPECT,
                   mediatorParameter.ID_FIX_ADD, mediatorParameter.ID_FIX_REMOVE, mediatorParameter.ID_FIX_WAIT, mediatorParameter.ID_LOG, mediatorParameter.ID_IMPORTXML, mediatorParameter.ID_LOG_DEB, mediatorParameter.ID_LOG_INF,
                   mediatorParameter.ID_LOG_CRI, mediatorParameter.ID_LOG_ERR, mediatorParameter.ID_MNUUNDO, mediatorParameter.ID_MNUREDO, mediatorParameter.ID_PROCESS, mediatorParameter.ID_BASICSETUP}:
            self.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, (lambda x: self.OnNewAction(x)), id=ID)
            
            
        # Link
        self.Bind(wx.EVT_MENU, self.OnMnuEditCut        ,id = mediatorParameter.ID_MNUEDITCUT)
        self.Bind(wx.EVT_MENU, self.OnMnuEditCopy        ,id = mediatorParameter.ID_MNUEDITCOPY)
        self.Bind(wx.EVT_MENU, self.OnMnuEditPaste        ,id = mediatorParameter.ID_MNUEDITPASTE)
        self.Bind(wx.EVT_MENU, self.OnMnuFilePrintSetup       ,id = mediatorParameter.ID_MNUFILEPRINTSETUP)
        self.Bind(wx.EVT_MENU, self.OnMnuFilePrint        ,id = mediatorParameter.ID_MNUFILEPRINT)
        self.Bind(wx.EVT_MENU, self.OnMnuFileNewProject        ,id = mediatorParameter.ID_MNUFILENEWPROJECT)
        self.Bind(wx.EVT_MENU, self.OnMnuUndo        ,id = mediatorParameter.ID_MNUUNDO)
        self.Bind(wx.EVT_MENU, self.OnMnuRedo        ,id = mediatorParameter.ID_MNUREDO)
        self.Bind(wx.EVT_MENU, self.OnMnuFileNewSequenceDiagram        ,id = mediatorParameter.ID_MNUFILENEWSEQUENCEDIAGRAM)
        self.Bind(wx.EVT_MENU, self.OnMnuFileSave        ,id = mediatorParameter.ID_MNUFILESAVE)
        self.Bind(wx.EVT_MENU, self.OnMnuFileOpen        ,id = mediatorParameter.ID_MNUFILEOPEN)
        self.Bind(wx.EVT_MENU, self.OnMnuFileSaveAs        ,id = mediatorParameter.ID_MNUFILESAVEAS)
       
        self.Bind(wx.EVT_CLOSE, self.Close, self)

    def OnTitle(self, event):
        """
        Callback for title selection
        """
        menu = wx.Menu()
        menu.Append(mediatorParameter.ID_NEW_TITLE, "New Title")
        menu.Append(mediatorParameter.ID_END_TITLE, "End Title")
        event.PopupMenu(menu)
    
    def OnSetup(self, event):
        """
        Callback for Setup selection
        """
        menu = wx.Menu()
        menu.Append(mediatorParameter.ID_SETUPCARO, "OPTION1")
        menu.Append(mediatorParameter.ID_SETUPCARO, "OPTION2")
        event.PopupMenu(menu)


    def OnLoop(self, event):
        """
        Callback for loop selection
        """
        menu = wx.Menu()
        menu.Append(mediatorParameter.ID_FOR, "For")
        menu.Append(mediatorParameter.ID_WHILE, "While")
        event.PopupMenu(menu)
        
    def OnLog(self, event):
        """
        Callback for log selection
        """
        menu = wx.Menu()
        menu.Append(mediatorParameter.ID_LOG_DEB, "Debug")
        menu.Append(mediatorParameter.ID_LOG_INF, "Info")
        menu.Append(mediatorParameter.ID_LOG_WAR, "Warning")
        menu.Append(mediatorParameter.ID_LOG_ERR, "Error")
        menu.Append(mediatorParameter.ID_LOG_CRI, "Critical")
        event.PopupMenu(menu)

    
    def OnFixLog(self, event):
        """
        Callback for log selection
        """
        menu = wx.Menu()
        menu.Append(mediatorParameter.ID_FIX_INIT, "Init")
        menu.Append(mediatorParameter.ID_FIX_START, "Start")
        menu.Append(mediatorParameter.ID_FIX_SETUP, "Setup")
        menu.Append(mediatorParameter.ID_FIX_STOP, "Stop")
        menu.Append(mediatorParameter.ID_FIX_FLUSH, "Flush")
        menu.Append(mediatorParameter.ID_FIX_EXPECT, "Expect")
        menu.Append(mediatorParameter.ID_FIX_ADD, "Add")
        menu.Append(mediatorParameter.ID_FIX_REMOVE, "Remove")
        menu.Append(mediatorParameter.ID_FIX_WAIT, "Wait")

        event.PopupMenu(menu)       
        
    def OnImage(self, event):
        """
        Callback for image saving
        """
        
        menu = wx.Menu()
        
        bmp = wx.MenuItem(menu, mediatorParameter.ID_MNUFILEEXPBMP, ".BMP")
        bmp.SetBitmap(CreateBitmap("bmp", 24, 23))
        jpg = wx.MenuItem(menu, mediatorParameter.ID_MNUFILEEXPJPG, ".JPG")
        jpg.SetBitmap(CreateBitmap("jpeg", 24, 23))
        png = wx.MenuItem(menu, mediatorParameter.ID_MNUFILEEXPPNG, ".PNG")
        png.SetBitmap(CreateBitmap("png", 24, 23))        
        
        menu.Append(bmp)
        menu.Append(jpg)
        menu.Append(png)
        event.PopupMenu(menu)
        
    def OnLink(self, event):
        """
        Callback for link creation
        """
 
        menu = wx.Menu()
        
        crea = wx.MenuItem(menu, mediatorParameter.ID_REL_REALISATION, "Create Order")
        crea.SetBitmap(CreateBitmap("arrowred", 24, 23))
        expe = wx.MenuItem(menu, mediatorParameter.ID_EXPECTED, "Expected Answer")
        expe.SetBitmap(CreateBitmap("arrowgreen", 24, 23))
        modi = wx.MenuItem(menu, mediatorParameter.ID_MODIFY, "Modify Order")
        modi.SetBitmap(CreateBitmap("arrowblue", 24, 23))        
        canc = wx.MenuItem(menu, mediatorParameter.ID_CANCEL, "Cancel Order")
        canc.SetBitmap(CreateBitmap("arrowblack", 24, 23))
        tries = wx.MenuItem(menu, mediatorParameter.ID_TRY, "Try ...")
        tries.SetBitmap(CreateBitmap("arroworange", 24, 23))      
        
        menu.Append(crea)
        menu.Append(expe)
        menu.Append(modi)
        menu.Append(canc)
        menu.Append(tries)
        event.PopupMenu(menu)       
    
    def OnOtherLink(self, event):
        menu = wx.Menu()
        
        note = wx.MenuItem(menu, mediatorParameter.ID_REL_NOTE, "Note Link")
        note.SetBitmap(CreateBitmap("arrowviolet", 24, 23))
        process = wx.MenuItem(menu, mediatorParameter.ID_PROCESS, "Process Link")
        process.SetBitmap(CreateBitmap("arrowgrey", 24, 23))    
        
        menu.Append(note)
        menu.Append(process)
        event.PopupMenu(menu)      

    def getCurrentDir(self):
        return self._lastDir

    def updateCurrentDir(self, fullPath):
        self._lastDir = fullPath[:fullPath.rindex(os.sep)] 
        
    def _createAcceleratorTable(self):
        """
        Accelerator table initialization

        """
        #init accelerator table
        lst=[
             (wx.ACCEL_CTRL,     ord('E'),   mediatorParameter.ID_MNUFILENEWSEQUENCEDIAGRAM),
             (wx.ACCEL_CTRL,     ord('e'),   mediatorParameter.ID_MNUFILENEWSEQUENCEDIAGRAM),
             (wx.ACCEL_CTRL,     ord('o'),   mediatorParameter.ID_MNUFILEOPEN),
             (wx.ACCEL_CTRL,     ord('O'),   mediatorParameter.ID_MNUFILEOPEN),
             (wx.ACCEL_CTRL,     ord('s'),   mediatorParameter.ID_MNUFILESAVE),
             (wx.ACCEL_CTRL,     ord('S'),   mediatorParameter.ID_MNUFILESAVE),
             (wx.ACCEL_CTRL,     ord('a'),   mediatorParameter.ID_MNUFILESAVEAS),
             (wx.ACCEL_CTRL,     ord('A'),   mediatorParameter.ID_MNUFILESAVEAS),
             (wx.ACCEL_CTRL,     ord('p'),   mediatorParameter.ID_MNUFILEPRINT),
             (wx.ACCEL_CTRL,     ord('P'),   mediatorParameter.ID_MNUFILEPRINT),
             (wx.ACCEL_CTRL,     ord('x'),   mediatorParameter.ID_MNUEDITCUT),
             (wx.ACCEL_CTRL,     ord('X'),   mediatorParameter.ID_MNUEDITCUT),
             (wx.ACCEL_CTRL,     ord('c'),   mediatorParameter.ID_MNUEDITCOPY),
             (wx.ACCEL_CTRL,     ord('C'),   mediatorParameter.ID_MNUEDITCOPY),
             (wx.ACCEL_CTRL,     ord('v'),   mediatorParameter.ID_MNUEDITPASTE),
             (wx.ACCEL_CTRL,     ord('V'),   mediatorParameter.ID_MNUEDITPASTE),
             (wx.ACCEL_CTRL,     ord('z'),   mediatorParameter.ID_MNUUNDO),
             (wx.ACCEL_CTRL,     ord('Z'),   mediatorParameter.ID_MNUUNDO),
             (wx.ACCEL_CTRL,     ord('y'),   mediatorParameter.ID_MNUREDO),
             (wx.ACCEL_CTRL,     ord('Y'),   mediatorParameter.ID_MNUREDO),

             ]
        acc=[]
        for el in lst:
            (el1, el2, el3)=el
            acc.append(wx.AcceleratorEntry(el1, el2, el3))
        return acc    
    
    
    def _initPrinting(self):
        """
        printing data initialization
        """
        self._printData = wx.PrintData()
        self._printData.SetPaperId(wx.PAPER_A4)
        self._printData.SetQuality(wx.PRINT_QUALITY_HIGH)
        self._printData.SetOrientation(wx.PORTRAIT)
        self._printData.SetNoCopies(1)
        self._printData.SetCollate(True)
        
    def OnMnuFileNewProject(self, event):
        """
        begin a new project
        """
        self._fileHandling.newProject()
        self._ctrl.updateTitle()
        
        
    def OnMnuFileNewSequenceDiagram(self, event):
        """
        begin a new sequence diagram
        """
        self._fileHandling.newDocument(SEQUENCE_DIAGRAM)
        self._ctrl.updateTitle()
        
    def OnMnuNewCaro(self, event):
        
        self._fileHandling.newDocument(SEQUENCE_DIAGRAM)
        umlFrame = self._fileHandling.getCurrentFrame()
        if not umlFrame: return 
        
        cmd = CreateOglSDInstanceCommand(100, 50, True, autoCreate = True, iterAuto = 'Client')
        cmdGroup = CommandGroup("Create SD Instance")
        cmdGroup.AddCommand(cmd)
        umlFrame.getHistory().addCommandGroup(cmdGroup)
        
        cmd = CreateOglSDInstanceCommand(1000, 50, True, autoCreate = True, iterAuto = 'RTGEN')
        cmdGroup = CommandGroup("Create SD Instance")
        cmdGroup.AddCommand(cmd)
        umlFrame.getHistory().addCommandGroup(cmdGroup)

        self._ctrl._currentAction = mediatorParameter.ACTION_SELECTOR
        self._ctrl.updateTitle()
        
    def OnMnuNewSlice(self, event):
        
        self._fileHandling.newDocument(SEQUENCE_DIAGRAM)
        umlFrame = self._fileHandling.getCurrentFrame()
        if not umlFrame: return 
        
        cmd = CreateOglSDInstanceCommand(100, 50, True, autoCreate = True, iterAuto = 'Client')
        cmdGroup = CommandGroup("Create SD Instance")
        cmdGroup.AddCommand(cmd)
        umlFrame.getHistory().addCommandGroup(cmdGroup)
        
        cmd = CreateOglSDInstanceCommand(1000, 50, True, autoCreate = True, iterAuto = 'RTGEN')
        cmdGroup = CommandGroup("Create SD Instance")
        cmdGroup.AddCommand(cmd)
        umlFrame.getHistory().addCommandGroup(cmdGroup)

        self._ctrl._currentAction = mediatorParameter.ACTION_SELECTOR
        self._ctrl.updateTitle()        
        
    def OnMnuFileOpen(self, event):
        """
        Open a diagram
        """
        self._loadFile()

    def OnMnuFileSave(self, event):
        """
        Save the current diagram to a file
        """
        self._saveFile()

    def OnMnuFileSaveAs(self, event):
        """
        Ask and save the current diagram to a file
        """
        self._saveFileAs()
        
    def OnMnuFileExportBmp(self, event):
        self._fileHandling.exportToBmp(-1)
        
    def OnMnuFileExportJpg(self, event):
        self._fileHandling.exportToJpg(-1)   
        
    def OnMnuFileExportPng(self, event):
        self._fileHandling.exportToPng(-1) 
        
    def OnMnuFilePrintSetup(self, event):
        """
        Display the print setup dialog box
        """
        dlg=wx.PrintDialog(self)
        dlg.GetPrintDialogData().SetSetupDialog(True)
        dlg.GetPrintDialogData().SetPrintData(self._printData)
        
        if dlg.ShowModal() == wx.ID_OK:
            self._printData=dlg.GetPrintDialogData().GetPrintData()
        dlg.Destroy()        
        

    def OnMnuFilePrint(self, event):
        """
        Print the current diagram
        """
        if not self._ctrl.getDiagram():
            displayWarning(("No diagram to print !"), ("Error"), self)
            return
        self._ctrl.deselectAllShapes()
        datas=wx.PrintDialogData()
        datas.SetPrintData(self._printData)
        datas.SetMinPage(1)
        datas.SetMaxPage(1)
        printer=wx.Printer(datas)
        printout = Printout(self._ctrl.getUmlFrame())
        if not printer.Print(self, printout, True):
            if printer.GetLastError() == wx.PRINTER_CANCELLED:
                displayWarning(("No diagram to print !"), ("Error"))
                
            elif printer.GetLastError() == wx.PRINTER_ERROR:
                displayWarning(("No diagram to print !"), ("Error"))

    def _loadFile(self, filename=""):
        """
        load the specified filename
        """

        # Make a list to be compatible with multi-files loading
        filenames = [filename]

        # Ask which filename to load ?
        if filename=="":
            dlg=wx.FileDialog(self, ("Choose a file"), self._lastDir, "", "*.xml", wx.FD_OPEN | wx.FD_MULTIPLE)
            if dlg.ShowModal() != wx.ID_OK:
                dlg.Destroy()
                return False
            self.updateCurrentDir(dlg.GetPath())
            filenames=dlg.GetPaths()
            dlg.Destroy()
            
        # Open the specified files
        for filename in filenames:
            try:
                if self._fileHandling.openFile(filename):
                    # Add to last opened files list
                    self._ctrl.updateTitle()
            except:
                displayWarning(("An error occured while loading the project !"),  ("Error"))
                
                
    def _saveFile(self):
        """
        save to the current filename

        """
        self._fileHandling.saveFile()
        self._ctrl.updateTitle()

    def _saveFileAs(self):
        """
        save to the current filename; Ask for the name
        """
        self._fileHandling.saveFileAs()
        self._ctrl.updateTitle()

    def Close(self, force=False):
        """
        Closing handler overload. Save files and ask for confirmation.
        """
        #Close all files
        if self._fileHandling.onClose()==False:
            return

        self._clipboard = None
        self._fileHandling = None
        self._ctrl = None
        self._prefs = None
        self.plugMgr = None
        self._printData.Destroy()
        self.Destroy()
        
    def OnNewAction(self, event):
        """
        Call the mediator to specifiy the current action.

        @param wxEvent event
        """
        self._ctrl.setCurrentAction(mediatorParameter.ACTIONS[event.GetId()])
        self._fileHandling.setModified(True)
        self._ctrl.updateTitle()
        
    def OnMnuEditCut(self, event):
        """
        Callback.
        """
        self._ctrlVP.OnMnuEditCut()
        
    def OnMnuEditCopy(self, event):
        """
        Callback.
        """
        self._ctrlVP.OnMnuEditCopy()
        
    def OnMnuEditPaste(self, event):
        """
        Callback.
        """
        self._ctrlVP.OnMnuEditPaste()
        
        
    def OnMnuUndo(self, event):
        if (self._fileHandling.getCurrentFrame()) is None:
            displayWarning(("No current project to undo"), ("No undo"))
            return 
        self._fileHandling.getCurrentFrame().getHistory().undo()
         
 
    def OnMnuRedo(self, event):
        if (self._fileHandling.getCurrentFrame()) is None:
            displayWarning(("No current project to redo"), ("No redo"))
            return
        self._fileHandling.getCurrentFrame().getHistory().redo()
        