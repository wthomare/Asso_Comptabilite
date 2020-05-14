# -*- coding: utf-8 -*-
import os

import AssoComptaUtils


execPath = os.getcwd()
userPath = os.getcwd()

def main():
    """
    main pyut function; create and run app

    @param string name : init name with the name
    """
    import os, sys
    global execPath, userPath

    # Path
    try:
        sys.path.append(execPath)
        os.chdir(execPath)
    except OSError as msg:
        AssoComptaUtils.displayError("Error while setting path: ", msg)


    from AssoComptaApp import BasicSoftwareApp
    app = BasicSoftwareApp(0)
    app.MainLoop()
    app = None
    
if __name__ == "__main__":
    execPath = os.getcwd()
    main()