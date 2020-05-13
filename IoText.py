# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 00:13:36 2020

@author: wilfr
"""

# -*- coding: utf-8 -*-

from mediator  import getMediator
import BasicSoftwareConsts
import BasicSoftwareXmlV10

class IoText(object):
    """
    To save datas in a compressed file format.
    IoFile is used to save or read Pyut file format who's
    are named *.put.


    Example::
        IoFile = io()
        io.save("myFileName.put", project)  # to save diagram
        io.open("pyFileName.put", project)    # to read file

    """
    def save(self, project):
        """
        To save save diagram in XML file.
        """
        import os
        oldpath = os.getcwd()
        path = getMediator().getAppPath()
        os.chdir(path)
        myXml = BasicSoftwareXmlV10.BasicSoftwareXml()
        doc = myXml.save(project)
        text = doc.toprettyxml()

        text = text.replace(r'<?xml version="1.0" ?>', r'<?xml version="1.0" encoding="iso-8859-1"?>')

        with open(project.getFilename(), "w") as file:
            file.write(text)
        os.chdir(oldpath)

    #>------------------------------------------------------------------------

    def open(self, filename, project):
        """
        To open a compressed file and create diagram.

        """
        import os

        oldpath = os.getcwd()
        path = getMediator().getAppPath()
        os.chdir(path)
        
        from xml.dom.minidom import parseString
        xmlString = ""
        if filename[-4:]=='.xml':
            with open(filename, "rb") as f:
                xmlString = f.read()
        else:
            print("not a xml file")
        
        dom = parseString(xmlString)
        myXml = BasicSoftwareXmlV10.BasicSoftwareXml()
        myXml.open(dom, project)
        
        os.chdir(oldpath)
