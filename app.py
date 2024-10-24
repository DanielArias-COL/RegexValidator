from views.main_form import MainWondow
from PyQt6.QtWidgets import QApplication

# Creación de la aplicación sin una clase contenedora
app = QApplication([])

# Inicialización del componente Login
MainWondow = MainWondow()

app.exec()
