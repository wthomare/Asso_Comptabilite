# -*- coding: utf-8 -*-
import commandGroup
from historyUtils import getTokenValue, HISTORY_FILE_NAME, GROUP_COMMENT_ID
import AssoComptaUtils

[upDate, create, delete, copy]=range(4)

class HistoryManager(object):
    """
    This class is the structure that manage the history of a given frame.
    It creates a file where are stored serialized 'CommandGroups' that
    are compound of commands. Each command is able to do the undo/redo
    operations and is also able to serialize/unserialize itself
    (See commandGroup and command).
    To see how it works, please see UnitTestHistory
    """
    
    #defines an unique id that will be added to the file base name
    #in order to have a unique file associated to each instance of
    #the history.
    historyId = 0

    
    def __init__(self, frame = None):        
        self._frame = frame
        
        #name of file for hard storage which is unique for each history
        self._fileName = (HISTORY_FILE_NAME + str(self.__class__.historyId))
        
        #for the next instance of the history...               
        self.__class__.historyId += 1

        #create the file to store the groups
        try:
            saveFile = open(self._fileName, 'w').close()
        except PermissionError:
            AssoComptaUtils.displayError("Permission Error. The History file [%s] is opened by a tier" %(self._fileName), "HistoryManager.__init__ Error")
        #number of groups added to the histroy
        self._groupCount = 0

        #index of the command group that will be undone
        self._groupToUndo = -1

        #reference to the last added group, for execute() mehtod
        self._groupToExecute = None
        
    def undo(self):
        """
        undo the current group command and make the previous one as current.
        """
        
        #check if there is a group to undo
        if self.isUndoPossible():
            
            # open the file to get its current content in a list
            with open(self._fileName, 'r') as saveFile:
                fileContent = saveFile.readlines()

            #unserialize the group to undo
            group, action = self._unserialize(fileContent[self._groupToUndo])
            group.setHistory(self)
            
            #undo all the commands that are in the group
            group.undo()
            
            if action == upDate:
                oldGroup = self._findOldGroup(fileContent[self._groupToUndo])
                if oldGroup:
                    group.redoUpDate(oldGroup)
                    self._groupToUndo -=1
            else:    
                # set the previous command as the command to be undone
                self._groupToUndo -= 1
                
    def redo(self):
        """
        take from the file the last undone command group and redo it.
        """
        #check if there is a group to redo
        if self.isRedoPossible():
            
            # open the file to get its current content in a list
            with open(self._fileName, 'r') as saveFile:                
                fileContent = saveFile.readlines()

            #the group to redo means that it will be the group to undo
            self._groupToUndo += 1

            #unserialize the group
            group, action = self._unserialize(fileContent[self._groupToUndo])
            group.setHistory(self)
            
            if action in [create, delete, copy]:
                #redo all the commands in the group
                group.redo()
            elif action == upDate:
                group.upDate(fileContent[self._groupToUndo])
            else:
                AssoComptaUtils.displayError("Unknow action type [%s]" %action, "HistoryManager.redo Error")

    def execute(self):
        """
        execute the last added command group and remove it after that.
        """

        self._groupToExecute.execute()
        self._groupToExecute = None
        
    def _unserialize(self, serializedGroup):
        """
        unserialize the specified string to return a command group
        @param serialized (string)  :   string from which will be
                                        constructed the group
        @return an initialized group (CommandGroup)
        """

        #get from the string the comment/description for the group
        grpComment = getTokenValue(GROUP_COMMENT_ID, serializedGroup)
        if 'upDate' in grpComment:
            action = upDate
        elif 'Create' in grpComment:
            action = create
        elif 'Delete' in grpComment:
            action = delete
        elif 'Copy' in grpComment:
            action = copy
        else:
            AssoComptaUtils.displayWarning("Unknow action in the history manager", "HistoryManager._unserialize Warning")
        
        #create an initialized group with only its comment
        group = commandGroup.CommandGroup(grpComment)
        group.setHistory(self)
        
        #unserialize the commands belonging to the group
        group.unserialize(serializedGroup)

        return group, action
    
    def _serialize(self, group):
        """
        serialize a group to store it in a file. Each serialized group is on
        one line.
        """
        return group.serialize() + "\n"
    
    def addCommandGroup(self, group):
        """
        add a command group to the file.
        @param group CommandGroup   :   group to add to the history.
        """
        
        group.setHistory(self)        
        self._groupToExecute = group
        
        # open the file to get its current content in a list
        with open(self._fileName, 'r') as saveFile:
            fileContent = saveFile.readlines()

        #add the serialized group to the file's content
        serialGroup = self._serialize(group)
        self._groupToUndo += 1
        fileContent.insert(self._groupToUndo, serialGroup)

        #remove all the groups that comes after new group
        del fileContent[self._groupToUndo + 1 : len(fileContent) + 1]
        
        #update the number of groups present in the history
        self._groupCount = len(fileContent)
        
        #save the new content on file, writting over the old content.
        with open(self._fileName, 'w') as saveFile:
            saveFile.writelines(fileContent)
            
    def destroy(self):
        """
        Destroy the file associated to the history. Should be called when
        the associated frame is closing.
        """
        import os
        os.remove(self._fileName)
        
    def isUndoPossible(self):
        """
        @return a boolean indicating if a undo is possible. Use it for e.g.
        (un)enable the undo item in a menu.
        """

        # the first group added has the index 0...
        return self._groupToUndo > -1
    
    def isRedoPossible(self):
        """
        @return a boolean indicating if a redo is possible. Use it for e.g.
        (un)enable the redo item in a menu.
        """
        #groupToUndo index begins at 0 so the count is bigger of one if
        #groupToUndo is on the last group added. If it's the case, the
        #it means that the last group hadn't been undone and so there is
        #no group to redo.
        return self._groupToUndo < self._groupCount - 1
    
    def getCommandGroupToRedo(self):
        """
        @return the the group (CommandGroup) that will be redone if we call
        the undo method. If all the groups have been undone None is returned.
        """
        
        #check if there a group to redo
        if self.isRedoPossible():
            
            # open the file to get its current content in a list
            with open(self._fileName, 'r') as saveFile:
                fileContent = saveFile.readlines()

            #get the group that is next to be redone
            group = self._unserialize(fileContent[self._groupToUndo + 1])
            group.setHistory(self)
            return group
        else:
            return None
        
    def getCommandGroupToUndo(self):
        """
        @return the the group (CommandGroup) that will be redone if we call
        the undo method. If all the groups have been undone None is returned.
        """
        
        #check if there is a group to undo
        if self.isUndoPossible():
            
            # open the file to get its current content in a list
        
            with open(self._fileName, 'r') as saveFile:
                fileContent = saveFile.readlines()

            #get the group that is next to be redone
            group = self._unserialize(fileContent[self._groupToUndo])
            group.setHistory(self)
            return group
        else:
            return None
        
    def getFrame(self):
        """
        @return the associated to the history frame
        """

        return self._frame
    
    def _findOlfGroup(self, serializedGroup):
        """
        Find the most recent former group of a shape in the history manager to rebuild it
        """
        
        shapeOccurence = []
        shapeId = eval(getTokenValue("shapeId", serializedGroup))
        oglShapeClassName = getTokenValue("oglShapeClass", serializedGroup)
        oglShapeModule =  getTokenValue("oglShapeModule", serializedGroup)
        
        basicSoftwareShapeClassName =  getTokenValue("basicSoftwareShapeClass", serializedGroup)
        basicSoftwareShapeModule =  getTokenValue("basicSoftwareShapeModule", serializedGroup)
        
        try:
            with open(self._fileName, 'r') as saveFile:
                fileContent = saveFile.readlines()
            
            for i in range(self._groupToUndo):
                if i>=0:
                    group, action = self._unserialize(fileContent[i])
                    oldShapeId = eval(getTokenValue("shapeId", fileContent[i]))
                    oldOglShapeClassName = getTokenValue("oglShapeClass", fileContent[i])
                    oldOglShapeClassModule = getTokenValue("oglShapeModule", fileContent[i])
        
                    oldBasicSoftwareShapeClassName = getTokenValue("basicSoftwareShapeClass", fileContent[i])
                    oldBasicSoftwareShapeModule = getTokenValue("basicSoftwareShapeModule", fileContent[i])
                    if [shapeId, oglShapeClassName,oglShapeModule, basicSoftwareShapeClassName,basicSoftwareShapeModule] == [oldShapeId, oldOglShapeClassName, oldOglShapeClassModule, oldBasicSoftwareShapeClassName, oldBasicSoftwareShapeModule]:
                        shapeOccurence.append(i)
            if shapeOccurence:
                return fileContent[i]
            else:
                return None
        except:
            msg = "Failed to _findOldGroup in the HistoryManager"
            AssoComptaUtils.displayWarning(msg, 'HistoryManager._findOldGroup Warning')