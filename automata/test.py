import unittest
from util import Automata, InvalidCharacterError, InvalidTransitionError

class TestAutomata(unittest.TestCase):

    def test_valid_binary_even(self):
        """Test con una cadena binaria válida que termina en un estado de aceptación."""
        automata = Automata("1100")
        self.assertTrue(automata.numeros_binarios())

    def test_invalid_binary_character(self):
        """Test con un carácter no binario en la cadena."""
        automata = Automata("1102")
        self.assertFalse(automata.numeros_binarios())

    def test_empty_string(self):
        """Test con una cadena vacía que debería fallar."""
        automata = Automata("")
        self.assertFalse(automata.numeros_binarios())

if __name__ == "__main__":
    unittest.main()
