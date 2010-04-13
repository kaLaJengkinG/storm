#===istalismanplugin===
# -*- coding: utf-8 -*-

# author ferym@jabbim.org.ru

def handler_cleaner(type, source, parameters):
    groupchat=source[1]
    st = [u'away',u'xa',u'dnd']
    if GROUPCHATS.has_key(groupchat):
      reply(type, source, u'Membersihkan...')
      cleans=xmpp.protocol.Presence(source[1]+'/'+get_bot_nick(source[1]))
      cleans.setShow(random.choice(st))
      cleans.setStatus(u'Membersihkan...')
      JCON.send(cleans)
      for x in range(1, 20):
        time.sleep(1.5)
        msg(groupchat, u'')
      reply(type, source, u'Selesai')
      done=xmpp.protocol.Presence(source[1]+'/'+get_bot_nick(source[1]))
      done.setShow('online')
      done.setStatus(u'be yourself but respect the others')
      JCON.send(done)
    else:
      reply(type, source, u'hanya berfungsi di ruang konferensi')
    
#register_command_handler(handler_cleaner, 'clean', ['mod','admin','all'], 20, 'Invisible cleaning of conference.', 'clean', ['clean'])
#register_command_handler(handler_cleaner, 'чисть', ['mod','admin','all'], 20, 'невидимая зачистка конференции.', 'чисть', ['чисть'])
register_command_handler(handler_cleaner, '!clean', ['mod','admin','all'], 20, 'Menyapu ruang konferensi tanpa terlihat.\n(menggunakan karakter null)', '!clean', ['!clean'])    
