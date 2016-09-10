import unittest
import decimal
import os
from csvparser import csvparser


class ParserTestCase(unittest.TestCase):
    def test(self):
        class AdPerformanceReportParser(csvparser.Parser):
            impressions = csvparser.IntegerField()
            clicks = csvparser.IntegerField()
            conversions = csvparser.IntegerField()
            cost = csvparser.DecimalField()
            ad_id = csvparser.CharField()

            default_fields_order = ['impressions', 'clicks', 'conversions',
                                    'cost', 'ad_id']
        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'test_files', 'adperformancereport.csv')

        rows = AdPerformanceReportParser.parse_file(file_path=file_path)
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