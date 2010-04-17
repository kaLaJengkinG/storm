#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  update_plugin.py

#  Initial Copyright © 2009 Als//ъыь <als-als@ya.ru>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import urllib2

from re import compile as re_compile

strip_tags = re_compile(r'<[^<>]+>')


def update_lastrev():
	try:
		req = urllib2.Request('http://storm-bot.googlecode.com/svn/trunk')#('http://googlecode')
		req.add_header = ('User-agent', 'Mozilla/5.0')
		r = urllib2.urlopen(req)
		target = r.read()
		od = re.search('<h2>storm-bot - Revision ',target)
		rev = target[od.end():]
		rev = rev[:re.search(': /trunk</h2>',rev).start()]
		return unicode(decode(rev),'windows-1251').strip()
	except:
		return ''
	
def update_lastrev_comment():
	try:
		req = urllib2.Request('http://storm-bot.googlecode.com/svn/trunk/LAST')
		req.add_header = ('User-agent', 'Mozilla/5.0')
		r = urllib2.urlopen(req)
		target = r.read()
		return unicode(decode(target),'windows-1251').strip()	
	except:
		return ''
	
def handler_update_lastrev(type, source, parameters):
	if parameters=='+':
		update_work(state=True)
		reply(type,source,u'auto-update new audit every hour ENABLE')
	elif parameters=='-':
		update_work(state=False)
		reply(type,source,u'auto-update new audit every hour DISABLE')	
	elif parameters=='*':
		update_work(known=True)
		reply(type,source,u'more than a nuisance :) to the new audit...')	
	else:		
		reply(type,source,u'latest revision of bot in SVN trunk branch - %s\nyour audit - %d\ncomment to the audit:\n\n%s' % (update_lastrev(), BOT_VER['rev'], update_lastrev_comment()))
	
def update_lastrev_autonotify():
	lastrev=update_lastrev()
	updinfo=get_update_autonotify_state()
	if updinfo['state']:
		if updinfo['known']:
			if int(lastrev)!=updinfo['actual']:
				msg(ADMINS[0], u'latest revision ot bot in SVN trunk branch - %s\nyour audit - %d\ncomment to the audit:\n\n%s' % (lastrev, BOT_VER['rev'], update_lastrev_comment()))
				update_work(known=False, actual=int(lastrev))
		else:
			msg(ADMINS[0], u'latest revision of bot in SVN trunk branch - %s\nyour audit - %d\ncomment to the audit:\n\n%s' % (lastrev, BOT_VER['rev'], update_lastrev_comment()))
			update_work(actual=int(lastrev))
		threading.Timer(3600, update_lastrev_autonotify).start()
	
def get_update_autonotify_state():
	if check_file(file='updinfo.cfg'):
		updinfo = eval(read_file('dynamic/updinfo.cfg'))
	else:
		print 'error creating update info DB!!! default is always notify'
		return
	if not 'state' in updinfo:
		updinfo={'state': True, 'known': False, 'actual': None}
		write_file('dynamic/updinfo.cfg', str(updinfo))
	return updinfo
	
def update_work(state=None, known=None, actual=None):
	DBPATH='dynamic/updinfo.cfg'
	if check_file(file='updinfo.cfg'):
		updinfo = eval(read_file(DBPATH))
		if state!=None:
			updinfo['state']=state
		if known!=None:
			updinfo['known']=known
		if actual:
			updinfo['actual']=actual
		write_file(DBPATH, str(updinfo))	
	else:
		print 'error creating update info DB!!! default is always notify'
		return	

def decode(text):
    return strip_tags.sub('', text.replace('<br>','\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t','').replace('>[:\n','')

register_command_handler(handler_update_lastrev, 'botupd', ['info','superadmin','all'], 100, 'Shows the last audit bot SVN branch in its trunk. Parameters:\n+ ENABLE auto-check of the new audit (check every hour)\n- DISABLE auto-check of the new audit\n* to mark that you are aware of the update. Reminders of the new audit disappear until a new update release', 'botupd<+/*>', ['botupd +','botupd *','botupd -'])
register_stage2_init(update_lastrev_autonotify)
register_stage0_init(get_update_autonotify_state)