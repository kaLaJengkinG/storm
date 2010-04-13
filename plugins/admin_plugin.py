#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  admin_plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def popups_check(gch):
	DBPATH='dynamic/'+gch+'/config.cfg'
	if GCHCFGS[gch].has_key('popups'):
		if GCHCFGS[gch]['popups'] == 1:
			return 1
		else:
			return 0
	else:
		GCHCFGS[gch]['popups']=1
		write_file(DBPATH,str(GCHCFGS[gch]))
		return 1
				
def handler_admin_join(type, source, parameters):
	if not source[1] in GROUPCHATS:
		source[2]=source[1].split('@')[0]
	if parameters:
		passw=''
		args = parameters.split()
		if not args[0].count('@') or not args[0].count('.')>=1:
			reply(type, source, u'read "help join"')
			return
		if len(args)>1:
			groupchat = args[0]
			passw = string.split(args[1], 'pass=', 1)
			if not passw[0]:
				reason = ' '.join(args[2:])
			else:
				reason = ' '.join(args[1:])
		else:
			groupchat = parameters
			reason = ''
		get_gch_cfg(groupchat)
		for process in STAGE1_INIT:
			with smph:
				INFO['thr'] += 1
				threading.Thread(None,process,'atjoin_init'+str(INFO['thr']),(groupchat,)).start()
		DBPATH='dynamic/'+groupchat+'/config.cfg'
		write_file(DBPATH, str(GCHCFGS[groupchat]))
		if passw:
			join_groupchat(groupchat, DEFAULT_NICK)
		else:
			join_groupchat(groupchat, DEFAULT_NICK, passw)
		MACROS.load(groupchat)
		reply(type, source, u'join to ' + groupchat)
#		if popups_check(groupchat):
#			if reason:
#				msg(groupchat, u'joined by '+source[2]+u' reason:\n'+reason)
#			else:
#				msg(groupchat, u'joined by '+source[2])
	else:
		reply(type, source, u'read "help join"')

def handler_admin_leave(type, source, parameters):
	if not source[1] in GROUPCHATS:
		source[2]=source[1].split('@')[0]
	args = parameters.split()
	if len(args)>1:
		level=int(user_level(source[1]+'/'+source[2], source[1]))
		if level<40 and args[0]!=source[1]:
			reply(type, source, u'not allowed')
			return
		reason = ' '.join(args[1:]).strip()
		if not GROUPCHATS.has_key(args[0]):
			reply(type, source, u'i am not there')
			return
		groupchat = args[0]
	elif len(args)==1:
		level=int(user_level(source[1]+'/'+source[2], source[1]))
		if level<40 and args[0]!=source[1]:
			reply(type, source, u'not allowed')
			return
		if not GROUPCHATS.has_key(args[0]):
			reply(type, source, u'i am not there')
			return
		reason = ''
		groupchat = args[0]
	else:
		if not source[1] in GROUPCHATS:
			reply(type, source, u'this command only possible in the conference')
			return
		groupchat = source[1]
		reason = ''
#	if popups_check(groupchat):
#		if reason:
#			msg(groupchat, u'leaved by '+source[2]+u' reason:\n'+reason)
#		else:
#			msg(groupchat, u'leaved by'+source[2])
	if reason:
		leave_groupchat(groupchat, u'leaved me by '+source[2]+u' reason:\n'+reason)
	else:
		leave_groupchat(groupchat,u'leaved me by '+source[2])
	reply(type, source, u'leaved ' + groupchat)


def handler_admin_msg(type, source, parameters):
	if not parameters:
		reply(type, source, u'read "help message"')
		return
	msg(string.split(parameters)[0], string.join(string.split(parameters)[1:]))
	reply(type, source, u'message sent')
	
def handler_glob_msg_help(type, source, parameters):
	total = '0'
	totalblock='0'
	if GROUPCHATS:
		gch=GROUPCHATS.keys()
		for x in gch:
			if popups_check(x):
				msg(x, u'News from '+source[2]+u':\n'+parameters+u'\nI remind that as usual all a help can be got writing a "help".\nAbout all of bugs, errors, suggestions and structural criticism, please to send me: write ".botadmin <text>", naturally without quotation marks.\nTHANKS FOR YOUR ATTENTION!')
				totalblock = int(totalblock) + 1
			total = int(total) + 1
		reply(type, source, 'message sent to '+str(totalblock)+' conference (from '+str(total)+')')
	else:
		reply(type, source, u'read "help hglobmsg"')
		
