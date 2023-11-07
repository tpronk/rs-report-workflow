# 02.summarize.py
#
# Summarize the scraped repo data in 01.scrape.json into a table
# stored in 02.summariz.csv. An experimental module 
# `NestedDataParser` is used to construct the summary data in the 
# table cells. It offers a short way to express aggregations such
# as "make a comma-separated list of collaborator usernames" or
# "get the number of executable examples"

# Modules
import json, logging, pandas
from NestedDataParser.core import NestedDataParser 

# Setup logging
logging.basicConfig(level = logging.INFO)
logging.info('*** Initialization')

# Scraped data
logging.info('Reading 01.scrape.json')
with open('../rs-report-data/01.scrape.json') as f:
    scrape_data = json.load(f)

# Config for NestedDataParser
logging.info('Reading a ParserConfig.json')
with open('src/ParserConfig.json') as f:
    parser_config = json.load(f)

# Apply each aggregation to each entry in the scraped data and 
# collect the results in a Data Frame called summaries
summaries = []
for scrape_entry in scrape_data:
    logging.info('Processing entry ' + scrape_entry['repo']['full_name'])
    summary = {}
    for current_name, current_config in parser_config.items():
        logging.info('Processing aggregation ' + current_name)
        summary[current_name] = NestedDataParser.resolve(scrape_entry, current_config)
    summaries.append(summary)

# Wrap up
pandas.DataFrame(summaries).to_csv('../rs-report-data/02.summarize.csv')
print(json.dumps(summaries[0:4], indent = 2))
