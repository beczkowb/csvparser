class CompareValidator(object):
    def __init__(self, threshold, compare_operator, error_message_template):
        self.threshold = threshold
        self.errors = []
        self.compare_operator = compare_operator
        self.error_message_template = error_message_template

    def is_valid(self, validated_object, field_name):
        object_is_valid = self.apply_operator(validated_object)
        if object_is_valid:
            return True
        else:
            self.errors = [self.error_message_template.format(field_name=field_name)]
            return False

    def apply_operator(self, value):
        pass


class CharFieldLengthValidator(CompareValidator):
    def apply_operator(self, value):
        return self.compare_operator(len(value), self.threshold)