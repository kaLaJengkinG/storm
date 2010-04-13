#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  complaint_plugin.py

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

def handler_complaint(type, source, parameters):
	if type == 'public':
		reply(type, source, u'this command works only in my private!')
	elif type == 'private':
		groupchat=source[1]
		if GROUPCHATS.has_key(groupchat):
			nicks = GROUPCHATS[groupchat].keys()
			args = parameters.split(' ')
			nick = args[0].strip()
			body = ' '.join(args[1:])
			if nick in GROUPCHATS[groupchat] and GROUPCHATS[groupchat][nick]['ishere']==1:		
				jidsource=groupchat+'/'+nick
				if user_level(jidsource,groupchat)>=15:
					reply(type,source,u'if once again a complaint will act on moderator - you are dead ]:->')
					return			
				if len(nick)>20 or len(body)>100:
					reply(type, source, u'а не много ли ты написал?')
					return
				for x in nicks:
					jid=groupchat+'/'+x
					if user_level(jid,groupchat)>=15 and GROUPCHATS[groupchat][x]['status'] in ['online','away','chat']:
						msg(jid, u'user <'+source[2]+u'>\ncomplaint on <'+nick+u'>\nreason <'+body+u'>\n\nYou can ban (ban '+nick+u' `reason`) or kicked (kick '+nick+u' `reason`) this users right now from my private')
				reply(type, source, u'complaint on <'+nick+u'> sent to all of moderators on this conference. If your complaint deemed spam, you will be banned')
			else:
				reply(type,source,u'you are sure that <'+nick+u'> is here?')
				
register_command_handler(handler_complaint, 'complaint',  ['muc','all'], 10, 'To complaint on certain nick on certain reason. Works only in my private!', 'complaint <nick> <reason>', ['complaint Joyo he is a spammer'])
