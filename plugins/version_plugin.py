#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  version_plugin.py

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

version_pending=[]
def handler_version(type, source, parameters):
	nick = source[2]
	groupchat=source[1]
	iq = xmpp.Iq('get')
	id='vers'+str(random.randrange(1000, 9999))
	globals()['version_pending'].append(id)
	iq.setID(id)
	iq.addChild('query', {}, [], 'jabber:iq:version');
	if parameters:
		jid=groupchat+'/'+parameters.strip()
		if GROUPCHATS.has_key(groupchat):
			nicks = GROUPCHATS[groupchat].keys()
			param = parameters.strip()
			if not nick in nicks:
				iq.setTo(param)
			else:
				if GROUPCHATS[groupchat][nick]['ishere']==0:
					reply(type, source, u'was he here? :-O')
					return
				iq.setTo(jid)
	else:
		jid=groupchat+'/'+nick
		iq.setTo(jid)
	JCON.SendAndCallForResponse(iq, handler_version_answ, {'type': type, 'source': source})
	return

def handler_version_answ(coze, res, type, source):
	id=res.getID()
	if id in globals()['version_pending']:
		globals()['version_pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		return
	rep =''
	if res:
		if res.getType() == 'result':
			name = '[no name]'
			version = '[no ver]'
			os = '[no os]'
			props = res.getQueryChildren()
			for p in props:
				if p.getName() == 'name':
					name = p.getData()
				elif p.getName() == 'version':
					version = p.getData()
				elif p.getName() == 'os':
					os = p.getData()
			if name:
				rep = u'\nClient    :' u'  '+name+u'\n'
			if version:
				rep +=u'Version :' u'  '+version+u'\n'
			if os:
				rep +=u'Os       :' u'  '+os
		else:
			rep = u'he |-)'
	else:
		rep = u'there is not such thing'
	reply(type, source, rep)
	
register_command_handler(handler_version, 'version', ['info','muc','all'], 0, 'Shows information about a client which utillizes user or server.', 'version [nick\server]', ['version','version guy','version jsmart.web.id'])