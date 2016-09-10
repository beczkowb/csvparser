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

    default_fields_order = ['impressions', 'clicks', 'conversions',
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

if __name__ == '__main__':
    unittest.main()