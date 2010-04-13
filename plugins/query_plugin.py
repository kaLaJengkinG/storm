#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  query_plugin.py

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

def handler_query_get_public(type, source, parameters):
	groupchat=source[1]
	DBPATH='dynamic/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
	else:
		reply(type,source,u'error creating of local database, you should report it to bot Admin')
		return
	if parameters:
		if localdb.has_key(string.lower(parameters)):
			reply(type, source, u'i know about <' + parameters + u'> :\n' + localdb[string.lower(parameters)])
		else:
			reply(type, source, u'i dont know about <' + parameters + '> :(')
	else:
			reply(type, source, u'and?')

def handler_query_get_private(type, source, parameters):
	if not parameters:
		reply(type, source, u'and?')
		return
	groupchat=source[1]
	DBPATH='dynamic/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
	else:
		reply(type,source,u'error creating of local database, you should report it to bot Admin')
		return
	tojid = ''
	rep = u'to whom?'
	localdb = eval(read_file(DBPATH))
	if GROUPCHATS.has_key(groupchat):
		nicks = GROUPCHATS[groupchat].keys()
		args = parameters.split(' ')
		if len(args)>=2:
			nick = args[0]
			body = ' '.join(args[1:])
			if get_bot_nick(groupchat) != nick:
				if nick in nicks:
					tojid = groupchat+'/'+nick
		else:
			tojid = groupchat+'/'+source[2]
			body = parameters
	if tojid:
		if localdb.has_key(string.lower(body)):
			if type == 'public':
				reply(type, source, u'sent to private')
			msg(tojid, u'i know about <' + body + u'> :\n'+localdb[string.lower(body)])
		else:
			reply(type, source, u'i dont know about <' + body + '> :(')
	else:
		reply(type, source, u'to whom?')

		
def handler_query_get_random(type, source, parameters):
	groupchat=source[1]
	DBPATH='dynamic/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
	else:
		reply(type,source,u'error creating of local database, you should report it to bot Admin')
		return
	if not localdb.keys():
		reply(type, source, u'database is empty!')
		return
	rep = random.choice(localdb.keys())
	reply(type, source, u'i know about <' + rep + u'> :\n' + localdb[rep])


def handler_query_set(type, source, parameters):
	if not parameters:
		reply(type, source, u'and?')
		return
	groupchat=source[1]
	DBPATH='dynamic/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
		keyval = string.split(parameters, '=', 1)
		if not len(keyval)<2:
			key = string.lower(keyval[0]).strip()
			value = keyval[1].strip()
			if not value:
				if localdb.has_key(key):
					del localdb[key]
				reply(type, source, key + u' -> deleted')
			else:
				localdb[key] = keyval[1].strip()+u' (from '+source[2]+')'
				reply(type, source, u'now i know about ' + key)
			write_file(DBPATH, str(localdb))
		else:
			reply(type, source, u'and?')
	else:
		reply(type,source,u'error creating of local database, you should report it to bot Admin')

def handler_query_count(type, source, parameters):
	groupchat=source[1]
	DBPATH='dynamic/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
		num=str(len(localdb.keys()))
		reply(type, source, 'database of answers/questions of this conference '+num+' records')
	else:
		reply(type,source,u'error creating of local database, you should report it to bot Admin')
		return

def handler_query_search(type, source, parameters):
	if not parameters:
		reply(type, source, u'and?')
		return
	rep=[]
	groupchat=source[1]	
	DBPATH='dynamic/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
		if not localdb.keys():
			reply(type, source, u'database is empty!')
			return
		for x in localdb:
			if x.count(parameters)>0:
				rep.append(x)
		if rep:
			reply(type,source,u'coincided with:\n'+', '.join(rep))
		else:
			reply(type,source,u'it did not coincide with anything :(')
	else:
		reply(type,source,u'error creating of local database, you should report it to bot Admin')
		return
		
def handler_query_all(type, source, parameters):
	groupchat=source[1]
	DBPATH='dynamic/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
		num=len(localdb.keys())
		if num == 0:
			reply(type, source, 'database is empty!')
			return
		reply(type, source, ', '.join(localdb.keys()))
	else:
		reply(type,source,u'error creating of local database, you should report it to bot Admin')
		return


register_command_handler(handler_query_get_public, '???', ['info','wtf','all'], 10, 'Search an answer for a question in database (Same with wtf on Sulci-bot).', '??? <query>', ['??? something', '??? something ещё'])
register_command_handler(handler_query_get_private, '!??', ['info','wtf','all'], 10, 'Search an answer for a question in database and sends it in private (Same with !word showpriv in Gluxi-bot).', '!?? <nick> <query>', ['!?? something', '!?? guy something'])
register_command_handler(handler_query_set, '!!!', ['info','wtf','admin','all'], 11, 'Sets an answer for a question in database (Same with dfn on Sulci-bot).', '!!! <query> = <answer>', ['!!! something = the best!', '!!! something ещё ='])
register_command_handler(handler_query_count, '???count', ['info','wtf','all'], 10, 'Shows the amount of questions in database (Same with wtfcount on Sulci-bot).', '!!! ???count', ['???count'])
register_command_handler(handler_query_get_random, '???rand', ['info','wtf','all'], 10, 'Shows the answer in randomize (Same with wtfrand on Sulci-bot).', '???rand', ['???rand'])
register_command_handler(handler_query_search, '???search', ['info','wtf','all'], 10, 'Search on database.', '???search <query>', ['???search something'])
register_command_handler(handler_query_all, '???all', ['info','wtf','all'], 10, 'Shows all of the keys on database (be carefull, flood!).', '???all', ['???all'])
