#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin



def admin_getglobadmins(type, source, parameters):
        res1 = u'List of global administrators:'
        res2 = u'List of global ignore:'
        res3 = u'List of local administrators:'
        res4 = u'List of local ignore:'
        
        res1_ = u''
        res2_ = u''
        res3_ = u''
        res4_ = u''
        i = 0
        j = 0
        k = 0
        a = 0
        if len(GLOBACCESS) == 1:
                reply(type, source, u'global access empty')
                return
        for jid in GLOBACCESS:
                if GLOBACCESS[jid] >=41:
                        i += 1
                        if GLOBACCESS[jid] == 100:
                                inf = ''
                        else:
                                inf = ': '+str(GLOBACCESS[jid])
                        res1_+= '\n'+str(i)+'. '+jid+inf
                        
                if GLOBACCESS[jid] <0:
                        j += 1
                        if GLOBACCESS[jid] == -100:
                                inf_ = ''
                        else:
                                inf_ = ': '+str(GLOBACCESS[jid])
                        res2_ += '\n'+str(j)+'. '+jid+inf_
#*************************************************************************#

        for conf in ACCBYCONF:
                for jid in ACCBYCONF[conf]:
                        if ACCBYCONF[conf][jid] >= 41:
                                k +=1
                                if ACCBYCONF[conf][jid] == 100:
                                        inf__ = ''
                                else:
                                        inf__ = ': '+str(ACCBYCONF[conf][jid])
                                res3_ += '\n'+str(k)+'. '+jid+inf__
                        if ACCBYCONF[conf][jid] <= 0:
                                a +=1
                                if ACCBYCONF[conf][jid] == -100:
                                        inf___ = ''
                                else:
                                        inf___ = ': '+str(ACCBYCONF[conf][jid])
                                res4_ += '\n'+str(a)+'. '+jid+inf___                                
        if res1_ == '':
                res1_ = u'\nempty'
        if res2_ == '':
                res2_ = u'\nempty'
        if res3_ == '':
                res3_ = u'\nempty'
        if res4_ == '':
                res4_ = u'\nempty'
                
        res1 += res1_
        res2 += res2_
        res3 += res3_
        res4 += res4_
        
#        reply(type, source, res1+'\n'+res2+'\n'+res3+'\n'+res4)
        reply(type,source,u'sent to private')
        reply('private', source, res1+'\n'+res2+'\n'+res3+'\n'+res4)


register_command_handler(admin_getglobadmins, 'access_ext', ['superadmin','admin','new','all'], 100, 'Show all global and local access', 'access_ext', ['access_ext'])
