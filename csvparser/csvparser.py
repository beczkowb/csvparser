# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import decimal
import operator
from . import validators


class Parser(object):
    fields_order = None

    def __init__(self):
        self.errors = None

    @classmethod
    def parse_file(cls, file_path, start_from_line=1, end_at_line=None,
                   csv_reader=csv.reader, **kwargs):

        with open(file_path, 'r') as file:
            reader = csv_reader(file, **kwargs)
            fields = cls.get_all_field_names_declared_by_user()

            for skipped_row in range(1, start_from_line):
                next(reader)

            for line_num, row in enumerate(reader, start=start_from_line):
                if end_at_line is not None and line_num > end_at_line:
                    break

                instance = cls()
                for i, field in enumerate(fields):
                    setattr(instance, field, row[i])
                yield instance

    @classmethod
    def get_all_field_names_declared_by_user(cls):
        return cls.fields_order

    def is_valid(self):
        self.errors = []

        for field in self.get_all_field_names_declared_by_user():
            getattr(type(self), field).is_valid(self, type(self), field)
            field_errors = getattr(type(self), field).errors(self)
            self.errors.extend(field_errors)

        return len(self.errors) == 0


class CharFieldMinLengthValidator(validators.CharFieldLengthValidator):
    def __init__(self, min_length):
        super(CharFieldMinLengthValidator, self).__init__(min_length, operator.ge,
                                                          '{field_name} len smaller than min_length')


class NumericalFieldValueValidator(validators.CompareValidator):
    def apply_operator(self, value):
        return self.compare_operator(value, self.threshold)


class IntegerFieldMaxValidator(NumericalFieldValueValidator):
    def __init__(self, max_value):
        super(IntegerFieldMaxValidator, self).__init__(max_value, operator.le,
                                                       '{field_name} higher than max')


class IntegerFieldMinValidator(NumericalFieldValueValidator):
    def __init__(self, min_value):
        super(IntegerFieldMinValidator, self).__init__(min_value, operator.ge,
                                                       '{field_name} lower than min')


class DecimalFieldMaxValidator(NumericalFieldValueValidator):
    def __init__(self, max_value):
        if not isinstance(max_value, decimal.Decimal):
            raise TypeError('max_value on DecimalFieldMaxValidator has to be decimal')

        super(DecimalFieldMaxValidator, self).__init__(max_value, operator.le,
                                                       '{field_name} higher than max_value')


class DecimalFieldMinValidator(NumericalFieldValueValidator):
    def __init__(self, min_value):
        if not isinstance(min_value, decimal.Decimal):
            raise TypeError('min_value on DecimalFieldMinValidator has to be decimal')

        super(DecimalFieldMinValidator, self).__init__(min_value, operator.ge,
                                                       '{field_name} lower than min_value')
