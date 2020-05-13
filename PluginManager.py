from glob import glob
import os, sys

from BasicSoftwareUtils import displayError

class PluginManager():
    """
    Interface between the application and the plugins.

    This class is responsible to search for available plugins, load them,
    extract runtime information and give the information to those who need it
    (for example the `AppFrame` to create the import/export submenus).
    """
    def __init__(self):
        """
        Singleton Constructor.
        At init time, this class searches for the plugins in the plugins
        directory.
        """
        # Init
        self.ioPlugs = []
        self.toPlugs = []
        # get the file names
        try:
            os.chdir("plugins")
        except:
            dirn = os.path.dirname(__file__)
            filename = os.path.join(dirn, 'plugins')
            os.chdir(filename)

        sys.path.append(os.getcwd())
        ioPlugs = glob("Io*.py")
        toPlugs = glob("To*.py")
        os.chdir(os.pardir)

        # remove extension
        ioPlugs = map(lambda x: os.path.splitext(x)[0], ioPlugs)
        toPlugs = map(lambda x: os.path.splitext(x)[0], toPlugs)

        # Import I/O plugins
        for plug in ioPlugs:
            module = None
            try:
                module = __import__(plug)
            except:
                msg = 'Error importing plugin [%s] with message' %(plug)
                displayError(msg, 'Import module Error')
                
            if module:
                cl = eval("module.%s" % (module.__name__))
                self.ioPlugs.append(cl)

        # Import tools plugins
        for plug in toPlugs:
            module = None
            try:
                module = __import__(plug)
            except:
                msg = 'Error importing plugin [%s] with message' %(plug)
                displayError(msg, 'Import module Error')
                
            if module is not None:
                cl = eval("module.%s" % (module.__name__))
                self.toPlugs.append(cl)

    #>------------------------------------------------------------------------

    def getPluginsInfo(self):
        """
        Get textual information about available plugins.

        @return String []
        """
        s = []
        for plug in self.ioPlugs + self.toPlugs:
            obj = plug(None, None)
            s.append("Plugin : %s version %s (c) by %s" % (obj.getName(), obj.getVersion(), obj.getAuthor()))
        return s

    #>------------------------------------------------------------------------

    def getInputPlugins(self):
        """
        Get the input plugins.
        Returns a list of classes (the plugins classes).

        @return Class []
        """
        s = []
        for plug in self.ioPlugs:
            obj = plug(None, None)
            if obj.getInputFormat() is not None:
                s.append(plug)
        return s

    #>------------------------------------------------------------------------

    def getOutputPlugins(self):
        """
        Get the output plugins.
        Returns a list of classes (the plugins classes).

        @return Class []
        """
        s = []
        for plug in self.ioPlugs:
            obj = plug(None, None)
            if obj.getOutputFormat() is not None:
                s.append(plug)
        return s

    #>------------------------------------------------------------------------
    
    def getToolPlugins(self):
        """
        Get the tool plugins.
        Returns a list of classes (the plugins classes).

        @return Class []
        """
        return self.toPlugs

    #>------------------------------------------------------------------------

def test():
    p = PluginManager()
    for info in p.getPluginsInfo():
        print(info)

if __name__ == "__main__": test()
