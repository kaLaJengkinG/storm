#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  macro_plugin.py

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

def macroadd_handler(type, source, parameters):
	pl = MACROS.parse_cmd(parameters)
	if (len(pl)<2):
		reply(type, source, u'it is not enough arguments')
		return
	else:
		if pl[1].split()[0] in COMMAND_HANDLERS or pl[1].split()[0] in MACROS.gmacrolist or pl[1].split()[0] in MACROS.macrolist[source[1]]:
			real_access = MACROS.get_access(pl[1].split()[0], source[1])
			if real_access < 0 and pl[1].split()[0] in COMMAND_HANDLERS:
				real_access = COMMANDS[pl[1].split()[0]]['access']
			else:
				pass
			if real_access:
				if not has_access(source, real_access, source[1]):
					reply(type, source, u'dream ]:->')
					return
		else:
			reply(type, source, u'i do not see a command in macro')
			return				
		MACROS.add(pl[0], pl[1], source[1])
		MACROS.flush()		
		reply(type, source, u'added')
	
def gmacroadd_handler(type, source, parameters):
	pl = MACROS.parse_cmd(parameters)
	if (len(pl)<2):
		rep = u'it is not enough arguments'
	else:
		MACROS.add(pl[0], pl[1])
		write_file('dynamic/macros.txt', str(MACROS.gmacrolist))
		rep = u'added'
	reply(type, source, rep)

def macrodel_handler(type, source, parameters):
	if parameters:
		MACROS.remove(parameters, source[1])
#		write_file('dynamic/'+source[1]+'macros.txt', str(MACROS.macrolist[source[1]]))
		MACROS.flush()
		rep = u'removed'
	else:
		rep = u'it is not enough arguments'
	reply(type, source, rep)
	
def gmacrodel_handler(type, source, parameters):
	if parameters:
		MACROS.remove(parameters)
		write_file('dynamic/macros.txt', str(MACROS.gmacrolist))
		rep = u'removed'
	else:
		rep = u'it is not enough arguments'
	reply(type, source, rep)

def macroexpand_handler(type, source, parameters):
	if parameters:
		rep=MACROS.comexp(parameters, source)
		if not rep:
			rep = u'not expand. it is not enough rights'
	else:
		rep = u'it is not enough arguments'
	reply(type, source, rep)
	
def gmacroexpand_handler(type, source, parameters):
	if parameters:
		rep=MACROS.comexp(parameters, source, '1')
	else:
		rep = u'it is not enough arguments'
	reply(type, source, rep)

def macroinfo_handler(type, source, parameters):
	rep=''
	if parameters:
		try:
			if MACROS.macrolist[source[1]].has_key(parameters):
				rep = parameters+' -> '+MACROS.macrolist[source[1]][parameters]
		except:
			rep = u'there is no such macro'
	elif parameters == 'allmac':
		rep += '\n'.join([x+' -> '+ MACROS.macrolist[source[1]][x] for x in MACROS.macrolist[source[1]]])
	if not rep:
		rep=u'not enough rights *FIGA*'
	reply(type, source, rep)
	
def gmacroinfo_handler(type, source, parameters):
	rep=''
	if parameters:
		if MACROS.gmacrolist.has_key(parameters):
			rep = parameters+' -> '+MACROS.gmacrolist[parameters]
		else:
			rep = u'there is no such macro'
	elif parameters == 'allmac':
		rep += '\n'.join([x+' -> '+ MACROS.macrolist[x] for x in MACROS.macrolist])
	reply(type, source, rep)
	
def macrolist_handler(type, source, parameters):
	rep,dsbll,dsblg,glist,llist=u'List of macros:',[],[],[],[]
	if MACROS.macrolist[source[1]]:
		for macro in MACROS.macrolist[source[1]].keys():
			if macro in COMMOFF[source[1]]:
				dsbll.append(macro)
			else:
				llist.append(macro)
		dsbll.sort()
		llist.sort()
		rep += u'\nLOCAL\n'+', '.join(llist)
		if dsbll:
			rep+=u'\n\nThe followings local macros are power-offs in this conference:\n'+', '.join(dsbll)
	else:
		rep+=u'\nLOCAL\nempty\n'
	for macro in MACROS.gmacrolist.keys():
		if macro in COMMOFF[source[1]]:
			dsblg.append(macro)
		else:
			glist.append(macro)
	dsblg.sort()
	glist.sort()
	rep += u'\nGLOBAL\n'+', '.join(glist)
	if dsblg:
		rep+=u'\n\nThe followings global macros are power-offs in this conference:\n'+', '.join(dsblg)
	if type=='public':
		reply(type, source, u'sent to private')
	reply('private', source, rep)
	
