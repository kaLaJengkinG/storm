#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  order_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  First Version and Idea © 2007 dimichxp <dimichxp@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

order_stats = {}
order_obscene_words = [u' babi ', u' memek ', u' vagina ', u' kontol ', u' bangsat ', u' perek ', u' tetek ', u' (_|_) ', u' fuck ', u' tai ', u' titit ', u' peler ', u' penis ', u' itil ', u' entot ', u' kentot ']


def order_check_obscene_words(body):
	body=body.lower()
	body=u' '+body+u' '
	for x in order_obscene_words:
		if body.count(x):
			return True
	return False

def order_check_time_flood(gch, jid, nick):
	lastmsg=order_stats[gch][jid]['msgtime']
	if lastmsg and time.time()-lastmsg<=2.2:
		order_stats[gch][jid]['msg']+=1
		if order_stats[gch][jid]['msg']>3:
			order_stats[gch][jid]['devoice']['time']=time.time()
			order_stats[gch][jid]['devoice']['cnd']=1
			order_stats[gch][jid]['msg']=0
			order_kick(gch, nick, u'-time- message too fast')
			return True
		return False

def order_check_len_flood(mlen, body, gch, jid, nick):			
	if len(body)>mlen:
		order_stats[gch][jid]['devoice']['time']=time.time()
		order_stats[gch][jid]['devoice']['cnd']=1
		order_kick(gch, nick, u'-len- flood *FUCK*')
		return True
	return False
				
def order_check_obscene(body, gch, jid, nick):
	if order_check_obscene_words(body):
		order_stats[gch][jid]['devoice']['time']=time.time()
		order_stats[gch][jid]['devoice']['cnd']=1
		order_kick(gch, nick, u'-obscene- censor of bahasa Indonesia')
		return True
	return False
			
def order_check_caps(body, gch, jid, nick):
	ccnt=0
	nicks = GROUPCHATS[gch].keys()
	for x in nicks:
		if body.count(x):
			body=body.replace(x,'')
	for x in [x for x in body.replace(' ', '')]:
		if x.isupper():
			ccnt+=1
	if ccnt>=len(body)/2 and ccnt>9:
		order_stats[gch][jid]['devoice']['time']=time.time()
		order_stats[gch][jid]['devoice']['cnd']=1
		order_kick(gch, nick, u'-caps- use capital letters')
		return True
	return False
		
def order_check_like(body, gch, jid, nick):		
	lcnt=0
	lastmsg=order_stats[gch][jid]['msgtime']
	if lastmsg and order_stats[gch][jid]['msgbody']:
		if time.time()-lastmsg>60:
			order_stats[gch][jid]['msgbody']=body.split()
		else:
			for x in order_stats[gch][jid]['msgbody']:
				for y in body.split():
					if x==y:
						lcnt+=1
			if lcnt:
				lensrcmsgbody=len(body.split())
				lenoldmsgbody=len(order_stats[gch][jid]['msgbody'])
				avg=(lensrcmsgbody+lenoldmsgbody/2)/2
				if lcnt>avg:
					order_stats[gch][jid]['msg']+=1
					if order_stats[gch][jid]['msg']>=2:
						order_stats[gch][jid]['devoice']['time']=time.time()
						order_stats[gch][jid]['devoice']['cnd']=1
						order_stats[gch][jid]['msg']=0
						order_kick(gch, nick, u'-like- repetition of messages')
						return True
			order_stats[gch][jid]['msgbody']=body.split()
	else:
		order_stats[gch][jid]['msgbody']=body.split()
	return False

####################################################################################################

def order_kick(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	kick=query.addChild('item', {'nick':nick, 'role':'none'})
	kick.setTagData('reason', get_bot_nick(groupchat)+': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)
	
def order_visitor(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	visitor=query.addChild('item', {'nick':nick, 'role':'visitor'})
	visitor.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)
	
def order_ban(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'nick':nick, 'affiliation':'outcast'})
	ban.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)
	
def order_unban(groupchat, jid):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	query.addChild('item', {'jid':jid, 'affiliation':'none'})
	iq.addChild(node=query)
	JCON.send(iq)
	
def order_check_idle():
	for gch in GROUPCHATS.keys():
		if GCHCFGS[gch]['filt']['idle']['cond']==1:
			timee=GCHCFGS[gch]['filt']['idle']['time']
			now=time.time()
			for nick in GROUPCHATS[gch].keys():
				if GROUPCHATS[gch][nick]['ishere']==1:
					if user_level(gch+'/'+nick,gch)<11:
						idle=now-GROUPCHATS[gch][nick]['idle']
						if idle > timee:
							order_kick(gch, nick, u'-idle- silence for about '+timeElapsed(idle))
	threading.Timer(120,order_check_idle).start()
	
