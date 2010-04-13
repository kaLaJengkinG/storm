#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  more_plugin.py

#  Initial Copyright © 2009 Als <als-als@ya.ru>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_more(type, source, parameters):
	if type!='private':
		if source[1] in GCHCFGS.keys() and GCHCFGS[source[1]]['more']==1:
			if LAST['gch'][source[1]]['msg']:
				reply(type,source, LAST['gch'][source[1]]['msg'])
	else:
		reply(type,source, u'a sense?')

def handler_more_control(type, source, parameters):			
	pass
			
			
def handler_more_outmsg(target, body, obody):
	if target in GCHCFGS.keys() and GCHCFGS[target]['more']==1:
		if hash(obody)!=LAST['gch'][target]['msg']:
			if len(obody)>1000:
				LAST['gch'][target]['msg']=obody[1000:]

def init_more(gch):
	if not 'more' in GCHCFGS[gch]:
		GCHCFGS[gch]['more']=1
	if GCHCFGS[gch]['more']:
		LAST['gch'][gch]['msg']=''
			

register_command_handler(handler_more, 'more', ['muc','all'], 0, 'Finishes poll and shows it’s result.', 'more', ['more'])
register_command_handler(handler_more_control, 'more*', ['admin','muc','all'], 20, 'Finishes poll and shows it’s result.', 'more*', ['more*'])
			
register_outgoing_message_handler(handler_more_outmsg)
register_stage1_init(init_more)
