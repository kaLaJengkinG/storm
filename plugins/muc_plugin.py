#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  muc_plugin.py

#  Initial Copyright © 2009 dr.Schmurge <JID: dr.schmurge@gajim.org>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details. 


#def handler_bot_nick(type, source, parameters):
#	if not parameters:
#		reply(type, source, u'hmmmm?')
#		return
#	else:
#		add_gch(source[1], parameters)
#		join_groupchat(source[1], parameters)
#	reply(type, source, u'OK')
#
#def handler_admin(type, source, parameters):
#	groupchat = source[1]
#	if not parameters:
#		reply(type, source, u'hmmmm?')
#		return
#	else:
#		nick = parameters
#		if GROUPCHATS.has_key(source[1]):
#			if not nick in GROUPCHATS[groupchat]:
#				reply(type, source, u'who?')
#				return
#			else:
#				jid = get_true_jid(groupchat+'/'+nick)
#				order_admin(groupchat, jid, u'')
#				return
#
#def handler_owner(type, source, parameters):
#	groupchat = source[1]
#	if not parameters:
#		reply(type, source, u'hmmmm?')
#		return
#	else:
#		nick = parameters
#		if GROUPCHATS.has_key(source[1]):
#			if not nick in GROUPCHATS[groupchat]:
#				reply(type, source, u'who?')
#				return
#			else:
#				jid = get_true_jid(groupchat+'/'+nick)
#				order_owner(groupchat, jid, u'')
#				return
#
#def handler_unban(type, source, parameters):
#	groupchat = source[1]
#	if not parameters:
#		reply(type, source, u'hmmmm?')
#		return
#	else:
#		jid = parameters
#		order_unban(groupchat, jid)
#		reply(type, source, u'it is done :)')
#		return
#
#def handler_admin(type, source, parameters):
#	groupchat = source[1]
#	if not parameters:
#		reply(type, source, u'hmmmm?')
#		return
#	else:
#		nick = parameters
#		if GROUPCHATS.has_key(source[1]):
#			if not nick in GROUPCHATS[groupchat]:
#				reply(type, source, u'who?')
#				return
#			else:
#				jid = get_true_jid(groupchat+'/'+nick)
#				order_admin(groupchat, jid, u'')
#				return
#				
#def handler_ban(type, source, parameters):
#	groupchat = source[1]
#	if not parameters:
#		reply(type, source, u'hmmmm?')
#		return
#	else:
#		if not parameters.count('@'):
#			nick = parameters
#			if GROUPCHATS.has_key(source[1]):
#				if not nick in GROUPCHATS[groupchat]:
#					reply(type, source, u'who?')
#					return
#				else:
#					jid = get_true_jid(groupchat+'/'+nick)
#					order_banjid(groupchat, jid, u'')
#					reply(type, source, u'it is done')
#					return
#		else:
#			jid = parameters
#			order_banjid(groupchat, jid, u'')
#			reply(type, source, u'it is done')
#			return
#
#def handler_ban_nick(type, source, parameters):
#	groupchat = source[1]
#	if not parameters:
#		reply(type, source, u'hmmmm?')
#		return
#	else:
#		nick = parameters
#		if GROUPCHATS.has_key(source[1]):
#			if not nick in GROUPCHATS[groupchat]:
#				reply(type, source, u'who?')
#				return
#			else:
#				jid = get_true_jid(groupchat+'/'+nick)
#				order_banjid(groupchat, jid, u'')
#				reply(type, source, u':)')
#				return
		
#def handler_ban_jid(type, source, parameters):
#	groupchat = source[1]
#	if not parameters:
#		reply(type, source, u'hmmmm?')
#		return
#	else:
#	        if not parameters.count(' '):
#			jid = parameters
#			order_banjid(groupchat, jid, u'')
#			reply(type, source, u':)')
#			return
#		else:
#			parameters = parameters.split()
#			jid = parameters[0]
#			order_banjid(groupchat, jid, parameters[1])
#			reply(type, source, u':)')
#			return
			
