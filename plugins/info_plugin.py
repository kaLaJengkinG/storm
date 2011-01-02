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
		rep = u'\n- Session PID: '+str(os.getpid())
		rep += u'\n- Working time: '+timeElapsed(uptime)
		rep += u'\n- Messages posted: %s\n- Presences proceed: %s\n- Iq-queries proceed: %s\n- Commands executed: %s' % (str(INFO['msg']),str(INFO['prs']),str(INFO['iq']),str(INFO['cmd']))
		if os.name=='posix':
			try:
				pr = os.popen('ps -o rss -p %s' % os.getpid())
				pr.readline()
				mem = pr.readline().strip()
			finally:
				pr.close()
			if mem: rep += u'\n- Memory usage: %s Kb ' % mem
		(user, system,qqq,www,eee,) = os.times()
		rep += u'\n- CPU time spent: %.2f seconds\n- System time spent: %.2f seconds\n- Total system-wide time: %.2f seconds' % (user, system, user + system)
		rep += u'\n- Total generated streams: %s\n- Total active streams: %s ' % (INFO['thr'], threading.activeCount())
	else:
		rep = u'*PARDON*'
	reply(type, source, rep)

register_command_handler(handler_getrealjid, 'truejid', ['info','admin','muc','all'], 20, 'Real JID of the indicated nick shows. Works only if a bot is a moderator certainly', 'truejid <nick>', ['truejid Pily'])
register_command_handler(handler_total_in_muc, 'here', ['info','admin','muc','all'], 10, 'Shows the amount of users being in a conference.', 'here', ['here'])
register_command_handler(handler_bot_uptime, 'botup', ['info','admin','all'], 10, 'Shows how many time a bot works without falling.', 'botup', ['botup'])