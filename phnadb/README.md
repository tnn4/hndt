# Python Hacker News API Database

Python module for caching Hacker News API calls in a sqlite backend.

# Setup

This module interacts with sqlite through an ORM and requires the installation of specific `pip` packages:
- SqlAlchemy

You'll want to use venv to prevent the global package conflict problem. [see](https://stackoverflow.com/questions/41972261/what-is-a-virtualenv-and-why-should-i-use-one)

```sh
./setup.sh # OR python3 -m venv venv

```

To work in your virtualenv, Activate the environment
```bash
# on bash
. ./venv/bin/activate
# on windows
venv\Scripts\activate

pip install sqlachemy
```

Leave the environment
```
deactivate
```

