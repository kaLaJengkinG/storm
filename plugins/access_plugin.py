#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  access_plugin.py

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


def handler_access_login(type, source, parameters):
	if type == 'public':
		reply(type, source, u'Stupid, this command had to perform in the private!!! ]:->')
	jid = get_true_jid(source)
	if parameters.strip() == ADMIN_PASSWORD:
		GLOBACCESS[jid]=100
		reply('private', source, u'Global full access granted')
	else:
		reply('private', source, u'Incorrect password')

def handler_access_logout(type, source, parameters):
	jid = get_true_jid(source)
	del GLOBACCESS[jid]
	reply(type, source, u'Access withdrawn')

def handler_access_view_access(type, source, parameters):
	accdesc={'-100':u'(full ignored)','-1':u'(blocked)','0':u'(none)','1':u'(poor member :D )','10':u'(user)','11':u'(member)','15':u'(moder)','16':u'(moder)','20':u'(admin)','30':u'(owner)','40':u'(pionir)','100':u'(bot admin)'}
	if not parameters:
		level=str(user_level(source[1]+'/'+source[2], source[1]))
		if level in accdesc.keys():
			levdesc=accdesc[level]
		else:
			levdesc=''		
		reply(type, source, level+u' '+levdesc)
	else:
		if not source[1] in GROUPCHATS:
			reply(type, source, u'This is only possible in the conference')
			return
		nicks = GROUPCHATS[source[1]].keys()
		if parameters.strip() in nicks:
			level=str(user_level(source[1]+'/'+parameters.strip(),source[1]))
			if level in accdesc.keys():
				levdesc=accdesc[level]
			else:
				levdesc=''
			reply(type, source, level+' '+levdesc)
		else:
			reply(type, source, u'dia ada di sini? :-O')

def handler_access_set_access(type, source, parameters):
	if not source[1] in GROUPCHATS:
		reply(type, source, u'This is only possible in the conference')
		return
	splitdata = string.split(parameters)
	if len(splitdata) > 1:
		try:
			int(splitdata[1].strip())
		except:
			reply(type, source, u'perintah salah, baca "help set_access"')
			return				
		if int(splitdata[1].strip())>100 or int(splitdata[1].strip())<-100:
			reply(type, source, u'perintah salah, read help on using the command')
			return		
	nicks=GROUPCHATS[source[1]]
	if not splitdata[0].strip() in nicks and GROUPCHATS[source[1]][splitdata[0].strip()]['ishere']==0:
		reply(type, source, u'dia ada di sini? :-O')
		return
	tjidto=get_true_jid(source[1]+'/'+splitdata[0].strip())
	tjidsource=get_true_jid(source)
	groupchat=source[1]
	jidacc=user_level(source, groupchat)
	toacc=user_level(tjidto, groupchat)

	if len(splitdata) > 1:
		if tjidsource in ADMINS:
			pass
		else:
			if tjidto==tjidsource:
				if int(splitdata[1]) > int(jidacc):
					reply(type, source, u'*FIGA*')
					return
			elif int(toacc) > int(jidacc):
				reply(type, source, u'*FIGA*')
				return		
			elif int(splitdata[1]) >= int(jidacc):
				reply(type, source, u'*FIGA*')
				return	
	else:
		if tjidsource in ADMINS:
			pass
		else:
			if tjidto==tjidsource:
				pass
			elif int(toacc) > int(jidacc):
				reply(type, source, u'*FIGA*')
				return

	if len(splitdata) == 1:		
		change_access_perm(source[1], tjidto)
		if splitdata[0].strip()==source[2]:
			reply(type, source, u'akses dicabut, anda perlu rejoin room')
		else:
			reply(type, source, u'akses dicabut, %s, perlu rejoin room' % splitdata[0].strip())
	elif len(splitdata) == 2:
		change_access_temp(source[1], tjidto, splitdata[1].strip())
		reply(type, source, u'diberikan akses sementara')
	elif len(splitdata) == 3:
		change_access_perm(source[1], tjidto, splitdata[1].strip())
		reply(type, source, u'diberikan akses permanen')		
		
