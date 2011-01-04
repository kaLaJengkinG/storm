#! /usr/bin/env python
# -*- coding: utf-8 -*-

#  Talisman core
#  pybot.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Modifications Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Parts of code Copyright © Boris Kotov <admin@avoozl.ru>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

from __future__ import with_statement
import sys
import os
os.chdir(os.path.dirname(sys.argv[0]))

sys.path.insert(1, 'modules')

import xmpp
import time
import threading
import random
import types
import traceback
import codecs
import macros

threading.stack_size(65536)

################################################################################
GENERAL_CONFIG_FILE = 'config.txt'

fp = open(GENERAL_CONFIG_FILE, 'r')
GENERAL_CONFIG = eval(fp.read())
fp.close()

CONNECT_SERVER = GENERAL_CONFIG['CONNECT_SERVER']
PORT = GENERAL_CONFIG['PORT']
JID = GENERAL_CONFIG['JID']
PASSWORD = GENERAL_CONFIG['PASSWORD']
RESOURCE = GENERAL_CONFIG['RESOURCE']

GROUPCHAT_CACHE_FILE = 'dynamic/chatrooms.list'
GROUPCHAT_STATUS_CACHE_FILE='dynamic/statuses.list'
GLOBACCESS_FILE = 'dynamic/globaccess.cfg'
ACCBYCONF_FILE = 'dynamic/accbyconf.cfg'
PLUGIN_DIR = 'plugins'

DEFAULT_NICK = GENERAL_CONFIG['DEFAULT_NICK']
ADMINS = GENERAL_CONFIG['ADMINS']
ADMIN_PASSWORD = GENERAL_CONFIG['ADMIN_PASSWORD']

AUTO_RESTART = GENERAL_CONFIG['AUTO_RESTART']

PUBLIC_LOG_DIR = GENERAL_CONFIG['PUBLIC_LOG_DIR']
PRIVATE_LOG_DIR = GENERAL_CONFIG['PRIVATE_LOG_DIR']

ROLES={'none':0, 'visitor':0, 'participant':10, 'moderator':15}
AFFILIATIONS={'none':0, 'member':1, 'admin':5, 'owner':15}

LAST = {'c':'', 't':0, 'gch':{}}
INFO = {'start': 0, 'msg': 0, 'prs':0, 'iq':0, 'cmd':0, 'thr':0}

SVN_REPOS = 'http://storm-bot.googlecode.com/svn/trunk'

BOT_VER = {'rev': 19, 'botver': {'name': 'stOrm', 'ver': 'ver. 1.02-%s [antiflood]', 'os': ''}}
################################################################################

COMMANDS = {}
MACROS = macros.Macros()

GROUPCHATS = {}

############ lists handlers ############
MESSAGE_HANDLERS = []
OUTGOING_MESSAGE_HANDLERS = []
JOIN_HANDLERS = []
LEAVE_HANDLERS = []
IQ_HANDLERS = []
PRESENCE_HANDLERS = []
STAGE0_INIT =[]
STAGE1_INIT =[]
STAGE2_INIT =[]
########################

COMMAND_HANDLERS = {}

GLOBACCESS = {}
ACCBYCONF = {}
ACCBYCONFFILE = {}

COMMOFF = {}
GREETZ={}

GCHCFGS={}

JCON = None

smph = threading.BoundedSemaphore(value=30)
mtx = threading.Lock()
wsmph = threading.BoundedSemaphore(value=1)
################################################################################

def initialize_file(filename, data=''):
	if not os.access(filename, os.F_OK):
		fp = file(filename, 'w')
		if data:
			fp.write(data)
		fp.close()

