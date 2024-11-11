import unittest
import  os

from draw_automata.util import GeneratorAutomata, Automata, InvalidRegexException


class TestAutomata(unittest.TestCase):
    def setUp(self):
        self.generador = GeneratorAutomata()

    def test_process_basic_expression(self):
        expr = 'a|b'
        automata = self.generador.process_expresion(expr)

        self.assertIsInstance(automata, Automata)
        self.assertIn(automata.initial_state, automata.state)
        self.assertTrue(any(estado.is_final for estado in automata.state.values()))

        initial_states = [automata.initial_state]
        destinations_a = [dest for dest in automata.state[automata.initial_state].transactions.get('a', [])]
        destination_b = [dest for dest in automata.state[automata.initial_state].transactions.get('b', [])]

        self.assertTrue(destinations_a or destination_b)
        self.assertTrue(destinations_a[0] in automata.state and destination_b[0] in automata.state)

    def test_process_expression_with_star(self):
        expr = 'a*'
        automata = self.generador.process_expresion(expr)

        self.assertIsInstance(automata, Automata)
        self.assertIn(automata.initial_state, automata.state)
        self.assertTrue(any(estado.is_final for estado in automata.state.values()))

        initial_state = automata.initial_state
        self.assertIn('a', automata.state[initial_state].transactions)
        destinations_a = automata.state[initial_state].transactions['a']

        for destino in destinations_a:
            self.assertIn(destino, automata.state)

    def test_process_expression_with_positive_closure(self):
        expr = 'a+'
        automata = self.generador.process_expresion(expr)

        self.assertIsInstance(automata, Automata)
        self.assertIn(automata.initial_state, automata.state)
        self.assertTrue(any(estado.is_final for estado in automata.state.values()))

        initial_states = automata.initial_state
        self.assertIn('a', automata.state[initial_states].transactions)
        destinos_a = automata.state[initial_states].transactions['a']

        for destino in destinos_a:
            self.assertIn(destino, automata.state)

    def test_visualizar_automata(self):
        expr = 'a*(a|b)'
        automata = self.generador.process_expresion(expr)
        dot = self.generador.visualize_automata()

        self.assertIsNotNone(dot)
        self.assertIn('digraph', dot.source)

if __name__ == '__main__':
    unittest.main()