#def handler_visitor(type, source, parameters):
#	groupchat = source[1]
#	if not parameters:
#		reply(type, source, u'what?')
#		return
#	else:
#		nick = parameters
#		if GROUPCHATS.has_key(source[1]):
#			if not nick in GROUPCHATS[groupchat]:
#				reply(type, source, u'who?')
#				return
#			else:
#				#jid = get_true_jid(groupchat+'/'+nick)
#				order_visitor(groupchat, nick, u'')
#				reply(type, source, u':)')
#				return

#def handler_participant(type, source, parameters):
#	groupchat = source[1]
#	if not parameters:
#		reply(type, source, u'what?')
#		return
#	else:
#		nick = parameters
#		if GROUPCHATS.has_key(source[1]):
#			if not nick in GROUPCHATS[groupchat]:
#				reply(type, source, u'who?')
#				return
#			else:
#				#jid = get_true_jid(groupchat+'/'+nick)
#				order_participant(groupchat, nick, u'')
#				reply(type, source, u':)')
#				return

#def handler_kick(type, source, parameters):
#	groupchat = source[1]
#	if not parameters:
#		reply(type, source, u'what?')
#		return
#	else:
#		nick = parameters
#		if GROUPCHATS.has_key(source[1]):
#			if not nick in GROUPCHATS[groupchat]:
#				reply(type, source, u'who?')
#				return
#			else:
#				#jid = get_true_jid(groupchat+'/'+nick)
#				order_kick(groupchat, nick, u'')
#				reply(type, source, u':)')
#				return

#def handler_member(type, source, parameters):
#	groupchat = source[1]
#	if not parameters:
#		reply(type, source, u'what?')
#		return
#	else:
#		nick = parameters
#		if GROUPCHATS.has_key(source[1]):
#			if not nick in GROUPCHATS[groupchat]:
#				reply(type, source, u'who?')
#				return
#			else:
#				jid = get_true_jid(groupchat+'/'+nick)
#				order_member(groupchat, jid, u'')
#				reply(type, source, u':)')
#				return

#def handler_moderator(type, source, parameters):
#	groupchat = source[1]
#	if not parameters:
#		reply(type, source, u'what?')
#		return
#	else:
#		nick = parameters
#		if GROUPCHATS.has_key(source[1]):
#			if not nick in GROUPCHATS[groupchat]:
#				reply(type, source, u'who?')
#				return
#			else:
#				#jid = get_true_jid(groupchat+'/'+nick)
#				order_moderator(groupchat, nick, u'')
#				reply(type, source, u':)')
#				return

#def handler_unmember(type, source, parameters):
	#groupchat = source[1]
	#if not parameters:
		#reply(type, source, u'Кого?')
		#return
	#else:
		#nick = parameters
		#if GROUPCHATS.has_key(source[1]):
			#if not nick in GROUPCHATS[groupchat]:
				#reply(type, source, u'А он тут?')
				#return
			#else:
				#jid = get_true_jid(groupchat+'/'+nick)
				#order_unmember(groupchat, jid)
				#reply(type, source, u'Готово')
				#return

#def handler_where(type, source, parameters):
#	#reply(type, source, 'я сижу в '+str(len(GROUPCHATS.keys()))+' комнатах:\n'+'\n'.join(GROUPCHATS.keys()).encode('utf8')) #+' ['+str(len(GROUPCHATS.has_key(GROUPCHATS.keys()))))
#	cnt = 0
#	gch = ''
#	gch_cnt = []
#	for gch in GROUPCHATS.keys():
#		for nicks in GROUPCHATS[gch]:
#			#if user_level(gch+'/'+nicks,gch)>=0:
#				cnt += 1
#		gch_cnt.append((gch, cnt))
#		cnt = 0
#	n = 1
#	msg = u'Total number of conferences: '+str(len(gch_cnt))+'\n'
#	for i in gch_cnt:
#		msg += str(n)+'. '+i[0]+' ['+str(i[1])+']\n'
#		n += 1
#	reply(type, source, msg)
	
#def handler_who_was(type, source, parameters):
	#gch = source[1]
	#for x in GROUPCHATS[gch].keys():
		#x = x.encode("utf-8")
	#reply(type, source, u'я здесь видела '+str(len(GROUPCHATS[gch].keys()))+' юзеров:\n'+', '.join([x]))

