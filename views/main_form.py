from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QPushButton, QMessageBox

class MainWondow(QDialog):
    def __init__(self):
        super().__init__()

        #We initialice the view
        self.ui = uic.loadUi('views/main.ui',self)
         
        #We connect the UI to the class variables.
        self.regular_expression = self.ui.lineEditER
        self.input_string= self.ui.plainTextEditInputStrings
        self.acepted_strings = self.ui.plainTextEditAcceptedStrings
        self.ui.show()


