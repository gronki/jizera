# coding: utf-8
from jizera import app
from flask import render_template, abort
from jizera.database import get_db, get_db_cursor

@app.route('/browse')
def browser():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT
        locations.name as location_name,
        locations.latitude, locations.longitude,
        (
        	select count(*)
        	from observations
        	where observations.location_id = locations.id
        ) as observations_count,
        (
        	select observations.created
        	from observations
        	where observations.location_id = locations.id
        	order by observations.created desc limit 1
        ) as last_observation_created
        from locations
        order by last_observation_created desc limit 10;
        """)
    data = cur.fetchall()
    return render_template("browse.html", obslist=data)

@app.route('/location/<n>')
def show_location(n):
    return "lokalizacja {}".format(n)
