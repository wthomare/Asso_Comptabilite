# -*- coding: utf-8 -*-
import os

import BasicSoftwareUtils


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
        BasicSoftwareUtils.displayError("Error while setting path: ", msg)


    from BasicSoftwareApp import BasicSoftwareApp
    app = BasicSoftwareApp(0)
    app.MainLoop()
    app = None
    
if __name__ == "__main__":
    execPath = os.getcwd()
    main()