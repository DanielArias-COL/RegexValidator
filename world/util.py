import re

class Util ():

    def matchStrings(self, expression, text):
        """
        Finds the positions of matches for a regular expression in a text.

        Args:
            expression (str): Regular expression to search for.
            text (str): Text in which the search will be performed.

        Returns:
            list: A list of tuples, each containing the start and end position of a match.
        """

        p = re.compile(expression)

        posiciones = [(match.start(), match.end()) for match in p.finditer(text)]
        
        return posiciones
    

    def removeSpaces(self, str):
        """
        Removes whitespace at the beginning of the string.

        Args:
            str (str): The input string from which leading whitespace will be removed.

        Returns:
            str: A new string with leading whitespace removed.
        """
        return str.lstrip()

    