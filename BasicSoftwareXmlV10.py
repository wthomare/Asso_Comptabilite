# -*- coding: utf-8 -*-

from BasicSoftwareConst         import diagramTypeAsString, SEQUENCE_DIAGRAM, OBJECT_NAME
from BasicSoftwareSDInstance    import BasicSoftwareSDInstance
from BasicSoftwareUtils         import displayError
from BasicSoftwareSuperObject   import BasicSoftwareSuperObject
from BasicSoftwareLink          import BasicSoftwareLink

# reading file

from OglSDInstance              import OglSDInstance
from OglLink                    import OglLink
from OglNote                    import OglNote
from OglTitle                   import OglTitle
from OglTitleEnd                import OglTitleEnd
from OglFor                     import OglFor
from OglWhile                   import OglWhile
from OglFixLog                  import OglFixLog
from OglImport                  import OglImport
from OglLog                     import OglLog
from OglStatement               import OglStatement


from MiniOgl.ControlPoint      import ControlPoint
import wx
import OglObjectFactory
import OglLinkFactory

class IDFactory:
    nextID=1
    def __init__(self):
        self._dicID = {}
        
    def getID(self, aclass):
      
        if aclass in self._dicID:
            return self._dicID[aclass]
        else:
            id = IDFactory.nextID
            self._dicID[aclass] = id
            IDFactory.nextID+=1
            return id
        
