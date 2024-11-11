import os
import re
import tempfile
from graphviz import Digraph
from PIL import Image

os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"


class State:
    """
       Represents a state in the automaton.

       This class is used to define a state with a unique identifier, a dictionary of transactions (representing
       state transitions), and a flag indicating if the state is a final state.
       """

    def __init__(self, id):
        """
            Initializes a new state with the given identifier.

            Args:
                id (int): The unique identifier for the state.
            """
        self.id = id
        self.transactions = {}
        self.is_final = False


class Automata:
    """
       Represents a finite automaton.

       This class defines a finite automaton with multiple states, where one is the initial state.
       It also includes a counter to assign unique IDs to each state.
       """

    def __init__(self):
        """
               Initializes an empty automaton with no states and no initial state.

               The counter_states variable is used to assign unique IDs to states as they are created.
               """
        self.state = {}
        self.initial_state = None
        self.counter_states = 0

    def create_state(self):
        """
                Creates a new state with a unique identifier and adds it to the automaton.

                This method generates a new state ID based on the current counter, creates a new instance of the
                `State` class, and then adds the state to the automaton's state dictionary.

                Returns:
                    str: The unique identifier of the newly created state.
                """
        id_state = f'q{self.counter_states}'
        self.counter_states += 1
        new_state = State(id_state)
        self.state[id_state] = new_state
        return id_state

    def add_transition(self, origin, symbol, destination):
        """
               Adds a transition between two states in the automaton for a given symbol.

               This method checks if both the origin and destination states exist in the automaton,
               and then adds a transition from the origin state to the destination state for the specified symbol.
               If the symbol doesn't already exist in the origin state's transactions, it is created.

               Args:
                   origin (str): The identifier of the origin state.
                   symbol (str): The symbol triggering the transition.
                   destination (str): The identifier of the destination state.
               """
        if origin in self.state and destination in self.state:
            if symbol not in self.state[origin].transactions:
                self.state[origin].transactions[symbol] = set()
            self.state[origin].transactions[symbol].add(destination)


class InvalidRegexException(Exception):
    """
        Exception raised for invalid regular expressions.

        This exception is raised when a regular expression does not conform to the expected syntax or
        contains invalid characters, such as unbalanced parentheses or unsupported operators.
        """
    pass


