#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  info_plugin.py

#  Initial Copyright © 2007 Als <Als@exploru.net>
#  Parts of code Copyright © Bohdan Turkynewych aka Gh0st <tb0hdan[at]gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_getrealjid(type, source, parameters):
	groupchat=source[1]
	if GROUPCHATS.has_key(groupchat):
		nicks = GROUPCHATS[groupchat].keys()
		nick = parameters.strip()
		if not nick in nicks:
			reply(type,source,u'are you sure, that <'+nick+u'> was here?')
			return
		else:
			jidsource=groupchat+'/'+nick
			if get_true_jid(jidsource) == 'None':
				reply(type, source, u'I am not moderator')
				return
			truejid=get_true_jid(jidsource)
			if type == 'public':
				reply(type, source, u'sent to private')
		reply('private', source, u'true jid <'+nick+u'> --> '+truejid)
		
		
def handler_total_in_muc(type, source, parameters):
	groupchat=source[1]
	if GROUPCHATS.has_key(groupchat):
		inmuc=[]
		for x in GROUPCHATS[groupchat].keys():
			if GROUPCHATS[groupchat][x]['ishere']==1:
				inmuc.append(x)
		reply(type, source, u'i see here '+str(len(inmuc))+u' users\n'+u', '.join(inmuc))
	else:
		reply(type, source, u'*PARDON*')
		
		
def handler_bot_uptime(type, source, parameters):
	if INFO['start']:
		uptime=int(time.time() - INFO['start'])
		rep = u'i has been working for '+timeElapsed(uptime)
		rep += u'\ni was got %s messagess, created %s presences and %s iq-queries, and executed %s commands\n'%(str(INFO['msg']),str(INFO['prs']),str(INFO['iq']),str(INFO['cmd']))
		if os.name=='posix':
			try:
				pr = os.popen('ps -o rss -p %s' % os.getpid())
				pr.readline()
				mem = pr.readline().strip()
			finally:
				pr.close()
			if mem: rep += u'i also occupied %s kb of memory, ' % mem
		(user, system,qqq,www,eee,) = os.times()
		rep += u'spent %.2f seconds of processor, %.2f seconds of system time with totally %.2f seconds of general system time\n' % (user, system, user + system)
		rep += u'generated totally %s streams, now active %s streams' % (INFO['thr'], threading.activeCount())
	else:
		rep = u'*PARDON*'
	reply(type, source, rep)

register_command_handler(handler_getrealjid, 'truejid', ['info','admin','muc','all'], 20, 'Real JID of the indicated nick shows. Works only if a bot is a moderator certainly', 'truejid <nick>', ['truejid Pily'])
register_command_handler(handler_total_in_muc, 'here', ['info','muc','all'], 10, 'Shows the amount of users being in a conference.', 'here', ['here'])
register_command_handler(handler_bot_uptime, 'botup', ['info','admin','all'], 10, 'Shows how many time a bot works without falling.', 'botup', ['botup'])