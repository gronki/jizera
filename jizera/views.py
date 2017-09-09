# coding: utf-8

from flask import request, g
from flask import render_template, abort, redirect, url_for
from flask import flash
from jizera import app
from jizera.database import get_db, get_db_cursor
from datetime import datetime, timedelta

@app.template_filter('timeago')
def filter_timeago(d):
    td = datetime.now() - d
    if td.days == 0:
        minutes = td.seconds / 60.0
        if minutes < 10:
            return u"przed chwilą"
        elif minutes < 50:
            return u"{} minut temu".format(int(round(minutes)))
        elif minutes < 80:
            return u"około godziny temu"
        else: return u"{} godzin(y) temu".format(int(round(minutes / 60)))
    elif td.days == 1:
        return u"wczoraj"
    elif td.days == 2:
        return u"przedwczoraj"
    else:
        return u"%d dni temu" % td.days

@app.template_filter('onlydate')
def filter_onlydate(d):
    return d.strftime('%d.%m.%Y')

import jizera.report
import jizera.browse
import jizera.observations
import jizera.locations

@app.route('/')
def index():
    cur = get_db_cursor()
    cur.execute("""SELECT
        observations.id AS observation_id,
        observations.created AS created,
        observations.date_start AS date_start,
        observers.id AS observer_id,
        (observers.name || " " || observers.lastname) AS observer_name,
        locations.name AS location_name,
        locations.latitude AS latitude,
        locations.longitude AS longitude,
        printf("@%.5f,%.5f", locations.latitude, locations.longitude) as latlng
        FROM observations
        JOIN observers ON (observers.id = observations.observer_id)
        JOIN locations ON (locations.id = observations.location_id)
        ORDER BY observations.created DESC
        LIMIT 5;
        """)
    recent = cur.fetchall()

    cur.execute("""SELECT observers.id AS id,
        (observers.name || " " || observers.lastname) AS name,
        observers.created as joined
        FROM observers ORDER BY observers.created DESC LIMIT 5;""")
    new_observers = cur.fetchall()

    return render_template('index.html',
        recent=recent,
        new_observers = new_observers)

@app.route('/observer/<n>')
def show_observer(n):
    return "obserwator {}".format(n)

@app.route('/articles/<name>')
def show_article(name):
    return "This is not yet implemented."
