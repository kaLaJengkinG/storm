#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  vcard_plugin.py

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

vcard_pending=[]

def handler_vcardget(type, source, parameters):
	vcard_iq = xmpp.Iq('get')
	id='vcard'+str(random.randrange(1000, 9999))
	globals()['vcard_pending'].append(id)
	vcard_iq.setID(id)
	vcard_iq.addChild('vCard', {}, [], 'vcard-temp');
	if parameters:
		if GROUPCHATS.has_key(source[1]):
			nicks = GROUPCHATS[source[1]].keys()
			nick = parameters.strip()
			if not nick in nicks:
				vcard_iq.setTo(nick)
			else:
				if GROUPCHATS[source[1]][nick]['ishere']==0:
					reply(type, source, u'was he here? :-O')
					return				
				jid=source[1]+'/'+nick
				vcard_iq.setTo(jid)
	else:
		jid=source[1]+'/'+source[2]
		vcard_iq.setTo(jid)
		nick=''
	JCON.SendAndCallForResponse(vcard_iq, handler_vcardget_answ, {'type': type, 'source': source, 'nick': nick})
		

def handler_vcardget_answ(coze, res, type, source, nick):
	id=res.getID()
	if id in globals()['vcard_pending']:
		globals()['vcard_pending'].remove(id)
	else:
		print 'ooops!'
		return
	rep =''
	if res:
		if res.getType()=='error':
			if not nick:
				reply(type,source,u'hehehe, your client does not support a vcard')
				return
			else:
				reply(type,source,u'hehehe, his client does not support a vcard')
				return
		elif res.getType() == 'result':
			name,nickname,url,email,desc = '','','','',''
			if res.getChildren():
				props = res.getChildren()[0].getChildren()
			else:
				if not nick:
					reply(type,source,u'fill in the vcard')
					return
				else:
					reply(type,source,u'pass to him, that he should fill in the vcard')
					return
			for p in props:
				if p.getName() == 'NICKNAME':
					nickname = p.getData()
				if p.getName() == 'FN':
					name = p.getData()				
				if p.getName() == 'URL':
					url = p.getData()
				if p.getName() == 'EMAIL':
					email = p.getData()
				if p.getName() == 'DESC':
					desc = p.getData()
			if nickname:
				if not nick:
					rep = u'about you I know the following:\nnick: '+nickname
				else:
					rep = u'about '+nick+u' I know the following:\nnick: '+nickname
			if not name=='':
				rep +='\nname: '+name				
			if not url=='':
				rep +='\nurl: '+url
			if not email=='':
				rep +=u'\nemail: '+email		
			if not desc=='':
				rep +=u'\nabout: '+desc
			if rep=='':
				rep = u'empty vcard'
		else:
			rep = u'He |-)'
	else:
		rep = u'something in any way...'
	reply(type, source, rep)



register_command_handler(handler_vcardget, 'vcard', ['info','muc','all'], 10, 'Show the indicated of user vcard.', 'vcard [nick]', ['vcard guy','vcard'])