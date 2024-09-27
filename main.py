from ThompsonNFA.postfixer import shunting_yard
from ThompsonNFA.construction import thompson
from ThompsonNFA.nfa import evaluate_string
from DFNA.subsetmethod import clousureE, move, setClousureE, subset_construction

def testSubSetMethod(nfa):
    print('Subset construction (TRAND):')
    EstadosD, TranD, Subconjuntos = subset_construction(nfa)
    print(TranD)
    # Traducir los estados en Subconjuntos
    translated_subconjuntos = {}
    for label, estados in Subconjuntos.items():
        translated_states = [nfa.state_to_number.get(state, -1) for state in estados]
        translated_subconjuntos[label] = translated_states
    print("Subconjuntos traducidos:", translated_subconjuntos)
    return TranD, translated_subconjuntos

if __name__ == "__main__":
    infix = input('Enter infix expression: ')
    postfix, symbols = shunting_yard(infix)
    print('Postfix expression:', postfix)
    print('Symbols:', symbols)
    nfa = thompson(postfix)
    i,a =nfa.build_transition_table()
    for symbol in symbols:
        nfa.alphabet.add(symbol)
    print(nfa.get_transition_table())
    print(i)
    print(a)
    #testSubSetMethod(nfa)
    string = list(input('Enter string to evaluate: '))
    paths, status = evaluate_string(string,nfa)
    print(status)

