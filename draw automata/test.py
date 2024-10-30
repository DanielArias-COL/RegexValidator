import os
from dibujar_automata.util import GeneradorAutomata, InvalidRegexException

class TestAutomata:
    def __init__(self):
        self.generador = GeneradorAutomata()

    def prueba_expresion(self, expr, nombre_prueba):
        print(f"Probando expresión regular: '{expr}'")
        try:
            automata = self.generador.procesar_expresion(expr)
            output_path = f'{nombre_prueba}.png'
            output_path = self.generador.visualizar_automata(output_path=output_path)

            if os.path.exists(output_path):
                print(f"Imagen generada: '{output_path}'")
            else:
                print(f"Error: No se generó el archivo de imagen '{output_path}'. Verifica si Graphviz está instalado correctamente.")

        except InvalidRegexException as e:
            print(f"Error: {e}")

    def ejecutar_pruebas(self):
        self.prueba_expresion('a', 'prueba1')
        self.prueba_expresion('ab', 'prueba2')
        self.prueba_expresion('a|b', 'prueba3')
        self.prueba_expresion('(a|b)c', 'prueba4')
        self.prueba_expresion('a*', 'prueba5')
        self.prueba_expresion('(ab)*', 'prueba6')
        self.prueba_expresion('a+b', 'prueba7')
        self.prueba_expresion('(a|b)*c', 'prueba8')
        self.prueba_expresion(')()(||12', 'prueba9')  # Esta prueba generará un error

if __name__ == "__main__":
    pruebas = TestAutomata()
    pruebas.ejecutar_pruebas()
