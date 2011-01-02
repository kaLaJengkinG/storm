#===istalismanplugin===
# -*- coding: utf-8 -*-

# author ferym@jabbim.org.ru

def handler_cleaner(type, source, parameters):
    groupchat=source[1]
    st = [u'away',u'xa',u'dnd']
    if GROUPCHATS.has_key(groupchat):
      reply(type, source, u'Cleaning...')
      cleans=xmpp.protocol.Presence(source[1]+'/'+get_bot_nick(source[1]))
      cleans.setShow(random.choice(st))
      cleans.setStatus(u'Cleaning...')
      JCON.send(cleans)
      for x in range(1, 20):
        time.sleep(1.5)
        msg(groupchat, u'')
      reply(type, source, u'Finished')
      done=xmpp.protocol.Presence(source[1]+'/'+get_bot_nick(source[1]))
      done.setShow('online')
      done.setStatus(u'be yourself but respect the others')
      JCON.send(done)
    else:
      reply(type, source, u'This command only possible in the conference')
    
register_command_handler(handler_cleaner, '!clean', ['muc','admin','all'], 20, 'Invisible cleaning of conference.', 'clean', ['clean'])