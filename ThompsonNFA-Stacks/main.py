from postfixer import shunting_yard
from construction import thompson

if __name__ == "__main__":
    infix = input('Enter infix expression: ')
    postfix = shunting_yard(infix)
    print('Postfix expression:', postfix)
    nfa = thompson(postfix)
    nfa.print_transition_table()
