from postfixer import shunting_yard
from construction import thompson
from nfa import evaluate_string

if __name__ == "__main__":
    infix = input('Enter infix expression: ')
    postfix, symbols = shunting_yard(infix)
    print('Postfix expression:', postfix)
    nfa = thompson(postfix)
    nfa.print_transition_table()
    print(nfa.get_transition_table())
    string = list(input('Enter string to evaluate: '))
    paths, status = evaluate_string(string,nfa)
    print(status)