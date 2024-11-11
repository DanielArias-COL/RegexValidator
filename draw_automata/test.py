import unittest
import  os

from draw_automata.util import GeneradorAutomata, Automata, InvalidRegexException


class TestAutomata(unittest.TestCase):
    def setUp(self):
        self.generador = GeneradorAutomata()

    def test_procesar_expresion_basica(self):
        expr = 'a|b'
        automata = self.generador.procesar_expresion(expr)

        # Verificar que el autómata tiene los estados correctos
        self.assertIsInstance(automata, Automata)
        self.assertIn(automata.estado_inicial, automata.estados)
        self.assertTrue(any(estado.es_final for estado in automata.estados.values()))

        # Verificar transiciones para la expresión 'a|b'
        estados_iniciales = [automata.estado_inicial]
        destinos_a = [dest for dest in automata.estados[automata.estado_inicial].transiciones.get('a', [])]
        destinos_b = [dest for dest in automata.estados[automata.estado_inicial].transiciones.get('b', [])]

        self.assertTrue(destinos_a or destinos_b)
        self.assertTrue(destinos_a[0] in automata.estados and destinos_b[0] in automata.estados)

    def test_procesar_expresion_con_estrella(self):
        expr = 'a*'
        automata = self.generador.procesar_expresion(expr)

        # Verificar que el autómata tiene los estados correctos
        self.assertIsInstance(automata, Automata)
        self.assertIn(automata.estado_inicial, automata.estados)
        self.assertTrue(any(estado.es_final for estado in automata.estados.values()))

        # Verificar transiciones para la expresión 'a*'
        estado_inicial = automata.estado_inicial
        self.assertIn('a', automata.estados[estado_inicial].transiciones)
        destinos_a = automata.estados[estado_inicial].transiciones['a']

        for destino in destinos_a:
            self.assertIn(destino, automata.estados)

    def test_procesar_expresion_con_cierre_positivo(self):
        expr = 'a+'
        automata = self.generador.procesar_expresion(expr)

        # Verificar que el autómata tiene los estados correctos
        self.assertIsInstance(automata, Automata)
        self.assertIn(automata.estado_inicial, automata.estados)
        self.assertTrue(any(estado.es_final for estado in automata.estados.values()))

        # Verificar transiciones para la expresión 'a+'
        estado_inicial = automata.estado_inicial
        self.assertIn('a', automata.estados[estado_inicial].transiciones)
        destinos_a = automata.estados[estado_inicial].transiciones['a']

        for destino in destinos_a:
            self.assertIn(destino, automata.estados)

    def test_visualizar_automata(self):
        expr = 'a*(a|b)'
        automata = self.generador.procesar_expresion(expr)
        dot = self.generador.visualizar_automata()

        # Verificar que el objeto Dot se genera correctamente
        self.assertIsNotNone(dot)
        self.assertIn('digraph', dot.source)

if __name__ == '__main__':
    unittest.main()