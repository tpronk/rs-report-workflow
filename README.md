# rs-report-workflow
A simple workflow where SOMEF is used as a library and SOMEF output is processed a bit

# Requirements
Python 3.9.x

# How to install
1. Clone this repo to your device
2. Run `python setup.py`. By default, it configures SOMEF with its standard settings
3. Optionally, finish up configuring SOMEF by running `somef configure`

# How to use
1. To collect the metadata, run `python 01.scrape.py`. This scrapes the repos defined in `input_repos.json` and saves the output in the file `01.scrape.json`
2. To summarize the collected metadata, run `python 02.summarize`, which produces the file `02.summarize.csv`