class GeneratorAutomata:
    """
       A class for generating finite automata from regular expressions.

       This class processes regular expressions to generate finite automata. It validates the expressions,
       processes subexpressions, handles special operators such as '*', '+', and '|', and visualizes the resulting automaton.
       """

    def __init__(self):
        """
               Initializes the GeneratorAutomata instance.

               Sets up the automaton as None, which will later be populated when processing an expression.
               """
        self.automata = None

    def validate_expresion(self, expr):
        """
                Validates the syntax of the given regular expression.

                This method checks if the expression contains only valid characters (letters, digits, and operators)
                and ensures that parentheses are balanced.

                Args:
                    expr (str): The regular expression to validate.

                Raises:
                    InvalidRegexException: If the expression contains invalid characters or unbalanced parentheses.
                """
        if not re.match(r'^[a-zA-Z0-9|()*+]*$', expr):
            raise InvalidRegexException("The expression contains invalid characters.")
        stack = []
        for char in expr:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise InvalidRegexException("Unbalanced parentheses in the expression.")
                stack.pop()
        if stack:
            raise InvalidRegexException("Unbalanced parentheses in the expression.")

    def process_expresion(self, expr):
        """
                Processes the regular expression and generates an automaton.

                This method validates the expression, creates a new automaton, and processes the expression
                by breaking it down into subexpressions. It assigns a final state to the automaton.

                Args:
                    expr (str): The regular expression to process.

                Returns:
                    Automata: The generated finite automaton.
                """
        self.validate_expresion(expr)
        self.automata = Automata()
        initial_state = self.automata.create_state()
        self.automata.initial_state = initial_state
        current_state = self.process_subexpression(initial_state, expr)
        self.automata.state[current_state].is_final = True
        return self.automata

    def process_subexpression(self, initial_state, subexpr):
        """
                Processes a subexpression within the regular expression.

                This method handles specific subexpressions, including unions (|), parentheses, and operators like '*' and '+'.
                It recursively processes parentheses and applies transitions for each symbol.

                Args:
                    initial_state (str): The state from which the subexpression starts.
                    subexpr (str): The subexpression to process.

                Returns:
                    str: The final state after processing the subexpression.
                """
        current_state = initial_state
        i = 0
        while i < len(subexpr):
            if subexpr[i] == '|':
                current_state = self.process_union(initial_state, subexpr)
                break
            elif subexpr[i] == '(':
                level = 1
                j = i + 1
                while j < len(subexpr) and level > 0:
                    if subexpr[j] == '(':
                        level += 1
                    elif subexpr[j] == ')':
                        level -= 1
                    j += 1
                subexpr_internal = subexpr[i + 1:j - 1]
                current_state = self.process_subexpression(current_state, subexpr_internal)
                i = j
            elif subexpr[i] in '*+':
                current_state = self.process_star(current_state, subexpr[i - 1], subexpr[i])
                i += 1
            else:
                nuevo_estado = self.automata.create_state()
                self.automata.add_transition(current_state, subexpr[i], nuevo_estado)
                current_state = nuevo_estado
                i += 1
        return current_state

    def process_star(self, previous_state, symbol, operator):
        """
                Processes the '*' or '+' operators in the regular expression.

                This method handles the Kleene star ('*') and the 'plus' ('+') operators by creating the necessary transitions.

                Args:
                    previous_state (str): The state from which the transition starts.
                    symbol (str): The symbol that the operator is applied to.
                    operator (str): The operator, either '*' or '+'.

                Returns:
                    str: The new state after applying the operator.
                """
        if operator == '*':
            self.automata.add_transition(previous_state, symbol, previous_state)
        elif operator == '+':
            new_state = self.automata.create_state()
            self.automata.add_transition(previous_state, symbol, new_state)
            self.automata.add_transition(new_state, symbol, new_state)
            return new_state
        return previous_state

    def process_union(self, initial_state, expr):
        """
               Processes the union ('|') operator in the regular expression.

               This method handles the union by splitting the expression at the '|' character and processing each part
               as a separate subexpression, connecting them to a common final state.

               Args:
                   initial_state (str): The initial state of the automaton.
                   expr (str): The regular expression with the union operator.

               Returns:
                   str: The final state after processing the union.
               """
        state_final = self.automata.create_state()
        parts = expr.split('|')
        for parte in parts:
            current_state = initial_state
            for symbol in parte:
                new_state = self.automata.create_state() if symbol != parte[-1] else state_final
                self.automata.add_transition(current_state, symbol, new_state)
                current_state = new_state
        return state_final

    def visualize_automata(self):
        """
                Visualizes the generated automaton as a PNG image.

                This method generates a visual representation of the finite automaton using Graphviz's Digraph,
                and saves it as a PNG image in the system's temporary directory.

                Returns:
                    str: The file path where the automaton image is saved.
                """
        dot = Digraph(comment='Autómata Finito')
        dot.attr(rankdir='LR')

        for state_id, state in self.automata.state.items():
            shape = 'doublecircle' if state.is_final else 'circle'
            dot.node(state_id, state_id, shape=shape)

        dot.node('', '', shape='none')
        dot.edge('', self.automata.initial_state)

        for state_id, state in self.automata.state.items():
            for symbol, destinations in state.transactions.items():
                for destiny in destinations:
                    dot.edge(state_id, destiny, label=symbol)

        temp_dir = tempfile.gettempdir()
        file_path = f"{temp_dir}/automata"
        dot.render(file_path, format='png', cleanup=True)

        print(f"Autómata save in: {file_path}.png")
        return file_path + '.png'


def test_automata(expr):
    generator = GeneratorAutomata()
    automata = generator.process_expresion(expr)
    dot = generator.visualize_automata()
    file_path = generator.visualize_automata()

    print(f"Autómata generated for the expression: {expr}")
    print("The autómata has been saved as 'automata.png'")

    img = Image.open(file_path)
    img.show()
