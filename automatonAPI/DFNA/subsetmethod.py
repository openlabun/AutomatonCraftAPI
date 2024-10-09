# Convertion of an NFA to a DFA using the subset construction method
# based on the algorithm from the book Compiladores: Principios, Técnicas y Herramientas. Addison-Wesley. 1990

from ThompsonNFA.nfa import NFA


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
                if isinstance(next_state, list):
                    while isinstance(next_state[0], list):
                        next_state = next_state[0]
                    for i in next_state:
                        if i not in estados_cerradura:
                            estados_cerradura.add(i)
                            stack.append(i)
                elif next_state not in estados_cerradura:
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

def move(T, a, nfa, switch=False):
    """Calcula el conjunto de estados a los que se puede llegar desde cualquier estado en T con el símbolo a"""
    # Usamos un conjunto para evitar duplicados
    move_set = set()

    # Para cada estado en el conjunto T
    for state in T:
        # Revisamos todas las transiciones desde el estado actual
        for (current_state, symbol), next_states in nfa.transitions.items():
            if symbol == "&" and switch:
                continue
            if current_state == state and symbol == a:
                # Si el símbolo coincide con 'a', añadimos los estados alcanzables al conjunto
                for next_state in next_states:
                    
                    if isinstance(next_state, list):
                        while isinstance(next_state[0], list):
                            next_state = next_state[0]
                        move_set.update(next_state)  # Si next_state es una lista, añadimos sus elementos
                    else:
                        move_set.add(next_state)  # Si es un estado individual, lo añadimos directamente
    return move_set

def subset_construction(nfa):
    EstadosD = []  # Conjunto de estados DFA
    TranD = {}     # Transiciones DFA como diccionario
    Subconjuntos = {}  # Para almacenar los subconjuntos de cada estado
    SubconjuntosEstadosSignificativos = {}  # Para almacenar los subconjuntos de estados significativos de cada estado 
    estadosA = []
    estadosI = []

    # Agregamos la cerradura epsilon del estado inicial del NFA
    initial_closure = tuple(clousureE(nfa.initial, nfa))  # Convertimos a tupla para usarlo en comparaciones
    EstadosD.append(initial_closure)

    # Creamos una lista para estados por procesar
    pending_states = [initial_closure]

    # Mapa para los labels
    state_labels = {}
    label_counter = 0
    if nfa.accept in initial_closure:
        estadosA.append(chr(65 + label_counter))
    if nfa.initial in initial_closure:
        estadosI.append(chr(65 + label_counter))
    

    while pending_states:
        T = pending_states.pop(0)  # Sacamos el siguiente conjunto de estados por procesar
        
        # Asignar un label a T si no tiene uno
        if T not in state_labels:
            state_labels[T] = chr(65 + label_counter)  # 65 es el código ASCII para 'A'
            initial=state_labels[T]
            label_counter += 1
        
        TSignificativos = []
        for state in T:
            if move([(state)], '&', nfa):
                pass
            else:
                TSignificativos.append(state)
        
        # Guardar el subconjunto correspondiente al estado
        Subconjuntos[state_labels[T]] = T
        SubconjuntosEstadosSignificativos[state_labels[T]] = TSignificativos

        for a in nfa.alphabet:  # Iteramos sobre el alfabeto del NFA
            U = tuple(setClousureE(move(T, a, nfa,switch=True), nfa))  # Calculamos la cerradura epsilon del conjunto U

            
            # Si el conjunto U no es vacío y no está en EstadosD, lo agregamos
            if U and U not in EstadosD:
                EstadosD.append(U)
                pending_states.append(U)

                # Asignar un label a U si no tiene uno
                state_labels[U] = chr(65 + label_counter)  # 65 es 'A'
                label_counter += 1

                #Marcar el estado si es final con un *
                if nfa.accept in U:
                    state_labels[U] = state_labels[U]
                    accept = state_labels[U]
                    estadosA.append(state_labels[U])
            
            # Agregamos la transición al DFA
            if U:
                TranD[(state_labels[T], a)] = state_labels.get(U, None)
        
    #Build new Graph with the new 
    dfa = NFA(estadosI,estadosA)
    for key, value in TranD.items():
        if value:
            if isinstance(value, list):
                if isinstance(value[0], list):
                    while isinstance(value[0], list):
                        value = value[0]
            dfa.add_transition(key[0], key[1], value)

    
    return EstadosD, TranD, Subconjuntos, SubconjuntosEstadosSignificativos, dfa, estadosA, estadosI

def subset(nfa):
    EstadosD, TranD, Subconjuntos, SubconjuntosEstadosSignificativos, dfa, estadosA, estadosI = subset_construction(nfa)
    # Traducir los estados en Subconjuntos
    translated_subconjuntos = {}
    for label, estados in Subconjuntos.items():
        translated_states = [nfa.state_to_number.get(state, -1) for state in estados]
        translated_subconjuntos[label] = translated_states
    # Traducir los estados en Subconjuntos
    translated_subconjuntos2 = {}
    for label, estados in SubconjuntosEstadosSignificativos.items():
        translated_states = [nfa.state_to_number.get(state, -1) for state in estados]
        translated_subconjuntos2[label] = translated_states
    return TranD, translated_subconjuntos, translated_subconjuntos2, dfa, estadosA, estadosI
