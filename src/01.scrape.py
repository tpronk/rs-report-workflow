# 01.scape.py
#
# For each repo in the Amsterdam UMC organization:
# - collect repo and collaborators data via GitHub API
# - collect software metadata via SOMEF
# - output is stored in ../../data/01.scrape.json

# More info:
# - GitHub Python API: https://github.com/PyGithub/PyGithub
# - SOMEF: https://github.com/KnowledgeCaptureAndDiscovery/somef

# *** Modules
import json, logging, os, pandas as pd
from github import Github, Auth
from somef import somef_cli
from somef.export import json_export

# *** Initialization
# Setup logging
logging.basicConfig(level = logging.INFO)
logging.info('*** Initialization')

# Get access to GitHub REST API
logging.info('Connecting to GitHub')
try:
    github_token = os.environ['GITHUB_TOKEN']
except Exception as e:
    errorMessage = 'Could not find the GITHUB_TOKEN environment variable. This variable should contain your GitHub authentication token).'
    raise Exception(errorMessage)
logging.info('Got GitHub token from environment')

auth_token = Auth.Token(github_token)
github_api = Github(auth = auth_token)
logging.info('Instantiated github class')

# *** Execution
logging.info('*** Execution')

# Get input_repos belonging to AmsterdamUMC organization
org = github_api.get_organization('AmsterdamUMC')
input_repos = org.get_repos(type = 'all') 
logging.info('Found ' + str(input_repos.totalCount) + ' input_repos')

# Raw data from GitHub repo, GitHub collaborators, and SOMEF
scrape_data = []
for repo in input_repos:
    # SOMEF data
    repo_data = repo.raw_data
    # SOMEF data
    try:
        somef_data = somef_cli.cli_get_data(threshold=0.8, ignore_classifiers=False, repo_url=repo.html_url).results
        json_export.save_codemeta_output(somef_data, '../rs-report-data/01.temp.json', pretty=False)
        with open('../rs-report-data/01.temp.json') as f:
            codemeta_data = json.load(f)
    except Exception as e:
        somef_data = None
    # Collaborators data
    collaborators = repo.get_collaborators(affiliation ='direct')
    collaborators_data = []
    for collaborator in collaborators:
        collaborators_data.append(collaborator.raw_data)
    # Output entry for this repo
    scrape_data.append({
        'repo': repo_data,
        'collaborators': collaborators_data,
        'somef': somef_data
    })

# *** Wrap up
with open('../rs-report-data/01.scrape.json', 'w') as f:
    json.dump(scrape_data, f)
logging.info('Stored ../rs-report-data/01.scrape.json')

github_api.close()
logging.info('Done!')