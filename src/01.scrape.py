# 01.scape.py
#
# For each repo in input_repos.json
# - collect repo and collaborators data via GitHub API
# - collect software metadata via SOMEF
# - output is stored in ../../data/01.scrape.json

# More info:
# - GitHub Python API: https://github.com/PyGithub/PyGithub
# - SOMEF: https://github.com/KnowledgeCaptureAndDiscovery/somef

# Modules
import json, logging, os
from somef import somef_cli

# Setup logging
logging.basicConfig(level = logging.INFO)
logging.info('*** Initialization')

# Input repos
logging.info('Reading input_repos.json')
with open('../rs-report-data/config/input_repos.json') as f:
    input_repos = json.load(f)

# Raw data from GitHub repo, GitHub collaborators, and SOMEF
scrape_data = []
for input_repo in input_repos:
    logging.info('Processing ' + input_repo['label'])

    # SOMEF data
    somef_data = somef_cli.cli_get_data(
        threshold=0.8, 
        ignore_classifiers=False, 
        repo_url=input_repo['url']
    ).results
        
    # Output entry for this input_repo
    scrape_data.append({
        'label': input_repo['label'],
        'source': input_repo['source'],
        'notes': input_repo['notes'],
        'somef': somef_data
    })

# Wrap up
with open('../rs-report-data/interim/01.scrape.json', 'w') as f:
    json.dump(scrape_data, f)
logging.info('Stored ../rs-report-data/interim/01.scrape.json')
logging.info('Done!')