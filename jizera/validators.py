# coding: utf-8

from re import match
from flask import request, Markup
from datetime import datetime

rexp_email = r"([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9\-\.]+\.[a-zA-Z]+)"
rexp_date_ddmmyyyy = r"([0-9]{2})\.([0-9]{2})\.([0-9]{4})"
rexp_date_yyyymmdd = r"([0-9]{4})\-([0-9]{2})\-([0-9]{2})"
rexp_time_hhmm = r"([0-9]{2})\:([0-9]{2})"

rexp_float = r'\-?[0-9]+(?:[\.,][0-9]+)?'
rexp_int = r'\-?[0-9]+'

def validate(validation, what, field):
    value = request.form[field]
    value_print = Markup.escape(value)

    what = what.split()

    if value == '':
        if not 'optional' in what:
            validation[field] = u'To pole nie może być puste.'
        return

    if 'email' in what:
        if not match(rexp_email + r'$',value):
            validation[field] = u'To nie wygląda mi na poprawny adres e-mail :('
            return

    if 'date' in what:
        m = match(rexp_date_yyyymmdd + r'$',value)
        if m:
            if  int(m.group(3)) == 0 or int(m.group(3)) > 31 \
                or int(m.group(2)) == 0 or int(m.group(2)) > 12 \
                or int(m.group(1)) < 1950 or int(m.group(1)) > datetime.now().year:
                validation[field] = u"Nie sądzisz, że coś jest nie tak z tą datą?";
                return
        else:
            validation[field] = u'Najbardziej lubię datę w formacie: {}, ' \
                u'niestety powyższa mi na taką nie wygląda :(' \
                .format(datetime.now().strftime('%Y-%m-%d'))
            return
    if 'time' in what:
        m = match(rexp_time_hhmm + r'$', value)
        if m:
            if  int(m.group(1)) > 23 or int(m.group(2)) > 59:
                validation[field] = u"Druid Arkadiusz mówi, że nie ma takiej godziny...";
                return
        else:
            validation[field] = u"W moich stronach zapisujemy czas w formacie %s." % datetime.now().strftime('%H:%M')
            return
    if 'float' in what:
        if not match(rexp_float + r'$', value):
            validation[field] = u"Nie potrafię odczytać liczby: {}".format(value_print)
    if 'float-list' in what:
        if not match(r'(' + rexp_float + r'|\s+)+$', value):
            validation[field] = u"Nie potrafię odczytać listy liczb: {} :(".format(value_print)
    if 'int' in what:
        if not match(rexp_int + r'$', value):
            validation[field] = u"Nie potrafię odczytać liczby całkowitej: {}".format(value_print)
    if 'int-list' in what:
        if not match(r'(' + rexp_int + r'|\s+)+$', value):
            validation[field] = u"Nie potrafię odczytać tej sekwencji liczb całkowitych: {} :(".format(value_print)
