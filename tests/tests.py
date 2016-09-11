import unittest
import decimal
import os
import csv
from csvparser import csvparser


class AdPerformanceReportParser(csvparser.Parser):
    impressions = csvparser.IntegerField()
    clicks = csvparser.IntegerField()
    conversions = csvparser.IntegerField()
    cost = csvparser.DecimalField()
    ad_id = csvparser.CharField()

    fields_order = ['impressions', 'clicks', 'conversions',
                    'cost', 'ad_id']


class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.simple_test_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'test_files', 'adperformancereport.csv')

        self.simple_test_file_with_headers_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'test_files', 'adperformancereport_with_headers.csv')

        self.simple_test_file_with_summary_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'test_files', 'adperformancereport_with_summary.csv')

        self.simple_test_file_with_headers_and_summary_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'test_files', 'adperformancereport_with_headers_and_summary.csv')

        self.simple_test_file_with_headers_and_summary_path_and_custom_reader = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'test_files', 'adperformancereport_with_headers_and_summary_and_custom_reader.csv')

    def test_simple(self):
        rows = AdPerformanceReportParser.parse_file(file_path=self.simple_test_file_path)
        rows = list(rows)
        row1, row2 = rows

        self.assertEqual(row1.impressions, 1000)
        self.assertEqual(row1.clicks, 200)
        self.assertEqual(row1.conversions, 5)
        self.assertEqual(row1.cost, decimal.Decimal('50000.03'))
        self.assertEqual(row1.ad_id, '1232188')

        self.assertEqual(row2.impressions, 56000)
        self.assertEqual(row2.clicks, 3224)
        self.assertEqual(row2.conversions, 900)
        self.assertEqual(row2.cost, decimal.Decimal('202000.44'))
        self.assertEqual(row2.ad_id, '8324125')

    def test_custom_reader(self):
        rows = AdPerformanceReportParser.parse_file(
            file_path=self.simple_test_file_path,
            csv_reader=csv.reader, dialect='unix'
        )
        rows = list(rows)
        row1, row2 = rows

        self.assertEqual(row1.impressions, 1000)
        self.assertEqual(row1.clicks, 200)
        self.assertEqual(row1.conversions, 5)
        self.assertEqual(row1.cost, decimal.Decimal('50000.03'))
        self.assertEqual(row1.ad_id, '1232188')

        self.assertEqual(row2.impressions, 56000)
        self.assertEqual(row2.clicks, 3224)
        self.assertEqual(row2.conversions, 900)
        self.assertEqual(row2.cost, decimal.Decimal('202000.44'))
        self.assertEqual(row2.ad_id, '8324125')

    def test_with_headers(self):
        rows = AdPerformanceReportParser.parse_file(
            file_path=self.simple_test_file_with_headers_path,
            start_from_line=2
        )
        rows = list(rows)
        row1, row2 = rows

        self.assertEqual(row1.impressions, 1000)
        self.assertEqual(row1.clicks, 200)
        self.assertEqual(row1.conversions, 5)
        self.assertEqual(row1.cost, decimal.Decimal('50000.03'))
        self.assertEqual(row1.ad_id, '1232188')

        self.assertEqual(row2.impressions, 56000)
        self.assertEqual(row2.clicks, 3224)
        self.assertEqual(row2.conversions, 900)
        self.assertEqual(row2.cost, decimal.Decimal('202000.44'))
        self.assertEqual(row2.ad_id, '8324125')

    def test_with_summary(self):
        rows = AdPerformanceReportParser.parse_file(
            file_path=self.simple_test_file_with_summary_path,
            end_at_line=2  # inclusive
        )
        rows = list(rows)
        row1, row2 = rows

        self.assertEqual(row1.impressions, 1000)
        self.assertEqual(row1.clicks, 200)
        self.assertEqual(row1.conversions, 5)
        self.assertEqual(row1.cost, decimal.Decimal('50000.03'))
        self.assertEqual(row1.ad_id, '1232188')

        self.assertEqual(row2.impressions, 56000)
        self.assertEqual(row2.clicks, 3224)
        self.assertEqual(row2.conversions, 900)
        self.assertEqual(row2.cost, decimal.Decimal('202000.44'))
        self.assertEqual(row2.ad_id, '8324125')

    def test_with_headers_and_summary(self):
        rows = AdPerformanceReportParser.parse_file(
            file_path=self.simple_test_file_with_headers_and_summary_path,
            start_from_line=2,
            end_at_line=3  # inclusive
        )
        rows = list(rows)
        row1, row2 = rows

        self.assertEqual(row1.impressions, 1000)
        self.assertEqual(row1.clicks, 200)
        self.assertEqual(row1.conversions, 5)
        self.assertEqual(row1.cost, decimal.Decimal('50000.03'))
        self.assertEqual(row1.ad_id, '1232188')

        self.assertEqual(row2.impressions, 56000)
        self.assertEqual(row2.clicks, 3224)
        self.assertEqual(row2.conversions, 900)
        self.assertEqual(row2.cost, decimal.Decimal('202000.44'))
        self.assertEqual(row2.ad_id, '8324125')

    def test_with_headers_and_summary_and_custom_reader(self):
        rows = AdPerformanceReportParser.parse_file(
            file_path=self.simple_test_file_with_headers_and_summary_path_and_custom_reader,
            start_from_line=2,
            end_at_line=3,
            csv_reader=csv.reader, delimiter=';', quotechar='|'
        )
        rows = list(rows)
        row1, row2 = rows

        self.assertEqual(row1.impressions, 1000)
        self.assertEqual(row1.clicks, 200)
        self.assertEqual(row1.conversions, 5)
        self.assertEqual(row1.cost, decimal.Decimal('50000.03'))
        self.assertEqual(row1.ad_id, '1232188')

        self.assertEqual(row2.impressions, 56000)
        self.assertEqual(row2.clicks, 3224)
        self.assertEqual(row2.conversions, 900)
        self.assertEqual(row2.cost, decimal.Decimal('202000.44'))
        self.assertEqual(row2.ad_id, '8324125')


