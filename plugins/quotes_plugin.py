#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  quotes_plugin.py

#  Initial Copyright © ???
#  Modifications Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import urllib2,re,urllib

from re import compile as re_compile

strip_tags = re_compile(r'<[^<>]+>')

def handler_bashorgru_get(type, source, parameters):
	if parameters.strip()=='':
		req = urllib2.Request('http://bash.org.ru/random')
	else:
		req = urllib2.Request('http://bash.org.ru/quote/'+parameters.strip())
		req.add_header = ('User-agent', 'Mozilla/5.0')
	try:
		r = urllib2.urlopen(req)
		target = r.read()
		"""link to the quote"""
		od = re.search('<div class="vote">',target)
		b1 = target[od.end():]
		b1 = b1[:re.search('</a>',b1).start()]
		b1 = strip_tags.sub('', b1.replace('\n', ''))
		b1 = 'http://bash.org.ru/quote/'+b1+'\n'
		"""quote"""
		od = re.search(r'<div class="q">.*?<div class="vote">.*?</div>.*?<div>(.*?)</div>.*?</div>', target, re.DOTALL)
		message = b1+od.group(1)
		message = decode(message)
		message = '\n' + message.strip()
		reply(type,source,unicode(message,'windows-1251'))
	except:
		reply(type,source,u'probably, they changed a mark again')
        
        
def handler_bashorgru_abyss_get(type, source, parameters):
    if parameters.strip()=='':
        req = urllib2.Request('http://bash.org.ru/abysstop')
    else:
        reply(type,source,u'an abyss does not support a number')
        return
    req.add_header = ('User-agent', 'Mozilla/5.0')
    try:
        r = urllib2.urlopen(req)
        target = r.read()
        id=str(random.randrange(1, 25))
        """start"""
        od = re.search('<b>'+id+':',target)
        q1 = target[od.end():]
        q1 = q1[:re.search('\n</div>',q1).start()]
        """quote"""
        od = re.search('<div>',q1)
        message = q1[od.end():]
        message = message[:re.search('</div>',message).start()]	         
        message = decode(message)
        message = '\n' + message.strip()
        reply(type,source,unicode(message,'windows-1251'))
    except:
        reply(type,source,u'does not turn out for some reason')        

def decode(text):
    return strip_tags.sub('', text.replace('<br />','\n').replace('<br>','\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t','').replace('||||:]','').replace('>[:\n','')

register_command_handler(handler_bashorgru_get, 'bo', ['fun','info','all'], 0, 'Shows casual quotation from bo (bash.org.ru). we can set the number show out also.', 'bo', ['bo 223344','bo'])
register_command_handler(handler_bashorgru_abyss_get, 'boa', ['fun','info','all'], 0, 'Shows casual quotation from the abyss of bo (bash.org.ru).', 'boa', ['boa'])
