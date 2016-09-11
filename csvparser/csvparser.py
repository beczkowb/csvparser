import csv
import decimal
import operator


class Parser(object):
    fields_order = None

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


class ParserField(object):
    fields_counter = 0

    def __init__(self, validators=None):
        if validators is None:
            self.validators = []
        else:
            self.validators = validators

        self.name = None
        self.init_done = False
        self.name = '_parser_field' + str(ParserField.fields_counter)
        self.errors_field_name = '_parser_field_errors' + str(ParserField.fields_counter)
        ParserField.fields_counter += 1

    def __set__(self, instance, value):
        setattr(instance, self.name, value)

    def is_valid(self, instance, cls, field_name):
        value = self.__get__(instance, cls)
        setattr(instance, self.errors_field_name, [])
        valid = True

        for validator in self.validators:
            if not validator.is_valid(value, field_name):
                current_errors = getattr(instance, self.errors_field_name)
                current_errors.extend(validator.errors)
                valid = False

        return valid

    def errors(self, instance):
        return getattr(instance, self.errors_field_name)


class IntegerField(ParserField):
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return int(getattr(instance, self.name))


class DecimalField(ParserField):
    def __get__(self, instance, cls):
        return decimal.Decimal(getattr(instance, self.name))


class CharField(ParserField):
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return getattr(instance, self.name)


class CompareValidator(object):
    def __init__(self, threshold, compare_operator, error_message_template):
        self.threshold = threshold
        self.errors = []
        self.compare_operator = compare_operator
        self.error_message_template = error_message_template

    def is_valid(self, string, field_name):
        string_is_valid = self.apply_operator(string)
        if string_is_valid:
            return True
        else:
            self.errors = [self.error_message_template.format(field_name=field_name)]
            return False

    def apply_operator(self, value):
        pass


class CharFieldLengthValidator(CompareValidator):
    def apply_operator(self, value):
        return self.compare_operator(len(value), self.threshold)


class CharFieldMaxLengthValidator(CharFieldLengthValidator):
    def __init__(self, max_length):
        super().__init__(max_length, operator.le,
                         '{field_name} len bigger than max_length')


class CharFieldMinLengthValidator(CharFieldLengthValidator):
    def __init__(self, min_length):
        super().__init__(min_length, operator.ge,
                         '{field_name} len smaller than min_length')