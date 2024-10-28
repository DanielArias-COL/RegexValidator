from PyQt6 import uic
from PyQt6.QtWidgets import QDialog
from mundo.util import Util
from PyQt6.QtGui import QColor, QTextCursor, QTextCharFormat



class MainWondow(QDialog):

    def __init__(self):
        super().__init__()

        #We initialice the view
        self.ui = uic.loadUi('views/main.ui',self)
        
         
        #We connect the UI to the class variables.
        self.regular_expression = self.ui.lineEditER
        self.input_string= self.ui.plainTextEditInputStrings
        self.acepted_strings = self.ui.textEditAcceptedStrings 
        self.validate_btn = self.ui.pushButtonValidate

        self.clase_util = Util()
        self.init_signal_slot()
        self.ui.show()

    
    def init_signal_slot(self):
        """
        Conecta los botones de la interfaz a sus respectivos métodos.

        Conecta el botón de validación (validate_btn) con el método validate_expression.
        """
        self.validate_btn.clicked.connect(self.validate_expression)

    
    def validate_expression(self):
        """
        Método para validar la expresión regular ingresada en el campo correspondiente.

        Este método obtiene la expresión regular y el texto de entrada, los envía a la clase Util para
        encontrar las posiciones de coincidencia, y luego utiliza esas posiciones para resaltar el
        texto en el campo acepted_strings.
        """
        expression = self.regular_expression.text()
        text = self.input_string.toPlainText()
        self.acepted_strings.setPlainText(text)

        positions_to_highlight = self.clase_util.matchStrings(expression, text)

        self.highlight_text(self.acepted_strings, positions_to_highlight)



    def highlight_text(self, text_edit, positions):
        """
        Resalta las coincidencias en el QTextEdit proporcionado.

        Este método recibe un QTextEdit y una lista de tuplas con posiciones de inicio y fin. Utiliza un
        QTextCursor para resaltar las coincidencias en el QTextEdit, aplicando un fondo de color.

        Parámetros:
        -----------
        text_edit : QTextEdit
            Campo de texto donde se resaltarán las coincidencias
        positions : list of tuple
            Lista de tuplas que contienen posiciones de inicio y fin de cada coincidencia
        """
        cursor = text_edit.textCursor()
        cursor.clearSelection()
        
        fmt = QTextCharFormat()
        fmt.setBackground(QColor(20, 219, 236))  

        cursor.movePosition(QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor)
            
        full_text = text_edit.toPlainText()
        
        for start, end in positions:
            
            if start < 0 or end > len(full_text) or start >= end:
                continue
            
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
            cursor.mergeCharFormat(fmt)
        
        cursor.setPosition(0)




        

    

