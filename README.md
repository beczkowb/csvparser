# About
Library for parsing and validating csv files using declared django-style parser classes.
It uses standard csv package. Tested on python 2.7 and 3.4.

# Installation
`pip install csvparser`

# Basic usage
Lets say that you want parse csv like below. We want to skip first row(header) and last(summary):

```
impressions,clicks,conversions,cost,ad_id
1000,200,5,50000.03,1232188
56000,3224,900,202000.44,8324125
```

Firstly declare proper class:

```python
from csvparser import parser
from csvparser import fields

class AdPerformanceReportParser(parser.Parser):
    impressions = fields.IntegerField()
    clicks = fields.IntegerField()
    conversions = fields.IntegerField()
    cost = fields.DecimalField()
    ad_id = fields.CharField()
    
    # YOU HAVE TO set this attribute
    fields_order = ['impressions', 'clicks', 'conversions', 'cost', 'ad_id']
```

Then parse file and get rows as objects:

```python
rows_as_objects = AdPerformanceReportParser.parse_file('/some/path/to/file', start_from_line=2)  # parse_file returns iterator 
```

To customize your parser you can pass your csv.reader and additional arguments for it as kwargs to `parse_file` method:
```python
import csv

rows_as_objects = AdPerformanceReportParser.parse_file('/some/path/to/file', start_from_line=2,
                                                       csv_reader=csv.reader, delimiter=';', quotechar='|') 
```

Parser fields supports validation:
```python
from csvparser import parser
from csvparser import fields
from csvparser import validators

class AdPerformanceReportParser(parser.Parser):
    impressions = fields.IntegerField(validators=[validators.IntegerFieldMinValidator(min_value=0)])
    clicks = fields.IntegerField(validators=[validators.IntegerFieldMinValidator(min_value=0)])
    conversions = fields.IntegerField(validators=[validators.IntegerFieldMinValidator(min_value=0)])
    cost = fields.DecimalField(validators=[validators.DecimalFieldMaxValidator(max_value=decimal.Decimal('5000000.00')),])
    ad_id = fields.CharField(validators=[
        validators.CharFieldMaxLengthValidator(max_length=20),
        validators.CharFieldMinLengthValidator(min_length=10)
    ])
    
    fields_order = ['impressions', 'clicks', 'conversions', 'cost', 'ad_id']
```

Now lets use `AdPerformanceReportParser` with validators:
```python
rows_as_objects = AdPerformanceReportParser.parse_file('/some/path/to/file', start_from_line=2)

for row in rows_as_objects:
    if row.is_valid():
        pass  # do something
    else:
        pass  # do something else
```

# Extending basic functionality

## Creating custom fields

You can create custom parser field. Lets say that you want to parse csv showed below:
```
impressions,clicks,conversions,cost,ad_id,ad_image
1000,200,5,50000.03,1232188,300x200_somefilename.jpg
56000,3224,900,202000.44,8324125,150x100_somefilename2.jpg
```

There is additional column `ad_image` which you want to parse to tuple of 3 strings (width, height, name)
To do this we have to create new parser field:
```python
from csvparser import fields

class AdImageField(fields.ParserField):
    @staticmethod
    def create_real_value(raw_value):
        size, name_and_format = raw_value.split('_')
        width, height = size.split('x')
        name, format = name_and_format.split('.')
        return width, height, name
```

As you can see, your custom field `AdImageField` have to inherit from `csvparser.ParserField`,
and declare staticmethod `create_real_value` which return parsed string.

Now, you can use your new field:
```python
from csvparser import parser

class AdPerformanceReportParser(parser.Parser):
    impressions = fields.IntegerField()
    clicks = fields.IntegerField()
    conversions = fields.IntegerField()
    cost = fields.DecimalField()
    ad_id = fields.CharField()
    ad_image = AdImageField()
    
    fields_order = ['impressions', 'clicks', 'conversions', 'cost', 'ad_id', 'ad_image']
```

## Creating custom validators
There is no easy way to create custom validators yet. There will be in next version.