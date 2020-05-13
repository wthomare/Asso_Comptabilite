class AbstractClassError(Exception): pass

class Io:
    """
    Base Class to save or open file format contains diarams.

    """
    def save(self, fileName, oglDiagram):
        """
        To save save diagram in file.

        @param String fileName : the file name who is saved diagram
        @param OglDiagram      : the diagram who is information

        """
        raise AbstractClassError()
    #>------------------------------------------------------------------------

    def open(self, fileName, oglDiagram):
        """
        To open a file and creating diagram.

        @param String fileName : the file name who is saved diagram
        @param OglDiagram      : the diagram who is information

        """
        raise AbstractClassError()
