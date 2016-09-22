import unittest
from csvparser.parser import Parser


class TestIterParser(unittest.TestCase):
    def test(self):
        def Field(object):
            def __init__(self, name):
                self.name = '_' + name

            def __get__(self, instance, owner):
                getattr(instance, self.name)

            def __set__(self, instance, value):
                setattr(instance, self.name, value)

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


if __name__ == '__main__':
    unittest.main()