def handler_ban_everywhere(type, source, jid):
	gch=source[1]
	for gch in GROUPCHATS.keys():
	    order_banjid(gch, jid, u'go to hell')
#	    reply(type, source, u'ban everywhere')
#	    return

def handler_unban_everywhere(type, source, jid):
	gch=source[1]
	for gch in GROUPCHATS.keys():
	    order_unban(gch, jid)
#	    reply(type, source, u'unban everywhere')
#	    return

def handler_member_everywhere(type, source, jid):
	gch=source[1]
	for gch in GROUPCHATS.keys():
	    order_member(gch, jid, u'congratulations! Be a good member')
#	    reply(type, source, u'member everywhere')
#	    return

def handler_unmember_everywhere(type, source, jid):
	gch=source[1]
	for gch in GROUPCHATS.keys():
	    order_unmember(gch, jid)
#	    reply(type, source, u'unmember everywhere')
#	    return

#def order_admin(groupchat, jid, reason):
#	iq = xmpp.Iq('set')
#	iq.setTo(groupchat)
#	iq.setID(str(random.randrange(1000, 9999)))
#	query = xmpp.Node('query')
#	query.setNamespace('http://jabber.org/protocol/muc#admin')
#	ban=query.addChild('item', {'jid':jid, 'affiliation':'admin'})
#	ban.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
#	iq.addChild(node=query)
#	JCON.send(iq)

#def order_owner(groupchat, jid, reason):
#	iq = xmpp.Iq('set')
#	iq.setTo(groupchat)
#	iq.setID(str(random.randrange(1000, 9999)))
#	query = xmpp.Node('query')
#	query.setNamespace('http://jabber.org/protocol/muc#admin')
#	ban=query.addChild('item', {'jid':jid, 'affiliation':'owner'})
#	ban.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
#	iq.addChild(node=query)
#	JCON.send(iq)
#
#def order_kick(groupchat, nick, reason):
#	iq = xmpp.Iq('set')
#	iq.setTo(groupchat)
#	iq.setID('kick'+str(random.randrange(1000, 9999)))
#	query = xmpp.Node('query')
#	query.setNamespace('http://jabber.org/protocol/muc#admin')
#	kick=query.addChild('item', {'nick':nick, 'role':'none'})
#	kick.setTagData('reason', get_bot_nick(groupchat)+': '+reason)
#	iq.addChild(node=query)
#	JCON.send(iq)

def order_unban(groupchat, jid):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	query.addChild('item', {'jid':jid, 'affiliation':'none'})
	iq.addChild(node=query)
	JCON.send(iq)

#def order_participant(groupchat, nick, reason):
#	iq = xmpp.Iq('set')
#	iq.setTo(groupchat)
#	iq.setID(str(random.randrange(1000, 9999)))
#	query = xmpp.Node('query')
#	query.setNamespace('http://jabber.org/protocol/muc#admin')
#	visitor=query.addChild('item', {'nick':nick, 'role':'participant'})
#	visitor.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
#	iq.addChild(node=query)
#	JCON.send(iq)

#def order_ban(groupchat, nick, reason):
#	iq = xmpp.Iq('set')
#	iq.setTo(groupchat)
#	iq.setID('kick'+str(random.randrange(1000, 9999)))
#	query = xmpp.Node('query')
#	query.setNamespace('http://jabber.org/protocol/muc#admin')
#	ban=query.addChild('item', {'nick':nick, 'affiliation':'outcast'})
#	ban.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
#	iq.addChild(node=query)
#	JCON.send(iq)

def order_banjid(groupchat, jid, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('ban'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'jid':jid, 'affiliation':'outcast'})
	ban.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def order_member(groupchat, jid, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID(str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'jid':jid, 'affiliation':'member'})
	ban.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

#def order_moderator(groupchat, nick, reason):
#	iq = xmpp.Iq('set')
#	iq.setTo(groupchat)
#	iq.setID(str(random.randrange(1000, 9999)))
#	query = xmpp.Node('query')
#	query.setNamespace('http://jabber.org/protocol/muc#admin')
#	visitor=query.addChild('item', {'nick':nick, 'role':'moderator'})
#	visitor.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
#	iq.addChild(node=query)
#	JCON.send(iq)

