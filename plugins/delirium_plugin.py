#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  commoff_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

poke_nicks={}

def handler_poke(type, source, parameters):
	if type=='private':
		reply(type,source,u':-P')
		return
	groupchat = source[1]
	if parameters:
		if parameters==u'last10':
			cnt=0
			rep=''
			nicks = set()
			for x in [poke_nicks[source[1]] for x in poke_nicks]:
				nicks = nicks | set(x)
			for x in nicks:
				cnt=cnt+1
				rep += str(cnt)+u') '+x+u'\n'
			reply('private',source,rep[:-1])
			return
		if not poke_nicks.has_key(source[1]):
			poke_nicks[source[1]]=source[1]
			poke_nicks[source[1]]=[]
		if len(poke_nicks[source[1]])==10:
			poke_nicks[source[1]]=[]
		else:
			poke_nicks[source[1]].append(source[2])
		if not parameters == get_bot_nick(source[1]):
			if parameters in GROUPCHATS[source[1]]:
				pokes=[]
				pokes.extend(poke_work(source[1]))
				pokes.extend(eval(read_file('static/delirium.txt'))['poke'])
				rep = random.choice(pokes)
				msg(source[1],u'/me '+rep % parameters)
			else:
				reply(type, source, u'but is he here? :-O')
		else:
			reply(type, source, u'intelligent, hard, yes? ]:->')	
	else:
		reply(type, source, u'dream? :D')
		
def handler_poke_add(type, source, parameters):
	if not parameters:
		reply(type, source, u'and?')
	if not parameters.count('%s'):
		reply(type, source, u'i do not see %s')
		return
	res=poke_work(source[1],1,parameters)
	if res:
		reply(type, source, u'added')
	else:
		reply(type, source, u'no longer available')
		
def handler_poke_del(type, source, parameters):
	if not parameters:
		reply(type, source, u'and?')
	if parameters=='*':
		parameters='0'
	else:
		try:
			int(parameters)
		except:
			reply(type,source,u'syntax disabled')
	res=poke_work(source[1],2,parameters)
	if res:
		reply(type, source, u'deleted')
	else:
		reply(type, source, u'no more available')
		
def handler_poke_list(type, source, parameters):
	rep,res=u'',poke_work(source[1],3)
	if res:
		res=sorted(res.items(),lambda x,y: int(x[0]) - int(y[0]))
		for num,phrase in res:
			rep+=num+u') '+phrase+u'\n'
		reply(type,source,rep.strip())
	else:
		reply(type,source,u'no custom phrases')
		
def handler_test(type, source, parameters):
	reply(type,source,u'passed')
	
def handler_clean_conf(type, source, parameters):
	if GROUPCHATS.has_key(source[1]):
                for x in range(1, 20):
			msg(source[1], '')
#			time.sleep(1.3)
		reply(type,source,u'cleaned, like my *nose*')
		
def handler_afools_control(type, source, parameters):
	if parameters:
		try:
			int(parameters)
		except:
			reply(type,source,u'syntax disabled')
		if int(parameters)>1:
			reply(type,source,u'syntax disabled')
		if parameters=="1":
			GCHCFGS[source[1]]['afools']=1
			reply(type,source,u'jokes are enabled')
		else:
			GCHCFGS[source[1]]['afools']=0
			reply(type,source,u'jokes are disabled')			
	else:
		if GCHCFGS[source[1]]['afools']==1:
			reply(type,source,u'jokes are enabled')
		else:
			reply(type,source,u'jokes are disabled')
	
			
def get_afools_state(gch):
	if not 'afools' in GCHCFGS[gch]:
		GCHCFGS[gch]['afools']=0
		
def poke_work(gch,action=None,phrase=None):
	DBPATH='dynamic/'+gch+'/delirium.txt'
	if check_file(gch,'delirium.txt'):
		pokedb = eval(read_file(DBPATH))
		if action==1:
			for x in range(1, 21):
				if str(x) in pokedb.keys():
					continue
				else:
					pokedb[str(x)]=phrase
					write_file(DBPATH, str(pokedb))
					return True
			return False
		elif action==2:
			if phrase=='0':
				pokedb.clear()
				write_file(DBPATH, str(pokedb))
				return True
			else:
				try:
					del pokedb[phrase]
					write_file(DBPATH, str(pokedb))
					return True
				except:
					return False
		elif action==3:
			return pokedb
		else:
			return pokedb.values()
	else:
		return None
		
