#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  trans_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  Parts of code Copyright © Krishna Pattabiraman (PyTrans project) <http://code.google.com/p/pytrans/>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import urllib
import httplib

trans_langs={u'en': u'english', u'ja': u'japanese', u'ru': u'russian', u'auto': u'Determine language', u'sq': u'Albanian', u'ar': u'Arabic', u'af': u'Afrikaans', u'be': u'Belarusian', u'bg': u'Bulgarian', u'cy': u'Welsh', u'hu': u'Hungarian', u'vi': u'Vietnamese', u'gl': u'Galician', u'nl': u'Dutch', u'el': u'Greek', u'da': u'Danish',u'iw': u'Hebrew', u'yi': u'Yiddish', u'id': u'Indonesian', u'ga': u'Irish', u'is': u'Icelandic', u'es': u'Spanish', u'it': u'Italian', u'ca': u'Catalan', u'zh-CN': u'Chinese', u'ko': u'Korean', u'lv': u'Latvian', u'lt': u'Lithuanian',u'mk': u'Macedonian', u'ms': u'Malay', u'mt': u'Maltese', u'de': u'German', u'no': u'Norwegian', u'fa': u'Persian', u'pl': u'Polish', u'pt': u'Portuguese', u'ro': u'Romanian', u'sr': u'Serbian', u'sk': u'Slovak', u'sl': u'Slovenian', u'sw': u'Swahili', u'tl': u'Filipino', u'th': u'Thai', u'tr': u'Turkish', u'uk': u'Ukrainian', u'fi': u'Finnish', u'fr': u'French', u'hi': u'Hindi', u'hr': u'Croatian', u'cs': u'Czech', u'sv': u'Swedish', u'et': u'Estonian'}

def handler_google_trans(type,source,parameters):
	param=parameters.split(None, 2)
	if param[0] in trans_langs.keys() and param[1] in trans_langs.keys() and len(param)>=3:
		(fl, tl, text)=param
		if fl=='auto':
			if tl=='auto':
				reply(type, source, u'failed requests. Read help on using the command')
				return
			else:
				answ=google_detect_lang(text)
				if answ in trans_langs.keys():
					fl=answ
				else:
					reply(type, source, answ)
					return
		answ=google_translate(text, fl, tl)
		answ=answ.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
		reply(type,source,answ)
	else:
		reply(type, source, u'failed requests. Read help on using the command')

def google_translate(text, from_lang, to_lang):
	try:
		req = urllib2.urlopen('http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&q=%s&langpair=%s%s' % (urllib2.quote(text.encode('utf-8')), from_lang+'%7C', to_lang))
	except urllib2.HTTPError, e:
		return str(e)
	answ=json.load(req)
	if answ['responseStatus']!=200:
		return str(answ['responseStatus'])+': '+answ['responseDetails']
	elif answ['responseData']:
		return answ['responseData']['translatedText']
	else:
		return u'Unknown error'

def google_detect_lang(text):
	try:
		req = urllib2.urlopen('http://ajax.googleapis.com/ajax/services/language/detect?v=1.0&q=' + urllib2.quote(text.encode('utf-8')))
	except urllib2.HTTPError, e:
		return str(e)
	answ=json.load(req)
	if answ['responseStatus']!=200:
		return str(answ['responseStatus'])+': '+answ['responseDetails']
	elif answ['responseData']:
		return answ['responseData']['language']
	else:
		return u'Unknown error'


try:
	import json
	register_command_handler(handler_google_trans, 'trans', ['info','all'], 10, 'Translate from one language to another. Via Google Translate engine. Available languages for translation:\n' + ', '.join(sorted([x.encode('utf-8')+': '+y.encode('utf-8') for x,y in trans_langs.iteritems()])), 'trans <source_lang> <target_lang> <text>', ['trans en ru hello', 'trans ru en привет'])
except ImportError:
	try:
		import simplejson as json
		register_command_handler(handler_google_trans, 'trans', ['info','all'], 10, 'Translate from one language to another. Via Google Translate engine. Available languages for translation:\n' + ', '.join(sorted([x.encode('utf-8')+': '+y.encode('utf-8') for x,y in trans_langs.iteritems()])), 'trans <source_lang> <target_lang> <text>', ['trans en ru hello', 'trans ru en привет'])
	except:
		print '====================================================\nYou need Python 2.6.x or simple_json package installed to use trans_plugin.py!!!\n====================================================\n'