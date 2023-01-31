# Here To Slay Discord Bot

## Requirements

+ Python 3.7.9

## Usage

``` bash
virtualenv -p python3.7 venv
source venv/bin/activate
pip install -r requirement.txt
python backend/main.py
```

## Linting

``` bash
pylint backend
black -l100 .
```
