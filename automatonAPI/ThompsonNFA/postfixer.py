#In order to parse regular expressions by Thompson method, we need to convert them to postfix notation.
#Postfix notation is a mathematical notation in which the operators follow the number, 
#is a way of writing expressions without the need for parentheses.
#This is done by using the Shunting Yard Algorithm.

#This is an implementation of the Shunting Yard Algorithm to convert infix expressions
#to postfix expressions extracted from: https://en.wikipedia.org/wiki/Shunting_yard_algorithm#The_algorithm_in_detail

#The algorithm is as follows:
#1. Read a token.
#2. If the token is a number (a symbol in our case), then add it to the output queue.
#3. If the token is an operator, then:
#    1. While there is an operator at the top of the operator stack with greater precedence:
#        1. Pop operators from the operator stack onto the output queue.
#    2. Push the current operator onto the operator stack.
#4. If the token is a left parenthesis, then push it onto the operator stack.
#5. If the token is a right parenthesis:
#    1. Until the token at the top of the operator stack is a left parenthesis, pop operators from the operator stack onto the output queue.
#    2. Pop the left parenthesis from the stack.
#    3. If the stack runs out without finding a left parenthesis, then there are mismatched parentheses.
#6. When there are no more tokens to read:
#    1. While there are still operator tokens on the stack:
#        1. If the operator token on the top of the stack is a parenthesis, then there are mismatched parentheses.
#        2. Pop the operator onto the output queue.
#7. Exit.

# First define the precedence of the operators and the operators themselves
# The higher the number, the higher the precedence
precedence = {
    '*': 1,
    '+': 1,
    '?': 1,
    '.': 2,
    '|': 3,
    '(': 4,
    ')': 4,
}

# Define the operators
operators = ['|', '.', '*', '+', '?', '(', ')']

# Define the shunting yard algorithm with parentheses validation
def shunting_yard(infix):
    output = []
    symbols = []
    stack = []
    infix = append_operator(infix)
    
    # Contadores de paréntesis para validación
    open_paren_count = 0
    close_paren_count = 0

    for c in infix:
        if c not in operators:
            output.append(c)
            if c not in symbols: 
                symbols.append(c)
        elif c == '(':
            stack.append(c)
            open_paren_count += 1  # Incrementa cuando encontramos '('
        elif c == ')':
            close_paren_count += 1  # Incrementa cuando encontramos ')'
            # Si hay más paréntesis de cierre que de apertura, hay un error
            if close_paren_count > open_paren_count:
                raise ValueError("Error: Paréntesis de cierre no tiene correspondiente paréntesis de apertura")
            
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()  # Elimina el paréntesis de apertura correspondiente
        else:
            # Comprobamos la precedencia de operadores
            while stack and precedence[stack[-1]] <= precedence[c]:
                currentC = stack.pop()
                output.append(currentC)
            stack.append(c)
    
    # Si hay más paréntesis de apertura que de cierre al final, hay un error
    if open_paren_count != close_paren_count:
        raise ValueError("Error: Paréntesis de apertura no tiene correspondiente paréntesis de cierre")
    
    # Vacía el stack restante
    while stack:
        currentC = stack.pop()
        # Si encontramos un paréntesis de apertura en el stack al final, es un error
        if currentC == '(':
            raise ValueError("Error: Paréntesis de apertura no tiene correspondiente paréntesis de cierre")
        output.append(currentC)

    return output, symbols


# Add the concatenation operator to the infix expression
def append_operator(infix):
    result = []
    for i, c in enumerate(infix):
        result.append(c)
        if c == '(' or c == '|':
            continue
        if i + 1 < len(infix):
            lookahead = infix[i + 1]
            if lookahead == ')' or lookahead == '|' or lookahead == '*' or lookahead == '+' or lookahead == '?':
                continue
            result.append('.')
        
    return result