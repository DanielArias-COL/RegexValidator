import re

class Util ():

    def matchStrings(self, expression, text):
        """
        Encuentra las posiciones de coincidencias para una expresión regular en un texto.

        Args:
            expression (str): Expresión regular a buscar.
            text (str): Texto en el que se realizará la búsqueda.

        Returns:
            list: Lista de tuplas, cada una contiene la posición de inicio y fin de una coincidencia.
        """
        
        p = re.compile(expression)

        posiciones = [(match.start(), match.end()) for match in p.finditer(text)]
        
        return posiciones

    