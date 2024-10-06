from ThompsonNFA.postfixer import shunting_yard
from ThompsonNFA.construction import thompson
from ThompsonNFA.nfa import evaluate_string
from DFNA.subsetmethod import subset
from FNA.significantstatesmethod import afdOptimization


if __name__ == "__main__":
    infix = input('Enter infix expression: ')
    postfix, symbols = shunting_yard(infix)
    print('Postfix expression:', postfix)
    print('Symbols:', symbols)
    nfa = thompson(postfix)
    i,a = nfa.build_transition_table()
    for symbol in symbols:
        nfa.alphabet.add(symbol)
    print(nfa.get_transition_table())
    print(i)
    print(a)
    a,b,c = subset(nfa)
    #AFD = afdOptimization(a,c)
    #print(AFD)
    string = list(input('Enter string to evaluate: '))
    paths, status = evaluate_string(string,nfa)
    print(status)

