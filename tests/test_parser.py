import unittest
import os
import decimal
from csvparser.parser import Parser
from csvparser import fields


class Field(object):
    def __init__(self, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)


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


class AdPerformanceReportParser(Parser):
    impressions = fields.IntegerField()
    clicks = fields.IntegerField()
    conversions = fields.IntegerField()
    cost = fields.DecimalField()
    ad_id = fields.CharField()

    fields_order = ['impressions', 'clicks', 'conversions', 'cost', 'ad_id']


class AdPerformanceReportWithNullableFieldsParser(Parser):
    impressions = fields.IntegerField(null_symbols=['--', ''])
    clicks = fields.IntegerField()
    conversions = fields.IntegerField()
    cost = fields.DecimalField()
    ad_id = fields.CharField(null_symbols=['--', ''])

    fields_order = ['impressions', 'clicks', 'conversions', 'cost', 'ad_id']


class AdPerformanceReportWithNullableFieldsAndDateFieldParser(Parser):
    impressions = fields.IntegerField(null_symbols=['--', ''])
    clicks = fields.IntegerField()
    conversions = fields.IntegerField()
    cost = fields.DecimalField()
    ad_id = fields.CharField(null_symbols=['--', ''])
    date = fields.DateField('%Y-%m-%d')

    fields_order = ['impressions', 'clicks', 'conversions', 'cost', 'ad_id', 'date']


class FromFileObjectTestCase(unittest.TestCase):
    def test(self):
        test_file_path = os.path.join('test_files', 'adperformancereport_with_headers.csv')
        test_file = open(test_file_path)
        results = AdPerformanceReportParser.parse_file_object(test_file, start_from_line=2)
        results = list(results)

        self.assertEqual(results[0].impressions, 1000)
        self.assertEqual(results[0].clicks, 200)
        self.assertEqual(results[0].conversions, 5)
        self.assertEqual(results[0].cost, decimal.Decimal('50000.03'))
        self.assertEqual(results[0].ad_id, '1232188')

        self.assertEqual(results[1].impressions, 56000)
        self.assertEqual(results[1].clicks, 3224)
        self.assertEqual(results[1].conversions, 900)
        self.assertEqual(results[1].cost, decimal.Decimal('202000.44'))
        self.assertEqual(results[1].ad_id, '8324125')


class ParserWithNullableFieldsTestCase(unittest.TestCase):
    def test(self):
        test_file_path = os.path.join('test_files', 'adperformancereport_with_headers_and_null_values.csv')
        results = AdPerformanceReportWithNullableFieldsParser.parse_file(test_file_path, start_from_line=2)
        results = list(results)

        self.assertEqual(results[0].impressions, None)
        self.assertEqual(results[0].clicks, 200)
        self.assertEqual(results[0].conversions, 5)
        self.assertEqual(results[0].cost, decimal.Decimal('50000.03'))
        self.assertEqual(results[0].ad_id, None)

        self.assertEqual(results[1].impressions, None)
        self.assertEqual(results[1].clicks, 3224)
        self.assertEqual(results[1].conversions, 900)
        self.assertEqual(results[1].cost, decimal.Decimal('202000.44'))
        self.assertEqual(results[1].ad_id, None)


class ParserWithDateFieldTestCase(unittest.TestCase):
    def test(self):
        test_file_path = os.path.join('test_files', 'adperformancereport_with_headers_and_null_values_and_date_field.csv')
        results = AdPerformanceReportWithNullableFieldsAndDateFieldParser.parse_file(test_file_path, start_from_line=2)
        results = list(results)

        self.assertEqual(results[0].impressions, None)
        self.assertEqual(results[0].clicks, 200)
        self.assertEqual(results[0].conversions, 5)
        self.assertEqual(results[0].cost, decimal.Decimal('50000.03'))
        self.assertEqual(results[0].ad_id, None)

        self.assertEqual(results[0].date.year, 2016)
        self.assertEqual(results[0].date.month, 9)
        self.assertEqual(results[0].date.day, 30)

        self.assertEqual(results[1].impressions, None)
        self.assertEqual(results[1].clicks, 3224)
        self.assertEqual(results[1].conversions, 900)
        self.assertEqual(results[1].cost, decimal.Decimal('202000.44'))
        self.assertEqual(results[1].ad_id, None)

        self.assertEqual(results[1].date.year, 2016)
        self.assertEqual(results[1].date.month, 12)
        self.assertEqual(results[1].date.day, 20)