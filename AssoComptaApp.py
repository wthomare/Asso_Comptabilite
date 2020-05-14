# -*- coding: utf-8 -*-

from AppFrame import RibbonFrame
from wx.adv import SplashScreen
import wx, os
import AssoComptaUtils


class BasicSoftwareApp(wx.App):
    """
    BasicSoftware : main BasicSoftware application class.
    BasicSoftware is the main application, a wxApp.
    Called from BasicSoftware.pyw
    """
    
    def __init__(self, val, splash=True, show=True):
        self._showSplash = splash
        self._showMainFrame = show
        wx.App.__init__(self, val)
        
    def OnInit(self):
        """
        Constructor.
        """
        provider = wx.SimpleHelpProvider()
        wx.HelpProvider.Set(provider)

        try:
            #Create the SplashScreen
            if self._showSplash:
                wx.InitAllImageHandlers()
                imgPath = "img" + os.sep + "logo_princ.png"
                img = wx.Image(imgPath)
                bmp = img.ConvertToBitmap()
                self.splash=SplashScreen(bmp, wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT, 60, None, -1)
                
                if self._showSplash:
                    self.splash.Show(True)
                    wx.Yield()

            #Create the application
            self._frame=RibbonFrame(parent = None, id=wx.ID_ANY, title='BasicSoftware', size=(1280,900))
            self.SetTopWindow(self._frame)

            if self._showSplash:
                self.splash.Show(False)
            self._AfterSplash()

            return True
        except: #Display all errors
            msg = "Failed to init the software"
            AssoComptaUtils.displayError(msg, "BasicSoftwareApp.OnInit Error")
            return False

    def _AfterSplash(self):
        """
        AfterSplash : Occure after the splash screen; launch the application
        BasicSoftwareApp : main BasicSoftware application class
    
        """
        try:
            if self._showMainFrame:
                self._frame.Show(True)
            
            if self._showSplash:
                self.splash.Close()
            
            return True
        except:
            msg = "Failed to launch the qfterSplash screen"
            AssoComptaUtils.displayError(msg, 'BasicSoftware.AfterSplash Error')
            
    
    def OnExit(self):
        self.__do   = None
        self._frame  = None
        self.splash = None
        # Seemed to be removed in latest versions of wxPython ???
        try:
            return wx.App.OnExit(self)
        except:
            pass
