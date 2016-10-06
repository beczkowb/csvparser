import unittest
from csvparser import fields


class TestClassWithDateField(object):
    date_attr1 = fields.DateField(date_format='%Y-%m-%d')
    date_attr2 = fields.DateField(date_format='%Y-%m-%d')


class TestClassWithDateField2(object):
    date_attr1 = fields.DateField(date_format='%d-%m-%Y')
    date_attr2 = fields.DateField(date_format='%Y-%m-%d')


class TestClassWithNullableFields(object):
    nullable_field1 = fields.CharField(null_symbols=['--', ''])
    nullable_field2 = fields.IntegerField(null_symbols=['--', ''])
    nullable_field3 = fields.IntegerField()


class DateFieldTestCase(unittest.TestCase):
    def test_date_format1(self):
        test_object = TestClassWithDateField()
        test_object.date_attr1 = '2016-07-09'
        test_object.date_attr2 = '2017-12-27'

        self.assertEqual(test_object.date_attr1.year, 2016)
        self.assertEqual(test_object.date_attr1.month, 7)
        self.assertEqual(test_object.date_attr1.day, 9)

        self.assertEqual(test_object.date_attr2.year, 2017)
        self.assertEqual(test_object.date_attr2.month, 12)
        self.assertEqual(test_object.date_attr2.day, 27)

    def test_date_format2(self):
        test_object = TestClassWithDateField2()
        test_object.date_attr1 = '23-12-1993'
        test_object.date_attr2 = '2017-12-27'

        self.assertEqual(test_object.date_attr1.year, 1993)
        self.assertEqual(test_object.date_attr1.month, 12)
        self.assertEqual(test_object.date_attr1.day, 23)

        self.assertEqual(test_object.date_attr2.year, 2017)
        self.assertEqual(test_object.date_attr2.month, 12)
        self.assertEqual(test_object.date_attr2.day, 27)


class NullableFieldTestCase(unittest.TestCase):
    def test(self):
        test_object = TestClassWithNullableFields()

        test_object.nullable_field1 = ''
        self.assertIsNone(test_object.nullable_field1)

        test_object.nullable_field1 = '--'
        self.assertIsNone(test_object.nullable_field1)

        test_object.nullable_field2 = '--'
        self.assertIsNone(test_object.nullable_field2)

        test_object.nullable_field2 = ''
        self.assertIsNone(test_object.nullable_field2)

        test_object.nullable_field3 = '--'

        with self.assertRaises(ValueError) as err:
            x = test_object.nullable_field3