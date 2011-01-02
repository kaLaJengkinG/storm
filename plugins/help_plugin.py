#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  help_plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Help Copyright © 2007 dimichxp <dimichxp@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_help_help(type, source, parameters):
	ctglist = []
	if parameters and COMMANDS.has_key(parameters.strip()):
		rep = COMMANDS[parameters.strip()]['desc'].decode("utf-8") + u'\nCategories: '
		for cat in COMMANDS[parameters.strip()]['category']:
			ctglist.append(cat)
		rep += ', '.join(ctglist).decode('utf-8')+u'\nUse: ' + COMMANDS[parameters.strip()]['syntax'].decode("utf-8") + u'\nExample:'
		for example in COMMANDS[parameters]['examples']:
			rep += u'\n  >>  ' + example.decode("utf-8")
		rep += u'\nNecessary level of access: ' + str(COMMANDS[parameters.strip()]['access'])
		if parameters.strip() in COMMOFF[source[1]]:
			rep += u'\nThis command has been power-off in this conference!!!'
		else:
			pass
	else:
		rep = u'write a word "commands" (without quotation marks), to get the list of commands, "help of <commands>" for the receipt of help on a command, macrolist for the receipt of list of macros, and also macroacc <macro> for the receipt of level of access to the certain macro\np.s. look the level of access in private'
	reply(type, source, rep)

def handler_help_commands(type, source, parameters):
	date=time.strftime('%a, %d %b %Y', time.gmtime()).decode('utf-8')
	groupchat=source[1]
	if parameters:
		rep,dsbl = [],[]
		total = 0
		param=parameters.encode("utf-8")
		catcom=set([((param in COMMANDS[x]['category']) and x) or None for x in COMMANDS]) - set([None])
		if not catcom:
			reply(type,source,u'does it exist? :-O')
			return
		for cat in catcom:
			if has_access(source, COMMANDS[cat]['access'],groupchat):
				if source[1] in COMMOFF:
					if cat in COMMOFF[source[1]]:
						dsbl.append(cat)
					else:
						rep.append(cat)
						total = total + 1
				else:
					rep.append(cat)
					total = total + 1					
		if rep:
			if type == 'public':
				reply(type,source,u'sent to private')
			rep.sort()
			answ=u'List of commands is in a category <'+parameters+u'> on '+date+u':\n\n' + u', '.join(rep) +u' - ('+str(total)+u' items)'
			if dsbl:
				dsbl.sort()
				answ+=u'\n\nThe followings commands has been power-offs in this conference:\n\n'+', '.join(dsbl)
			reply('private', source,answ)
		else:
			reply(type,source,u'dream ]:->')
	else:
		cats = set()
		for x in [COMMANDS[x]['category'] for x in COMMANDS]:
			cats = cats | set(x)
		cats = ', '.join(cats).decode('utf-8')
		if type == 'public':
			reply(type,source,u'sent to private')
		reply('private', source, u'List of commands is in a category on '+date+u'\n'+ cats+u'\n\nTo view the list of commands contained in a category, type "commands category" without quotation marks, for example "commands all"')


register_command_handler(handler_help_help, 'help', ['help','info','all'], 0, 'Show detail information about a certain command.', 'help [command]', ['help', 'help ping'])
register_command_handler(handler_help_commands, 'commands', ['help','info','all'], 0, 'Shows the list of all of categories of commands. At the query of category shows the list of commands being in it.', 'commands [category]', ['commands','commands all'])