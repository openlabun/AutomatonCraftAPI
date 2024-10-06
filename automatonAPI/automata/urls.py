from django.urls import path
from .views import ValidateExpression, BuildThompsonNFA, BuildSubsetDFA, OptimizeDFA, EvaluateString

urlpatterns = [
    path('validate/', ValidateExpression.as_view(), name='validate_expression'),
    path('thompson/', BuildThompsonNFA.as_view(), name='build_thompson_nfa'),
    path('subset/', BuildSubsetDFA.as_view(), name='build_subset_dfa'),
    path('optimize/', OptimizeDFA.as_view(), name='optimize_dfa'),
    path('evaluate/', EvaluateString.as_view(), name='evaluate_string'),
]