def handler_glob_msg(type, source, parameters):
	total = '0'
	totalblock='0'
	if parameters:
		if GROUPCHATS:
			gch=GROUPCHATS.keys()
			for x in gch:
				if popups_check(x):
					msg(x, u'News from '+source[2]+':\n'+parameters)
					totalblock = int(totalblock) + 1
				total = int(total) + 1
			reply(type, source, 'message sent to '+str(totalblock)+' conference (from '+str(total)+')')
	else:
		reply(type, source, u'read "help globmsg"')
	

def handler_admin_say(type, source, parameters):
	if parameters:
		args=parameters.split()[0]
		msg(source[1], parameters)
	else:
		reply(type, source, u'read "help say"')

def handler_admin_restart(type, source, parameters):
	if not source[1] in GROUPCHATS:
		source[2]=source[1].split('@')[0]
	if parameters:
		reason = parameters
	else:
		reason = ''
#	gch=[]
#	if GROUPCHATS:
#		gch=GROUPCHATS.keys()
#	if reason:
#		for x in gch:
#			if popups_check(x):
#				msg(x, u'restarted by '+source[2]+u' reason:\n'+reason)
#	else:
#		for x in gch:
#			if popups_check(x):
#				msg(x, u'restarted by '+source[2])
	prs=xmpp.Presence(typ='unavailable')
#	if reason:
#		prs.setStatus(source[2]+u': restarted me -> '+reason)
#	else:
#		prs.setStatus(source[2]+u': restarted me')
	JCON.send(prs)
	time.sleep(1)
	JCON.disconnect()

def handler_admin_exit(type, source, parameters):
	if not source[1] in GROUPCHATS:
		source[2]=source[1].split('@')[0]
	if parameters:
		reason = parameters
	else:
		reason = ''
#	gch=[]
#	if GROUPCHATS:
#		gch=GROUPCHATS.keys()
#	if reason:
#		for x in gch:
#			if popups_check(x):
#				msg(x, u'shut downed by '+source[2]+u' reason:\n'+reason)
#	else:
#		for x in gch:
#			if popups_check(x):
#				msg(x, u'shut downed by '+source[2])
	prs=xmpp.Presence(typ='unavailable')
#	if reason:
#		prs.setStatus(source[2]+u': shut me downed -> '+reason)
#	else:
#		prs.setStatus(source[2]+u': shut me downed')
	JCON.send(prs)
	time.sleep(2)
	os.abort()
	
def handler_popups_onoff(type, source, parameters):
	if not source[1] in GROUPCHATS:
		reply(type, source, u'this command only possible in conference')
		return
	if parameters:
		try:
			parameters=int(parameters.strip())
		except:
			reply(type,source,u'read "help popups"')
			return		
		DBPATH='dynamic/'+source[1]+'/config.cfg'
		if parameters==1:
			GCHCFGS[source[1]]['popups']=1
			reply(type,source,u'global notifications are turned on')
		else:
			GCHCFGS[source[1]]['popups']=0
			reply(type,source,u'global notifications are turned off')
		write_file(DBPATH,str(GCHCFGS[source[1]]))
	else:
		ison=GCHCFGS[source[1]]['popups']
		if ison==1:
			reply(type,source,u'global notifications are turned on here')
		else:
			reply(type,source,u'global notifications are turned off here')
			
def handler_botautoaway_onoff(type, source, parameters):
	if not source[1] in GROUPCHATS:
		reply(type, source, u'this command only possible in the conference')
		return
	if parameters:
		try:
			parameters=int(parameters.strip())
		except:
			reply(type,source,u'read "help autoaway"')
			return		
		DBPATH='dynamic/'+source[1]+'/config.cfg'
		if parameters==1:
			GCHCFGS[source[1]]['autoaway']=1
			reply(type,source,u'auto-status enabled')
		else:
			GCHCFGS[source[1]]['autoaway']=0
			reply(type,source,u'auto-status disabled')
		get_autoaway_state(source[1])
		write_file(DBPATH,str(GCHCFGS[source[1]]))
	else:
		ison=GCHCFGS[source[1]]['autoaway']
		if ison==1:
			reply(type,source,u'auto-status is enable here')
		else:
			reply(type,source,u'auto-status is disable here')	
	
