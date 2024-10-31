import talib


def get_grouped_indicators():
    return talib.get_function_groups().items()


def get_indicators():
    return talib.get_functions()