####################################################################################################

def handler_order_message(type, source, body):
	nick=source[2]
	groupchat=source[1]
	if groupchat in GROUPCHATS.keys() and user_level(source,groupchat)<11:
		if get_bot_nick(groupchat)!=nick:
			jid=get_true_jid(groupchat+'/'+nick)
			if groupchat in order_stats and jid in order_stats[groupchat]:
				if GCHCFGS[groupchat]['filt']['time']==1:
					if order_check_time_flood(groupchat, jid, nick):	return
				if GCHCFGS[groupchat]['filt']['len']==1:
					if order_check_len_flood(900, body, groupchat, jid, nick):	return
				if GCHCFGS[groupchat]['filt']['obscene']==1:
					if order_check_obscene(body, groupchat, jid, nick):	return
				if GCHCFGS[groupchat]['filt']['caps']==1:
					if order_check_caps(body, groupchat, jid, nick):	return
				if GCHCFGS[groupchat]['filt']['like']==1:
					if order_check_like(body, groupchat, jid, nick):	return
				order_stats[groupchat][jid]['msgtime']=time.time()
				
def handler_order_join(groupchat, nick, aff, role):
	jid=get_true_jid(groupchat+'/'+nick)
	if nick in GROUPCHATS[groupchat] and user_level(groupchat+'/'+nick,groupchat)<11:
		now = time.time()
		if not groupchat in order_stats.keys():
			order_stats[groupchat] = {}
		if jid in order_stats[groupchat].keys():
			if order_stats[groupchat][jid]['devoice']['cnd']==1:
				if now-order_stats[groupchat][jid]['devoice']['time']>300:
					order_stats[groupchat][jid]['devoice']['cnd']=0
				else:
					order_visitor(groupchat, nick, u'voting rights stripped for previous violations')

			if GCHCFGS[groupchat]['filt']['kicks']['cond']==1:
				kcnt=GCHCFGS[groupchat]['filt']['kicks']['cnt']
				if order_stats[groupchat][jid]['kicks']>kcnt:
					order_ban(groupchat, nick, u'too many kicks!!!')
					return

			if GCHCFGS[groupchat]['filt']['fly']['cond']==1:
				lastprs=order_stats[groupchat][jid]['prstime']['fly']
				order_stats[groupchat][jid]['prstime']['fly']=time.time()	
				if now-lastprs<=70:
					order_stats[groupchat][jid]['prs']['fly']+=1
					if order_stats[groupchat][jid]['prs']['fly']>4:
						order_stats[groupchat][jid]['prs']['fly']=0
						fmode=GCHCFGS[groupchat]['filt']['fly']['mode']
						ftime=GCHCFGS[groupchat]['filt']['fly']['time']
						if fmode=='ban':
							order_ban(groupchat, nick, u'stop flying!!!')
							time.sleep(ftime)
							order_unban(groupchat, jid)
						else:
							order_kick(groupchat, nick, u'stop flying!!!')
							return
				else:
					order_stats[groupchat][jid]['prs']['fly']=0
			
			if GCHCFGS[groupchat]['filt']['obscene']==1:		
				if order_check_obscene(nick, groupchat, jid, nick):	return
			
			if GCHCFGS[groupchat]['filt']['len']==1:	
				if order_check_len_flood(20, nick, groupchat, jid, nick):	return
			
		elif nick in GROUPCHATS[groupchat]:
			order_stats[groupchat][jid]={'kicks': 0, 'devoice': {'cnd': 0, 'time': 0}, 'msgbody': None, 'prstime': {'fly': 0, 'status': 0}, 'prs': {'fly': 0, 'status': 0}, 'msg': 0, 'msgtime': 0}

	elif groupchat in order_stats and jid in order_stats[groupchat]:
		del order_stats[groupchat][jid]
	else:
		pass			

