from collections import deque
import json

# Define the NFA class


class NFA:
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept
        self.transitions = {}
        self.state_to_number = None
        self.transition_table = None
        self.alphabet = set()

    def add_transition(self, state, symbol, next_state):
        if (state, symbol) not in self.transitions:
            self.transitions[(state, symbol)] = []
        self.transitions[(state, symbol)].append(next_state)

    def set_initial(self, initial):
        self.initial = initial

    def set_accept(self, accept):
        self.accept = accept

    def set_transitions(self, transitions):
        self.transitions = transitions

    def ennunmerate_states(self):
        # Diccionario para almacenar el número asignado a cada estado
        state_to_number = {}

        # Cola para realizar el recorrido BFS
        queue = deque([self.initial])

        # El estado inicial se numera como 0
        state_to_number[self.initial] = 0
        current_number = 1  # El siguiente número a asignar
        # Mientras haya estados en la cola
        while queue:
            # Tomamos el estado actual de la cola
            current_state = queue.popleft()

            # Recorremos todas las transiciones desde este estado
            for (state, symbol), next_states in self.transitions.items():
                if state == current_state:  # Si la transición parte del estado actual
                    # Iteramos sobre los estados de destino (next_states puede ser una lista)
                    for next_state in next_states:
                        if isinstance(next_state, list):
                            while isinstance(next_state[0], list):
                                next_state = next_state[0]
                            for state in next_state:
                                if state not in state_to_number:
                                    state_to_number[state] = current_number
                                    current_number += 1
                                    # Agregamos el estado a la cola para seguir explorando
                                    queue.append(state)
                        else:
                            # Si next_state no es una lista, lo tratamos como un estado individual
                            if next_state not in state_to_number:
                                state_to_number[next_state] = current_number
                                current_number += 1
                                # Agregamos el estado a la cola
                                queue.append(next_state)

        # Verificamos que el estado de aceptación también tenga un número
        if self.accept not in state_to_number:
            state_to_number[self.accept] = current_number

        return state_to_number

    def build_transition_table(self):
        # Obtener la enumeración de los estados
        self.state_to_number = self.ennunmerate_states()

        # Inicializar la tabla de transición
        transition_table = {}
        initial_state_num = self.state_to_number.get(self.initial)
        accept_state_num = self.state_to_number.get(self.accept)

        for (state, symbol), next_states in self.transitions.items():
            current_state_num = self.state_to_number.get(state)

            if current_state_num not in transition_table:
                transition_table[current_state_num] = {}

            for next_state in next_states:
                # Verificamos si next_state es una lista y manejamos cada uno
                if isinstance(next_state, list):
                    while isinstance(next_state[0], list):
                        next_state = next_state[0]
                    for sub_state in next_state:
                        next_state_num = self.state_to_number.get(sub_state)
                        if symbol in transition_table[current_state_num]:
                            # Si ya existe la entrada para este símbolo, agregamos el estado a la lista
                            if next_state_num not in transition_table[current_state_num][symbol]:
                                transition_table[current_state_num][symbol].append(
                                    next_state_num)
                        else:
                            # Si no existe la entrada, inicializamos la lista
                            transition_table[current_state_num][symbol] = [
                                next_state_num]
                else:
                    next_state_num = self.state_to_number.get(next_state)
                    if symbol in transition_table[current_state_num]:
                        # Si ya existe la entrada para este símbolo, agregamos el estado a la lista
                        if next_state_num not in transition_table[current_state_num][symbol]:
                            transition_table[current_state_num][symbol].append(
                                next_state_num)
                    else:
                        # Si no existe la entrada, inicializamos la lista
                        transition_table[current_state_num][symbol] = [
                            next_state_num]
        self.transition_table = transition_table
        return initial_state_num, accept_state_num

    # Print the transition table

    def print_transition_table(self):
        for state, transitions in self.transition_table.items():
            print(f"State {state}: {transitions}")

    def get_transition_table(self):
        # Inicializar un diccionario para la tabla de transiciones
        transition_table_json = {}

        # Construir el diccionario para JSON
        for current_state, transitions in self.transition_table.items():
            transition_table_json[current_state] = {}
            for symbol, next_states in transitions.items():
                transition_table_json[current_state][symbol] = next_states

        # Convertir el diccionario a JSON
        return transition_table_json

    def get_transitions_by_state(self, state):
        if state == self.accept:
            return None, self.accept
        for (s, symbol), next_states in self.transitions.items():
            if s == state:
                return symbol, next_states
        return None, []  # Si no se encuentra el estado

    # From number to state
    def get_state_by_number(self, number):
        for state, num in self.state_to_number.items():
            if num == number:
                return state
        return None


