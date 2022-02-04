from rest_framework import serializers

class conversaoSerializer(serializers.Serializer):
    BRL = serializers.FloatField()
    USD = serializers.FloatField()
    EUR = serializers.FloatField()
    GBP = serializers.FloatField()
    ARS = serializers.FloatField()
    CAD = serializers.FloatField()
    AUD = serializers.FloatField()
    JPY = serializers.FloatField()
    CNY = serializers.FloatField()
    BTC = serializers.FloatField()