def handler_order_presence(prs):
	ptype = prs.getType()
	if ptype=='unavailable' or ptype=='error':
		return
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	stmsg = prs.getStatus()
	jid=get_true_jid(groupchat+'/'+nick)
	item=findPresenceItem(prs)
	
	if groupchat in order_stats and jid in order_stats[groupchat]:
		if item['affiliation'] in ['member','admin','owner']:
			del order_stats[groupchat][jid]
			return
	else:
		if item['affiliation']=='none':
			order_stats[groupchat][jid]={'kicks': 0, 'devoice': {'cnd': 0, 'time': 0}, 'msgbody': None, 'prstime': {'fly': 0, 'status': 0}, 'prs': {'fly': 0, 'status': 0}, 'msg': 0, 'msgtime': 0}
	
	if nick in GROUPCHATS[groupchat] and user_level(groupchat+'/'+nick,groupchat)<11:
		if groupchat in order_stats and jid in order_stats[groupchat]:
			now = time.time()
			if now-GROUPCHATS[groupchat][nick]['joined']>1:
				if item['role']=='participant':
					order_stats[groupchat][jid]['devoice']['cnd']=0
				lastprs=order_stats[groupchat][jid]['prstime']['status']
				order_stats[groupchat][jid]['prstime']['status']=now

				if GCHCFGS[groupchat]['filt']['presence']==1:
					if now-lastprs>300:
						order_stats[groupchat][jid]['prs']['status']=0
					else:
						order_stats[groupchat][jid]['prs']['status']+=1
						if order_stats[groupchat][jid]['prs']['status']>5:
							order_stats[groupchat][jid]['prs']['status']=0
							order_kick(groupchat, nick, u'presence flood!')
							return

				if GCHCFGS[groupchat]['filt']['obscene']==1:		
					if order_check_obscene(nick, groupchat, jid, nick):	return
				
				if GCHCFGS[groupchat]['filt']['prsstlen']==1 and stmsg:
					if order_check_len_flood(200, nick, groupchat, jid, nick):	return

def handler_order_leave(groupchat, nick, reason, code):
	jid=get_true_jid(groupchat+'/'+nick)
	if nick in GROUPCHATS[groupchat] and user_level(groupchat+'/'+nick,groupchat)<11:
		if groupchat in order_stats and jid in order_stats[groupchat]:
			if GCHCFGS[groupchat]['filt']['presence']==1:
				if reason=='Replaced by new connection':
					return
				if code:
					if code=='307': # kick
						order_stats[groupchat][jid]['kicks']+=1
						return
					elif code=='301': # ban
						del order_stats[groupchat][jid]
						return
					elif code=='407': # members-only
						return
			if GCHCFGS[groupchat]['filt']['fly']['cond']==1:
				now = time.time()
				lastprs=order_stats[groupchat][jid]['prstime']['fly']
				order_stats[groupchat][jid]['prstime']['fly']=time.time()
				if now-lastprs<=70:
					order_stats[groupchat][jid]['prs']['fly']+=1
				else:
					order_stats[groupchat][jid]['prs']['fly']=0

######################################################################################################################

