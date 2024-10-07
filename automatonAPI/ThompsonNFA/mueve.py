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
        
    
    print(f"Estado actual: {state}, Símbolo: {symbol}, Próximos estados: {next_states}")
    # Procesar transiciones epsilon (símbolo "&")
    if symbol == "&":
        for next_state in next_states:
            if isinstance(next_state, list):
                for state in next_state:
                    all_paths = route(string[:], state, nfa, path.copy(), all_paths)  # Copia el camino
            else:
                all_paths = route(string[:], next_state, nfa, path.copy(), all_paths)  # Copia el camino
    
    # Procesar transiciones normales, coincidiendo el símbolo
    elif string and string[0] == symbol:
        for next_state in next_states:
            if isinstance(next_state, list):
                next_state = next_state[0]
            # Consumir el símbolo y moverse al siguiente estado
            new_string = string.copy()  # Copia la cadena
            new_string.pop(0)
            all_paths = route(new_string, next_state, nfa, path.copy(), all_paths)  # Avanzar en la cadena
    
    # Si no hay coincidencias o transiciones
    if string or symbol != "&":
        all_paths.append((path.copy(), False))  # Añadir camino no aceptado solo al final
    return all_paths  # Retornar todos los caminos