def route(string, state, nfa, path=None, all_paths=None):
    if path is None:
        path = []  # Inicializar el camino

    if all_paths is None:
        all_paths = []  # Inicializar la lista de todos los caminos

    # Agregar el estado actual al camino
    path.append(state)

    # Si el estado actual es el estado de aceptación y la cadena está vacía
    if state == nfa.accept and not string:
        all_paths.append((path.copy(), True))  # Añadir camino aceptado
        return all_paths

    # Obtener el símbolo y los próximos estados desde la transición actual
    transition = nfa.get_transitions_by_state(state)
    if transition is None:
        print("No hay transición desde el estado actual.")
        all_paths.append((path.copy(), False))  # Añadir camino no aceptado
        return all_paths

    symbol, next_states = transition
    if isinstance(next_states, list):
        while isinstance(next_states[0], list):
            next_states = next_states[0]
    print(
        f"Estado actual: {state}, Símbolo: {symbol}, Próximos estados: {next_states}")
    # Procesar transiciones epsilon (símbolo "&")
    if string and symbol == "&" and string[0] == "&":
        for next_state in next_states:
            if isinstance(next_state, list):
                next_state = next_state[0]
            # Consumir el símbolo y moverse al siguiente estado
            new_string = string.copy()  # Copia la cadena
            new_string.pop(0)
            all_paths = route(new_string, next_state, nfa,
            path.copy(), all_paths)  # Avanzar en la cadena
    if symbol == "&":
        for next_state in next_states:
            if isinstance(next_state, list):
                for state in next_state:
                    # Copia el camino
                    all_paths = route(
                        string[:], state, nfa, path.copy(), all_paths)
            else:
                # Copia el camino
                all_paths = route(string[:], next_state,
                nfa, path.copy(), all_paths)

    # Procesar transiciones normales, coincidiendo el símbolo
    elif string and string[0] == symbol:
        for next_state in next_states:
            if isinstance(next_state, list):
                next_state = next_state[0]
            # Consumir el símbolo y moverse al siguiente estado
            new_string = string.copy()  # Copia la cadena
            new_string.pop(0)
            all_paths = route(new_string, next_state, nfa,
            path.copy(), all_paths)  # Avanzar en la cadena

    # Si no hay coincidencias o transiciones
    if string or symbol != "&":
        # Añadir camino no aceptado solo al final
        all_paths.append((path.copy(), False))
    return all_paths  # Retornar todos los caminos


def evaluate_string(string, nfa):
    caminos = route(string, nfa.initial, nfa)
    state_to_number = nfa.state_to_number
    status = "Rechazada"
    caminoA = []
    for camino, aceptado in caminos:
        if aceptado:
            status = "Aceptada"
        caminoA = []
        for state in camino:
            if isinstance(state, list):
                while isinstance(state[0], list):
                    state = state[0]
                caminoA.append(state_to_number[state[0]])
            else:
                caminoA.append(state_to_number[state])
        print(f"Camino: {caminoA}, Aceptado: {aceptado}")
        camino = [state for state in caminoA]

    # ToJSON
    json_caminos = []
    caminoB = []
    for camino, aceptado in caminos:
        caminoB = []
        for state in camino:
            if isinstance(state, list):
                while isinstance(state[0], list):
                    state = state[0]
                caminoB.append(state_to_number[state[0]])
            else:
                caminoB.append(state_to_number[state])
        camino = [state for state in caminoB]
        json_caminos.append({"camino": camino, "aceptado": aceptado})

    return json_caminos, status


