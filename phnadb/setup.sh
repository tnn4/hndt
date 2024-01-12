#!/usr/bin/env bash

python3 -m venv venv

# https://stackoverflow.com/questions/59997065/pip-python-normal-site-packages-is-not-writeable
python3 -m pip install sqlalchemy