#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  invite_plugin.py

#  Initial Copyright © 2008 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

invite_pending=[]

def handler_invite_start(type, source, parameters):
	truejid,nick,reason='','',''
	if not parameters:
		reply(type,source,u'and?')
		return
	if not parameters.count('@'):
		nicks = GROUPCHATS[source[1]].keys()
		nick=parameters.split()[0]
		if not nick in nicks:
			reply(type,source,u'are you sure, that <'+nick+u'> is here?')
			return
		else:
			truejid=get_true_jid(source[1]+'/'+nick)
			reason=' '.join(parameters.split()[1:])
	else:
		truejid=parameters
	msg=xmpp.Message(to=source[1])
	id = 'inv'+str(random.randrange(1, 1000))
	globals()['invite_pending'].append(id)
	msg.setID(id)
	x=xmpp.Node('x')
	x.setNamespace('http://jabber.org/protocol/muc#user')
	inv=x.addChild('invite', {'to':truejid})
	if reason:
		inv.setTagData('reason', reason)
	else:
		inv.setTagData('reason', u'you had been invited by '+source[2])
	msg.addChild(node=x)
#	print unicode(msg)
#	JCON.SendAndCallForResponse(msg, handler_invite_answ,{'type': type, 'source': source})
	JCON.send(msg)

"""		
def handler_invite_answ(coze, res, type, source):
	id = res.getID()
	if id in globals()['ping_pending']:
		globals()['ping_pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		return
	if res:
		print unicode(res)
		for p in [x.getTag('decline') for x in res.getTags('x')]:
			if p!= None:
				reason=p.getTagData('reason')
				if reason:
					reply(type, source, u'user does not want to come here: '+reason)
				else:
					reply(type, source, u'user does not want to come here')
"""					
					
register_command_handler(handler_invite_start, 'invite', ['muc','all'], 30, 'Invite of the specify user into a conference.', 'invite [nick/JID] [reason]', ['invite guy','invite guy@jsmart.web.id','invite guy@jsmart.web.id important'])
