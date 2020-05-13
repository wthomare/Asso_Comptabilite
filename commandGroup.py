# -*- coding: UTF-8 -*-

from historyUtils import getTokenValue, makeToken, makeValuatedToken, GROUP_BEGIN_ID, GROUP_END_ID, GROUP_COMMENT_ID, COMMAND_BEGIN_ID, COMMAND_END_ID, TOKEN_BEGIN, TOKEN_END

class CommandGroup(object):
    """
    This class is a part of the history system of PyUt. It brings together
    different commands used for doing a undo or redo. For example, when we
    select many shapes and we delete them, then there is a command 'created'
    for each one that is added to a CommandGroupe. This way, when we want
    to do an undo, all the deleted shapes will be reconstructed in one action.
    """
    
    def __init__(self, comment = ""):
        """
        Constructor.
        
        @param comment  String  :   a short description/comment in
                                    view to display in the menu or
                                    other GUI part.
        """

        #history to which belongs the group. Init when the group is added.
        self._history = None

        # list of commands belonging to the group
        self._commands = []
        
        self._comment = comment
        self._commonData = []
        
    #>------------------------------------------------------------------------
        
    def addCommand(self, command):
        """
        Add the specified command to the group
        @param command Command : command to add
        """

        command.setGroup(self)
        self._commands.append(command)
        
    #>------------------------------------------------------------------------

    def removeCommand(self, command):
        """
        Remove the specified command from the group
        @param command Command : command to remove
        """
        
        self._commands.remove(command)
        
    #>------------------------------------------------------------------------
        
    def serialize(self):
        """
        Transform all the commands belonging to the group into strings in
        view to store them in a file.
        @return a string representing the command.
        """
        #add the begining informations of the group
        serializedGroup = (makeToken(GROUP_BEGIN_ID) +
                           makeValuatedToken(GROUP_COMMENT_ID, self._comment))

        #add the begining informations and setup informations of
        #each command. After that add the ending informations of
        #for each command.
        for command in self._commands:
            serializedGroup += (makeToken(COMMAND_BEGIN_ID) + command.serialize() +  makeToken(COMMAND_END_ID))
            serializedGroup += makeToken(GROUP_END_ID)
            return serializedGroup


    #>------------------------------------------------------------------------

    def unserialize(self, serializedCommands):
        """
        unserialize the specified commands and add them to the group
        @param serializedCommands (string) :    a string representation
                                                of the commands belonging
                                                to the group.
        """

        #define the begining and ending token of a serialized command
        commandBegin = TOKEN_BEGIN + COMMAND_BEGIN_ID + TOKEN_END
        commandEnd = TOKEN_BEGIN + COMMAND_END_ID + TOKEN_END

        #looking for the begining of the first command
        cStart = serializedCommands.find(commandBegin)

        #while there is still a command begining token we can
        #proceed to the unserialization.
        while cStart > -1:
            
            #we don't need anymore of the begining token
            cStart += len(commandBegin)
            
            #find the ending token for this command
            cEnd = serializedCommands.find(commandEnd, cStart)

            #we work only on the useful data
            serialCommand = serializedCommands[cStart : cEnd]

            commandModuleName = getTokenValue(COMMAND_MODULE_ID, serialCommand)
            
            #get the name of the class of the command
            commandClassName = getTokenValue(COMMAND_CLASS_ID, serialCommand)

            #import the module which contains the command class an get that class
            try:
                
                commandClass = getattr(__import__(commandModuleName), commandClassName)

                #construction of an uninitialized command
                command = commandClass()
                command.setGroup(self)

                #unserialization and setup of the command
                command.unserialize(serialCommand)

                #add the command to the group
                self.addCommand(command)

                #looking for the next command begining token
                cStart = serializedCommands.find(commandBegin, cEnd)
            except:
                print("Failed to unserialized a group in the commandGroup")
                
    #>------------------------------------------------------------------------ 
        
    def redo(self):
        """
        Call the redo() method of all commands belonging to the group
        """
        for command in self._commands:
            command.redo()

    #>------------------------------------------------------------------------
    
    def undo(self):
        """
        Call the undo() method of all commands belonging to the group
        """
        for command in self._commands:
            command.undo()
            
    def redoUpDate(self, serializedGroup):
        for command in self._commands:
            command.redoUpDate('serializedGroup')
            
    def UpDate(self, serializedGroup):
        for command in self._commands:
            command.upDate(serializedGroup)

    #>------------------------------------------------------------------------

    def execute(self):
        """
        Call the execute() method of all commands belonging to the group 
        """
        for command in self._commands:
            command.execute()

    #>------------------------------------------------------------------------
            
    def getHistory(self):
        """
        return the history to which belongs the group
        """

        return self._history
    
    #>------------------------------------------------------------------------

    def setHistory(self, history):
        """
        Set the history to which belongs the group. Avoid to call this method
        because it is called automaticaly when the group is added.
        @param history (HistoryManager) : history to which belongs the group
        """

        self._history = history
    
    #>------------------------------------------------------------------------

    def getComment(self):
        """
        return the comment/description of the group
        """

        return self._comment

    #>------------------------------------------------------------------------

    def setComment(self, comment):
        """
        set the comment/description of the group
        @param comment (string) : comment/description of group to display
        """

        self._comment = comment
        
    #>------------------------------------------------------------------------

    def addCommonData(self, commonData):
        """
        Add a data that is common to all the commands belonging to the group.
        A common data should contain a identificator so that a given command
        can get only the pertinent data for itself. For e.g. linkCommand will
        get only the tuples ("link", (shapeToLink, linkId)).
        WARNING : the common data is NOT serialized, so they are lost after
        an unserialization. You have to use these data in a command before
        the serialization of the group.

        @param commonData (tuple)   :   data that a command add to be used by
                                        an other command.
        """
        self._commonData.append(commonData)

    #>------------------------------------------------------------------------
    
    def getCommonData(self):
        """
        @return a list of common data, so a command can use informations
        produced by an other command in the same group.
        WARNING : the common data is NOT serialized, so they are lost after
        an unserialization. You have to use these data in a command before
        the serialization of the group.
        """
        return self._commonData
        
