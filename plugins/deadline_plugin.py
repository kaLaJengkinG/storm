#===istalismanplugin===
# -*- coding: utf-8 -*-

# This plugin allows the admin to add multiple deadlines (date + message) 
# and display to all how many days remain till deadlines.

import datetime, time

DEADLINES_FILE = 'dynamic/DEADLINES.txt'
DEADLINES = []

def handler_deadline(type, source, parameters):
    global DEADLINES
    message = ''
    for deadline in DEADLINES:
        message += "\n"
        message += _format_deadline(
                deadline['date'] - datetime.date.today(),
                deadline['message'])
    if message == '':
        smsg(type, source, 'no deadlines.')
    else:
        smsg(type, source, message)

def handler_deadline_list(type, source, parameters):
    global DEADLINES
    message = ''
    i = 0
    for deadline in DEADLINES:
        message += "\n"
        message += '% 4i %s %s' % (i, deadline['date'], deadline['message'])
        i += 1
    smsg(type, source, message)

def handler_deadline_delete(type, source, parameters):
    global DEADLINES
    try:
        i = int(parameters)
        del DEADLINES[i]
        _save_deadlines()
        smsg(type, source, 'removed deadline ' + str(i))
    except Exception, e:
        smsg(type, source, 'Error: ' + str(e))

def handler_deadline_add(type, source, parameters):
    global DEADLINES
    if len(string.split(parameters)) < 2:
        smsg(type, source, 'invalid syntax')
        return
    try:
        (sdate, message) = string.split(parameters, maxsplit=1)
        date = _parse_date(sdate)
        add_deadline(date, message)
        smsg(type, source, 'added new deadline: %s %s' % (date, message))
    except Exception, e:
        smsg(type, source, 'error: ' + str(e))

def add_deadline(date, message):
    global DEADLINES
    deadline = {}
    deadline['date'] = date
    deadline['message'] = message
    DEADLINES.append(deadline)
    _sort_deadlines()
    _save_deadlines()

def _format_deadline(timedelta, message):
    days = timedelta.days
    if days > 2:
        return message + u' - through ' + str(days - 1) + u' ' + _plural(days - 1, u'day', u'day', u'day') + '.'
    if days == 2:
        return message + u' - after tomorrow.'
    if days == 1:
        return message + u' - tomorrow.'
    if days == 0:
        return message + u' - today!'
    if days == -1:
        return message + u' - yesterday!!'
    if days == -2:
        return message + u'- day before!!!'
    if days < -2:
        return message + u' - long.'

def _plural(number, form1, form2, form3):
    if number in (11, 12, 13, 14):
        return form3
    else:
        tens = number % 10
        if tens == 1:
            return form1
        elif tens in (2, 3, 4):
            return form2
        else:
            return form3

def _load_deadlines():
    global DEADLINES
    DEADLINES = eval(read_file(DEADLINES_FILE))
    _sort_deadlines()

def _save_deadlines():
    global DEADLINES
    write_file(DEADLINES_FILE, str(DEADLINES))

def _sort_deadlines():
    global DEADLINES
    DEADLINES.sort(_cmp_deadlines)

def _cmp_deadlines(a, b):
    d = cmp(a['date'], b['date'])
    if d == 0:
        return cmp(a['message'], b['message'])
    else:
        return d

def _parse_date(sdate):
    date = time.strptime(sdate, '%Y-%m-%d')
    return datetime.date(date.tm_year, date.tm_mon, date.tm_mday)

initialize_file(DEADLINES_FILE, "[]")
_load_deadlines()

register_command_handler(handler_deadline, '!deadline', ['admin','all'], 20, 'Displays the number of days till deadline.', '!deadline', ['!deadline'])
register_command_handler(handler_deadline_list, '!deadline_list', ['superadmin','all'], 100, 'Displays all registered deadlines.', '!deadline_list', ['!deadline_list'])
register_command_handler(handler_deadline_delete, '!deadline_del', ['superadmin','all'], 100, 'Removes deadline with specified ID.', '!deadline_del id', ['!deadline_del 0', '!deadline_del 5'])
register_command_handler(handler_deadline_add, '!deadline_add', ['superadmin','all'], 100, 'Adds new deadline.', '!deadline_add yyyy-mm-dd message', ['!deadline_add 2009-01-01 New Year'])
