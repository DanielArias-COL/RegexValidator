from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QMessageBox

from draw_automata.util import GeneradorAutomata, probar_automata
from world.test import expression
from world.util import Util
from PyQt6.QtGui import QColor, QTextCursor, QTextCharFormat



class MainWondow(QDialog):

    def __init__(self):
        super().__init__()

        #We initialice the view
        self.probar_automata = None
        self.ui = uic.loadUi('views/main.ui',self)
        
         
        #We connect the UI to the class variables.
        self.regular_expression = self.ui.lineEditER
        self.input_string= self.ui.plainTextEditInputStrings
        self.acepted_strings = self.ui.textEditAcceptedStrings 
        self.validate_btn = self.ui.pushButtonValidate
        self.generateAutomata_btn = self.ui.pushButtonGenerateAutomata    

        self.clase_util = Util()
        self.generador_automata = GeneradorAutomata()
        self.init_signal_slot()
        self.ui.show()

    
    def init_signal_slot(self):
        """        
        Connects the interface buttons to their respective methods.

        Connects the validation button (validate_btn) with the validate_expression method.

        """
        self.validate_btn.clicked.connect(self.validate_expression)
        self.generateAutomata_btn.clicked.connect(self.generate_automata)
        

    
    def validate_expression(self):
        """
        Method to validate the regular expression entered in the corresponding field.

        This method retrieves the regular expression and the input text, sends them to the Util class to
        find the match positions, and then uses those positions to highlight the text in the accepted_strings field.

        """
        expression = self.clase_util.removeSpaces(self.regular_expression.text())
        text = self.input_string.toPlainText()
        self.acepted_strings.setPlainText(text)

        positions_to_highlight = self.clase_util.matchStrings(expression, text)

        self.highlight_text(self.acepted_strings, positions_to_highlight)


    def generate_automata(self):

        expression = self.clase_util.removeSpaces(self.regular_expression.text())

        try:
            # Genera el autómata con la expresión ingresada
            self.generador_automata.procesar_expresion(expression)
            self.generador_automata.visualizar_automata()
            self.probar_automata = probar_automata(expression)
            QMessageBox.information(self, "Éxito", "El autómata se ha generado y guardado como 'automata.png'")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Ocurrió un error al generar el autómata: {e}")

    def highlight_text(self, text_edit, positions):
        """
        Highlights the matches in the provided QTextEdit.

        This method receives a QTextEdit and a list of tuples with start and end positions. It uses a
        QTextCursor to highlight the matches in the QTextEdit by applying a background color.

        Parameters:
        -----------
        text_edit : QTextEdit
            Text field where the matches will be highlighted
        positions : list of tuple
            List of tuples containing the start and end positions of each match

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




        

    

