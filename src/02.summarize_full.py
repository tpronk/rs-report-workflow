# 02.summarize.py
#
# Summarize the scraped repo data in 01.scrape.json into a table
# stored in 02.summariz.csv. An experimental module 
# `NestedDataParser` is used to construct the summary data in the 
# table cells. It offers a short way to express aggregations such
# as "make a comma-separated list of collaborator usernames" or
# "get the number of executable examples"

# Modules
import json, logging, pandas, numpy
from NestedDataParser.core import NestedDataParser 

# Setup logging
logging.basicConfig(level = logging.INFO)
logging.info('*** Initialization')

# Scraped data
logging.info('Reading 01.scrape.json')
with open('../rs-report-data/01.scrape.json') as f:
    scrape_data = json.load(f)

# SomefFields
logging.info('Reading SomefFields.json')
with open('src/SomefFields.json') as f:
    SomefFieldsFromSchema = json.load(f)

# Get a list of all the SOMEF variables in the scraped data
results = []
SomefFieldsFromData = []
for scrape_entry in scrape_data:
    result = {}
    result['full_name'] = scrape_entry['repo']['full_name']
    for somef_field in scrape_entry['somef'].keys():
        current_data = scrape_entry['somef'][somef_field]
        if not(somef_field in SomefFieldsFromData):
            SomefFieldsFromData.append(somef_field)
        if (somef_field == 'somef_provenance'):
            for provenance_item in current_data.keys():
                result[somef_field + '.' + provenance_item] = current_data[provenance_item]
        else:
            result[somef_field + '.n'] = len(current_data)
            result[somef_field + '.v'] = values = ", ".join(map(lambda entry: str(entry['result']['value']), current_data))
    results.append(result)
            
# Wrap up
pandas.DataFrame(results).to_csv('../rs-report-data/02.summarize_full.csv')
# Fields existing in schema but not in data
list(numpy.setdiff1d(list(SomefFieldsFromSchema.keys()), SomefFieldsFromData))
# Fields existing in data but not in schema
list(numpy.setdiff1d(SomefFieldsFromData, list(SomefFieldsFromSchema.keys())))


