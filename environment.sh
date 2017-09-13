#!/usr/bin/env bash

export FLASK_APP=jizera
export FLASK_DEBUG=1
export JIZERA_SETTINGS=$(readlink -f settings.py)
