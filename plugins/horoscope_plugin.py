#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  horoscope_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import urllib2,re

from re import compile as re_compile

strip_tags = re_compile(r'<[^<>]+>')


horodb={u'aquarius': u'11', u'cancer': u'4', u'libra': u'7', u'capricorn': u'10', u'virgo': u'6', u'gemini': u'3', u'sagittarius': u'9', u'scorpio': u'8', u'taurus': u'2', u'leo': u'5', u'aries': u'1', u'pisces': u'12'}

def handler_horoscope_globa(type, source, parameters):
	if parameters:
		if parameters==u'signs':
			reply('private',source,', '.join(horodb.keys()))
			return
		if horodb.has_key(string.lower(parameters)):
			req = urllib2.Request('http://horo.gala.net/?lang=ru&sign='+horodb[string.lower(parameters)])
			req.add_header = ('User-agent', 'Mozilla/5.0')
			r = urllib2.urlopen(req)
			target = r.read()
			"""sign name"""
			od = re.search('<span class=SignName>',target)
			h1 = target[od.end():]
			h1 = h1[:re.search('</span>',h1).start()]
			h1 += '\n'
			"""day"""
			od = re.search('<td class=blackTextBold nowrap>',target)
			h2 = target[od.end():]
			h2 = h2[:re.search('</td>',h2).start()]
			h2 += '\n'
			"""horoscope"""
			od = re.search('<td class=stext>',target)
			h3 = target[od.end():]
			h3 = h3[:re.search('</td>',h3).start()]
			if len(h3)<5:
				reply(type,source,u'horoscope is not present now')
				return
			message = h1+h2+h3
			message = decode(message)
			message=message.strip()
			reply(type,source,u'sent to private')
			reply('private',source,unicode(message,'windows-1251'))
		else:
			reply(type, source, u'is that a sign of zodiac?')	
			return	
	else:
		reply(type,source,u'what sign of horoscope you want to search?')
		return


def decode(text):
    return strip_tags.sub('', text.replace('<br>','\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t','').replace('>[:\n','')

register_command_handler(handler_horoscope_globa, 'horoscope', ['info','fun','all'], 0, 'Shows a horoscope for the indicated sign of horoscope. All of signs are a "horoscope signs".', 'horoscope [sign]', ['horoscope libra','horoscope virgo'])
