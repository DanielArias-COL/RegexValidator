import os
from dibujar_automata.util import GeneradorAutomata


class TestAutomata:
    def __init__(self):
        self.generador = GeneradorAutomata()

    def prueba_expresion(self, expr, nombre_prueba):
        print(f"Probando expresión regular: '{expr}'")
        automata = self.generador.procesar_expresion(expr)

        # Generar y visualizar el autómata en una imagen
        output_path = f'{nombre_prueba}.png'
        output_path = self.generador.visualizar_automata(output_path=output_path)

        # Confirmar que el archivo se ha creado antes de seguir
        if os.path.exists(output_path):
            print(f"Imagen generada: '{output_path}'")
        else:
            print(
                f"Error: No se generó el archivo de imagen '{output_path}'. Verifica si Graphviz está instalado correctamente.")

    def ejecutar_pruebas(self):
        # Pruebas con diferentes expresiones regulares
        self.prueba_expresion('a', 'prueba1')  # Expresión simple
        self.prueba_expresion('ab', 'prueba2')  # Concatenación simple
        self.prueba_expresion('a|b', 'prueba3')  # Unión de símbolos
        self.prueba_expresion('(a|b)c', 'prueba4')  # Unión con concatenación
        self.prueba_expresion('a*', 'prueba5')  # Estrella de Kleene
        self.prueba_expresion('(ab)*', 'prueba6')  # Concatenación con estrella de Kleene
        self.prueba_expresion('a+b', 'prueba7')  # Estrella de Kleene con símbolo positivo
        self.prueba_expresion('(a|b)*c', 'prueba8')  # Unión con estrella de Kleene y concatenación


if __name__ == "__main__":
    pruebas = TestAutomata()
    pruebas.ejecutar_pruebas()
