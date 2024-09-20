# Define the NFA class
class NFA:
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept
        self.transitions = {}

    def add_transition(self, state, symbol, next_state):
        if (state, symbol) not in self.transitions:
            self.transitions[(state, symbol)] = []
        self.transitions[(state, symbol)].append(next_state)


# Functions to create basic NFA fragments
# Rule #1: An Empty Expression (ε) is an NFA with two states and an epsilon transition between them.
# Rule #2: A Single Symbol (a) is an NFA with two states, one initial state and one final state, and a transition between them labeled with the symbol.
def basic_nfa(initial=None, accept=None):
    initial = object()
    accept = object()
    nfa = NFA(initial, accept)
    return nfa

# Functions to create NFA fragments for operators

# Rule #3: Union expression
def union_nfa(nfa1, nfa2):
    initial = object()
    accept = object()
    nfa = basic_nfa(initial, accept)
    nfa.add_transition(initial, "e", nfa1.initial)
    nfa.add_transition(initial, "e", nfa2.initial)
    nfa.add_transition(nfa1.accept, "e", accept)
    nfa.add_transition(nfa2.accept, "e", accept)
    return nfa

# Rule #4: Concatenation expression
def concat_nfa(nfa1, nfa2):
    nfa1.add_transition(nfa1.accept, "e", nfa2.initial)
    nfa1.accept = nfa2.accept
    return nfa1

# Rule #5: Kleene star expression
def kleene_nfa(nfa):
    initial = object()
    accept = object()
    nfa.add_transition(initial, "e", accept)
    nfa.add_transition(initial, "e", nfa.initial)
    nfa.add_transition(nfa.accept, "e", nfa.initial)
    nfa.add_transition(nfa.accept, "e", accept)
    nfa.initial = initial
    nfa.accept = accept
    return nfa

# Rule #6: Positive closure expression
def positive_nfa(nfa):
    initial = object()
    accept = object()
    nfa.add_transition(initial, "e", nfa.initial)
    nfa.add_transition(nfa.accept, "e", accept)
    nfa.add_transition(nfa.accept, "e", nfa.initial)
    nfa.initial = initial
    nfa.accept = accept
    return nfa

# Rule #7: Optional expression
def optional_nfa(nfa):
    initial = object()
    accept = object()
    nfa.add_transition(initial, "e", nfa.initial)
    nfa.add_transition(nfa.accept, "e", accept)
    nfa.initial = initial
    nfa.accept = accept


