from ThompsonNFA.nfa import evaluate_string_dfa

def afdOptimization(TranD, translated_subconjuntos,dfa, initial, accept = []):
    # Optimización del DFA
    # Se eliminan los estados equivalentes

    #Identificar los estados equivalentes en el DFA con translated_subconjuntos
    equivalent_states = []
    for label1, estados1 in translated_subconjuntos.items():
        for label2, estados2 in translated_subconjuntos.items():
            if label1 != label2 and estados1 == estados2:
                if (label2, label1) not in equivalent_states:
                    equivalent_states.append((label1, label2))

    # Eliminar los estados equivalentes del DFA en la TranD y en el dfa
    todelete = []
    todeletedfa = []
    for label1, label2 in equivalent_states:
        for key, value in TranD.items():
            if value == label2:
                TranD[key] = label1
            if key[0] == label2:
                if key[0] in accept:
                    accept.remove(key[0])
                todelete.append(key)
        for key, value in dfa.transitions.items():
            if value == label2:
                dfa.transitions[key] = label1
            if key[0] == label2:
                todeletedfa.append(key)
    
    #quitar repetidos en todelete y todeletedfa
    todelete = list(set(todelete))
    todeletedfa = list(set(todeletedfa))
    for key in todelete:
        del TranD[key]
    for key in todeletedfa:
        del dfa.transitions[key]

    dfa.set_accept(accept)
    dfa.set_initial(initial)

    dfa.set_transitions(TranD)

    return TranD, dfa, initial, accept