class CharFieldMaxLengthValidatorTestCase(unittest.TestCase):
    def test(self):
        validator = csvparser.CharFieldMaxLengthValidator(max_length=10)
        valid_string = '12345'
        invalid_string = '1234567891011'
        self.assertEqual(validator.is_valid(valid_string, 'test_charfield'), True)
        self.assertEqual(validator.is_valid(invalid_string, 'test_charfield'), False)
        self.assertEqual(validator.errors, ['test_charfield len higher than max_length'])


class CharFieldWithLengthValidatorTestCase(unittest.TestCase):
    def test(self):

        class A(object):
            test_charfield = csvparser.CharField(validators=[csvparser.CharFieldMaxLengthValidator(max_length=5)])

        valid_test_object = A()
        valid_test_object.test_charfield = '1234'

        invalid_test_object = A()
        invalid_test_object.test_charfield = '123456'

        self.assertEqual(A.test_charfield.is_valid(valid_test_object, A, 'test_charfield'), True)
        self.assertEqual(A.test_charfield.is_valid(invalid_test_object, A, 'test_charfield'), False)

        self.assertEqual(A.test_charfield.errors(valid_test_object), [])
        self.assertEqual(A.test_charfield.errors(invalid_test_object), ['test_charfield len higher than max_length'])

    def test_with_2_validators(self):

        class A(object):
            test_charfield = csvparser.CharField(
                validators=[
                    csvparser.CharFieldMaxLengthValidator(max_length=5),
                    csvparser.CharFieldMinLengthValidator(min_length=1)
                ]
            )

        valid_test_object = A()
        valid_test_object.test_charfield = '1'

        invalid_test_object = A()
        invalid_test_object.test_charfield = ''

        invalid_test_object2 = A()
        invalid_test_object2.test_charfield = '123456'

        self.assertEqual(A.test_charfield.is_valid(valid_test_object, A, 'test_charfield'), True)
        self.assertEqual(A.test_charfield.is_valid(invalid_test_object, A, 'test_charfield'), False)
        self.assertEqual(A.test_charfield.is_valid(invalid_test_object2, A, 'test_charfield'), False)

        self.assertEqual(A.test_charfield.errors(valid_test_object), [])
        self.assertEqual(A.test_charfield.errors(invalid_test_object), ['test_charfield len smaller than min_length'])
        self.assertEqual(A.test_charfield.errors(invalid_test_object2), ['test_charfield len higher than max_length'])


class IntegerFieldMaxValidatorTestCase(unittest.TestCase):
    def test(self):
        class A(object):
            test_integerfield = csvparser.IntegerField(
                validators=[
                    csvparser.IntegerFieldMaxValidator(max_value=5),
                ]
            )

        valid_test_object = A()
        valid_test_object.test_integerfield = '1'

        invalid_test_object = A()
        invalid_test_object.test_integerfield = '30'

        self.assertEqual(A.test_integerfield.is_valid(valid_test_object, A, 'test_integerfield'), True)
        self.assertEqual(A.test_integerfield.is_valid(invalid_test_object, A, 'test_integerfield'), False)

        self.assertEqual(A.test_integerfield.errors(valid_test_object), [])
        self.assertEqual(A.test_integerfield.errors(invalid_test_object), ['test_integerfield higher than max'])