def handler_order_filt(type, source, parameters):
	if parameters:
		parameters=parameters.split()
		if len(parameters)<2:
			reply(type,source,u'invalid syntax')
			return
		if GCHCFGS[source[1]].has_key('filt'):
			if parameters[0]=='time':
				if parameters[1]=='0':
					reply(type,source,u'filt time has been disabled')
					GCHCFGS[source[1]]['filt']['time']=0
				elif parameters[1]=='1':
					reply(type,source,u'filt time has been enabled')
					GCHCFGS[source[1]]['filt']['time']=1
				else:
					reply(type,source,u'invalid syntax')
			elif parameters[0]=='presence':
				if parameters[1]=='0':
					reply(type,source,u'filt presence has been disabled')
					GCHCFGS[source[1]]['filt']['presence']=0
				elif parameters[1]=='1':
					reply(type,source,u'filt presence has been enabled')
					GCHCFGS[source[1]]['filt']['presence']=1
				else:
					reply(type,source,u'invalid syntax')
			elif parameters[0]=='len':
				if parameters[1]=='0':
					reply(type,source,u'filt len has been disabled')
					GCHCFGS[source[1]]['filt']['len']=0
				elif parameters[1]=='1':
					reply(type,source,u'filt len has been enabled')
					GCHCFGS[source[1]]['filt']['len']=1
				else:
					reply(type,source,u'invalid syntax')
			elif parameters[0]=='like':
				if parameters[1]=='0':
					reply(type,source,u'filt like has been disabled')
					GCHCFGS[source[1]]['filt']['like']=0
				elif parameters[1]=='1':
					reply(type,source,u'filt like has been enabled')
					GCHCFGS[source[1]]['filt']['like']=1
				else:
					reply(type,source,u'invalid syntax')
			elif parameters[0]=='caps':
				if parameters[1]=='0':
					reply(type,source,u'filt caps has been disabled')
					GCHCFGS[source[1]]['filt']['caps']=0
				elif parameters[1]=='1':
					reply(type,source,u'filt caps has been enabled')
					GCHCFGS[source[1]]['filt']['caps']=1
				else:
					reply(type,source,u'invalid syntax')	
			elif parameters[0]=='prsstlen':
				if parameters[1]=='0':
					reply(type,source,u'filt prsstlen has been disabled')
					GCHCFGS[source[1]]['filt']['prsstlen']=0
				elif parameters[1]=='1':
					reply(type,source,u'filt prsstlen has been enabled')
					GCHCFGS[source[1]]['filt']['prsstlen']=1
				else:
					reply(type,source,u'invalid syntax')
			elif parameters[0]=='obscene':
				if parameters[1]=='0':
					reply(type,source,u'filt obscene has been disabled')
					GCHCFGS[source[1]]['filt']['obscene']=0
				elif parameters[1]=='1':
					reply(type,source,u'filt obscene has been enabled')
					GCHCFGS[source[1]]['filt']['obscene']=1
				else:
					reply(type,source,u'invalid syntax')
			elif parameters[0]=='fly':
				if parameters[1]=='cnt':
					try:
						int(parameters[2])
					except:
						reply(type,source,u'invalid syntax')
					if int(parameters[2]) in xrange(0,121):
						reply(type,source,u'filt fly for '+parameters[2]+u' seconds')
						GCHCFGS[source[1]]['filt']['fly']['time']=int(parameters[2])	
					else:
						reply(type,source,u'no more than two minutes (120 seconds)')
				elif parameters[1]=='mode':
					if parameters[2] in ['kick','ban']:
						if parameters[2] == 'ban':
							reply(type,source,u'flying will be banned')
							GCHCFGS[source[1]]['filt']['fly']['mode']='ban'
						else:
							reply(type,source,u'flying will be kicked')
							GCHCFGS[source[1]]['filt']['fly']['mode']='kick'	
					else:
						reply(type,source,u'invalid syntax')		
				elif parameters[1]=='0':
					reply(type,source,u'filt fly has been disabled')
					GCHCFGS[source[1]]['filt']['fly']['cond']=0
				elif parameters[1]=='1':
					reply(type,source,u'filt fly has been enabled')
					GCHCFGS[source[1]]['filt']['fly']['cond']=1
				else:
					reply(type,source,u'invalid syntax')
			elif parameters[0]=='kicks':
				if parameters[1]=='cnt':
					try:
						int(parameters[2])
					except:
						reply(type,source,u'invalid syntax')
					if int(parameters[2]) in xrange(2,10):
						reply(type,source,u'autoban after '+parameters[2]+u' kicks')
						GCHCFGS[source[1]]['filt']['kicks']['cnt']=int(parameters[2])	
					else:
						reply(type,source,u'from 2 to 10 kicks')
				elif parameters[1]=='0':
					reply(type,source,u'filt kicks has been disabled')
					GCHCFGS[source[1]]['filt']['kicks']['cond']=0
				elif parameters[1]=='1':
					reply(type,source,u'filt kicks has been enabled')
					GCHCFGS[source[1]]['filt']['kicks']['cond']=1
				else:
					reply(type,source,u'invalid syntax')
			elif parameters[0]=='idle':
				if parameters[1]=='time':
					try:
						int(parameters[2])
					except:
						reply(type,source,u'invalid syntax')			
					reply(type,source,u'autokick idle for '+parameters[2]+u' seconds ('+timeElapsed(int(parameters[2]))+u')')
					GCHCFGS[source[1]]['filt']['idle']['time']=int(parameters[2])
				elif parameters[1]=='0':
					reply(type,source,u'filt idle has been disabled')
					GCHCFGS[source[1]]['filt']['idle']['cond']=0
				elif parameters[1]=='1':
					reply(type,source,u'filt idle has been enabled')
					GCHCFGS[source[1]]['filt']['idle']['cond']=1
			else:
				reply(type,source,u'invalid syntax')
				return					
			DBPATH='dynamic/'+source[1]+'/config.cfg'
			write_file(DBPATH, str(GCHCFGS[source[1]]))
		else:
			reply(type,source,u'something strange happened, report it to the admin of bot')
	else:
		rep,foff,fon=u'',[],[]
		time=GCHCFGS[source[1]]['filt']['time']
		prs=GCHCFGS[source[1]]['filt']['presence']
		flen=GCHCFGS[source[1]]['filt']['len']
		like=GCHCFGS[source[1]]['filt']['like']
		caps=GCHCFGS[source[1]]['filt']['caps']
		prsstlen=GCHCFGS[source[1]]['filt']['prsstlen']
		obscene=GCHCFGS[source[1]]['filt']['obscene']
		fly=GCHCFGS[source[1]]['filt']['fly']['cond']
		flytime=str(GCHCFGS[source[1]]['filt']['fly']['time'])
		flymode=GCHCFGS[source[1]]['filt']['fly']['mode']
		kicks=GCHCFGS[source[1]]['filt']['kicks']['cond']
		kickscnt=str(GCHCFGS[source[1]]['filt']['kicks']['cnt'])
		idle=GCHCFGS[source[1]]['filt']['idle']['cond']
		idletime=GCHCFGS[source[1]]['filt']['idle']['time']
		if time:
			fon.append(u'time is filter for fast messages')
		else:
			foff.append(u'filt time')
		if prs:
			fon.append(u'presence is for frequently change of status ')
		else:
			foff.append(u'filt presence')
		if flen:
			fon.append(u'len is filter for long messages (flood)')
		else:
			foff.append(u'filt len')
		if like:
			fon.append(u'like is filter for suspiciously of identical messages')
		else:
			foff.append(u'filt like')
		if caps:
			fon.append(u'caps is filter for capital letters')
		else:
			foff.append(u'filt caps')
		if prsstlen:
			fon.append(u'prsstlen is filter for long messages on status')
		else:
			foff.append(u'filt prsstlen')
		if obscene:
			fon.append(u'obscene is filter for censor of bahasa Indonesia')
		else:
			foff.append(u'filt obscene')
		if fly:
			fon.append(u'fly is filter for flying (mode '+flymode+u', timer '+flytime+u' seconds)')
		else:
			foff.append(u'filt fly')
		if kicks:
			fon.append(u'kicks is filter for autoban after '+kickscnt+u' kicks')
		else:
			foff.append(u'filt kicks')
		if idle:
			fon.append(u'idle is filter for silence autokick after '+str(idletime)+u' seconds ('+timeElapsed(idletime)+u')')
		else:
			foff.append(u'filt idle')
		fon=u', '.join(fon)
		foff=u', '.join(foff)
		if fon:
			rep+=u'ENABLE\n'+fon+u'\n\n'
		if foff:
			rep+=u'DISABLE\n'+foff
		reply(type,source,rep.strip())


