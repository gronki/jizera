# coding: utf-8
from jizera import app
from flask import render_template, abort
from jizera.database import get_db_cursor

@app.route('/observation/<n>')
def show_observation(n):

    observation_id = int(n)

    cur = get_db_cursor()

    obs_info = cur.execute("""SELECT
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
        WHERE observations.id = ?;
        """, (observation_id,)).fetchone()

    if obs_info == None: abort(404)

    obs_extras = {}

    for dt in ['sqm','tube','meteor','dslr','bortle']:
        obs_extras[dt] = cur.execute("""SELECT * FROM {dt}_data
            WHERE {dt}_data.observation_id = ?;""".format(dt = dt),
            (observation_id,)).fetchall()

    return render_template('show_observation.html', data=obs_info, extras=obs_extras)
