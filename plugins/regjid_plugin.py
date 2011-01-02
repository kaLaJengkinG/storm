#===istalismanplugin===
# -*- coding: utf-8 -*- 40tman

import os, xmpp, time, sys, time, pdb, urllib, threading, types, random

LAST_REG_JID={}
JID_REG_TIME={}

def generate_reg(_len = None, sg = None):
  if sg == None:
    sg = 'aoeuizxcvbnmsdfghjklqwrtyp1234567890'
  if _len == None:
    _len = random.Random().randint(1, 100)
  s = ''
  l = len(sg)
  while _len > 0:
    s += sg[random.Random().randint(0, l - 1)]
    _len -= 1
  return s

  
def hnd_gonew_jid(type,source,parameters):
  l = parameters.lower()
  s= parameters.split()
  jid=get_true_jid(source[1]+'/'+source[2])
  if jid in JID_REG_TIME:
    if time.time() - JID_REG_TIME[jid]['time']<30:
      reply(type,source,u'time limit, wait for 30 seconds')
      return
    else:
      JID_REG_TIME[jid]['time']=time.time()
  if not jid in JID_REG_TIME:
    JID_REG_TIME[jid]={'time':time.time()}
  if not parameters:
    reply(type,source,u'and?')
    return
  if len(parameters)>50:
    reply(type,source,u'booo too much!')
    return
  if not l.count(u'@')>0:
    reply(type,source,u'jid should be match the form ')
    return
  if not l.count(u'.')>0:
    reply(type,source,u'incorrectly entered the server name')
    return
  aka=l.split('@')
  dom=aka[1].split()[0]
  reply(type,source,'Ok')
  LAST_REG_JID[source[1]+'/'+source[2]]={}
  pas = generate_reg(random.Random().randint(5,10))
  if l.count(' ')>0:
    pas = s[1]
  name, domain, password, newBotJid, mainRes = aka[0], dom, pas, 0,'QIP'
  print u'START'
  node = name
  jid = xmpp.JID(node=node, domain=domain, resource=mainRes)
  cl = xmpp.Client(jid.getDomain(), debug=[])
  con = cl.connect()
  if not con:
    reply(type,source,u'unable to connect to '+s[0])
    return
  cl.RegisterHandler('message', hnd_newreg_Hnd)
  try:
    xmpp.features.register(cl, domain, {'username': node, 'password':password})
    print u'Registered'
  except:
    reply(type,source,u'cannot register '+unicode(JCON.lastErr)+', '+unicode(JCON.lastErrCode))
  try:
    au=cl.auth(jid.getNode(), password, jid.getResource())
    if not au:
      reply(type,source,u'failed on registration, perhaps jid had been used and/or exceeded server time limit')
      return
  except UnicodeEncodeError:
    reply(type,source,u'unicode encoding error') #русский пока не поддерживаеться плагином
    return
  cl.sendInitPresence()
  reply(type,source,u'successfully register as: '+node+'@'+domain+u'\n with password: '+password)
  threading.Thread(None, hnd_regs_timer, 'at'+str(random.randrange(0, 999)), (type, source)).start()
  while LAST_REG_JID:
    cl.Process(1)
  print 'unavibile'
  try:
    cl.disconnect()
  except:
    pass

def hnd_regs_timer(cl):
  time.sleep(30)
  try:
    cl.disconnect()
  except:
    pass
  
    
def hnd_newreg_Hnd(cl,mess):
  print '1 mess!'
  try:
    body=mess.getBody()
    if LAST_REG_JID:
      for x in LAST_REG_JID:
        msg(x,body[:450])
        del LAST_REG_JID[x]
  except (RuntimeError,IOError,AttributeError):
    pass
        
    
  
register_command_handler(hnd_gonew_jid, 'regjid', ['all'], 10, 'Register a JID, if you specify only JID, the password will generate by the bot (5-10 characters)', 'regjid <name@server> <password>', ['regjid username@server.tld 12345','regjid username@server.tld'])
