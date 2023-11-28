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

# Setup logging
logging.basicConfig(level = logging.INFO)
logging.info('*** Initialization')

# Scraped data
logging.info('Reading 01.scrape.json')
with open('01.scrape.json') as f:
    scrape_data = json.load(f)

# SomefFields
logging.info('reading somef_fields.json')
with open('../rs-report-data/config/somef_fields.json') as f:
    somef_fields_from_schema = json.load(f)

# Get a list of all the SOMEF variables in the scraped data
results = []
somef_fields_from_data = []
for scrape_entry in scrape_data:
    result = {}
    result['label'] = scrape_entry['label']
    for somef_field in scrape_entry['somef'].keys():
        current_data = scrape_entry['somef'][somef_field]
        if not(somef_field in somef_fields_from_data):
            somef_fields_from_data.append(somef_field)
        if (somef_field == 'somef_provenance'):
            for provenance_item in current_data.keys():
                result[somef_field + '.' + provenance_item] = current_data[provenance_item]
        else:
            #result['n.' + somef_field] = len(current_data)
            result[somef_field] = '(' + str(len(current_data)) + ') ' + (", ".join(map(lambda entry: str(entry['result']['value']), current_data)))
    results.append(result)
            
# *** Wrap up
# Fields existing in schema but not in data
logging.info('Fields in SOMEF schema but not in data')
logging.info(list(numpy.setdiff1d(list(somef_fields_from_schema.keys()), somef_fields_from_data)))
# Fields existing in data but not in schema
logging.info('Fields in data but not in SOMEF schema')
logging.info(list(numpy.setdiff1d(somef_fields_from_data, list(somef_fields_from_schema.keys()))))
# Save as long
df_wide = pandas.DataFrame(results)
df_long = pandas.melt(
    df_wide,
    id_vars = ['label'], 
    value_vars = df_wide.columns[1 : len(df_wide.columns)]
)
df_long = df_long[[not pandas.isna(elem) for elem in df_long.value]]
df_long.to_csv('02.summarize.csv')

logging.info('Done!')
