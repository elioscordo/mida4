from rest_framework import serializers


class TimeSymbolSerializer(serializers.Serializer):
    vwap = serializers.FloatField()
    open = serializers.FloatField()
    close = serializers.FloatField()
    low = serializers.FloatField()
    high = serializers.FloatField()
    volume = serializers.IntegerField()
    trade_count = serializers.IntegerField()
    timestamp = serializers.DateTimeField()


class TimeIndicatorSerializer(serializers.Serializer):
    value = serializers.FloatField()
    timestamp = serializers.DateTimeField()


class IndicatorSerializer(serializers.Serializer):
    values = TimeIndicatorSerializer(many=True)
    type = serializers.ReadOnlyField(default='single')


class MultiIndicatorSerializer(serializers.Serializer):
    cols = IndicatorSerializer(many=True)
    options = serializers.JSONField(required=False)
    type = serializers.ReadOnlyField(default='multi')