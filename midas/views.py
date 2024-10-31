
from rest_framework.views import APIView
from midas.alpaca.proxy import fetch_alpaca_data
from .serializers import TimeSymbolSerializer, IndicatorSerializer, \
    MultiIndicatorSerializer
from rest_framework.response import Response
from rest_framework import status
from midas.models import IndicatorInstance
import math


class TimeSymbolView(APIView):
    def get(self, request, symbol, format=None):
        try:
            data = fetch_alpaca_data(symbol).data[symbol]
            serializer = TimeSymbolSerializer(
                data, many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class IndicatorSymbolView(APIView):
    def single_indicator(self, symbol, symbol_data, indicator, indicator_data):
        time_values = []
        data_symbol = symbol_data.data[symbol]
        for index, value in enumerate(indicator_data):
            time_values.append({
                'timestamp': data_symbol[index].timestamp,
                'value': value if not math.isnan(value) else None
            })
        out = {
            "name": indicator.name,
            "options": indicator.options,
            "values": time_values,
        }
        serializer = IndicatorSerializer(out)
        return serializer

    def multi_indicator(self, symbol, symbol_data, indicator, indicator_data):
        cols = []
        for col in indicator_data.columns:
            data_cols = getattr(indicator_data, col)
            col_values = []
            data_symbol = symbol_data.data[symbol]
            for index, value in enumerate(data_cols):
                col_values.append({
                    'timestamp': data_symbol[index].timestamp,
                    'value': value if not math.isnan(value) else None
                })
            col_dict = {
                "name": col,
                "values": col_values
            }
            cols.append(col_dict)
        out = {
            "options": indicator.options,
            "cols": cols
        }
        serializer = MultiIndicatorSerializer(
            out
        )
        return serializer

    def get(self, request, symbol, instance, format=None):
        try:
            symbol_data = fetch_alpaca_data(symbol)
            indicator = IndicatorInstance.objects.get(
                name=instance
            )
            indicator_data = indicator.process(symbol_data.df)
            serializer = None
            if hasattr(indicator_data, "columns"):
                serializer = self.multi_indicator(symbol, symbol_data,
                                                  indicator, indicator_data)
            else:
                serializer = self.single_indicator(symbol, symbol_data,
                                                   indicator, indicator_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