def handler_access_set_access_glob(type, source, parameters):
	if not source[1] in GROUPCHATS:
		reply(type, source, u'This is only possible in the conference')
		return
	if parameters:
		splitdata = parameters.strip().split()
		if len(splitdata)<1 or len(splitdata)>2:
			reply(type, source, u'eee?')
			return
		nicks=GROUPCHATS[source[1]].keys()
		if not splitdata[0].strip() in nicks and GROUPCHATS[source[1]][splitdata[0].strip()]['ishere']==0:
			reply(type, source, u'dia ada di sini? :-O')
			return
		tjidto=get_true_jid(source[1]+'/'+splitdata[0])
		if len(splitdata)==2:
			change_access_perm_glob(tjidto, int(splitdata[1]))
			reply(type, source, u'diberikan')
		else:
			change_access_perm_glob(tjidto)
			reply(type, source, u'dihapus')
			
def get_access_levels():
	global GLOBACCESS
	global ACCBYCONFFILE
	GLOBACCESS = eval(read_file(GLOBACCESS_FILE))
	for jid in ADMINS:
		GLOBACCESS[jid] = 100
		write_file(GLOBACCESS_FILE, str(GLOBACCESS))
	ACCBYCONFFILE = eval(read_file(ACCBYCONF_FILE))

register_command_handler(handler_access_login, 'login', ['access','admin','all'], 0, 'Login sebagai admin-bot, perintah harus diketik secara private!', 'login <sandi>', ['login rahasia'])
register_command_handler(handler_access_login, 'logout', ['access','admin','all'], 0, 'Logout sebagai bot admin.', 'logout', ['logout'])
register_command_handler(handler_access_view_access, 'access', ['access','admin','all'], 0, 'Menunjukkan tingkat akses user.\n-100 - diabaikan, seluruh pesan oleh pengguna dengan akses ini akan diabaikan pada tingkat kernel\n-1 - ditiadakan\n0 - perintah dan macro sangat dibatasi, otomatis dikenal sebagai visitor\n10 - parintah dan macro standar, otomatis dikenal sebagai participan\n11 - perintah dan macro diperluas (akses juga ;-) !!!), otomatis dikenal sebagai member\n15 (16) - perintah dan macro moderator, otomatis dikenal sebagai moderator\n20 - perintah dan macro admin, otomatis dikenal sebagai admin\n30 - perintah dan macro owner, otomatis dikenal sebagai owner\n40 - tidak semua perintah diiplementasikan, dapat menggunakan perintah leave dan join bot\n100 - admin-bot, patuh semua perintah', 'access [nick]', ['access', 'access guy'])
register_command_handler(handler_access_set_access, 'set_access', ['access','admin','all'], 15, 'Menetapkan atau menghapus akses lokal.\nKetik tanpa level setelah nick, bot perlu rejoin conference. bila parameter ketiga "permanen" disebutkan, akses ditetapkan permanen, bila tidak akses akan hilang saat bot rejoin conference.\n-100 - diabaikan, seluruh pesan oleh pengguna dengan akses ini akan diabaikan pada tingkat kernel\n-1 - ditiadakan\n0 - perintah dan macro sangat dibatasi, otomatis dikenal sebagai visitor\n10 - parintah dan macro standar, otomatis dikenal sebagai participan\n11 - perintah dan macro diperluas (akses juga ;-) !!!), otomatis dikenal sebagai member\n15 (16) - perintah dan macro moderator, otomatis dikenal sebagai moderator\n20 - perintah dan macro admin, otomatis dikenal sebagai admin\n30 - perintah dan macro owner, otomatis dikenal sebagai owner\n40 - tidak semua perintah diiplementasikan, dapat menggunakan perintah leave dan join bot\n100 - admin-bot, patuh semua perintah', 'set_access <nick> <level> [permanen]', ['set_access guy 20', 'set_access guy 30 permanen'])
register_command_handler(handler_access_set_access_glob, 'globacc', ['access','superadmin','all'], 100, 'Menetapkan atau menghapus akses lokal.\nKetik tanpa level setelah nick untuk menghapus akses.', 'globacc <nick> <level>', ['globacc guy 100','globacc guy'])

register_stage0_init(get_access_levels)