class BasicSoftwareXml:
    """
    Class for saving and loading a PyUT UML diagram in XML.
    This class offers two main methods that are save() and load().
    Using the dom XML model, you can, with the saving method, get the
    diagram corresponding XML view. For loading, you have to parse
    the file and indicate the UML frame on which you want to draw
    (See `UmlFrame`).

    Sample use::

        # Write
        pyutXml = PyutXml()
        text = pyutXml.save(oglObjects)
        file.write(text)

        # Read
        dom = parse(StringIO(file.read()))
        pyutXml = PyutXml()
        myXml.open(dom, umlFrame)

    """

    def __init__(self):
        """
        Constructor
        @author C.Dutoit
        """
        self._idFactory = IDFactory()
        
    def _BasicSoftwareSDInstance2xml(self, basicSoftwareSDInstance, xmlDoc):
        """
        Exporting an BasicSoftwareSDInstance to an minidom Element.
        """
        root = xmlDoc.createElement("SDInstance")
        Id = self._idFactory.getID(basicSoftwareSDInstance)
        root.setAttribute('id', str(Id))
        root.setAttribute('instanceName', str(basicSoftwareSDInstance.getInstanceName()))
        root.setAttribute('lifeLineLength', str(basicSoftwareSDInstance.getLifeLineLength()))
        return root
    
    def _OglSDInstance2xml(self, oglSDInstance, xmlDoc):
        """
        Exporting an OglSDInstance to a miniDom Element.
        """
        root = xmlDoc.createElement('GraphicSDInstance')
        self._appendOglBase(oglSDInstance, root)
        root.appendChild(self._BasicSoftwareSDInstance2xml(oglSDInstance.getBasicSoftware(), xmlDoc))
        return root
    
    def _BasicSoftwareField2xml(self, basicSoftwareField, xmlDoc):
        """
        Exporting an BasicSoftwareField to an minidom Element.
        """
        root = xmlDoc.createElement("Field")
        root.appendChild(self._BasicSoftwareParam2xml(basicSoftwareField, xmlDoc))
        root.setAttribute("visibility", basicSoftwareField.getVisibility())
        return root

    def _BasicSoftwareParam2xml(self, basicSoftwareParam, xmlDoc):
        root = xmlDoc.createElement("Param")
        
        root.setAttribute("name", basicSoftwareParam.getName())
        root.setAttribute("type", basicSoftwareParam.getType())
        defaultValue = basicSoftwareParam.getDefaultValue()
        if defaultValue:
            root.setAttribute("defaultValue", defaultValue)
        return root
    
    def _BasicSoftwareLink2xml(self, basicSoftwareLink, xmlDoc):
        """
        Exporting an BasicSoftwareLink to an minidom Element.        
        """
        root = xmlDoc.createElement("Field")
        
        root.setAttribute("name", str(basicSoftwareLink.getName()))
        root.setAttribute("tyoe", str(basicSoftwareLink.getType()))
        root.setAttribute("price", str(basicSoftwareLink.getPrice()))
        root.setAttribute("quantity", str(basicSoftwareLink.getQty()))
        root.setAttribute("way", str(basicSoftwareLink.getWay()))
        root.setAttribute("account", str(basicSoftwareLink.getAccount()))
        root.setAttribute("cltType", str(basicSoftwareLink.getCltType()))
        root.setAttribute("restriction", str(basicSoftwareLink.getRestriction()))
        root.setAttribute("validity", str(basicSoftwareLink.getValidity()))
        root.setAttribute("prceMode", str(basicSoftwareLink.getPrcMode()))
        root.setAttribute("relation", str(basicSoftwareLink.getRelationship()))
        root.setAttribute("waiting", str(basicSoftwareLink.getWaitingTime()))
        root.setAttribute("answer", str(basicSoftwareLink.getExpectAnswer()))

        Id  = self._IdFactory.getID(basicSoftwareLink.getSource())
        root.setAttribute("sourceId", str(Id))
        
        Id  = self._IdFactory.getID(basicSoftwareLink.getDestination())
        root.setAttribute("destId", str(Id))

        return root

    def _BasicSoftwareSuperObject2xml(self, basicSoftwareSuperObject, xmlDoc):
         
        root = xmlDoc.createElement(OglObjectFactory.getName(basicSoftwareSuperObject))

        Id = self._idFactory.getID(basicSoftwareSuperObject)
        root.setAttribute("id", str(Id))
        
        name = str(basicSoftwareSuperObject.getName())
        name = name.replace('\n','\\\\\\\\')
        root.setAttribute("name", name)
        
        root.setAttribute("type", str(basicSoftwareSuperObject.getType()))
        root.setAttribute("pollTimeout", str(basicSoftwareSuperObject.getPollTimeout()))
        root.setAttribute("timeout", str(basicSoftwareSuperObject.getTtmeout()))
        root.setAttribute("dataFormat", str(basicSoftwareSuperObject.getDataFormat()))
        root.setAttribute("unitTestInst", str(basicSoftwareSuperObject.getUnitTestInst()))
        root.setAttribute("logFilesList", str(basicSoftwareSuperObject.getLogFilesList()))
        root.setAttribute("fieldsToExclude", str(basicSoftwareSuperObject.getFieldsToExclude()))
        root.setAttribute("fieldsToCheck", str(basicSoftwareSuperObject.getFieldsToCheck()))
        root.setAttribute("function", str(basicSoftwareSuperObject.getFunction()))
        root.setAttribute("pattern", str(basicSoftwareSuperObject.getPattern()))
        root.setAttribute("message", str(basicSoftwareSuperObject.getMessage()))
        root.setAttribute("path", str(basicSoftwareSuperObject.getPath()))
        root.setAttribute("statement", str(basicSoftwareSuperObject.getStatement()))
        root.setAttribute("instruction", str(basicSoftwareSuperObject.getInstruction()))
        root.setAttribute("ObjectType", str(basicSoftwareSuperObject.getInstanceTitleType()))

        root.setAttribute("txttwo", str(basicSoftwareSuperObject.getTxttwo()))
        root.setAttribute("txttwo2", str(basicSoftwareSuperObject.getTxttwo2()))
        root.setAttribute("txtthree", str(basicSoftwareSuperObject.getTxtthree()))
        root.setAttribute("txtthree2", str(basicSoftwareSuperObject.getTxtthree2()))
        root.setAttribute("ccbthree", str(basicSoftwareSuperObject.getccbThree()))

        return root
    
    def _appendOglBase(self, oglObject, root):
        """
        Saves the position and size of the OGL object in XML node.
        """
        w, h = oglObject.GetModel().GetSize()
        root.setAttribute("width", str(w))
        root.setAttribute("height", str(h))
        
        x, y = oglObject.GetModel().GetPosition()
        root.setAttribute("x", str(x))
        root.setAttribute("y", str(y))
        
    def _OglLink2xml(self, oglLink, xmlDoc):
        
        root = xmlDoc.createElement("GraphicLink")

        x, y = oglLink.GetSource().GetModel().GetPosition()
        root.setAttribute("srcX", str(x))
        root.setAttribute("srcY", str(y))

        x, y = oglLink.GetDestination().GetModel().GetPosition()
        root.setAttribute("dstX", str(x))
        root.setAttribute("dstY", str(y))
        root.setAttribute("spline", str(oglLink.GetSpline()))
        
        for x,y in oglLink.GetSegments()[1:-1]:
            item = xmlDoc.createElement('ControlPoint')
            item.setAttribute('x', str(x))
            item.setAttribute('y', str(y))
            root.appendChild(item)
        
        root.appendChild(self._BasicSoftwareLink2xml(oglLink.getBasicSoftwareSuperObject(), xmlDoc))
        return root
    
    def _OglNote2xml(self, oglNote, xmlDoc):
        
        root = xmlDoc.createElement("GraphicNote")

        self._appendOglBase(oglNote, root)
        root.appendChild(self._BasicSoftwareSuperObject2xml(oglNote.getBasicSoftwareSuperObject(), xmlDoc))
        return root
    
    def _OglImport2xml(self, oglImport, xmlDoc):
        
        root = xmlDoc.createElement("GraphicInsert")
        self._appendOglBase(oglImport, root)
        
        root.appendChild(self._BasicSoftwareSuperObject2xml(oglImport.getBasicSoftwareSuperObject(), xmlDoc))
        return root
    
    def _OglFixLog2xml(self, oglFixLog, xmlDoc):
        
        root = xmlDoc.createElement("GraphicFixLog")
        
        self._appendOglBase(oglFixLog, root)
        root.appendChild(self._BasicSoftwareSuperObject2xml(oglFixLog.getBasicSoftwareSuperObject(), xmlDoc))
        return root
        
    def _OglLog2xml(self, oglLog, xmlDoc):

        root = xmlDoc.createElement("GraphicLog")
        
        self._appendOglBase(oglLog, root)
        root.appendChild(self._BasicSoftwareSuperObject2xml(oglLog.getBasicSoftwareSuperObject(), xmlDoc))
        return root
        
    def _OglTitle2xml(self, oglTitle, xmlDoc):
        root = xmlDoc.createElement("GraphicTitle")

        self._appendOglBase(oglTitle, root)
        root.appendChild(self._BasicSoftwareSuperObject2xml(oglTitle.getBasicSoftwareSuperObject(), xmlDoc))
        return root

    def _OglTitleEnd2xml(self, oglTitle, xmlDoc):
        root = xmlDoc.createElement("GraphicTitleEnd")

        self._appendOglBase(oglTitle, root)
        root.appendChild(self._BasicSoftwareSuperObject2xml(oglTitle.getBasicSoftwareSuperObject(), xmlDoc))
        return root

    def _OglFor2xml(self, oglFor, xmlDoc):
        root = xmlDoc.createElement("GraphicFor")

        self._appendOglBase(oglFor, root)
        root.appendChild(self._BasicSoftwareSuperObject2xml(oglFor.getBasicSoftwareSuperObject(), xmlDoc))
        return root

    def _OglWhile2xml(self, oglWhile, xmlDoc):
        root = xmlDoc.createElement("GraphicWhile")

        self._appendOglBase(oglWhile, root)
        root.appendChild(self._BasicSoftwareSuperObject2xml(oglWhile.getBasicSoftwareSuperObject(), xmlDoc))
        return root

    def _OglStatement2xml(self, oglStatement, xmlDoc):
        root = xmlDoc.createElement("GraphicStatement")

        self._appendOglBase(oglStatement, root)
        root.appendChild(self._BasicSoftwareSuperObject2xml(oglStatement.getBasicSoftwareSuperObject(), xmlDoc))
        return root

    def save(self, project):
        from xml.dom.minidom import Document
        gauge, dlg = None, None             
        
        try:
            xmlDoc = Document()
            top = xmlDoc.createElement('BasicSoftwareProject')
            top.setAttribute("version", "10")
            xmlDoc.appendChild(top)
            
            dlg = wx.Dialog(None, wx.ID_ANY, 'Saving ...', style=wx.STAY_ON_TOP|wx.CAPTION, size=wx.Size(207,70))
            gauge = wx.Gauge(dlg, wx.ID_ANY, 100, pos=wx.Point(2,5), size=wx.Size(200,30))
            
            for document in project.getDocuments():
                documentNode = xmlDoc.createElement("BasicSoftwareDocument")
                documentNode.setAttribute('type', diagramTypeAsString(document.getType()))
                top.appendChild(documentNode)
                
                oglObjects = document.getFrame().getUmlObjects()
                for i in range(len(oglObjects)):
                    gauge.SetValue(i*100/len(oglObjects))
                    oglObject = oglObjects[i]
                    if isinstance(oglObject, OglNote):
                        documentNode.appendChild(self._OglNote2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglTitle):
                        documentNode.appendChild(self._OglTitle2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglTitleEnd):
                        documentNode.appendChild(self._OglTitleEnd2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglFor):
                        documentNode.appendChild(self._OglFor2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglWhile):
                        documentNode.appendChild(self._OglWhile2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglLink):
                        documentNode.appendChild(self._OglLink2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglSDInstance):
                        documentNode.appendChild(self._OglSDInstance2xml(oglObject, xmlDoc))    
                    elif isinstance(oglObject, OglStatement):
                        documentNode.appendChild(self._OglStatement2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglFixLog):
                        documentNode.appendChild(self._OglFixLog2xml(oglObject, xmlDoc))                        
                    elif isinstance(oglObject, OglImport):
                        documentNode.appendChild(self._OglImport2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglLog):
                        documentNode.appendChild(self._OglLog2xml(oglObject, xmlDoc))
        except:
            try:
                dlg.Destroy()
            except:
                msg = "Save error"
                displayError(msg, 'BasicSoftwareXML.save Error')
            finally:
                return xmlDoc
        dlg.Destroy()
        return xmlDoc
    
    def _getOglSDInstances(self, xmlOglSDInstances, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for basicSoftware classes.
        """
        
        for xmlOglSDInstance in xmlOglSDInstances:
            basicSoftwareSDInstance = BasicSoftwareSDInstance()
            oglSDInstance = OglSDInstance(basicSoftwareObject = basicSoftwareSDInstance, parentFrame=umlFrame)
            
            xmlSDInstance = xmlOglSDInstance.getElementsByTagName('SDInstance')[0]
            
            basicSoftwareSDInstance.setId(int(xmlSDInstance.getAttribute('id')))
            basicSoftwareSDInstance.setInstanceName(xmlSDInstance.getAttribute('instanceName'))
            basicSoftwareSDInstance.setInstanceLifeLineLength(eval(xmlSDInstance.getAttribute('lifeLineLength').encode('utf8')))
            dicoOglObjects[basicSoftwareSDInstance.getId()] = oglSDInstance
            
            x = eval(xmlOglSDInstance.getAttribute('x').encode('utf8'))
            y = eval(xmlOglSDInstance.getAttribute('y').encode('utf8'))
            w = eval(xmlOglSDInstance.getAttribute('width').encode('utf8'))
            h = eval(xmlOglSDInstance.getAttribute('height').encode('utf8'))
            oglSDInstance.SetSize(w,h)
            umlFrame.addShape(oglSDInstance, x, y)
            
    def _getControlPoints(self, link):
        allControlPoints = []
        for cp in link.getElementsByTagName('ControlPoint'):
            x, y = cp.getAttribute('x'), cp.getAttribute('y')
            point = ControlPoint(x,y)
            allControlPoints.append(point)
        return allControlPoints
    
    def _getBasicSoftwareLink(self, obj):
        
        link = obj.getElementsByTagName("Link")[0]
        
        aLink = BasicSoftwareLink()
        aLink.setName(link.getAttribute("name").encode('utf8'))
        aLink.setType(int(link.getAttribute("name").encode('utf8')))
        aLink.setQty(link.getAttribute("name").encode('utf8'))
        aLink.setPrice(link.getAttribute("name").encode('utf8'))
        aLink.setWay(link.getAttribute("name").encode('utf8'))
        aLink.setAccount(link.getAttribute("name").encode('utf8'))
        aLink.setRestriction(link.getAttribute("name").encode('utf8'))
        aLink.setCltType(link.getAttribute("name").encode('utf8'))
        aLink.setValidity(link.getAttribute("name").encode('utf8'))
        aLink.setPrcMode(link.getAttribute("name").encode('utf8'))
        aLink.setRelationship(link.getAttribute("name").encode('utf8'))
        aLink.setWaitingTime(link.getAttribute("name").encode('utf8'))
        aLink.setExpectAnswer(link.getAttribute("name").encode('utf8'))
        
        sourceId = int(link.getAttribute('sourceId'))
        dstId = int(link.getAttribute('dstId'))
        return sourceId, dstId, aLink
    
    def _getOglLinks(self, xmlOglLinks, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        
        for link in xmlOglLinks:
            
            sx = eval(link.getAttribute('srcX').encode('utf8'))
            sy = eval(link.getAttribute('srcY').encode('utf8'))            
            dx = eval(link.getAttribute('dstX').encode('utf8'))            
            dy = eval(link.getAttribute('dstX').encode('utf8'))
            spline = int(eval(link.getAttribute('spline').encode('utf8')))
            
            ctrlpts = []
            for ctrlpt in link.getElementsByTagName("ControlPoint"):
                x = eval(ctrlpt.getAttribute("x").encode("utf8"))
                y = eval(ctrlpt.getAttribute("y").encode("utf8"))
                ctrlpts.append(ControlPoint(x,y).encode('utf8'))
                
            srcId, dstId, basicSoftwareLink = self._getBasicSoftwareLink(link)
            src = dicoOglObjects[srcId]
            dst = dicoOglObjects[dstId]
            linkType = int(basicSoftwareLink.getType())
            oglLinkFactory = OglLinkFactory.getOglLinkFactory()
            oglLink = oglLinkFactory.getOglLink(src, basicSoftwareLink, dst, linkType)
            src.addLink(oglLink)
            dst.addLink(oglLink)
            umlFrame.GetDiagram().AddShape(oglLink, withModeUpdate=False)
            
            oglLink.SetSpline(spline)
            
            srcAnchor = oglLink.GetSource()
            dstAnchor =oglLink.GetDestination()
            srcAnchor.SetPosition(sx, sy)
            dstAnchor.SetPosition(dx, dy)
            
            line = srcAnchor.GetLines()[0]
            parent = line.GetSource().GetParent()
            selfLink = parent is line.GetDestination().GetParent()
            
            for ctrl in ctrlpts:
                line.AddControl(ctrl)
                if selfLink:
                    x, y = ctrl.GetPosition()
                    ctrl.SetParent(parent)
                    ctrl.SetPosition(x, y)
                    
        def _getOglSuperObject(self, xmlOglSuperObjects, dicoOglObjects, dicoLink, dicoFather, umlFrame):
            for xmlOglSuperObject in xmlOglSuperObjects:
                basicSoftwareSuperObject = BasicSoftwareSuperObject()
                
                height = eval(xmlOglSuperObject.getAttribute('height').encode('utf8'))
                width = eval(xmlOglSuperObject.getAttribute('width').encode('utf8'))
                
                for BasicSoftwareType in OBJECT_NAME:
                    if xmlOglSuperObject.getElementsByTagName(BasicSoftwareType):
                        xmlSuperObject = xmlOglSuperObject.getElementByTagName(BasicSoftwareType)[0]               
                        Type = int(xmlSuperObject.getAttribute('type').encode('utf8'))
                        name = xmlSuperObject.getAttribute('name')
                        name = name.replace("\\\\\\\\", "\n")
                        
                        basicSoftwareSuperObject.setId(int(xmlSuperObject.getAttribute('id')))
                        
                        basicSoftwareSuperObject.setName(xmlSuperObject.getAttribute('name').encode('utf8'))
                        basicSoftwareSuperObject.setFilename(xmlSuperObject.getAttribute('filename').encode('utf8'))
                        basicSoftwareSuperObject.setType(int(xmlSuperObject.getAttribute('type').encode('utf8')))
                        basicSoftwareSuperObject.setTxtTwo(xmlSuperObject.getAttribute('txttwo').encode('utf8'))
                        basicSoftwareSuperObject.setTxtTwo2(xmlSuperObject.getAttribute('txttwo2').encode('utf8'))
                        basicSoftwareSuperObject.setTxtThree(xmlSuperObject.getAttribute('txtthree').encode('utf8'))
                        basicSoftwareSuperObject.setTxtThree2(xmlSuperObject.getAttribute('txtthree2').encode('utf8'))
                        basicSoftwareSuperObject.setccbThree(xmlSuperObject.getAttribute('ccbthree').encode('utf8'))
                        basicSoftwareSuperObject.setPollTimeout(xmlSuperObject.getAttribute('pollTimeout').encode('utf8'))
                        basicSoftwareSuperObject.setDataFormat(xmlSuperObject.getAttribute('timeout').encode('utf8'))
                        basicSoftwareSuperObject.setUnitTestInst(xmlSuperObject.getAttribute('dataFormat').encode('utf8'))
                        basicSoftwareSuperObject.setLogFilesList(xmlSuperObject.getAttribute('unitTestInst').encode('utf8'))
                        basicSoftwareSuperObject.setFieldsToExclude(xmlSuperObject.getAttribute('fieldsToExclude').encode('utf8'))
                        basicSoftwareSuperObject.setFieldsToCheck(xmlSuperObject.getAttribute('fieldsToCheck').encode('utf8'))
                        basicSoftwareSuperObject.setFunction(xmlSuperObject.getAttribute('function').encode('utf8'))
                        basicSoftwareSuperObject.setPattern(xmlSuperObject.getAttribute('pattern').encode('utf8'))
                        basicSoftwareSuperObject.setLogMessage(xmlSuperObject.getAttribute('message').encode('utf8'))
                        basicSoftwareSuperObject.setStatement(xmlSuperObject.getAttribute('statement').encode('utf8'))
                        basicSoftwareSuperObject.setInstruction(xmlSuperObject.getAttribute('instruction').encode('utf8'))
                        basicSoftwareSuperObject.setPath(xmlSuperObject.getAttribute('path').encode('utf8'))
                        basicSoftwareSuperObject.setInstanceTitleType(xmlSuperObject.getAttribute('ObjectType').encode('utf8'))
                        
                        oglObjectFactory = OglObjectFactory.getOglObjectFactory()
                        oglObject = oglObjectFactory.getOglObject(basicSoftwareSuperObject, Type, width,height)
                        
                        dicoOglObjects[basicSoftwareSuperObject.getId()] = oglObject()
                        
                        x = eval(xmlOglSuperObject.getAttribute('x').encode('utf8'))
                        y = eval(xmlOglSuperObject.getAttribute('y').encode('utf8'))
                        umlFrame.addShape(oglObject, x, y)
                        
    def open(self, dom, project, gg = True):
        """
        To open a file and creating diagram
        """
        
        dlgGauge, gauge = None, None
        try:
            if gg:
                dlgGauge = wx.Dialog(None, wx.ID_ANY, "Loading ...", style=wx.STAY_ON_TOP|wx.CAPTION, size = wx.Size(207, 70))
                gauge = wx.Gauge(dlgGauge, wx.ID_ANY, 5, pos=wx.Point(2, 5), size=wx.Size(200, 30))
                dlgGauge.Show()
                
                dlgGauge.SetTitle("Reading file ...")
                gauge.SetValue(1)
                
            for documentNode in dom.getElementsByTagName("basicSoftwareDocument"):
                dicoOglObjects = {}
                dicoLink = {}
                dicoFather = {}
                document = project.newDocument(SEQUENCE_DIAGRAM)
                umlFrame = document.getFrame()
                
                for GraphicSuperObject in ['GraphicNote', 'GraphicTitle', 'GraphicFor', 'GraphicWhile', 'GraphicStatement', 'GraphicFixLog', 'GraphicInsert', 'GraphicLog']:
                    self._getOglSuperObject(documentNode.getElementsByTagName(GraphicSuperObject), dicoOglObjects, dicoLink, dicoFather, umlFrame)
                
                self._getOglSDInstances(documentNode.getElementsByTagName("GraphicSDInstance"), dicoOglObjects, dicoLink, dicoFather, umlFrame)
                self._getOglLinks(documentNode.getElementsByTagName("GraphicLink"), dicoOglObjects, dicoLink, dicoFather, umlFrame)
                
                if gg:
                    gauge.SetValue(2)
                    dlgGauge.SetTitle("Fixing link's destination ...")
                for links in dicoLink.values():
                    for link in links:
                        link[1].setDestination(dicoOglObjects[link[0].getBasicSoftwareObject()])
                    if gg:
                        dlgGauge.SetTitle("Adding fathers ...")
                        gauge.SetValue(3)
                    for child, fathers in dicoFather.items():
                        for father in fathers:
                            umlFrame.createInheritanceLink(dicoOglObjects[child], dicoOglObjects[father])
                        
                    if gg:
                        dlgGauge.SetTitle("Adding Links ...")
                        gauge.SetValue(4)
                    for src, links in dicoLink.items():
                        for link in links:
                            createdLink = umlFrame.createNewLink(dicoOglObjects[src], dicoOglObjects[link[1].getDestination().getId()], link[1].getType())
                        
                            basicSoftware = createdLink.getBasicSoftwareObject()
                            basicSoftware.setDestCard(link[1].getDestCard())
                            basicSoftware.setSrcCard(link[1].getSrcCard())
                            basicSoftware.setName(link[1].getName())
        except:
            
            if dlgGauge: dlgGauge.Destroy()
            msg = "Error while loading a XML file"
            displayError(msg, "ProphetXML.open Error")
            return
            
            umlFrame.Refresh()
            if gg:
                gauge.SetValue(5)
                if dlgGauge: dlgGauge.Destroy()