def get_order_cfg(gch):
	if not 'filt' in GCHCFGS[gch]:
		GCHCFGS[gch]['filt']={}		
	for x in ['time','presence','len','like','caps','prsstlen','obscene','kicks','fly','excess','idle']:
		if x == 'excess':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={'cond':0, 'mode': 'kick'}
			continue		
		if x == 'kicks':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={'cond':1, 'cnt': 2}
			continue
		if x == 'fly':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={'cond':1, 'mode': 'ban', 'time': 60}
			continue
		if x == 'idle':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={'cond':0, 'time': 3600}
			continue
		if not x in GCHCFGS[gch]['filt']:
			GCHCFGS[gch]['filt'][x]=1

register_message_handler(handler_order_message)
register_join_handler(handler_order_join)
register_leave_handler(handler_order_leave)
register_presence_handler(handler_order_presence)
register_command_handler(handler_order_filt, 'filt', ['admin','muc','all'], 20, 'Enable or disable certain filters in a conference.\ntime is a filter of time\nlen is a filter of quantitative messages\npresence is a filter of presence\nlike is a filter of identical messages\ncaps is a filter of сaps (CAPITAL letters)\nprsstlen is a filter of long status messages\nobscene - filter of censor bahasa Indonesia\nfly is a filter of flying (frequent in/out in conference), it has two modes  kick or ban, timer 0 to 120 seconds\nkicks is autoban after N kicks, a parameter of cnt is an amount of kicks from 1 to 10\nidle is a filter of idle that kick kick for silence in conference after N seconds, N = setting time in seconds.', 'filt [filt] [mode] [status]', ['filt len 1', 'filt len 0','filt fly mode ban'])

register_stage1_init(get_order_cfg)
register_stage2_init(order_check_idle)
