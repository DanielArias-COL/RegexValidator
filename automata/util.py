class InvalidCharacterError(Exception):
    """Excepción para caracteres inválidos en la cadena de entrada."""
    pass

class InvalidTransitionError(Exception):
    """Excepción para transiciones inválidas en el autómata."""
    pass

class Automata:
    def __init__(self, cadena):
        self.cadena = cadena
        self.estado = 1
        self.transiciones = {
            1: {"0": 2, "1": 2},
            2: {"0": 3, "1": 2},
            3: {"0": 3, "1": 2}
        }

    def numeros_binarios(self):
        try:
            for i, char in enumerate(self.cadena):
                if char not in self.transiciones[self.estado]:
                    raise InvalidCharacterError(f"Carácter inválido '{char}' en posición {i}")
                self.estado = self.transiciones[self.estado][char]
            if self.estado == 3:
                return True
            else:
                raise InvalidTransitionError("La cadena no termina en un estado de aceptación.")
        except (InvalidCharacterError, InvalidTransitionError) as e:
            print(e)
            return False
