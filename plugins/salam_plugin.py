#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  salam_plugin.py
#  Coded by bLaDe

def handler_salam_1(type, source, parameters):
	replies = [u'Halo', u'halo', u'apa kabar?', u'met gabung', u'hi juga', u'nak mana km?', u'np baru muncul?', u'qu tanen ma km', u'dari mana aja c?', u'tar eah bos na ge sibuk tuh']
	balas = random.choice(replies)
	if type == 'public':
		if source[1]:
			reply(type, source, balas)
	elif type == 'private':
		reply(type, source, balas)

def handler_salam_2(type, source, parameters):
	replies = [u'salam', u'kumsalam', u'waskum', u'wa\' alaikumsalam', u'wa\' alaikumsalam wwbr', u'kumsalam plen', u'kumsalam boss']
	balas = random.choice(replies)
	if type == 'public':
		if source[1]:
			reply(type, source, balas)
	elif type == 'private':
		reply(type, source, balas)		
		
def handler_pamit(type, source, parameters):
	replies = [u'sampai jumpa', u'jgn bosan maen sini lagi ya?', u'maapin yah kalo ada kata yg salah', u'ikuuuuuttt..., he he']
	balas = random.choice(replies)
	if type == 'public':
		if source[1]:
			reply(type, source, balas)
	elif type == 'private':
		reply(type, source, balas)

register_command_handler(handler_pamit, 'pamit', ['new'], 0, '', '', [''])
register_command_handler(handler_pamit, 'bye', ['new'], 0, '', '', [''])
register_command_handler(handler_salam_1, 'halo', ['new'], 0, '', '', [''])
register_command_handler(handler_salam_1, 'Halo', ['new'], 0, '', '', [''])
register_command_handler(handler_salam_1, 'hola', ['new'], 0, '', '', [''])
register_command_handler(handler_salam_1, 'Hi', ['new'], 0, '', '', [''])
register_command_handler(handler_salam_1, 'hi', ['new'], 0, '', '', [''])
register_command_handler(handler_salam_2, 'askum', ['new'], 0, '', '', [''])
register_command_handler(handler_salam_2, 'Askum', ['new'], 0, '', '', [''])