def order_unmember(groupchat, jid):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID(str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	query.addChild('item', {'jid':jid, 'affiliation':"none"})
	iq.addChild(node=query)
	JCON.send(iq)

#register_command_handler(handler_bot_nick, 'botnick', ['muc','all'], 20, 'changes the bots nickname in conference.', 'botnick <nick>', ['botnick pink'])
#register_command_handler(handler_admin, 'admin', ['muc','all'], 30, 'to let bot make someone an admin of conference.', 'admin <nick>', ['admin joe'])
#register_command_handler(handler_owner, 'owner', ['muc','all'], 30, 'bot will make the specified person an ownerof the conference.', 'owner <nick>', ['owner fred'])
#register_command_handler(handler_unban, 'unban', ['muc','all'], 20, 'to unban a person from the conference.', 'unban <jid>', ['unban guy@jsmart.web.id'])
#register_command_handler(handler_ban, 'ban', ['muc','all'], 20, 'ban someone from conference you can also specify a reason for the ban', 'ban <nick/jid> <reason>', ['ban guy@jsmart.web.id', 'ban joe', 'ban joe asshole'])
#register_command_handler(handler_ban_nick, 'bannick', ['muc','all'], 20, 'ban nick from room you can also give a reason for the ban', 'ban <nick>', ['ban sammy', 'ban sammy flood'])
#register_command_handler(handler_ban_jid, 'banjid', ['muc','all'], 20, 'ban of JID, bot will save the specified jid in the ban list thus preventing him or her from entering the conference', 'banjid <JID>', ['banjid guy@jsmart.web.id'])
#register_command_handler(handler_visitor, 'visitor', ['muc','all'], 20, 'to make someone a visitor in conference note that he or she might not be able to send messages directly in the conference', 'visitor <nick>', ['visitor sammy'])
#register_command_handler(handler_participant, 'participant', ['muc','all'], 20, 'makes the given nick a participant and granting him voice', 'participant <nick>', ['participant leon'])
#register_command_handler(handler_kick, 'kick', ['muc','all'], 15, 'kicks person out of the conference, you can also give a reason for the kick', 'kick <nick> <reason>', ['kick sam', 'kick sam spamming'])
#register_command_handler(handler_member, 'member', ['muc','all'], 20, 'gives the role of member to a participant in conference', 'member <nick>', ['member roxy'])
#register_command_handler(handler_moderator, 'mod', ['muc','all'], 20, 'gives soneone the role of moderator note moderators can see jid of others and can also kick', 'mod <nick>', ['mod genko'])
#register_command_handler(handler_member, 'unmember', ['muc','all'], 20, 'Забрать права зарегистрированного участника чата', 'унмембер <nick>', ['унмембер Вася'])
#register_command_handler(handler_where, 'show', ['muc','all'], 100, 'shows the list where bot is currently active', 'show', ['show'])
register_command_handler(handler_member_everywhere, 'fullmember', ['superadmin','all'], 100, 'member a jid everywhere where bot sits in conference', 'fullmember <jid>', ['fullmember guy@jsmart.web.id'])
register_command_handler(handler_unmember_everywhere, 'fullunmember', ['superadmin','all'], 100, 'unmember a jid everywhere where bot sits in conference', 'fullunmember <jid>', ['fullunmember guy@jsmart.web.id'])
register_command_handler(handler_ban_everywhere, 'fullban', ['superadmin','all'], 100, 'ban a jid everywhere where bot sits in conference', 'fullban <jid>', ['fullban guy@jsmart.web.id'])
register_command_handler(handler_unban_everywhere, 'fullunban', ['superadmin','all'], 100, 'unban a jid everywhere bot sits', 'fullunban <jid>', ['fullunban guy@jsmart.web.id'])
#register_command_handler(handler_who_was, 'хтобыл', ['muc','all'], 20, 'Показывает ники всех, кто заходил в комнату за текущую сессию бота', 'хтобыл', ['хтобыл'])
