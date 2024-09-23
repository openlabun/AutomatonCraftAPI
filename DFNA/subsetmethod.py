# Convertion of an NFA to a DFA using the subset construction method
# based on the algorithm from the book Compiladores: Principios, Técnicas y Herramientas. Addison-Wesley. 1990


def clousureE(estado, nfa):
    """Calcula la cerradura epsilon (epsilon closure) de un estado en un NFA"""
    # Usamos un conjunto para evitar duplicados
    estados_cerradura = set()
    estados_cerradura.add(estado)

    # Creamos una pila para realizar una exploración en profundidad
    stack = [estado]

    # Mientras haya estados por procesar en la pila
    while stack:
        current_state = stack.pop()
        symbol, nextStates = nfa.get_transitions_by_state(current_state)

        # Si el símbolo es "&", seguimos buscando más transiciones epsilon
        if symbol == '&':
            for next_state in nextStates:
                if next_state not in estados_cerradura:
                    estados_cerradura.add(next_state)
                    stack.append(next_state)

    return estados_cerradura

def setClousureE(moveList, nfa):
    """Calcula la cerradura epsilon (epsilon closure) de un conjunto de estados que salen de Mueve"""
    clousure = set()
    for state in moveList:
        for i in clousureE(state, nfa):
            clousure.add(i)
    return clousure

def move(T, a, nfa):
    """Calcula el conjunto de estados a los que se puede llegar desde cualquier estado en T con el símbolo a"""
    # Usamos un conjunto para evitar duplicados
    move_set = set()

    # Para cada estado en el conjunto T
    for state in T:
        # Revisamos todas las transiciones desde el estado actual
        for (current_state, symbol), next_states in nfa.transitions.items():
            if current_state == state and symbol == a:
                # Si el símbolo coincide con 'a', añadimos los estados alcanzables al conjunto
                for next_state in next_states:
                    if isinstance(next_state, list):
                        move_set.update(next_state)  # Si next_state es una lista, añadimos sus elementos
                    else:
                        move_set.add(next_state)  # Si es un estado individual, lo añadimos directamente
    return move_set

def subset_construction(nfa):
    EstadosD = []  # Conjunto de estados DFA
    TranD = {}     # Transiciones DFA como diccionario
    Subconjuntos = {}  # Para almacenar los subconjuntos de cada estado

    # Agregamos la cerradura epsilon del estado inicial del NFA
    initial_closure = tuple(clousureE(nfa.initial, nfa))  # Convertimos a tupla para usarlo en comparaciones
    EstadosD.append(initial_closure)

    # Creamos una lista para estados por procesar
    pending_states = [initial_closure]

    # Mapa para los labels
    state_labels = {}
    label_counter = 0

    while pending_states:
        T = pending_states.pop(0)  # Sacamos el siguiente conjunto de estados por procesar
        
        # Asignar un label a T si no tiene uno
        if T not in state_labels:
            state_labels[T] = chr(65 + label_counter)  # 65 es el código ASCII para 'A'
            label_counter += 1
        
        # Guardar el subconjunto correspondiente al estado
        Subconjuntos[state_labels[T]] = T

        for a in nfa.alphabet:  # Iteramos sobre el alfabeto del NFA
            U = tuple(setClousureE(move(T, a, nfa), nfa))  # Calculamos la cerradura epsilon del conjunto U
            
            # Si el conjunto U no es vacío y no está en EstadosD, lo agregamos
            if U and U not in EstadosD:
                EstadosD.append(U)
                pending_states.append(U)

                # Asignar un label a U si no tiene uno
                state_labels[U] = chr(65 + label_counter)  # 65 es 'A'
                label_counter += 1
            
            # Agregamos la transición al DFA
            if U:
                TranD[(state_labels[T], a)] = state_labels.get(U, None)

    return EstadosD, TranD, Subconjuntos


            