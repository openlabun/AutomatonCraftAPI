from re_reader import re_reader
from re_parser import re_parser
from nfa import NFA
from time import process_time

program_title = '''

#        FINITE AUTOMATA        #

Generate NFA's based on a regular expression NOTE: for epsilon expression, please use the letter "e"
'''

main_menu = '''
What would you like to do?
1. Set a regular expression
2. Test a string with the given regular expression
0. Exit out of the program
'''
thompson_msg = '''
    # THOMPSON AND POWERSET CONSTRUCION # '''
invalid_opt = '''
Err: That's not a valid option!
'''
generate_diagram_msg = '''
Would you like to generate and view the diagram? [y/n] (default: n)'''
type_regex_msg = '''
Type in a regular expression '''
type_string_msg = '''
Type in a string '''

if __name__ == "__main__":
    print(program_title)
    opt = None
    regex = None
    method = None

    while opt != 0:
        print(main_menu)
        opt = input('> ')

        if opt == '1':
            print(type_regex_msg)
            regex = input('> ')

            try:
                reader = re_reader(regex)
                tokens = reader.CreateTokens()
                parser = re_parser(tokens)
                tree = parser.Parse()

                print('\n\tExpression accepted!')
                print('\tParsed tree:', tree)

            except AttributeError as e:
                print(f'\n\tERR: Invalid expression (missing parenthesis)')

            except Exception as e:
                print(f'\n\tERR: {e}')

        if opt == '2':
            if not regex:
                print('\n\tERR: You need to set a regular expression first!')
                opt = None
            else:
                print(thompson_msg)
                print(type_string_msg)
                regex_input = input('> ')

                nfa = NFA(tree, reader.GetSymbols(), regex_input)
                start_time = process_time()
                nfa_regex = nfa.EvalRegex()
                stop_time = process_time()

                print('\nTime to evaluate: {:.5E} seconds'.format(
                    stop_time - start_time))
                print('Does the string belongs to the regex (NFA)?')
                print('>', nfa_regex)

                print(generate_diagram_msg)
                generate_diagram = input('> ')

                if generate_diagram == 'y':
                    nfa.WriteNFADiagram()

        elif opt == '0':
            print('See you later!')
            exit(1)