"""def handler_changebotstatus(type, source, parameters):
	if parameters:
		args,show,status=parameters.split(' ',1),'',''
		if args[0] in ['away','xa','dnd','chat']:
			show=args[0]
		else:
			show=None
			status=parameters
		if not status:
			try:
				status=args[1]
			except:
				status=None
		change_bot_status(source[1],status,show,0)
		GCHCFGS[gch]['status']={'status': status, 'show': show}
	else:
		stmsg=GROUPCHATS[source[1]][get_bot_nick(source[1])]['stmsg']
		status=GROUPCHATS[source[1]][get_bot_nick(source[1])]['status']
		if stmsg:
			reply(type,source, u'I am now '+status+u' ('+stmsg+u')')
		else:
			reply(type,source, u'I am now '+status)"""
			
def get_autoaway_state(gch):
	if not 'autoaway' in GCHCFGS[gch]:
		GCHCFGS[gch]['autoaway']=1
	if GCHCFGS[gch]['autoaway']:
		LAST['gch'][gch]['autoaway']=0
		LAST['gch'][gch]['thr']=None
		
"""def set_default_gch_status(gch):
	if isinstance(GCHCFGS[gch].get('status'), str): #temp workaround
		GCHCFGS[gch]['status']={'status': u'write "help" and follow the instructions to understand how to work with me', 'show': u''}
	elif not isinstance(GCHCFGS[gch].get('status'), dict):
		GCHCFGS[gch]['status']={'status': u'write "help" and follow the instructions to understand how to work with me', 'show': u''}"""


register_command_handler(handler_admin_join, 'join', ['superadmin','muc','all'], 100, 'Join conference, if there is a password write that password right after the name of conference.', 'join <conference> [pass=12345] [reason]', ['join tangerang@conference.jabberid.org', 'join tangerang@conference.jabberid.org *VICTORY*', 'join tangerang@conference.jabberid.org pass=12345 *VICTORY*'])
register_command_handler(handler_admin_leave, 'leave', ['admin','muc','all'], 30, 'Leave conference.', 'leave <conference> [reason]', ['leave tangerang@conference.jabberid.org sleep', 'leave sleep','leave'])
register_command_handler(handler_admin_msg, 'message', ['admin','muc','all'], 40, 'Send message on behalf of bot to a certain JID.', 'message <jid> <message>', ['message guy@jabberid.org how are you?'])
register_command_handler(handler_admin_say, 'say', ['admin','muc','all'], 20, 'Talk through bot.', 'say <message>', ['say *HI* peoples'])
register_command_handler(handler_admin_restart, 'restart', ['superadmin','all'], 100, 'Restart bot.', 'restart [reason]', ['restart','restart refreshing'])
register_command_handler(handler_admin_exit, 'exit', ['superadmin','all'], 100, 'Shutdown bot.', 'exit [reason]', ['exit','exit fixing bug'])
register_command_handler(handler_glob_msg, 'globmsg', ['superadmin','muc','all'], 100, 'Send news/message to all conference, where the bot exist.', 'globmsg [message]', ['globmsg hi all!'])
register_command_handler(handler_glob_msg_help, 'hglobmsg', ['superadmin','muc','all'], 100, 'Send news/message to all conference, where the bot exist.', 'globmsg [message]', ['globmsg hi all!'])
register_command_handler(handler_popups_onoff, 'popups', ['admin','muc','all'], 30, 'Off (0) On (1) message about join/leaves, restarts/off, and also global news for certain conf. Without a parameter the bot will based on current status.', 'popups [conf] [1|0]', ['popups tangerang@conference.jabberid.org 1','popups tangerang@conference.jabberid.org 0','popups'])
#register_command_handler(handler_botautoaway_onoff, 'autoaway', ['admin','muc','all'], 30, 'Off (0) on (1) auto-status away due to abscence of commands within 10 minutes, without an option it will show current status.', 'autoaway [1|0]', ['autoaway 1','autoaway'])
#register_command_handler(handler_changebotstatus, 'stch', ['admin','muc','all'], 20, 'Change bot status according to the list:\naway - absent,\nxa - extended away,\ndnd - dont disturb,\nchat - free for chat,\nand also status message (if it given).', 'stch [status] [message]', ['stch away','stch away go to work'])

register_stage1_init(get_autoaway_state)
#register_stage1_init(set_default_gch_status)
