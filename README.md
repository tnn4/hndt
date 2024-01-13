# Python Hacker News API Data Tools

Tested on: PopOS 22.04 / Ubuntu 22.04

Python tools for getting data from the [Hacker News API](https://github.com/HackerNews/API) and saving it to a [sqlite datbase](https://www.sqlite.org/) for data analysis, science, ML, AI, etc.

Python Hacker News API Wrapper (PHNAW)
- Convenience API wrapper library for use with the Hacker News API

Python Hacker News API Database (PHNDB)
- Contains functions for taking API responses and caching into an SQL database for data analysis

```
HN API <-> PHNAW <-Responses-> PHNAC <-> SQLite
```

You can use this to build data sets from Hacker News.

# Quick start

```sh
# Get sqlalchemy if you wish to use database functions

# Create virtual environment to keep development environment clean
python3 -m venv venv
# Activate the virtual environments
. venv/bin/activate
python3 -m pip install sqlalchemy

# install data analysis libraries

# install nltk
python3 -m pip install -U nltk
python3
# download required data e.g. stopwords
>>> import nltk
>>> nltk.download('stopwords')

# install numpy
python3 -m pip install -U numpy

# verify endpoints
python3 test_endpoints.py

. venv/bin/activate # on Windows: venv/Scripts/Activate.ps1

# Get some posts from the API and insert into the database
# WARN: depends on sqlachemy, so set up venv first
python3 test_db.py

# Test
chmod +x main.py && ./main.py

# If you wish to gather data and Run in background and log stdout to file
nohup python3 <your-python-script> | tee log.txt &
```

## Gathering data
```sh
see: https://docs.python.org/3/library/venv.html
# activate virtual env (on linux)
. venv/bin/activate
# activate virtual env (on Windows)
venv/Scripts/Activate.ps1

python3 main.py
```
API data will be cached to `hn.sqlite` which contains `items` and `users` tables. 

## Datasets

Example sqlite database and csv data with schemas can be found in `datasets`.

## Read sqlite database 

Download and install latest binary of sqlite3 for your platform [here](https://www.sqlite.org/download.html)

```bash
sqlite3
sqlite> .open hn_example.sqlite
sqlite> .databases
sqlite> .tables
sqlite> SELECT * from users;
sqlite> SELECT * from items;

# Output to csv
# see: https://stackoverflow.com/questions/6076984/sqlite-how-do-i-save-the-result-of-a-query-as-a-csv-file

# switch to csv
sqlite > .mode csv
# choose output file
sqlite > .output test.csv
# write data to output
sqlite > select * from items;
# switch back to terminal
sqlite > .output stdout
``` 

## Setup tools remote host with ansible

Make sure you have ansible installed

```sh
# Get rid of the default version provided by Ubuntu
sudo apt remove ansible
sudo apt --purge autoremove

sudo apt update
sudo apt upgrade

# Get the latest repo
sudo apt -y install software-properties-common
sudo apt-add-repository ppa:ansible/ansible

sudo apt install ansible
```

```sh
# Run 'setup' once first to install prerequisites
# Run 'run' for subsequent runs
./ansible-start.sh [ setup | run ]
```

## Run script remotely

You can use tmux see: [tmux cheatshett](https://tmuxcheatsheet.com/)

```
# ssh to remote
tmux
python3 main.py
# Ctrl-b d to detach, process runs in background
tmux ls
tmux a -t 0
```

# Development

See:
- [Python Hacker News API Wrapper](phnaw/README.md)
- [Python Hacker News API DB](phnadb/README.md)

## Generating Documentation

```sh
# see doc on command line
python3 -m pydoc <path/to/py_module>

# export docs to html
python3 -m pydoc -w <path/to/py_module>
```


## Archive / Backup

Create git repo and commit files. Create a `.gitignore` and ignore all files you don't want added.
```sh
git init
git checkout -b main
git add .
git commit -m 'msg'
```

```
./archive.sh 
```

OR

`git archive -o hn.zip HEAD`

## Troubleshooting

### Python3 version conflicts:
Run uninstallation scripts
```sh
V=<version-to-remove>
sudo rm -rf /usr/bin/python$V
sudo rm -rf /usr/lib/python$V
sudo rm -rf /usr/local/lib/python$V
```

Reinstall Python3:
```sh
sudo apt-get install --reinstall python3
```

Restore symlink to a working version
```sh
sudo ln -sf /usr/bin/python<version> /usr/local/bin/python3
```