def remix_string(parameters):
	remixed=[]
	for word in parameters.split():
		tmp=[]
		if len(word)<=1:
			remixed.append(word)
			continue
		elif len(word)==2:
			tmp=list(word)
			random.shuffle(tmp)
			remixed.append(u''.join(tmp))
		elif len(word)==3:
			tmp1=list(word[1:])
			tmp2=list(word[:-1])
			tmp=random.choice([tmp1,tmp2])
			if tmp==tmp1:
				random.shuffle(tmp)
				remixed.append(word[0]+u''.join(tmp))
			else:
				random.shuffle(tmp)
				remixed.append(u''.join(tmp)+word[-1])					
		elif len(word)>=4:
			tmp=list(word[1:-1])
			random.shuffle(tmp)
			remixed.append(word[0]+u''.join(tmp)+word[-1])
	return u' '.join(remixed)

def handler_kick_ass(type, source, parameters):
	if GROUPCHATS.has_key(source[1]):
		if len(parameters.split()) == 3:
			splitdata = string.split(parameters)
			rep,jid,msgnum,smlnum = '','',int(splitdata[1]),int(splitdata[2])
			if msgnum>500 or smlnum>500:
				reply(type,source,u'sorry :-(')
				return
			reply(type,source,u'PERHATIAN SPAMMING!!!')
			if splitdata[0]==u':)':
				for x in range(0, msgnum):
					for y in range(0, smlnum):
						rep += u'*CRAZY* '
					msg(source[1], rep)
					rep = ''
#					time.sleep(0.5)
			else:
				if splitdata[0].count('@'):
					jid=splitdata[0]
				else:
					jid=source[1]+'/'+splitdata[0]
				print jid
				for x in range(0, msgnum):
					for y in range(0, smlnum):
						rep += u'*CRAZY* '
					msg(jid, rep)
					rep=''
#					time.sleep(0.5)
			reply(type,source,u'Sukses!!!')
		else:
			reply(type,source,u'read "help spam"')
	
register_command_handler(handler_poke, 'poked', ['fun','all','poked'], 10, ' Poke the user. Forces him to pay attention to you /in chat.\nlast10 It will show last poked nicks list instead of nickname.', 'poked <nick>|<параметр>', ['poked qwerty','poked + пришиб %s','poked - 2','poked *'])
register_command_handler(handler_poke_add, 'poked+', ['fun','all','poked'], 20, ' Add a custom phrases. The variable %s in the phrase refers to a place to insert a nickname (mandatory parameter). The phrase should be written by a third person, it will use the following form "/me your phrase". max number of custom phrases is 20 characters.', 'poked+ <phrase>', ['poked+ sing %s'])
register_command_handler(handler_poke_del, 'poked-', ['fun','all','poked'], 20, 'Delete a custom phrase. Write the number of phrase to erase the words, the bot will delete it permanently. Write the commands "poked*" to view the list. In order to delete all phrases just specify "*" instead of phrase number.', 'poked- <number>', ['poked- 5','poked- *'])
register_command_handler(handler_poke_list, 'poked*', ['fun','all','poked'], 20, 'Displays a list of all custom phrases and its number.', 'poked*', ['poked*'])
register_command_handler(handler_test, 'тест', ['fun','info','all'], 0, 'Passed simply answers.', 'тест', ['тест'])
register_command_handler(handler_test, 'test', ['fun','info','all'], 0, 'Passed simply answers.', 'test', ['test'])
register_command_handler(handler_clean_conf, 'clean', ['fun','muc','all'], 30, 'Clean current conference (with null character).', 'clean', ['clean'])
register_command_handler(handler_afools_control, 'afools', ['fun','muc','all'], 30, 'Enables and disables the bots jokes, which the bot sometimes substitutes (command is always executed!) Standard response of commands.', 'afools <1|0>', ['afools 1','afools 0'])

#  listed below command handler are not recommended
register_command_handler(handler_kick_ass, 'spam', ['fun','superadmin','muc','all'], 100, 'Spamming a JID in current conference with smiles ( :) ).\nTarget of spam is determine by first parameter <nick>.\nRepetition of spam is determine by the second parameter <amount>.\nThe amount of spam determined by third parameter <amount>.\nWrite this command in private.', 'spam <nick> <amount> <amount>', ['spam guy 1000 10','spam guy 500 8'])

register_stage1_init(get_afools_state)
