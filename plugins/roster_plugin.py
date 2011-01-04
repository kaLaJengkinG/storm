#===istalismanplugin===
# -*- coding: utf-8 -*-


def roster_sub(type,source,parameters):
        if parameters:
                if not parameters.count('@') or not parameters.count('.'):
                        reply(type,source,u'read the help command!')
                        return
                ROSTER = JCON.getRoster()
                ROSTER.Subscribe(parameters)
                reply(type,source,u'subscribed!')

def roster_unsub(type,source,parameters):
        if parameters:
                if  not parameters.count('@') or not parameters.count('.'):
                        reply(type,source,u'read the help command!')
                        return
                ROSTER = JCON.getRoster()
                ROSTER.Unsubscribe(parameters)
                ROSTER.delItem(parameters)
                reply(type,source,u'unsubscribed!')

def roster_show(type,source,parameters):
        ROSTER = JCON.getRoster()
        list, col = '', 0
        rep = ROSTER.getItems()
        for jid in rep:
                if not jid.count('@conf'):
                    col = col + 1
                    list += '\n'+str(col)+'. '+jid
        if col != 0:
                reply(type, source, (u'\nTotal: %s contacts in my roster:' % str(col))+list)
        else:
                reply(type, source, u'My roster is empty...')
		
register_command_handler(roster_show, 'roster_show', ['superadmin','all'], 100, 'Show contacts on bot roster.', 'roster_all', ['roster_show'])		
register_command_handler(roster_sub, 'roster_add', ['superadmin','all'], 100, 'Add a contact on bot roster.', 'roster_add <jid>', ['roster_add guy@server.tld'])
register_command_handler(roster_unsub, 'roster_del', ['superadmin','all'], 100, 'Delete a contact on bot roster.', 'roster_del <jid>', ['roster_del guy@server.tld'])
