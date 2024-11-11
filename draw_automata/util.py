import os
import re
import tempfile
from graphviz import Digraph
from PIL import Image

os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

class Estado:
    """
    Representa un estado en el autómata.
    """
    def __init__(self, id):
        self.id = id
        self.transiciones = {}
        self.es_final = False

class Automata:
    """
    Representa un autómata finito.
    """
    def __init__(self):
        self.estados = {}
        self.estado_inicial = None
        self.contador_estados = 0

    def crear_estado(self):
        id_estado = f'q{self.contador_estados}'
        self.contador_estados += 1
        nuevo_estado = Estado(id_estado)
        self.estados[id_estado] = nuevo_estado
        return id_estado

    def agregar_transicion(self, origen, simbolo, destino):
        if origen in self.estados and destino in self.estados:
            if simbolo not in self.estados[origen].transiciones:
                self.estados[origen].transiciones[simbolo] = set()
            self.estados[origen].transiciones[simbolo].add(destino)

class InvalidRegexException(Exception):
    pass

class GeneradorAutomata:
    """
    Generador de autómatas a partir de expresiones regulares.
    """
    def __init__(self):
        self.automata = None

    def validar_expresion(self, expr):
        if not re.match(r'^[a-zA-Z0-9|()*+]*$', expr):
            raise InvalidRegexException("La expresión contiene caracteres inválidos.")
        stack = []
        for char in expr:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise InvalidRegexException("Paréntesis desbalanceados en la expresión.")
                stack.pop()
        if stack:
            raise InvalidRegexException("Paréntesis desbalanceados en la expresión.")

    def procesar_expresion(self, expr):
        self.validar_expresion(expr)
        self.automata = Automata()
        estado_inicial = self.automata.crear_estado()
        self.automata.estado_inicial = estado_inicial
        estado_actual = self.procesar_subexpresion(estado_inicial, expr)
        self.automata.estados[estado_actual].es_final = True
        return self.automata

    def procesar_subexpresion(self, estado_inicial, subexpr):
        estado_actual = estado_inicial
        i = 0
        while i < len(subexpr):
            if subexpr[i] == '|':
                estado_actual = self.procesar_union(estado_inicial, subexpr)
                break
            elif subexpr[i] == '(':
                nivel = 1
                j = i + 1
                while j < len(subexpr) and nivel > 0:
                    if subexpr[j] == '(':
                        nivel += 1
                    elif subexpr[j] == ')':
                        nivel -= 1
                    j += 1
                subexpr_interna = subexpr[i + 1:j - 1]
                estado_actual = self.procesar_subexpresion(estado_actual, subexpr_interna)
                i = j
            elif subexpr[i] in '*+':
                estado_actual = self.procesar_estrella(estado_actual, subexpr[i - 1], subexpr[i])
                i += 1
            else:
                nuevo_estado = self.automata.crear_estado()
                self.automata.agregar_transicion(estado_actual, subexpr[i], nuevo_estado)
                estado_actual = nuevo_estado
                i += 1
        return estado_actual

    def procesar_estrella(self, estado_anterior, simbolo, operador):
        if operador == '*':
            self.automata.agregar_transicion(estado_anterior, simbolo, estado_anterior)
        elif operador == '+':
            nuevo_estado = self.automata.crear_estado()
            self.automata.agregar_transicion(estado_anterior, simbolo, nuevo_estado)
            self.automata.agregar_transicion(nuevo_estado, simbolo, nuevo_estado)
            return nuevo_estado
        return estado_anterior

    def procesar_union(self, estado_inicial, expr):
        estado_final = self.automata.crear_estado()
        partes = expr.split('|')
        for parte in partes:
            estado_actual = estado_inicial
            for simbolo in parte:
                nuevo_estado = self.automata.crear_estado() if simbolo != parte[-1] else estado_final
                self.automata.agregar_transicion(estado_actual, simbolo, nuevo_estado)
                estado_actual = nuevo_estado
        return estado_final

    def visualizar_automata(self):
        dot = Digraph(comment='Autómata Finito')
        dot.attr(rankdir='LR')

        # Dibuja todos los estados y marca el estado final con doble círculo
        for estado_id, estado in self.automata.estados.items():
            shape = 'doublecircle' if estado.es_final else 'circle'
            dot.node(estado_id, estado_id, shape=shape)

        # Nodo inicial
        dot.node('', '', shape='none')
        dot.edge('', self.automata.estado_inicial)

        # Agregar transiciones
        for estado_id, estado in self.automata.estados.items():
            for simbolo, destinos in estado.transiciones.items():
                for destino in destinos:
                    dot.edge(estado_id, destino, label=simbolo)

        # Guardar en un directorio temporal
        temp_dir = tempfile.gettempdir()
        file_path = f"{temp_dir}/automata"
        dot.render(file_path, format='png', cleanup=True)

        print(f"Autómata guardado en: {file_path}.png")
        return file_path + '.png'

def probar_automata(expr):
    generador = GeneradorAutomata()
    automata = generador.procesar_expresion(expr)
    dot = generador.visualizar_automata()
    file_path = generador.visualizar_automata()

    print(f"Autómata generado para la expresión: {expr}")
    print("El autómata ha sido guardado como 'automata.png'")

    # Abrir la imagen generada
    img = Image.open(file_path)
    img.show()
