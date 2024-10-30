from PIL import Image

from dibujar_automata.util import GeneradorAutomata


def test_generar_y_visualizar_automata(expr):

    print(f"Probando con la expresión regular: {expr}")

    generador = GeneradorAutomata()
    generador.procesar_expresion(expr)

    output_path = generador.visualizar_automata('automata.png')
    print(f"Autómata generado y guardado en {output_path}")

    img = Image.open(output_path)
    img.show()


if __name__ == "__main__":
    expresion = "(a|b)*ab+"
    test_generar_y_visualizar_automata(expresion)
