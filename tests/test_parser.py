import unittest
from csvparser.parser import Parser


class Field(object):
    def __init__(self, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)


class TestParser(Parser):
    pass


class IterParserTestCase(unittest.TestCase):
    def test(self):
        class TestParser(Parser):
            attr1 = Field('attr1')
            attr2 = Field('attr2')

            fields_order = ['attr1', 'attr2']

        test_parser = TestParser()
        test_parser.attr1 = 'cat'
        test_parser.attr2 = 'dog'

        x, y = test_parser
        self.assertEqual(x, 'cat')
        self.assertEqual(y, 'dog')
        self.assertEqual(list(test_parser), ['cat', 'dog'])


class CheckIfFieldsOrderContainsProperNamesTestCase(unittest.TestCase):
    def test(self):
        class TestParser(Parser):
            field1 = Field('field1')
            field2 = Field('field2')

            fields_order = ['field', 'field2']

        with self.assertRaises(ValueError) as e:
            TestParser.check_if_fields_order_contains_proper_names()

        TestParser.fields_order = ['field', 'field']

        with self.assertRaises(ValueError) as e:
            TestParser.check_if_fields_order_contains_proper_names()

        TestParser.fields_order = ['field1', 'field']

        with self.assertRaises(ValueError) as e:
            TestParser.check_if_fields_order_contains_proper_names()

        TestParser.fields_order = ['field1', 'field2']

        self.assertTrue(TestParser.check_if_fields_order_contains_proper_names())


class FromFileObjectTestCase(unittest.TestCase):
    def test(self):
        pass


if __name__ == '__main__':
    unittest.main()