def read_file(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data
	
def write_file_gag(filename, data):
	mtx.acquire()
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()
	mtx.release()
	
def write_file(filename, data):
	with wsmph:
		write_file_gag(filename, data)

def check_file(gch='',file=''):
	pth,pthf='',''
	if gch:
		pthf='dynamic/'+gch+'/'+file
		pth='dynamic/'+gch
	else:
		pthf='dynamic/'+file
		pth='dynamic'
	if os.path.exists(pthf):
		return 1
	else:
		try:
			if not os.path.exists(pth):
				os.mkdir(pth,0755)
			if os.access(pthf, os.F_OK):
				fp = file(pthf, 'w')
			else:
				fp = open(pthf, 'w')
			fp.write('{}')
			fp.close()
			return 1
		except:
			return 0

################################################################################

def register_message_handler(instance):
	MESSAGE_HANDLERS.append(instance)
def register_outgoing_message_handler(instance):
	OUTGOING_MESSAGE_HANDLERS.append(instance)
def register_join_handler(instance):
	JOIN_HANDLERS.append(instance)
def register_leave_handler(instance):
	LEAVE_HANDLERS.append(instance)
def register_iq_handler(instance):
	IQ_HANDLERS.append(instance)
def register_presence_handler(instance):
	PRESENCE_HANDLERS.append(instance)
def register_stage0_init(instance):
	STAGE0_INIT.append(instance)
def register_stage1_init(instance):
	STAGE1_INIT.append(instance)
def register_stage2_init(instance):
	STAGE2_INIT.append(instance)

def register_command_handler(instance, command, category=[], access=0, desc='', syntax='', examples=[]):
	command = command.decode('utf-8')
	COMMAND_HANDLERS[command] = instance
	COMMANDS[command] = {'category': category, 'access': access, 'desc': desc, 'syntax': syntax, 'examples': examples}

def call_message_handlers(type, source, body):
	for handler in MESSAGE_HANDLERS:
		with smph:
			INFO['thr'] += 1
			threading.Thread(None,handler,'inmsg'+str(INFO['thr']),(type, source, body,)).start()
def call_outgoing_message_handlers(target, body, obody):
	for handler in OUTGOING_MESSAGE_HANDLERS:
		with smph:
			INFO['thr'] += 1
			threading.Thread(None,handler,'outmsg'+str(INFO['thr']),(target, body, obody,)).start()
def call_join_handlers(groupchat, nick, afl, role):
	for handler in JOIN_HANDLERS:
		with smph:
			INFO['thr'] += 1
			threading.Thread(None,handler,'join'+str(INFO['thr']),(groupchat, nick, afl, role,)).start()
def call_leave_handlers(groupchat, nick, reason, code):
	for handler in LEAVE_HANDLERS:
		with smph:
			INFO['thr'] += 1
			threading.Thread(None,handler,'leave'+str(INFO['thr']),(groupchat, nick, reason, code,)).start()
def call_iq_handlers(iq):
	for handler in IQ_HANDLERS:
		with smph:
			INFO['thr'] += 1
			threading.Thread(None,handler,'iq'+str(INFO['thr']),(iq,)).start()		
def call_presence_handlers(prs):
	for handler in PRESENCE_HANDLERS:
		with smph:
			INFO['thr'] += 1
			threading.Thread(None,handler,'prs'+str(INFO['thr']),(prs,)).start()				

def call_command_handlers(command, type, source, parameters, callee):
	real_access = MACROS.get_access(callee, source[1])
	if real_access < 0:
		real_access = COMMANDS[command]['access']
	if COMMAND_HANDLERS.has_key(command):
		if has_access(source, real_access, source[1]):
			with smph:
				INFO['thr'] += 1
				threading.Thread(None,COMMAND_HANDLERS[command],'command'+str(INFO['thr']),(type, source, parameters,)).start()		
		else:
			reply(type, source, u'insufficient privileges')

################################################################################

def find_plugins():
	print '\nLOADING PLUGINS'
	valid_plugins = []
	invalid_plugins = []
	possibilities = os.listdir('plugins')
	for possibility in possibilities:
		if possibility[-3:].lower() == '.py':
			try:
				fp = file(PLUGIN_DIR + '/' + possibility)
				data = fp.read(23)
				if data == '#===istalismanplugin===':
					valid_plugins.append(possibility)
				else:
					invalid_plugins.append(possibility)
			except:
				pass
	if invalid_plugins:
		print '\nfailed to load',len(invalid_plugins),'plug-ins:'
		invalid_plugins.sort()
		invp=', '.join(invalid_plugins)
		print invp
		print 'plugins header is not corresponding\n'
	else:
		print '\nthere are not unloadable plug-ins'
	return valid_plugins
	
################################################################################

def load_plugins():
	plugins = find_plugins()
	for plugin in plugins:
		try:
			fp = file(PLUGIN_DIR + '/' + plugin)
			exec fp in globals()
			fp.close()
		except:
			raise
	plugins.sort()
	print '\nloaded',len(plugins),'plug-ins:'
	loaded=', '.join(plugins)
	print loaded,'\n'
				
def get_gch_cfg(gch):
	cfgfile='dynamic/'+gch+'/config.cfg'
	if not check_file(gch,'config.cfg'):
		print 'unable to create config file for new groupchat!'
		raise
	try:
		cfg = eval(read_file(cfgfile))
		GCHCFGS[gch]=cfg
		LAST['gch'][gch]={}
	except:
		pass
	
def upkeep():
	tmr=threading.Timer(60, upkeep)
	tmr.start()
	sys.exc_clear()
	if os.name == 'nt':
		try:
			import msvcrt
			msvcrt.heapmin()
		except:
			pass
	import gc
	gc.collect()
		
################################################################################

def get_true_jid(jid):
	true_jid = ''
	if type(jid) is types.ListType:
		jid = jid[0]
	if type(jid) is types.InstanceType:
		jid = unicode(jid)
	stripped_jid = string.split(jid, '/', 1)[0]
	resource = ''
	if len(string.split(jid, '/', 1)) == 2:
		resource = string.split(jid, '/', 1)[1]
	if GROUPCHATS.has_key(stripped_jid):
		if GROUPCHATS[stripped_jid].has_key(resource):
			true_jid = string.split(unicode(GROUPCHATS[stripped_jid][resource]['jid']), '/', 1)[0]
		else:
			true_jid = stripped_jid
	else:
		true_jid = stripped_jid
	return true_jid

def get_bot_nick(groupchat):
	if check_file(file='chatrooms.list'):
		gchdb = eval(read_file(GROUPCHAT_CACHE_FILE))
		if gchdb.has_key(groupchat) and gchdb[groupchat]['nick']:
			return gchdb[groupchat]['nick']
		else:
			return DEFAULT_NICK
	else:
		print 'Error adding groupchat to groupchats list file!'
		
def get_gch_info(gch, info):
	if check_file(file='chatrooms.list'):
		gchdb = eval(read_file(GROUPCHAT_CACHE_FILE))
		if gchdb.has_key(gch):	return gchdb[gch].get(info)
		else:	return None
	else:
		print 'Error adding groupchat to groupchats list file!'	

def add_gch(groupchat=None, nick=None, passw=None):
	if check_file(file='chatrooms.list'):
		gchdb = eval(read_file(GROUPCHAT_CACHE_FILE))
		if not groupchat in gchdb:
			gchdb[groupchat] = groupchat
			gchdb[groupchat] = {}
			gchdb[groupchat]['nick'] = nick
			gchdb[groupchat]['passw'] = passw
		else:
			if nick and groupchat and passw:
				gchdb[groupchat]['nick'] = nick
				gchdb[groupchat]['passw'] = passw
			elif nick and groupchat:
				gchdb[groupchat]['nick'] = nick
			elif groupchat:
				del gchdb[groupchat]
			elif passw:
				gchdb[groupchat]['passw'] = passw
			else:
				return 0
		write_file(GROUPCHAT_CACHE_FILE, str(gchdb))
		return 1
	else:
		print 'Error adding groupchat to groupchats list file!'

def timeElapsed(time):
	minutes, seconds = divmod(time, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	months, days = divmod(days, 30)
	rep = u'%d sec.' % (round(seconds))
	if time>60: rep = u'%d min. %s' % (minutes, rep)
	if time>3600: rep = u'%d h %s' % (hours, rep)
	if time>86400: rep = u'%d d %s' % (days, rep)
	if time>2592000: rep = u'%d m %s' % (months, rep)
	return rep
	
def change_bot_status(gch,status,show,auto=0):
	prs=xmpp.protocol.Presence(gch+'/'+get_bot_nick(gch))
	if status:
		prs.setStatus(status)
	if show:
		prs.setShow(show)
	prs.setTag('c', namespace=xmpp.NS_CAPS, attrs={'node':SVN_REPOS,'ver':BOT_VER['botver']['ver'] %(BOT_VER['rev'])})
	JCON.send(prs)
	if auto:
		LAST['gch'][gch]['autoaway']=0
	else:
		LAST['gch'][gch]['autoaway']=1

################################################################################

def change_access_temp(gch, source, level=0):
	global ACCBYCONF
	jid = get_true_jid(source)
	try:
		level = int(level)
	except:
		level = 0
	if not ACCBYCONF.has_key(gch):
		ACCBYCONF[gch] = gch
		ACCBYCONF[gch] = {}
	if not ACCBYCONF[gch].has_key(jid):
		ACCBYCONF[gch][jid]=jid
	ACCBYCONF[gch][jid]=level

def change_access_perm(gch, source, level=None):
	global ACCBYCONF
	jid = get_true_jid(source)
	try:
		level = int(level)
	except:
		pass
	temp_access = eval(read_file(ACCBYCONF_FILE))
	if not temp_access.has_key(gch):
		temp_access[gch] = gch
		temp_access[gch] = {}
	if not temp_access[gch].has_key(jid):
		temp_access[gch][jid]=jid
	if level:
		temp_access[gch][jid]=level
	else:
		del temp_access[gch][jid]
	write_file(ACCBYCONF_FILE, str(temp_access))
	if not ACCBYCONF.has_key(gch):
		ACCBYCONF[gch] = gch
		ACCBYCONF[gch] = {}
	if not ACCBYCONF[gch].has_key(jid):
		ACCBYCONF[gch][jid]=jid
	if level:
		ACCBYCONF[gch][jid]=level
	else:
		del ACCBYCONF[gch][jid]
	get_access_levels()

def change_access_perm_glob(source, level=0):
	global GLOBACCESS
	jid = get_true_jid(source)
	temp_access = eval(read_file(GLOBACCESS_FILE))
	if level:
		temp_access[jid] = level
	else:
		del temp_access[jid]
	write_file(GLOBACCESS_FILE, str(temp_access))
	get_access_levels()
	
def change_access_temp_glob(source, level=0):
	global GLOBACCESS
	jid = get_true_jid(source)
	if level:
		GLOBACCESS[jid] = level
	else:
		del GLOBACCESS[jid]

def user_level(source, gch):
	global ACCBYCONF
	global GLOBACCESS
	global ACCBYCONFFILE
	jid = get_true_jid(source)
	if GLOBACCESS.has_key(jid):
		return GLOBACCESS[jid]
	if ACCBYCONFFILE.has_key(gch):
		if ACCBYCONFFILE[gch].has_key(jid):
			return ACCBYCONFFILE[gch][jid]
	if ACCBYCONF.has_key(gch):
		if ACCBYCONF[gch].has_key(jid):
			return ACCBYCONF[gch][jid]
	return 0

def has_access(source, level, gch):
	jid = get_true_jid(source)
	if user_level(jid,gch) >= int(level):
		return 1
	return 0

################################################################################
"""
def join_groupchat(groupchat=None, nick=DEFAULT_NICK, passw=None):
	if not groupchat in GROUPCHATS:
		GROUPCHATS[groupchat] = {}
	if check_file(groupchat,'macros.txt'):
		pass
	else:
		print 'IO error when creating macros.txt for ',groupchat
		
	add_gch(groupchat, nick, passw)

	prs=xmpp.protocol.Presence(groupchat+'/'+nick)
	prs.setStatus(GCHCFGS[groupchat]['status']['status'])
	prs.setShow(GCHCFGS[groupchat]['status']['show'])
	pres=prs.setTag('x',namespace=xmpp.NS_MUC)
	pres.addChild('history',{'maxchars':'0'})
	if passw:
		pres.setTagData('password', passw)
	JCON.send(prs)
"""

def join_groupchat(groupchat=None, nick=DEFAULT_NICK, passw=None):
        confstatus=[u'chat',u'Write "commands all" without quotation mark to get list of commands!']
        if check_file(file='statuses.list'):
          groupchatstatus = eval(read_file(GROUPCHAT_STATUS_CACHE_FILE))
          if groupchatstatus.has_key(groupchat):
            if groupchatstatus[groupchat]:
              confstatusr=groupchatstatus[groupchat]
              confstatus[0]=confstatusr[0]
              if confstatusr[1]:
                confstatus[1]=confstatusr[1]
        else:
          print 'Error: unable to create chatrooms status list file!'

        prs=xmpp.protocol.Presence(groupchat+'/'+nick)

      #Ставим статус и подпись | put the status and status message
        prs.setShow(confstatus[0])
        prs.setStatus(confstatus[1])
        pres=prs.setTag('x',namespace=xmpp.NS_MUC)
        prs.setTag('c', namespace=xmpp.NS_CAPS, attrs={'node':SVN_REPOS,'ver':BOT_VER['botver']['ver'] %(BOT_VER['rev'])})
        pres.addChild('history',{'maxchars':'0','maxstanzas':'0'})
        if passw:
                pres.setTagData('password', passw)
        JCON.send(prs)
        if not groupchat in GROUPCHATS:
                GROUPCHATS[groupchat] = {}
        if check_file(groupchat,'macros.txt'):
                pass
        else:
                msg(groupchat, u'Perhatian!!! Macro local base tidak dapat dibuat! Terjadi kesalahan, Harap segera laporkan kepada Admin-bot!')

        add_gch(groupchat, nick, passw)

def leave_groupchat(groupchat,status=''):
	prs=xmpp.Presence(groupchat, 'unavailable')
	if status:
		prs.setStatus(status)
	JCON.send(prs)
	if GROUPCHATS.has_key(groupchat):
		del GROUPCHATS[groupchat]
		add_gch(groupchat)
		if 'thr' in LAST['gch'][groupchat]:
			if not LAST['gch'][groupchat]['thr'] is None: LAST['gch'][groupchat]['thr'].cancel()

def msg(target, body):
	if not isinstance(body, unicode):
		body = body.decode('utf8', 'replace')
	obody=body
	if time.localtime()[1]==4 and time.localtime()[2]==1:
		body=remix_string(body)
	msg = xmpp.Message(target)
	if GROUPCHATS.has_key(target):
		msg.setType('groupchat')
		if len(body)>1000:
			body=body[:1000]+u' >>>>'
		msg.setBody(body.strip())
	else:
		msg.setType('chat')
		msg.setBody(body.strip())
	JCON.send(msg)
	call_outgoing_message_handlers(target, body, obody)

def reply(ltype, source, body):
	if not isinstance(body, unicode):
		body = body.decode('utf8', 'replace')
	if source[1] in GCHCFGS.keys() and GCHCFGS[source[1]]['afools']==1:
		if random.randrange(0,20) == random.randrange(0,20):
			body = random.choice(eval(read_file('static/delirium.txt'))['afools'])
	if ltype == 'public':
		msg(source[1], source[2] + ': ' + body)
	elif ltype == 'private':
		msg(source[0], body)

def isadmin(jid):
	if type(jid) is types.ListType:
		jid = jid[0]
	jid = str(jid)
	stripped_jid = string.split(jid, '/', 1)[0]
	resource = ''
	if len(string.split(jid, '/', 1)) == 2:
		resource = string.split(jid, '/', 1)[1]
	if stripped_jid in ADMINS:
		return 1
	elif GROUPCHATS.has_key(stripped_jid):
		if GROUPCHATS[stripped_jid].has_key(resource):
			if string.split(str(GROUPCHATS[stripped_jid][resource]['jid']), '/', 1)[0] in ADMINS:
				return 1
	return 0

################################################################################
def findPresenceItem(node):
	for p in [x.getTag('item') for x in node.getTags('x',namespace=xmpp.NS_MUC_USER)]:
		if p != None:
			return p
	return None

def messageHnd(con, msg):
	msgtype = msg.getType()
	fromjid = msg.getFrom()
	INFO['msg'] += 1
#	if fromjid.getStripped() not in GROUPCHATS and fromjid.getStripped() not in ADMINS:
#		return
	if user_level(fromjid,fromjid.getStripped())==-100:
		return
	if msg.timestamp:
		return
	body = msg.getBody()
	if body:
		body=body.strip()
	if not body:
		return
	if len(body)>7000:
		body=body[:7000]+u' >>>>'	
	if msgtype == 'groupchat':
		mtype='public'
		if GROUPCHATS.has_key(fromjid.getStripped()) and GROUPCHATS[fromjid.getStripped()].has_key(fromjid.getResource()):
			GROUPCHATS[fromjid.getStripped()][fromjid.getResource()]['idle'] = time.time()	
	elif msgtype == 'error':
		if msg.getErrorCode()=='500':
			time.sleep(0.6)
			JCON.send(xmpp.Message(fromjid, body, 'groupchat'))
		elif msg.getErrorCode()=='406':
			join_groupchat(fromjid.getStripped(), DEFAULT_NICK)
			time.sleep(0.6)
			JCON.send(xmpp.Message(fromjid, body, 'groupchat'))			
		return
	else:
		mtype='private'
	call_message_handlers(mtype, [fromjid, fromjid.getStripped(), fromjid.getResource()], body)
	
	bot_nick = get_bot_nick(fromjid.getStripped())
	if bot_nick == fromjid.getResource():
		return
	command,parameters,cbody,rcmd = '','','',''
	for x in [bot_nick+x for x in [':',',','>']]:
		body=body.replace(x,'')
	body=body.strip()
	if not body:
		return
	rcmd = body.split()[0].lower()
	if fromjid.getStripped() in COMMOFF and rcmd in COMMOFF[fromjid.getStripped()]:
		return
	cbody = MACROS.expand(body, [fromjid, fromjid.getStripped(), fromjid.getResource()])
	command=cbody.split()[0].lower()
	if cbody.count(' '):
		parameters = cbody[(cbody.find(' ') + 1):].strip()
	if command in COMMANDS:
		if fromjid.getStripped() in COMMOFF and command in COMMOFF[fromjid.getStripped()]:
			return
		else:
			if fromjid.getStripped() in GROUPCHATS:			
				if GCHCFGS[fromjid.getStripped()]['autoaway']==1:
					if LAST['gch'][fromjid.getStripped()]['autoaway']==1:
						change_bot_status(fromjid.getStripped(), GCHCFGS[fromjid.getStripped()]['status']['status'], GCHCFGS[fromjid.getStripped()]['status']['show'],)
			call_command_handlers(command, mtype, [fromjid, fromjid.getStripped(), fromjid.getResource()], unicode(parameters), rcmd)
			INFO['cmd'] += 1
			LAST['t'] = time.time()
			LAST['c'] = command
			if fromjid.getStripped() in GROUPCHATS:		
				if GCHCFGS[fromjid.getStripped()]['autoaway']==1:
					if LAST['gch'][fromjid.getStripped()]['thr']:
						LAST['gch'][fromjid.getStripped()]['thr'].cancel()
					LAST['gch'][fromjid.getStripped()]['thr']=threading.Timer(600,change_bot_status,(fromjid.getStripped(), u'i do nothing till '+time.strftime('%d.%m.%Y@%H:%M:%S GMT', time.gmtime()), 'away',1))
					LAST['gch'][fromjid.getStripped()]['thr'].start()

def presenceHnd(con, prs):
	fromjid = prs.getFrom()
	if user_level(fromjid,fromjid.getStripped())==-100:
		return
	ptype = prs.getType()
	groupchat = fromjid.getStripped()
	nick = fromjid.getResource()
	item = findPresenceItem(prs)
	INFO['prs'] += 1
	
	if ptype == 'subscribe':
		JCON.send(xmpp.protocol.Presence(to=fromjid, typ='subscribed'))
	elif ptype == 'unsubscribe':
		JCON.send(xmpp.protocol.Presence(to=fromjid, typ='unsubscribed'))

	if groupchat in GROUPCHATS:
		if ptype == 'unavailable':
			jid = item['jid']
			scode = prs.getStatusCode()
			reason = prs.getStatus()
			if scode == '303':
				newnick = prs.getNick()
				GROUPCHATS[groupchat][newnick] = {'jid': jid, 'idle': time.time(), 'joined': GROUPCHATS[groupchat][nick]['joined'], 'ishere': 1}
				for x in ['idle','status','stmsg']:
					try:
						del GROUPCHATS[groupchat][nick][x]
						if GROUPCHATS[groupchat][nick]['ishere']==1:
							GROUPCHATS[groupchat][nick]['ishere']=0
					except:
						pass
			else:
				for x in ['idle','status','stmsg','joined']:
					try:
						del GROUPCHATS[groupchat][nick][x]
						if GROUPCHATS[groupchat][nick]['ishere']==1:
							GROUPCHATS[groupchat][nick]['ishere']=0
					except:
						pass
				call_leave_handlers(groupchat, nick, reason, scode)
		elif ptype == 'available' or ptype == None:
			jid = item['jid']
			afl=prs.getAffiliation()
			role=prs.getRole()
			if not jid:
				jid=fromjid
#				time.sleep(2)
#				msg(groupchat, u'my functionality to a full degree without rights for administrator is impossible (exit)')
#				time.sleep(1)
#				leave_groupchat(groupchat, u'leaving due to lack of role administrator  %)')        
#				return
#			else:
			if nick in GROUPCHATS[groupchat] and GROUPCHATS[groupchat][nick]['jid']==jid and GROUPCHATS[groupchat][nick]['ishere']==1:
				pass
			else:
				GROUPCHATS[groupchat][nick] = {'jid': jid, 'idle': time.time(), 'joined': time.time(), 'ishere': 1, 'status': '', 'stmsg': ''}
				if role=='moderator' or user_level(jid,groupchat)>=15:
					GROUPCHATS[groupchat][nick]['ismoder'] = 1
				else:
					GROUPCHATS[groupchat][nick]['ismoder'] = 0
				call_join_handlers(groupchat, nick, afl, role)
		elif ptype == 'error':
			ecode = prs.getErrorCode()
			if ecode:
				if ecode == '409':
					join_groupchat(groupchat, nick + '-')
				elif ecode == '404':
					del GROUPCHATS[groupchat]
				elif ecode in ['401','403','405',]:
					leave_groupchat(groupchat, u'got %s error code' % str(ecode))
				elif ecode == '503':
					threading.Timer(60, join_groupchat,(groupchat, nick)).start()
		else:
			pass
		call_presence_handlers(prs)

def iqHnd(con, iq):
	fromjid = iq.getFrom()
	if user_level(fromjid,fromjid.getStripped())==-100:
		return
	global JCON, BOT_VER
	if not iq.getType() == 'error':
		if iq.getTags('query', {}, xmpp.NS_VERSION):
			if not BOT_VER['botver']['os']:
				osver=''
				if os.name=='nt':
					osname=os.popen("ver")
					osver=osname.read().strip().decode('cp866')+'\n'
					osname.close()			
				else:
					osname=os.popen("uname -sr", 'r')
					osver=osname.read().strip()+'\n'
					osname.close()			
				pyver = sys.version
				BOT_VER['botver']['os'] = osver + ' ' + pyver
			result = iq.buildReply('result')
			query = result.getTag('query')
			query.setTagData('name', BOT_VER['botver']['name'])
			query.setTagData('version', BOT_VER['botver']['ver'] % str(BOT_VER['rev']))
			query.setTagData('os', BOT_VER['botver']['os'])
			JCON.send(result)
			raise xmpp.NodeProcessed
		elif iq.getTags('time', {}, 'urn:xmpp:time'):
			tzo=(lambda tup: tup[0]+"%02d:"%tup[1]+"%02d"%tup[2])((lambda t: tuple(['+' if t<0 else '-', abs(t)/3600, abs(t)/60%60]))(time.altzone if time.daylight else time.timezone))
			utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
			result = iq.buildReply('result')
			reply=result.addChild('time', {}, [], 'urn:xmpp:time')
			reply.setTagData('tzo', tzo)
			reply.setTagData('utc', utc)
			JCON.send(result)
			raise xmpp.NodeProcessed
		elif iq.getTags('query', {}, xmpp.NS_DISCO_INFO):
			items=[]
			ids=[]
			ids.append({'category':'client','type':'bot','name':'stOrm'})
			features=[xmpp.NS_DISCO_INFO,xmpp.NS_DISCO_ITEMS,xmpp.NS_MUC,'urn:xmpp:time','urn:xmpp:ping',xmpp.NS_VERSION,xmpp.NS_PRIVACY,xmpp.NS_ROSTER,xmpp.NS_VCARD,xmpp.NS_DATA,xmpp.NS_LAST,xmpp.NS_COMMANDS,'msglog','fullunicode',xmpp.NS_TIME]
			info={'ids':ids,'features':features}
			b=xmpp.browser.Browser()
			b.PlugIn(JCON)
			b.setDiscoHandler({'items':items,'info':info})
		elif iq.getTags('query', {}, xmpp.NS_LAST):
			last=time.time()-LAST['t']
			result = iq.buildReply('result')
			query = result.getTag('query')
			query.setAttr('seconds',int(last))
			query.setData(LAST['c'])
			JCON.send(result)
			raise xmpp.NodeProcessed
		elif iq.getTags('query', {}, xmpp.NS_TIME):
			timedisp=time.strftime("%a, %d %b %Y %H:%M:%S UTC", time.localtime())
			timetz=time.strftime("%Z", time.localtime())
			timeutc=time.strftime('%Y%m%dT%H:%M:%S', time.gmtime())
			result = xmpp.Iq('result')
			result.setTo(fromjid)
			result.setID(iq.getID())
			query = result.addChild('query', {}, [], 'jabber:iq:time')
			query.setTagData('utc', timeutc)
			query.setTagData('tz', timetz)
			query.setTagData('display', timedisp)
			JCON.send(result)
			raise xmpp.NodeProcessed
		elif iq.getTags('ping', {}, 'urn:xmpp:ping'):
			result = xmpp.Iq('result')
			result.setTo(iq.getFrom())
			result.setID(iq.getID())
			JCON.send(result)
			raise xmpp.NodeProcessed
	call_iq_handlers(iq)
	INFO['iq'] += 1

def dcHnd():
	print 'DISCONNECTED'
	if AUTO_RESTART:
		print 'WAITING FOR RESTART...'
		time.sleep(10)
		print 'RESTARTING'
		os.execl(sys.executable, sys.executable, sys.argv[0])
	else:
		sys.exit(0)

################################################################################

def start():
	try:
		(USERNAME, SERVER) = JID.split("/")[0].split("@")
	except:
		print 'Wrong, wrong JID %s' % JID
		os.abort()
	print '\n...---===STARTING BOT===---...\n'
	
	pid = str(os.getpid())
	
	try:
		fp = file('storm.pid', 'r')
		p = fp.read()
		fp.close()
		if p <> pid:
			os.kill(int(p), 3)
			time.sleep(1)
			try:
				os.kill(int(p), 9)
			except:
				pass
			sys.stdout.write('pid %s killed.. ' % (p, ))
	except: pass

	fp = file('storm.pid', 'w')
	fp.write(pid)
	fp.close()
	
	global JCON
	JCON = xmpp.Client(server=SERVER, port=PORT, debug=[])
	
	load_plugins()

	print 'Waiting For Connection...\n'

	con=JCON.connect(server=(CONNECT_SERVER, PORT), secure=0,use_srv=True)
	if not con:
		print 'COULDN\'T CONNECT\nSleep for 30 seconds'
		time.sleep(30)
		sys.exit(1)
	else:
		print 'Connection Established'

	print 'Using',JCON.isConnected()

	print '\nWaiting For Authentication...'

	auth=JCON.auth(USERNAME, PASSWORD, RESOURCE)
	if not auth:
		print 'Auth Error. Incorrect login/password?\nError: ', JCON.lastErr, JCON.lastErrCode
		sys.exit(1)
	else:
		print 'Logged In'
	if auth!='sasl':
		print 'Warning: unable to perform SASL auth. Old authentication method used!'
		
	for process in STAGE0_INIT:
		with smph:
			INFO['thr'] += 1
			threading.Thread(None,process,'stage0_init'+str(INFO['thr'])).start()

	JCON.RegisterHandler('message', messageHnd)
	JCON.RegisterHandler('presence', presenceHnd)
	JCON.RegisterHandler('iq', iqHnd)
	JCON.RegisterDisconnectHandler(dcHnd)
	JCON.UnregisterDisconnectHandler(JCON.DisconnectHandler)
	print 'Handlers Registered'
	
#	JCON.getRoster()
	JCON.sendInitPresence()

	if check_file(file='chatrooms.list'):
		groupchats = eval(read_file(GROUPCHAT_CACHE_FILE))
		print 'Entering %s Rooms' % str(len(groupchats))
		for groupchat in groupchats:
			get_gch_cfg(groupchat)
			MACROS.init(groupchat)
			for process in STAGE1_INIT:
				with smph:
					INFO['thr'] += 1
					threading.Thread(None,process,'stage1_init'+str(INFO['thr']),(groupchat,)).start()
			write_file('dynamic/'+groupchat+'/config.cfg', str(GCHCFGS[groupchat]))
			with smph:
				INFO['thr'] += 1
				threading.Thread(None,join_groupchat,'gch'+str(INFO['thr']),(groupchat,groupchats[groupchat]['nick'] if groupchats[groupchat]['nick'] else DEFAULT_NICK,groupchats[groupchat]['passw'])).start()
				if groupchat in LAST['gch'].keys():
					if GCHCFGS[groupchat]['autoaway']==1:
						LAST['gch'][groupchat]['thr']=threading.Timer(600,change_bot_status,(groupchat, u'i do nothing till '+time.strftime('%d.%m.%Y@%H:%M:%S GMT', time.gmtime()), 'away',1))
						LAST['gch'][groupchat]['thr'].start()
	else:
		print 'Error: unable to create chatrooms list file!'

#	load_plugins()
	

	print '\nOk, now i\'m ready to work :)\n'
		
	INFO['start'] = time.time()
	upkeep()
	for process in STAGE2_INIT:
		with smph:
			INFO['thr'] += 1
			threading.Thread(None,process,'stage2_init'+str(INFO['thr'])).start()
			
	while 1:
		JCON.Process(10)

if __name__ == "__main__":
	try:
		start()
	except KeyboardInterrupt:
		print '\nINTERUPT (Ctrl+C)'
		prs=xmpp.Presence(typ='unavailable')
		prs.setStatus(u'got Ctrl-C -> shutdown')
		JCON.send(prs)
		time.sleep(2)
		print 'DISCONNECTED'
		print '\n...---===BOT STOPPED===---...\n'
		sys.exit(0)
	except:
		if AUTO_RESTART:
#			if sys.exc_info()[0] is not SystemExit:
			traceback.print_exc()
			try:
				JCON.disconnected()
			except IOError:
				pass
			try:
				time.sleep(5)
			except KeyboardInterrupt:
				print '\nINTERUPT (Ctrl+C)'
				prs=xmpp.Presence(typ='unavailable')
				prs.setStatus(u'got Ctrl-C -> shutdown')
				JCON.send(prs)
				time.sleep(2)
				print 'DISCONNECTED'
				print '\n...---===BOT STOPPED===---...\n'
				sys.exit(0)
				print 'WAITING FOR RESTART...'
			print 'RESTARTING'
			os.execl(sys.executable, sys.executable, sys.argv[0])
		else:
			raise
