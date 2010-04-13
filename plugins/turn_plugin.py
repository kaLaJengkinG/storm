#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  turn_plugin.py

#  Initial Copyright © 2008 dimichxp <dimichxp@gmail.com>
#  Idea © 2008 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

global_en2ru_table = dict(zip(u"qwertyuiop[]asdfghjkl;'zxcvbnm,./`йцукенгшщзхъфывапролджэячсмитьбю.ёQWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?~ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё", u"йцукенгшщзхъфывапролджэячсмитьбю.ёqwertyuiop[]asdfghjkl;'zxcvbnm,./`ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,ЁQWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?~"))

turn_msgs={}

def handler_turn_last(type, source, parameters):
	nick=source[2]
	groupchat=source[1]
	jid=get_true_jid(groupchat+'/'+nick)	
	if parameters:
		reply(type,source,reduce(lambda x,y:global_en2ru_table.get(x,x)+global_en2ru_table.get(y,y),parameters))
	else:
		if turn_msgs[groupchat][jid] is None:
			reply(type,source,u'and you talked nothing')
			return
		if turn_msgs[groupchat][jid] == u'turn':
			reply(type,source,u'not allowed')
			return		
		tmsg=turn_msgs[groupchat][jid]
		reply(type,source,reduce(lambda x,y:global_en2ru_table.get(x,x)+global_en2ru_table.get(y,y),tmsg))

def handler_turn_save_msg(type, source, body):
	time.sleep(1)
	nick=source[2]
	groupchat=source[1]
	jid=get_true_jid(groupchat+'/'+nick)
	if groupchat in turn_msgs.keys():
		if jid in turn_msgs[groupchat].keys() and jid != groupchat and jid != JID:
			turn_msgs[groupchat][jid]=body
	
def handler_turn_join(groupchat, nick, aff, role):
	jid=get_true_jid(groupchat+'/'+nick)
	if not groupchat in turn_msgs.keys():
		turn_msgs[groupchat] = {}
	if not jid in turn_msgs[groupchat].keys() and jid != JID:
		turn_msgs[groupchat][jid]=None


register_message_handler(handler_turn_save_msg)
register_join_handler(handler_turn_join)
register_command_handler(handler_turn_last, 'turn', ['muc','all'], 10, 'Commutes the lay-out of keyboard for the latest report from the user of causing command.', 'turn', ['turn'])