def macroaccess_handler(type, source, parameters):
	if parameters:
		args = parameters.split(' ')
		if len(args)==2:
			macro = args[0]
			if macro in MACROS.gmacrolist or macro in MACROS.macrolist[source[1]]:
				real_access = MACROS.get_access(macro, source[1])
				if real_access < 0:
					pass
				else:
					if not has_access(source, real_access, source[1]):
						reply(type,source,u'dreams ]:->')
						return
			elif macro in COMMAND_HANDLERS:
				if not user_level(source,source[1])==100:
					reply(type,source,u'dreams ]:->')
					return
				else:
					pass
			access = args[1]
			MACROS.give_access(macro,access,source[1])
			reply(type,source,u'gave')
			time.sleep(1)
			MACROS.flush()
		else:
			reply(type,source,u'that for a delirium?')
			
def gmacroaccess_handler(type, source, parameters):
	if parameters:
		args = parameters.split(' ')
		if len(args)==2:
			macro = args[0]
			access = args[1]
			MACROS.give_access(macro,access)
			reply(type,source,u'gave')
			time.sleep(1)
			write_file('dynamic/macroaccess.txt', str(MACROS.gaccesslist))
		else:
			reply(type,source,u'is that a delirium?')


register_command_handler(macroadd_handler, 'macroadd', ['admin','macro','all'], 20, 'Add local macro. Self macro must be celled in `` !!!', 'macroadd [name] [`macro`]', ['macroadd glitch `say /me thought, that all of glitch`'])
register_command_handler(gmacroadd_handler, 'gmacroadd', ['superadmin','macro','all'], 100, 'Add macro globally. Self macro must be celled in `` !!!', 'gmacroadd [name] [`macro`]', ['gmacroadd glitch `say /me thought, that all of glitch`'])

register_command_handler(macrodel_handler, 'macrodel', ['admin','macro','all'], 20, 'Delete local macro.', 'macrodel [name]', ['macrodel glitch'])
register_command_handler(gmacrodel_handler, 'gmacrodel', ['superadmin','macro','all'], 100, 'Delete macro globally.', 'gmacrodel [name]', ['gmacrodel glitch'])

register_command_handler(macroexpand_handler, 'macroexp', ['admin','macro','info','all'], 20, 'Expand local macro, ie. look at the finished macro raw.', 'macroexp [name] [parameter]', ['macroexp admin bot'])
register_command_handler(gmacroexpand_handler, 'gmacroexp', ['superadmin','macro','info','all'], 100, 'Expand global macro, ie. look at the finished macro raw.', 'gmacroexp [name] [parameter]', ['gmacroexp admin bot'])

register_command_handler(macroinfo_handler, 'macroinfo', ['admin','macro','info','all'], 20, 'Open the local macro, ie. just to look the macro. To see all the macro names insted write some macro "allmac" without quotes.', 'macroinfo [name]', ['macroinfo glitch','macroinfo allmac'])
register_command_handler(gmacroinfo_handler, 'gmacroinfo', ['superadmin','macro','info','all'], 100, 'Open the global macro, ie. just to look the macro. To see all the macro names insted write some macro "allmac" without quotes.', 'gmacroinfo [name]', ['gmacroinfo glitch','gmacroinfo allmac'])

register_command_handler(macrolist_handler, 'macrolist', ['help','macro','info','all'], 10, 'List of macros.', 'macrolist', ['macrolist'])

register_command_handler(macroaccess_handler, 'macroaccess', ['admin','macro','all'], 20, 'Change access in certain local macro.', 'macroaccess [macro] [access]', ['macroaccess glitch 10'])
register_command_handler(gmacroaccess_handler, 'gmacroaccess', ['superadmin','macro','all'], 100, 'Change access in certain macro globally.', 'gmacroaccess [macro] [access]', ['macroaccess admin 20'])