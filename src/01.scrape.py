# 01.scape.py
#
# For each repo in the Amsterdam UMC organization:
# - collect repo and collaborators data via GitHub API
# - collect software metadata via SOMEF
# - output is stored in ../../data/01.scrape.json

# More info:
# - GitHub Python API: https://github.com/PyGithub/PyGithub
# - SOMEF: https://github.com/KnowledgeCaptureAndDiscovery/somef

# Modules
import json, logging, os
from github import Github, Auth
from somef import somef_cli

# Config
selected_repo_names = [
    'AmsterdamUMC/AmsterdamUMCdb',
    'AmsterdamUMC/splithalfr',
    'AmsterdamUMC/jsQuestPlus',
    'AmsterdamUMC/psychojs_testing',
    'AmsterdamUMC/rs-report-workflow',
    'AmsterdamUMC/CohortSelector'
]

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

# Get input_repos belonging to AmsterdamUMC organization
org = github_api.get_organization('AmsterdamUMC')
input_repos = org.get_repos(type = 'all') 
logging.info('Found ' + str(input_repos.totalCount) + ' input_repos')

# Filter out selected repos
# selected_repos = list(filter(lambda item: item.full_name in selected_repo_names, input_repos))
# logging.info('Selected ' + str(len(selected_repos)) + ' input_repos')
# input_repos[0].full_name

# Raw data from GitHub repo, GitHub collaborators, and SOMEF
scrape_data = []
for repo in input_repos:
    if repo.full_name in selected_repo_names:
        logging.info('Processing ' + repo.full_name)
        # SOMEF data
        try:
            somef_data = somef_cli.cli_get_data(threshold=0.8, ignore_classifiers=False, repo_url=repo.html_url).results
        except Exception as e:
            somef_data = None

        # Collaborators data
        collaborators = repo.get_collaborators(affiliation ='direct')
        collaborators_data = []
        for collaborator in collaborators:
            collaborators_data.append(collaborator.raw_data)
            
        # Output entry for this repo
        scrape_data.append({
            'repo': repo.raw_data,
            'collaborators': collaborators_data,
            'somef': somef_data
        })

# Wrap up
with open('../rs-report-data/01.scrape.json', 'w') as f:
    json.dump(scrape_data, f)
logging.info('Stored ../rs-report-data/01.scrape.json')

github_api.close()
logging.info('Done!')