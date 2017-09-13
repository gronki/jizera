# coding: utf-8

import os
from flask import Flask, g
from datetime import datetime

# tworzymy instancje flaska
app = Flask(__name__)
app.config['VERSION'] = '170913'
app.config.from_envvar('JIZERA_SETTINGS')

import jizera.database
import jizera.views

if __name__ == '__main__':
    app.run()
