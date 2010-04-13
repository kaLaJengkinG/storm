#===istalismanplugin===
# -*- coding: utf-8 -*-

# plugin version 2.0
# copyright ferym@jabbim.org.ru
# All rights reserved. For questions or comments, please jid ferym@jabbim.org.ru
# для сайта http://bots.ucoz.ru (http://jabbrik.ru)
# автор: ferym@jabbim.org.ru
# часть кода: Gigabyte =)
# идея версии 2.0: ManGust

AMSGCONF = {}

def handler_amsg(type, source, parameters):
      ADMINFILE = 'static/amsg.txt'
      fp = open(ADMINFILE, 'r')
      txt = eval(fp.read())
      if checkbl(get_true_jid(source[1]+'/'+source[2]).lower()):
            reply(type, source, u'You are blocked because: '+checkbl(get_true_jid(source[1]+'/'+source[2]).lower()) )
            return
      if len(txt)>=1:
        if parameters:
          if len(parameters)>150:
            reply(type, source, u'you write the text too much!!!')
            return
      
          if not AMSGCONF.has_key(get_true_jid(source[1]+'/'+source[2])):
                AMSGCONF[get_true_jid(source[1]+'/'+source[2])] = {'timesend':time.time(), 'count':1}
          else:
                if time.time() - AMSGCONF[get_true_jid(source[1]+'/'+source[2])]['timesend'] <= 300:
                      reply(type, source, u'The limit for sending messages to the admin. Wait 5 minutes')
                      return
                else:
                      AMSGCONF[get_true_jid(source[1]+'/'+source[2])]['timesend'] = time.time()
                      AMSGCONF[get_true_jid(source[1]+'/'+source[2])]['count'] += 1

          for x in txt:
            msg(x, u'Note for subscribers from '+source[1]+'/'+source[2]+u' (jid: '+get_true_jid(source[1]+'/'+source[2])+u')\nText message: '+parameters)
          reply(type, source, u'Your message was sent.')
        else:
          reply(type, source, u'You forget to write the message!!!')
      else:
        if not AMSGCONF.has_key(get_true_jid(source[1]+'/'+source[2])):
            AMSGCONF[get_true_jid(source[1]+'/'+source[2])] = {'timesend':time.time(), 'count':1}
        else:
            if time.time() - AMSGCONF[get_true_jid(source[1]+'/'+source[2])]['timesend'] <= 300:
                  reply(type, source, u'The limit for sending messages to the admin. Wait 5 minutes')
                  return
            else:
                  AMSGCONF[get_true_jid(source[1]+'/'+source[2])]['timesend'] = time.time()
                  AMSGCONF[get_true_jid(source[1]+'/'+source[2])]['count'] += 1

        if parameters:
          if len(parameters)>150:
            reply(type, source, u'you write the text too much!!!')
            return

          for z in ADMINS:
            msg(z, u'Note for administrators bot (no subscribers.) From '+source[1]+'/'+source[2]+u' (jid: '+get_true_jid(source[1]+'/'+source[2])+u')\nText message: '+parameters)
          reply(type, source, u'Your message was sent!')
        else:
          reply(type, source, u'You forget to write the message!!!')
      
  
        

def amsg_subscribe(type, source, parameters):
    ADMINFILE = 'static/amsg.txt'
    fp = open(ADMINFILE, 'r')
    txt = eval(fp.read())
    if parameters:
      if parameters in txt:
        reply(type, source, u'this JID already exist in database')
        return
      else:
        txt.append(parameters)
        write_file(ADMINFILE,str(txt))
        fp.close()
        reply(type, source, u'JID '+parameters+u' subscribed for the notification')
    else:
      parameters = get_true_jid(source[1]+'/'+source[2])
      fp = open(ADMINFILE, 'r')
      txt = eval(fp.read())
      fp.close()
      if parameters in txt:
        reply(type, source, u'you are in the database already')
        return
      else:
        txt.append(get_true_jid(source[1]+'/'+source[2]))
        write_file(ADMINFILE,str(txt))
        
        reply(type, source, u'you are added to the list of subscribers')
      
def amsg_unsubscribe(type, source, parameters):
      ADMINFILE = 'static/amsg.txt'
      if parameters:
            fp = open(ADMINFILE, 'r')
            txt = eval(fp.read())
            fp.close()
            if parameters in txt:
                  txt.remove(parameters)
            else:
                  reply(type, source, u'you see in jid this mailing list? I - no!')
                  return
            write_file(ADMINFILE,str(txt))

            reply(type, source, u'JID '+parameters+u' unsubscribed from the notification')
      else:
            parameters = get_true_jid(source[1]+'/'+source[2])
            fp = open(ADMINFILE, 'r')
            txt = eval(fp.read())
            fp.close()
            if parameters in txt:
                  txt.remove(get_true_jid(source[1]+'/'+source[2]))
            else:
                  reply(type, source, u'o you see yourself in this mailing list? I - no!')
                  return
            write_file(ADMINFILE,str(txt))
            reply(type, source, u'emove you from the list of subscribers')
      
