# About
Library for parsing csv files using declared django-style parser classes.
It uses standard csv package. Tested on python3.4.

# Installation
`pip install csvreader`

# Usage
Lets say that you want parse csv like below. We want to skip first row(header) and last(summary):

```
impressions,clicks,conversions,cost,ad_id
1000,200,5,50000.03,1232188
56000,3224,900,202000.44,8324125
57000,3424,905,252000.47,--
```

Firstly declare proper class:

```python
import csvparser

class AdPerformanceReportParser(csvparser.Parser):
    impressions = csvparser.IntegerField()
    clicks = csvparser.IntegerField()
    conversions = csvparser.IntegerField()
    cost = csvparser.DecimalField()
    ad_id = csvparser.CharField()
    
    # YOU HAVE TO set this attribute
    fields_order = ['impressions', 'clicks', 'conversions', 'cost', 'ad_id']
```

Then parse file and get rows as objects:

```python
rows_as_objects = AdPerformanceReportParser.parse_file('/some/path/to/file', start_from_line=2, end_at_line=3)  # parse_file returns iterator 
```

To customize your parser you can pass your csv.reader and additional arguments for it as kwargs to `parse_file` method:
```python
import csv

rows_as_objects = AdPerformanceReportParser.parse_file('/some/path/to/file', start_from_line=2, end_at_line=3,
                                                       csv_reader=csv.reader, delimiter=';', quotechar='|') 
```