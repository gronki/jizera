# coding: utf-8
from jizera import app
from flask import render_template, abort
from jizera.database import get_db_cursor

@app.route('/location/<n>')
def show_location(n):
    return "lokalizacja {}".format(n)
