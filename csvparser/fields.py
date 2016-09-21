import decimal
from .csvparser import ParserField


class CharField(ParserField):
    @staticmethod
    def create_real_value(raw_value):
        return raw_value


class DecimalField(ParserField):
    @staticmethod
    def create_real_value(raw_value):
        return decimal.Decimal(raw_value)