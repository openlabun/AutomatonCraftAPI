from rest_framework import serializers

class NFAInputSerializer(serializers.Serializer):
    expression = serializers.CharField()
    states = serializers.JSONField()  # Para enviar los estados
    alphabet = serializers.ListField(child=serializers.CharField())  # Alfabeto
    