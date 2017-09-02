# coding: utf-8

from jizera import app
from jizera.database import get_db

from random import seed, gauss, uniform, randrange, randint, \
            lognormvariate as lognormal
from os import remove, path
from loremipsum import get_sentences
from datetime import datetime,timedelta
from time import time as timestamp
from math import cos, sqrt
import click


@app.cli.command('dummy-init', help = u'wypełnia bazę danych losowo wygenerowanymi wpisami')
@click.option('--observations', default = 1024, help = u'liczba obserwacji')
@click.option('--users', default = 56, help = u'liczba użytkownikóœ')
@click.option('--locations', default = 128, help = u'liczba miejscówek')
@click.option('--reviews', default = 256, help = u'liczba recenzji')
def cli_dummy_init(**kwargs):

    db = get_db()
    cur = db.cursor()

    # zasiewamy ziarno generatora liczb losowych
    seed()

    def pickrandom(arr):
        return arr[randrange(len(arr))]

    def emailize(s):
        return s.lower().replace(u' ',u'.')     \
            .replace(u'ą',u'a') \
            .replace(u'ś',u's') \
            .replace(u'ć',u'c') \
            .replace(u'ź',u'z') \
            .replace(u'ż',u'z') \
            .replace(u'ó',u'o') \
            .replace(u'ł',u'l') \
            .replace(u'ń',u'n') \
            .replace(u'ę',u'e')

    # tworzymy obserwatorow
    print u' -- OBSERWATORZY -- '

    observers = []

    rightnow = datetime.now().replace(microsecond=0)

    obs_names = [ u'Hieronim', u'Władimir', u'Aleksandr', u'Siergiej',
        u'Dobromir', u'Miłosław', u'Światowid', u'Brajan', u'Adam', u'Antoni',
        u'Andrzej', u'Dionizy', u'Łukasz', u'Stefan', u'Janusz', u'Paweł',
        u'Tomasz', u'Jan', u'Piotr', u'Oskar', u'Cezary', u'Ozjasz', u'Izaak',
        u'Elipson', u'Kuriusz', u'Zenifar', u'Aplojaz', u'Kerofan', u'Terazaf',
        u'Karmazyn', u'Halibut', u'Arfagor' ]
    obs_lastnames = [ u'Nowak', u'Kowalski', u'Wiśniewski', u'Dąbrowski',
        u'Lewandowski', u'Wójcik', u'Kamiński', u'Kowalczyk', u'Zieliński',
        u'Szymański', u'Woźniak', u'Kozłowski', u'Jankowski', u'Wojciechowski',
        u'Kwiatkowski', u'Kaczmarek', u'Mazur', u'Krawczyk', u'Piotrowski',
        u'Grabowski', u'Nowakowski', u'Pawłowski', u'Michalski', u'Nowicki',
        u'Adamczyk', u'Dudek', u'Zając', u'Wieczorek', u'Jabłoński', u'Król',
        u'Majewski', u'Olszewski', u'Jaworski', u'Wróbel', u'Malinowski',
        u'Pawlak', u'Witkowski', u'Walczak', u'Stępień', u'Górski',
        u'Rutkowski', u'Michalak', u'Sikora', u'Ostrowski', u'Baran', u'Duda',
        u'Szewczyk', u'Tomaszewski', u'Pietrzak', u'Marciniak', u'Wróblewski',
        u'Zalewski', u'Jakubowski', u'Jasiński', u'Zawadzki', u'Sadowski',
        u'Bąk', u'Chmielewski', u'Włodarczyk', u'Borkowski', u'Czarnecki',
        u'Sawicki', u'Sokołowski', u'Urbański', u'Kubiak', u'Maciejewski',
        u'Szczepański', u'Kucharski', u'Wilk', u'Kalinowski', u'Lis',
        u'Mazurek', u'Wysocki', u'Adamski', u'Kaźmierczak', u'Wasilewski',
        u'Sobczak', u'von Wygasch', u'Zambrowski', u'Karzach', u'Goldbaum' ]
    em_domain = [ u'gmail.com', u'mail.ru', u'pornhub.com', u'wp.pl', \
        u'thepiratebay.se', u'astro.uni.wroc.pl', u'nasa.gov', \
        u'buziaczek.pl', u'yahoo.com', u'microsoft.com', u'yandex.ru', \
        u'legia.pl', u'radom.pl', u'home.pl', u'mozilla.com', u'linux.com', \
        u'example.com' ]


    for i in range(kwargs['users']):
        while True:
            nam1 = pickrandom(obs_names)
            nam2 = pickrandom(obs_lastnames)
            em = emailize(nam1 + u' ' + nam2) + u'@' + pickrandom(em_domain)
            cur.execute('SELECT count(*) from observers ' \
                'where observers.email = ?;', (em,))
            if cur.fetchone()[0] == 0:
                break
            print u"E-mail {em} jest juz w bazie. Probuje dalej...".format(em=em)
        joined = rightnow - timedelta(seconds = 24*3600*365*4*(1 - sqrt(uniform(0,1))))
        cur.execute('insert into observers (created,modified,name,lastname,email) ' +
            'values (?,?,?,?,?);', (joined, joined + timedelta(days=1), nam1, nam2, em))

        observers.append(cur.lastrowid)
        print u'%8d %15s %15s %40s' % (cur.lastrowid,nam1,nam2,em)

    db.commit()

    # tworzymy miejsca
    print u" -- LOKALIZACJE --"

    locations = {}
    loc_names_a = [ u'Przyłęcze', u'Zadupie', u'Ostrowo', u'Konolipie',
        u'Nietopie', u'Durniewo', u'Gajowo', u'Koniowo', u'Świniarowo',
        u'Kozłowo', u'Kurowo', u'Zabrodzie', u'Sarniewo', u'Przystronie',
        u'Zalewo', u'Konotopy', u'Niedociągi', u'Pałoryje', u'Niezakłapy',
        u'Wilkowyje', u'Zakątrzewy', u'Podbiesiory', u'Dorycze', u'Kołacze',
        u'Dzikowo', u'Bobrowo', u'Pstrągowo', u'Zapieciory', u'Rzęwuszewo',
        u'Druszczyny' ]
    loc_names_b = [ u'Dolnośląskie', u'Łódzkie', u'Górne', u'Dolne',
        u'Wielkie', u'Małe', u'Wielkopolskie', u'Mazowieckie', u'Wiślańskie',
        u'Rządowe', u'Pierwsze', u'Drugie', u'Gdańskie', u'Osiedle',
        u'Niestraszne', u'Wiślane' ]
    for i in range(kwargs['locations']):
        while True:
            name = u'%s %s' % (pickrandom(loc_names_a), pickrandom(loc_names_b))
            cur.execute('SELECT COUNT(*) FROM locations \
                WHERE locations.name = ?;', (name,))
            if cur.fetchone()[0] == 0:
                break
            print u"Wieś {} istnieje. Próbuję innej nazwy...".format(name)
        l_lat = uniform(49.5,54.5)
        l_lng = uniform(14.7,23.7)
        cur.execute('insert into locations (created, modified, name, latitude, longitude) values (?,?,?,?,?);',
            (rightnow, rightnow, name, l_lat, l_lng))
        locations[cur.lastrowid] = (l_lat,l_lng)
        print u"%6d %30s %10.4f %10.4f" % (cur.lastrowid, name, l_lat, l_lng)

    db.commit()

    # dodajemy jakies recenzje
    print u' -- RECENZJE --'

    for i in range(kwargs['reviews']):
        print u' * Recenzja %d' % (i+1)
        rev = (u' '.join(get_sentences(randrange(1,9))))
        location_id = pickrandom(locations.keys())
        observer_id = pickrandom(observers)
        cur.execute('insert into reviews (created,modified,location_id,observer_id,comment) values (?,?,?,?,?);',
            (rightnow, rightnow, location_id, observer_id, rev))
        cid = cur.lastrowid
        print '%10d %10d %10d' % (cid,location_id,observer_id)
        print rev

    db.commit()

    # obserwacje
    print u' -- OBSERWACJE --'

    def yfun(x1,y1,x2,y2,x):
        return (y2 - y1) / float(x2 - x1) * float(x - x1) + y1

    time0 = timestamp()

    m_pi = 3.1415

    for i in range(kwargs['observations']):
        print u' * Obserwacja %d' % (i+1)
        yrsback = 3 * (1 - sqrt(uniform(0,1)))
        time = time0 - (yrsback * 365) * 24 * 3600
        date_start = datetime.fromtimestamp(time) \
              .replace(hour=22,minute=0,second=0,microsecond=0)
        loc_id = pickrandom(locations.keys())
        created = date_start + timedelta(seconds = 24*3600*lognormal(0,1))
        if created > rightnow:
            created = rightnow - timedelta(seconds = int(3600*uniform(0,6)))

        observer_id = pickrandom(observers)

        cur.execute('insert into observations ' +
            '(created, modified, date_start, date_end, location_id, ' + \
            'observer_id) values (?,?,?,?,?,?)',
            (created, created, date_start, date_start + timedelta(hours=1),
            loc_id, observer_id))
        obs_id = cur.lastrowid

        (lat,lng) = locations[loc_id]

        ss = (1 + cos(lat * 2 * m_pi / 2)) \
            + (1 + cos(lng * 2 * m_pi / 1))
        data_base = 0.25 * ss * (22.8-16) + gauss(16,0.1) \
            - 1.2 * (5 - yrsback) / 5

        print u"JASN = {:5.2f}, LAT = {:7.4f}, LNG = {:7.4f}".format(data_base,lat,lng)

        obsy = []
        if uniform(0,1) < 0.5:
            field_nr = randint(1,10)
            magnitude = data_base + gauss(0,0.1)
            cur.execute('insert into dslr_data ' +
                '(observation_id, field_nr, magnitude) values (?,?,?);',
                (obs_id, field_nr, magnitude))
            obsy.append('dslr')
            print '%18s %6d %10d %10.2f' % ('DSLR',cur.lastrowid,field_nr,magnitude)
        if uniform(0,1) < 0.3:
            num_stars = round(yfun(16,300,22.5,2800,data_base + gauss(0,1.0)))
            cur.execute('insert into tube_data (observation_id,num_stars) ' +
                'values (?,?);', (obs_id,num_stars))
            obsy.append('tuba')
            print '%18s %6d %d' % ('TUBA',cur.lastrowid,num_stars)
        if uniform(0,1) < 0.4:
            field_nr = randint(1,10)
            num_stars = round(yfun(16,10,22.5,60,data_base + gauss(0,0.4)))
            magnitude = yfun(16,3.5,22.5,7.5,data_base + gauss(0,0.4))
            cur.execute('insert into meteor_data (observation_id, ' +
                'field_nr, num_stars, magnitude) values (?,?,?,?);',
                ( obs_id, field_nr, num_stars, magnitude ))
            obsy.append('meteor')
            print '%18s %6d %10d %10d %8.2f' % ('METEOR',cur.lastrowid,field_nr,num_stars,magnitude)
        if uniform(0,1) < 0.7:
            magnitude_z = data_base + gauss(0,0.1)
            magnitude_n = data_base + gauss(-0.8,0.3)
            magnitude_e = data_base + gauss(-0.8,0.3)
            magnitude_s = data_base + gauss(-0.8,0.3)
            magnitude_w = data_base + gauss(-0.8,0.3)
            cur.execute('insert into sqm_data (observation_id, ' +
                'magnitude_z, magnitude_n, magnitude_e, magnitude_s, magnitude_w) ' +
                'values (?,?,?,?,?,?);', (obs_id, magnitude_z, magnitude_n,
                magnitude_e, magnitude_s, magnitude_w))
            obsy.append('sqm')
            print '%18s %6d %7.2f %7.2f %7.2f %7.2f %7.2f' % ('SQM',cur.lastrowid,
                magnitude_z, magnitude_n, magnitude_e, magnitude_s, magnitude_w)
        if uniform(0,1) < 0.6 or len(obsy) == 0:
            bortle_degrees = round(yfun(16,7,23.5,1,data_base))
            cur.execute('insert into bortle_data (observation_id, degrees) ' +
                'values (?,?);', (obs_id, bortle_degrees))
            obsy.append('bortle')
            print '%18s %6d %d' % ('BORTLE',cur.lastrowid,bortle_degrees)


        db.commit()


    print u' -- KONIEC --'
