#!/usr/bin/env bash

export FLASK_APP=jizera
export FLASK_ENV=development
export FLASK_DEBUG=1

source venv/bin/activate

python -m flask run