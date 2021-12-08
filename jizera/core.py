from flask import request, g, abort, redirect, render_template, flash, url_for, session
import sqlite3
import click
from datetime import datetime

#------------------------------------------------------------------------------#

from jizera import app

app.secret_key = 'asinarheaiwcthnoav8utn3aolwrnausvoatahn8wvlnla3yb560ola8'
database_uri = 'jizerasqm.db'
tzfmt = '%Y-%m-%d %H:%M:%S'

#------------------------------------------------------------------------------#

def get_db():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(database_uri,
            detect_types = sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.cli.command('reset')
def cli_init():
    db = get_db()
    cur = db.cursor()
    cur.execute('drop table if exists observations;')
    cur.execute('create table observations ('
        'id integer primary key,'
        'dateobs_ut datetime default (datetime(\'now\', \'utc\')),'
        'timezone integer default 0,'
        'latitude float not null,'
        'longitude float not null,'
        'sqm_avg float not null,'
        'sqm_std float,'
        'sqm_nsampl integer not null,'
        'rawdata varchar(511),'
        'obsname varchar(63),'
        'created timestamp default CURRENT_TIMESTAMP,'
        'modified timestamp default CURRENT_TIMESTAMP'
    ');')
    db.commit()

@app.cli.command('delete')
@click.argument('id')
def cli_delete(id):
    db = get_db()
    cur = db.cursor()
    cur.execute('select id,latitude,longitude,dateobs_ut from observations where id = ?;', (id,))
    row = cur.fetchone()
    if not row:
        print ('entry #{} doesn\'t exist'.format(id))
        return
    ans = input('Delete entry #{} location @{:.5f},{:.5f} created {} UT? [y/n] '.format(row['id'], row['latitude'], row['longitude'], row['dateobs_ut']))
    if ans.lower() == 'y':
        cur.execute('delete from observations where id = ?;', (id,))
        db.commit()
        print ('deleted')
    else: print('abort')

@app.teardown_appcontext
def close_db(e):
    db = g.pop('db', None)
    if db: db.close()

#------------------------------------------------------------------------------#

def validate(validation, field, what):

    from flask import Markup
    value = request.form[field]
    value_print = Markup.escape(value)

    what = what.split()

    if value.strip() == '':
        if not 'optional' in what:
            validation[field] = u'To pole nie może być puste.'
        return

    if 'email' in what:
        from re import match
        if not match(r"([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9\-\.]+\.[a-zA-Z]+)$", value):
            validation[field] = u'To nie wygląda mi na poprawny adres e-mail :('
            return

    if 'date' in what:
        from datetime import datetime
        try: datetime.strptime(value, '%Y-%m-%d')
        except ValueError as e:
            validation[field] = 'Najbardziej lubię datę w formacie: {}, '
            'niestety powyższa mi na taką nie wygląda :('
            ''.format(datetime.now().strftime('%Y-%m-%d'))
            return
    if 'time' in what:
        try: datetime.strptime(value, '%H:%M')
        except ValueError as e:
            validation[field] = "Druid Arkadiusz mówi, że nie ma takiej godziny..."
            return
    if 'float' in what:
        try: dum = float(value)
        except ValueError:
            validation[field] = u"zły format liczby, może spróbuj z kropką?"
    if 'float-list' in what:
        try:
            for s in value.split(): dum = float(s)
        except: validation[field] = u"liczby muszą być zapisane z kropką dziesiętną i oddzielone spacjami"
    if 'int' in what:
        try: dum = int(value)
        except ValueError:
            validation[field] = u"Nie potrafię odczytać liczby całkowitej: {}".format(value_print)
    if 'int-list' in what:
        try:
            for s in value.split(): dum = float(s)
        except: validation[field] = u"dozwolne są tylko liczby całkowite oddzielone spacjami"


#------------------------------------------------------------------------------#

@app.route('/', endpoint = 'list')
def action_list():
    db = get_db()
    cur = db.cursor()
    cur.execute('select * from observations order by created desc;')
    return render_template('list.html', rows = cur.fetchall())

@app.route('/csv', endpoint = 'csv')
def action_dld():
    db = get_db()
    cur = db.cursor()
    cur.execute('select id, latitude as lat, longitude as lon, \
        round(julianday(dateobs_ut) - 2400000.5, 3) as mjd, \
        round(sqm_avg, 2) as sqm \
        from observations order by created asc;')
    cols = ['id', 'lat', 'lon', 'sqm', 'mjd']
    l = [','.join(cols)]
    for row in cur.fetchall():
        l.append(','.join(str(row[k]) for k in cols))
    # return '<pre>{}</pre>'.format('\n'.join(l))
    from flask import Response
    return Response('\n'.join(l), mimetype = 'text/csv',
        headers = {'Content-disposition': 'attachment; filename=jz{}.csv' \
            .format(datetime.utcnow().strftime('%y%m%d'))})

@app.route('/add', endpoint = 'add', methods = ['POST', 'GET'])
def action_add():
    if request.method == 'GET':
        return render_template('add.html', f = dict(data = None, err = None))

    err = dict()
    validate(err, 'rawdata', 'float-list')
    validate(err, 'latitude', 'float')
    validate(err, 'longitude', 'float')

    if len(err) > 0:
        return render_template('add.html', f = dict(data = request.form, err = err))

    x = [float(s) for s in request.form['rawdata'].split()]
    if len(x) > 1:
        xavg = sum(x) / len(x)
        xstd = (sum([ (xi - xavg)**2 for xi in x ]) / (len(x) * (len(x) - 1)))**0.5
    else:
        xavg = x[0]
        xstd = None

    db = get_db()
    cur = db.cursor()
    cur.execute('insert into observations ('
        'dateobs_ut,'
        'timezone,'
        'latitude,'
        'longitude,'
        'sqm_avg,'
        'sqm_std,'
        'sqm_nsampl,'
        'rawdata,'
        'obsname'
    ') values (?,?,?,?,?,?,?,?,?);', (
        datetime.utcnow().strftime(tzfmt),
        request.form.get('timezone'),
        request.form.get('latitude'),
        request.form.get('longitude'),
        xavg,
        xstd,
        len(x),
        request.form.get('rawdata'),
        request.form.get('obsname'),
    ))

    db.commit()

    if len(request.form.get('obsname').strip()) > 0:
        session['obsname'] = request.form['obsname']

    flash('dodano pomiar ({}) w lokalizacji ({:.5f}, {:.5f})'\
        .format('{:.2f} +/- {:.2f}'.format(xavg, xstd) if xstd != None else '{:.2f}'.format(xavg),
        float(request.form['latitude']), float(request.form['longitude'])))

    return redirect(url_for('list'))

#------------------------------------------------------------------------------#


@app.template_filter('timeago')
def filter_timeago(d):
    td = datetime.utcnow() - d
    if td.days == 0:
        minutes = td.seconds / 60
        if minutes < 1.5:
            return u"teraz"
        elif minutes < 4.5:
            return u"{} minuty temu".format(int(round(minutes)))
        elif td.seconds < 46 * 60:
            return u"{} minut temu".format(int(round(minutes)))
        elif td.seconds < 80 * 60:
            return u"około godziny temu"
        else: return u"{} godzin(y) temu".format(int(round(minutes / 60)))
    elif td.days == 1:
        return u"wczoraj"
    elif td.days == 2:
        return u"przedwczoraj"
    else:
        return u"{} dni temu".format(td.days)

#------------------------------------------------------------------------------#