def amsg_show(type, source, parameters):
    ADMINFILE = 'static/amsg.txt'
    fp = open(ADMINFILE, 'r')
    txt = eval(fp.read())
    fp.close()
    if len(txt) == 0:
      reply(type, source, u'Subscriber base is empty!')
      return
    p =1
    spisok = ''
    for usr in txt:
          spisok += str(p)+'. '+usr+'\n'
          p +=1
    reply(type, source, u'Subscribers notifications (total '+str(len(txt))+u'):\n'+spisok)
          
def amsg_clear(type, source, parameters):
    ADMINFILE = 'static/amsg.txt'
    write_file(ADMINFILE,str('[]'))
    reply(type, source, u'cleared the list of subscribers')

def amsg_blacklist(type, source, parameters):
      ADMINFILE = 'static/blacklist.txt'
      if not parameters:
            reply(type, source, u'its not the correct format, read the help on command')
            return
      params = parameters.split(' ', 1)
      if len(params) == 2:

            if params[0] == 'add':
                  fp = open(ADMINFILE, 'r')
                  txt = eval(fp.read())
                  fp.close()
                  a = params[1].split('|', 1)
                  if txt.has_key(a[0].lower()):
                        reply(type, source, u'This JID already in the black list')
                        return
                  else:
                        if len(a) == 1:
                              txt[a[0].lower()] = u'Locked'
                        elif len(a) == 2:
                              txt[a[0].lower()] = a[1]
                              
                        write_file(ADMINFILE, str(txt))
                        reply(type, source, u'JID added to black list')

            elif params[0] == 'del':
                  fp = open(ADMINFILE, 'r')
                  txt = eval(fp.read())
                  fp.close()
                  if txt.has_key(params[1].lower() ):
                        del txt[params[1].lower()]
                        write_file(ADMINFILE, str(txt))
                        reply(type, source, u'JID removed from the black list')
                  else:
                        reply(type, source, u'JID is absent in the black list')
            else:
                  reply(type, source, u'Unknown command')
                  return
      elif len(params) == 1:
            if params[0] == 'show':
                  fp = open(ADMINFILE, 'r')
                  txt = eval(fp.read())
                  fp.close()
                  p = 1
                  spisok = ''
                  if len(txt.keys()) == 0:
                        reply(type, source, u'The black list is empty')
                        return
                  for usr in txt.keys():
                        spisok += str(p)+'. '+usr+' ('+txt[usr]+')\n'
                        p +=1
                  reply(type, source, u'Black list (total '+str(len(txt.keys()))+u'):\n'+spisok)
      else:
            reply(type, source, u'Unknown command')
            return

def checkbl(jid):
      jid = jid.lower()
      ADMINFILE = 'static/blacklist.txt'
      fp = open(ADMINFILE, 'r')
      txt = eval(fp.read())
      fp.close()

      if txt.has_key(jid):
            return txt[jid]
      else:
            return 0
      

register_command_handler(handler_amsg, 'amsg', ['all','amsg'], 0,'Sends a message to all administrators on the bot jid, specify from whom the message - do not, the bot itself shows the conference and the nickname of the sender.','amsg', ['amsg Hello, there are some problems, please come to me'])
#register_command_handler(handler_amsg, '.blade', ['all','amsg'], 0,'Sends a message to all administrators on the bot jid, specify from whom the message - do not, the bot itself shows the conference and the nickname of the sender.','amsg', ['.oxygen Hello, there are some problems, please come to me'])
register_command_handler(handler_amsg, 'message_admin', ['all','amsg'], 0,'Sends a message to all administrators on the bot jid, specify from whom the message - do not, the bot itself shows the conference and the nickname of the sender.','message_admin', ['message_admin Hello, there are some problems, please come to me'])
register_command_handler(amsg_subscribe, 'amsg_subscribe', ['all','amsg','superadmin'], 100, 'Subscription notification plugin amsg. List of jid`s which will be sent the message. Without the option its mean adds your jid', 'amsg_subscribe <jid>', ['amsg_subscribe user@server.tld'])
register_command_handler(amsg_unsubscribe, 'amsg_unsubscribe', ['all','amsg','superadmin'], 100, 'Unsubscription notifications plug amsg. Without the option means removes your jid', 'amsg_unsubscribe <jid>', ['amsg_unsubscribe user@server.tld'])
register_command_handler(amsg_show, 'amsg_show', ['all','amsg','superadmin'], 100, 'Viewing subscribers.', 'amsg_show', ['amsg_show'])
register_command_handler(amsg_clear, 'amsg_clear', ['all','amsg','superadmin'], 100, 'Purification of the list of subscribers', 'amsg_clear', ['amsg_clear'])
register_command_handler(amsg_blacklist, 'amsg_blacklist', ['all','amsg','superadmin'], 100, 'Block users (the command amsg will be unavailable)', 'amsg_blacklist <add|del|show>', ['amsg_blacklist add user@server.tld','amsg_blacklist add user@server.tld|reason','amsg_blacklist del user@server.tld','amsg_blacklist show'])
