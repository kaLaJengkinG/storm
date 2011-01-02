#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  send_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  Help Copyright © 2007 dimichxp <dimichxp@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

sendqueue={}


def handler_send_save(ltype, source, parameters):
	groupchat=source[1]
	if GROUPCHATS.has_key(groupchat):
		nicks = GROUPCHATS[groupchat].keys()
		args = parameters.split(' ')
		date=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
		fromnick=source[2]+u' from '+source[1]+u' at '+date+u' (UTC) said me to tell you the following message:\n\n'
		if len(args)>=2:
			nick = args[0]
			body = ' '.join(args[1:])
			if nick == 'botadmin':
				reply(ltype, source, u'I will tell it soon')
				msg(ADMINS[0], fromnick+body)
				return
			if get_bot_nick(groupchat) != nick:
				tojid = groupchat+'/'+nick
				if nick in nicks and GROUPCHATS[groupchat][nick]['ishere']==1:
					reply(ltype, source, u'was he here')
				else:
					if not groupchat in sendqueue:
						sendqueue[groupchat]=groupchat
						sendqueue[groupchat]={}
					if not tojid in sendqueue[groupchat]:
						sendqueue[groupchat][tojid] = tojid
						sendqueue[groupchat][tojid] = []
					sendqueue[groupchat][tojid].append(fromnick+body)
					reply(ltype, source, u'I will tell it soon')
					if check_file(groupchat,file='send.txt'):
						sendfp='dynamic/'+groupchat+'/send.txt'
						write_file(sendfp,str(sendqueue[groupchat]))
					else:
						print 'send_plugin.py error'
						pass

def handler_send_join(groupchat, nick, aff, role):
	tojid = groupchat+'/'+nick
	if groupchat in sendqueue:
		if sendqueue[groupchat].has_key(tojid) and sendqueue[groupchat][tojid]:
			for x in sendqueue[groupchat][tojid]:
				msg(tojid, x)
			sendqueue[groupchat][tojid] = []
			if check_file(groupchat,file='send.txt'):
				sendfp='dynamic/'+groupchat+'/send.txt'
				write_file(sendfp,str(sendqueue[groupchat]))
			else:
				print 'send_plugin.py error'
				pass
	else:
		pass
		
def get_send_cache(gch):
	sfc='dynamic/'+gch+'/send.txt'
	if not check_file(gch,'send.txt'):
		print 'error with caches in send_plugin.py'
		raise
	try:
		cache = eval(read_file(sfc))
		sendqueue[gch]={}
		sendqueue[gch]=cache
	except:
		pass	

register_join_handler(handler_send_join)
register_command_handler(handler_send_save, 'tell', ['muc','all'], 10, 'Memorizes a message and tell to the indicated nick as soon as the user join in the conference.', 'tell <nick> <message>', ['tell guy hello! I need to talk with you!!!'])

register_stage1_init(get_send_cache)
