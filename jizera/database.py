# coding: utf-8

from jizera import app, g
import os
import sqlite3
from datetime import datetime

def get_db():
    def adapt_datetime(ts):
        return ts.strftime(r'%Y-%m-%d %H:%M:%S')
    def convert_datetime(s):
        return datetime.strptime(s,r'%Y-%m-%d %H:%M:%S')
    if not hasattr(g,'db'):
        sqlite3.register_adapter(datetime, adapt_datetime)
        sqlite3.register_converter("datetime", convert_datetime)
        g.db = sqlite3.connect(app.config['DATABASE_URI'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

def get_db_cursor():
    return get_db().cursor()

@app.teardown_appcontext
def close_db(e):
    if hasattr(g,'db'):
        g.db.close()
        del g.db

@app.cli.command('reset', help = u'czyści bazę danych (!!!!)')
def cli_drop_db():
    db = get_db()
    with app.open_resource('sql/drop.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()
    with app.open_resource('sql/schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()

from jizera.dummy_init import cli_dummy_init