def evaluate_string_dfa(input_string, dfa):
    transitions = dfa.transitions
    # Definir el estado inicial
    current_states = ['A']  # Aquí se asume que 'A' es el estado inicial
    path = []  # Para almacenar el camino recorrido

    for symbol in input_string:
        next_states = []  # Lista para almacenar los próximos estados
        if symbol == "&":
            path.append(current_states)  # Almacenar el camino
            continue

        for state in current_states:
            # Obtener las transiciones para el estado actual y el símbolo
            for (state_key, transition_symbol), next_state_list in transitions.items():
                if state_key == state and (transition_symbol == symbol):
                    next_states.extend(next_state_list)
                    if isinstance(next_state_list, list):
                        # Almacenar el camino
                        path.append(
                            [state, transition_symbol, next_state_list[0]])
                    else:
                        path.append(
                            [state, transition_symbol, next_state_list])

        current_states = next_states  # Actualizar los estados actuales

        # Si no hay estados alcanzables, la cadena no es válida
        if not current_states:
            return path, False

    # Verificar si alguno de los estados actuales es un estado de aceptación
    print(f"Estados actuales: {current_states}")
    for state in current_states:
        print(f"Estado: {state}")
        print(f"Estados de aceptación: {dfa.accept}")
    is_accepted = any(state in dfa.accept for state in current_states)
    return path, is_accepted


# Functions to create basic NFA fragments
# Rule #1: An Empty Expression (ε) is an NFA with two states and an epsilon transition between them.
# Rule #2: A Single Symbol (a) is an NFA with two states, one initial state and one final state, and a transition between them labeled with the symbol.
def basic_nfa(initial, accept):
    i = initial
    a = accept
    nfa = NFA(i, a)
    return nfa

# Functions to create NFA fragments for operators

# Rule #3: Union expression


def union_nfa(nfa1, nfa2):
    initial = object()
    accept = object()
    nfa = basic_nfa(initial, accept)
    for (state, symbol), next_states in nfa1.transitions.items():
        nfa.add_transition(state, symbol, next_states)
    for (state, symbol), next_states in nfa2.transitions.items():
        nfa.add_transition(state, symbol, next_states)
    nfa.add_transition(initial, "&", nfa1.initial)
    nfa.add_transition(initial, "&", nfa2.initial)
    nfa.add_transition(nfa1.accept, "&", accept)
    nfa.add_transition(nfa2.accept, "&", accept)
    return nfa

# Rule #4: Concatenation expression


def concat_nfa(nfa1, nfa2):
    symbolns2, next_states2 = nfa2.get_transitions_by_state(nfa2.initial)
    for next_state in next_states2:
        nfa1.add_transition(nfa1.accept, symbolns2, next_state)

    for (state, symbol), next_states in nfa2.transitions.items():
        # Only if the state is not the initial state
        if state != nfa2.initial:
            nfa1.add_transition(state, symbol, next_states)
    nfa1.accept = nfa2.accept
    return nfa1

# Rule #5: Kleene star expression


def kleene_nfa(nfa):
    initial = object()
    accept = object()
    nfa.add_transition(initial, "&", accept)
    nfa.add_transition(initial, "&", nfa.initial)
    nfa.add_transition(nfa.accept, "&", nfa.initial)
    nfa.add_transition(nfa.accept, "&", accept)
    nfa.initial = initial
    nfa.accept = accept
    return nfa

# Rule #6: Positive closure expression


def positive_nfa(nfa):
    initial = object()
    accept = object()
    nfa.add_transition(initial, "&", nfa.initial)
    nfa.add_transition(nfa.accept, "&", accept)
    nfa.add_transition(nfa.accept, "&", nfa.initial)
    nfa.initial = initial
    nfa.accept = accept
    return nfa

# Rule #7: Optional expression


def optional_nfa(nfa):
    initial = object()
    accept = object()
    nfa.add_transition(initial, "&", nfa.initial)
    nfa.add_transition(nfa.accept, "&", accept)
    nfa.add_transition(initial, "&", accept)
    nfa.initial = initial
    nfa.accept = accept
    return nfa
