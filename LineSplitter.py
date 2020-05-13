# -*- coding: utf-8 -*-
class LineSplitter:
    """
    This class offers a text split algorithm.
    You can give your text to the method split and this will return you
    a list of string, length of text for each string <= total width.

    Sample of use::
        text = "Hi, how are you today ?"
        splittedLines = LineSplitter().split(text, dc, 12)
    """

    def split(self, text, dc, width):
        """
        Split a text in lines fitting in width pixels.

        @param String text : text to split
        @param wxDC dc
        @param int width : width for the text, in pixels
        @return String [] : a list of strings fitting in width pixels
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        lines = text.splitlines()
        newLines = []
        for line in lines:
            words = line.split()
            wline = 0
            newLine = "".encode('utf8')
            for word in words:
                try:
                    word += " ".encode('utf8')
                except:
                    word += " "
                wword = dc.GetTextExtent(word)[0]
                if wline + wword <= width:
                    try:
                        newLine += word.encode('utf8')
                        wline += wword
                    except:
                        newLine += word
                        wline += wword
                else:
                    newLines.append(newLine[:-1]) # remove last space
                    try:
                        newLine = word.encode('utf8')
                        wline = wword
                    except:
                        newLine = word
                        wline = wword                        
            newLines.append(newLine[:-1])
        return newLines