class IntegerFieldMinValidatorTestCase(unittest.TestCase):
    def test(self):
        class A(object):
            test_integerfield = csvparser.IntegerField(
                validators=[
                    csvparser.IntegerFieldMinValidator(min_value=5),
                ]
            )

        valid_test_object = A()
        valid_test_object.test_integerfield = '30'

        invalid_test_object = A()
        invalid_test_object.test_integerfield = '1'

        self.assertEqual(A.test_integerfield.is_valid(valid_test_object, A, 'test_integerfield'), True)
        self.assertEqual(A.test_integerfield.is_valid(invalid_test_object, A, 'test_integerfield'), False)

        self.assertEqual(A.test_integerfield.errors(valid_test_object), [])
        self.assertEqual(A.test_integerfield.errors(invalid_test_object), ['test_integerfield lower than min'])


class IntegerFieldMinMaxValidatorsTestCase(unittest.TestCase):
    def test(self):
        class A(object):
            test_integerfield = csvparser.IntegerField(
                validators=[
                    csvparser.IntegerFieldMinValidator(min_value=1),
                    csvparser.IntegerFieldMaxValidator(max_value=5),
                ]
            )

        invalid_object1 = A()
        invalid_object1.test_integerfield = 6

        invalid_object2 = A()
        invalid_object2.test_integerfield = 0

        valid_object1 = A()
        valid_object1.test_integerfield = 1

        valid_object2 = A()
        valid_object2.test_integerfield = 3

        valid_object3 = A()
        valid_object3.test_integerfield = 5

        self.assertEqual(A.test_integerfield.is_valid(invalid_object1, A, 'test_integerfield'), False)
        self.assertEqual(A.test_integerfield.errors(invalid_object1), ['test_integerfield higher than max'])

        self.assertEqual(A.test_integerfield.is_valid(invalid_object2, A, 'test_integerfield'), False)
        self.assertEqual(A.test_integerfield.errors(invalid_object2), ['test_integerfield lower than min'])

        self.assertEqual(A.test_integerfield.is_valid(valid_object1, A, 'test_integerfield'), True)
        self.assertEqual(A.test_integerfield.errors(valid_object1), [])

        self.assertEqual(A.test_integerfield.is_valid(valid_object2, A, 'test_integerfield'), True)
        self.assertEqual(A.test_integerfield.errors(valid_object2), [])

        self.assertEqual(A.test_integerfield.is_valid(valid_object3, A, 'test_integerfield'), True)
        self.assertEqual(A.test_integerfield.errors(valid_object3), [])


class DecimalFieldMinValidatorTestCase(unittest.TestCase):
    def test(self):
        class A(object):
            test_decimalfield = csvparser.DecimalField(
                validators=[
                    csvparser.DecimalFieldMinValidator(min_value=decimal.Decimal('1.00'))
                ]
            )

        valid_test_object = A()
        valid_test_object.test_decimalfield = decimal.Decimal('1.0')

        invalid_test_object = A()
        invalid_test_object.test_decimalfield = decimal.Decimal('0.0')

        self.assertEqual(A.test_decimalfield.is_valid(valid_test_object, A, 'test_decimalfield'), True)
        self.assertEqual(A.test_decimalfield.is_valid(invalid_test_object, A, 'test_decimalfield'), False)

        self.assertEqual(A.test_decimalfield.errors(valid_test_object), [])
        self.assertEqual(A.test_decimalfield.errors(invalid_test_object), ['test_decimalfield lower than min_value'])

        with self.assertRaises(TypeError) as e:
            validator = csvparser.DecimalFieldMinValidator(min_value=1.0)


class DecimalFieldMaxValidatorTestCase(unittest.TestCase):
    def test(self):
        class A(object):
            test_decimalfield = csvparser.DecimalField(
                validators=[
                    csvparser.DecimalFieldMaxValidator(max_value=decimal.Decimal('5.00'))
                ]
            )

        valid_test_object = A()
        valid_test_object.test_decimalfield = decimal.Decimal('1.0')

        invalid_test_object = A()
        invalid_test_object.test_decimalfield = decimal.Decimal('10.0')

        self.assertEqual(A.test_decimalfield.is_valid(valid_test_object, A, 'test_decimalfield'), True)
        self.assertEqual(A.test_decimalfield.is_valid(invalid_test_object, A, 'test_decimalfield'), False)

        self.assertEqual(A.test_decimalfield.errors(valid_test_object), [])
        self.assertEqual(A.test_decimalfield.errors(invalid_test_object), ['test_decimalfield higher than max_value'])

        with self.assertRaises(TypeError) as e:
            validator = csvparser.DecimalFieldMaxValidator(max_value=1.0)


if __name__ == '__main__':
    unittest.main()