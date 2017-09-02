# coding: utf-8

import os
from flask import Flask, g
from datetime import datetime

# tworzymy instancje flaska
app = Flask(__name__)
app.secret_key = 'J4893a8h2KbQKIjn278U80Xiv3443XZJ'
maps_api_key = 'AIzaSyBdhoSL2YRJZTYdaPKfSTrTkiDsgAiHbts'

import jizera.database
import jizera.views
import jizera.report
import jizera.browse

if __name__ == '__main__':
    app.run()
