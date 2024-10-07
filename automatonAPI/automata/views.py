from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Funtion to convert infix to postfix
from ThompsonNFA.postfixer import shunting_yard

# Function to convert build the NFA from the postfix expression by Thompson's construction
from ThompsonNFA.construction import thompson

# Function to convert the NFA to DFA by the subset construction method
from DFNA.subsetmethod import subset

# Function to optimize the DFA by significant states method
from FNA.significantstatesmethod import afdOptimization

# Funtion to evaluate the string in the NFA
from ThompsonNFA.nfa import evaluate_string, evaluate_string_dfa



optimizeddfa= None

def thompsonfunct(postfix, symbols):
    nfa = thompson(postfix)
    i, a = nfa.build_transition_table()
    for symbol in symbols:
        nfa.alphabet.add(symbol)
    global thompsonnfa
    thompsonnfa = nfa
    return Response({
        'transition_table': nfa.get_transition_table(),
        'initial_state': i,
        'accept_states': a
    }), nfa
    
def subsetfunct(nfa):
    TranD, TranslatedSubset, TranslatedSubsetSignificantSates, dfa, estadosA, estadosI = subset(nfa)
    # Convertir las claves de TranD de tuplas a cadenas
    TranD_str = {f'{T}:({a},{U})' for (T, a), U in TranD.items()}
    #Trand Json
    global subsetdfna
    subsetdfna = dfa
    return Response({
        'TranD': TranD_str,
        'States': TranslatedSubset,
        'initial_state': estadosI,
        'accept_states': estadosA,
    }),TranD, TranslatedSubset, TranslatedSubsetSignificantSates, dfa, estadosA, estadosI


class ValidateExpression(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'expression': openapi.Schema(type=openapi.TYPE_STRING, description='Mathematical expression to validate.')
            }
        ),
        responses={
            200: openapi.Response(
                description='Successful response',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'postfix': openapi.Schema(type=openapi.TYPE_STRING, description='Postfix notation of the expression.'),
                        'symbols': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description='Symbols extracted from the expression.')
                    }
                )
            ),
            400: openapi.Response(
                description='Error response',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message.')
                    }
                )
            ),
        }
    )
    def post(self, request):
        expression = request.data['expression']
        try:
            postfix, symbols = shunting_yard(expression)
            return Response({
                'postfix': postfix,
                'symbols': symbols
            })
        except ValueError as e:
            return Response({
                'error': str(e)
            })


class BuildThompsonNFA(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'postfix': openapi.Schema(type=openapi.TYPE_STRING, description='Postfix expression for NFA construction.'),
                'symbols': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description='Symbols for NFA construction.')
            }
        ),
        responses={
            200: openapi.Response(
                description='Successful response with NFA',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'nfa': openapi.Schema(type=openapi.TYPE_OBJECT, description='NFA representation.'),
                    }
                )
            ),
            400: openapi.Response(
                description='Error response',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message.')
                    }
                )
            ),
        }
    )
    def post(self, request):
        postfix = request.data['postfix']
        symbols = request.data['symbols']
        try:
            response, nfa = thompsonfunct(postfix, symbols)
            return response
        except ValueError as e:
            return Response({
                'error': str(e)
            })


class BuildSubsetDFA(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'postfix': openapi.Schema(type=openapi.TYPE_STRING, description='Postfix expression for DFA construction.'),
                'symbols': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description='Symbols for DFA construction.')
            }
        ),
        responses={
            200: openapi.Response(
                description='Successful response with DFA',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'TranD': openapi.Schema(type=openapi.TYPE_OBJECT, description='Transitions of the DFA.'),
                        'States': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description='States of the DFA.'),
                        'initial_state': openapi.Schema(type=openapi.TYPE_STRING, description='Initial state of the DFA.'),
                        'accept_states': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description='Accept states of the DFA.')
                    }
                )
            ),
            400: openapi.Response(
                description='Error response',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message.')
                    }
                )
            ),
        }
    )
    def post(self, request):
        postfix = request.data['postfix']
        symbols = request.data['symbols']
        response, nfa = thompsonfunct(postfix, symbols)
        try:
            response, TranD, States,StatesS, dfa, estadosA, estadosI= subsetfunct(nfa)
            return response
        except ValueError as e:
            return Response({
                'error': str(e)
            })


class OptimizeDFA(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'postfix': openapi.Schema(type=openapi.TYPE_STRING, description='Postfix expression for DFA optimization.'),
                'symbols': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description='Symbols for DFA optimization.')
            }
        ),
        responses={
            200: openapi.Response(
                description='Successful response with optimized DFA',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'TranD': openapi.Schema(type=openapi.TYPE_OBJECT, description='Optimized transitions of the DFA.'),
                        'States': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description='States of the DFA translated to the numbers.'),
                        'initial_state': openapi.Schema(type=openapi.TYPE_STRING, description='Initial state of the DFA.'),
                        'accept_states': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description='Accept states of the DFA.')
                    }
                )
            ),
            400: openapi.Response(
                description='Error response',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message.')
                    }
                )
            ),
        }
    )
    def post(self, request):
        postfix = request.data['postfix']
        symbols = request.data['symbols']
        response, nfa = thompsonfunct(postfix, symbols)
        response, TranD, States, StatesS, dfa, estadosA, estadosI = subsetfunct(nfa)
        try:
            print(estadosA)
            print(estadosI)
            TranD, AFD, initial, accept = afdOptimization(TranD, StatesS,dfa, estadosI, estadosA)
            global optimizeddfa
            optimizeddfa = AFD
            TranD_str = {f'{T}:({a},{U})' for (T, a), U in TranD.items()}
            return Response({
                'TranD': TranD_str,
                'States': StatesS,
                'initial_state': initial,
                'accept_states': accept
            })
        except ValueError as e:
            return Response({
                'error': str(e)
            })

class EvaluateString(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'string': openapi.Schema(type=openapi.TYPE_STRING, description='Input string to evaluate.'),
                'method': openapi.Schema(type=openapi.TYPE_STRING, description='Method to use for evaluation (thompson, subset, optimize).')
            }
        ),
        responses={
            200: openapi.Response(
                description='Successful evaluation response',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'paths': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description='Paths taken during evaluation.'),
                        'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Evaluation status (True/False).')
                    }
                )
            ),
            400: openapi.Response(
                description='Error response',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message.')
                    }
                )
            ),
        }
    )
    def post(self, request):
        string = list(request.data['string'])
        method = request.data['method']
        global thompsonnfa
        global subsetdfna
        global optimizeddfa
        try:
            if method == 'thompson':
                paths, status = evaluate_string(string, thompsonnfa)
            elif method == 'subset':
                paths, status = evaluate_string_dfa(string, subsetdfna)
            elif method == 'optimize':
                paths, status = evaluate_string_dfa(string, optimizeddfa)
            return Response({
                'paths': paths,
                'status': status
            })
        except ValueError as e:
            return Response({
                'error': str(e)
            })
