#  Copyright (c) 2009, Thiago Lechuga
#
#  SSHController.py is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

 
"""

@author: Thiago Lechuga
@copyright: (C) 2009 Thiago Lechuga
@license: GNU General Public License (GPL)
"""

import pexpect
import sys, getpass
import ConfigParser, os

class SSHController:


    def __init__(self):
        
        #Obtendo configuracoes do arquivo
        configdict = ConfigParser.ConfigParser()
        configdict.read('/home/thiago/workspace/Escalonador/src/principal/config.ini')        

        #self.COMMAND_PROMPT = '[$#] '
        #self.TERMINAL_PROMPT = r'Terminal type\?'
        #self.TERMINAL_TYPE = 'vt100'
        #self.SSH_NEWKEY = r'Are you sure you want to continue connecting \(yes/no\)\?'
        
        self.COMMAND_PROMPT = configdict.get('system','COMMAND_PROMPT')
        self.TERMINAL_PROMPT = configdict.get('system','TERMINAL_PROMPT')
        self.TERMINAL_TYPE = configdict.get('system','TERMINAL_TYPE')
        self.SSH_NEWKEY = configdict.get('system','SSH_NEWKEY')                
        
        self.child=None;

    
    def login(self, host, user, password):
    
        self.child = pexpect.spawn('ssh -l %s %s'%(user, host))
    
        i = self.child.expect([pexpect.TIMEOUT, self.SSH_NEWKEY, '[Pp]assword: '])
        if i == 0: # Timeout
            print 'ERROR!'
            print 'SSH could not login. Here is what SSH said:'
            print self.child.before, self.child.after
            sys.exit (1)
        if i == 1: # SSH does not have the public key. Just accept it.
            self.child.sendline ('yes')
            self.child.expect ('[Pp]assword: ')
        self.child.sendline(password)
        # Now we are either at the command prompt or
        # the login process is asking for our terminal type.
        i = self.child.expect (['Permission denied', self.TERMINAL_PROMPT, self.COMMAND_PROMPT])
        if i == 0:
            print 'Permission denied on host:', host
            sys.exit (1)
        if i == 1:
            self.child.sendline (self.TERMINAL_TYPE)
            self.child.expect (self.COMMAND_PROMPT)
        return self.child
    
    def logout(self):
        """Close the connection to the remote host.
            
        """
        self.child.sendline('exit')
        self.child=None        


#===============================================================================
# # (current) UNIX password:
# def change_password(child, user, oldpassword, newpassword):
# 
#    child.sendline('passwd') 
#    i = child.expect(['[Oo]ld [Pp]assword', '.current.*password', '[Nn]ew [Pp]assword'])
#    # Root does not require old password, so it gets to bypass the next step.
#    if i == 0 or i == 1:
#        child.sendline(oldpassword)
#        child.expect('[Nn]ew [Pp]assword')
#    child.sendline(newpassword)
#    i = child.expect(['[Nn]ew [Pp]assword', '[Rr]etype', '[Rr]e-enter'])
#    if i == 0:
#        print 'Host did not like new password. Here is what it said...'
#        print child.before
#        child.send (chr(3)) # Ctrl-C
#        child.sendline('') # This should tell remote passwd command to quit.
#        return
#    child.sendline(newpassword)
#===============================================================================
    def scp(self,host, login, senha, arquivoRem, arquivoLoc):
        comando="scp "+login+"@"+host+":"+arquivoRem +" "+ arquivoLoc        
        foo = pexpect.spawn(comando)
    
        i = foo.expect([pexpect.TIMEOUT, self.SSH_NEWKEY, '[Pp]assword: '])
        if i == 0: # Timeout
            print 'ERROR!'
            print 'SSH could not login. Here is what SSH said:'
            print foo.before, foo.after
            sys.exit (1)
        if i == 1: # SSH does not have the public key. Just accept it.
            foo.sendline ('yes')
            foo.expect ('[Pp]assword: ')
        foo.sendline(senha)
        try:
            foo.expect(self.COMMAND_PROMPT)
        except pexpect.EOF, e:
            pass
            #Parece que quando termina o comando ele termina o spawn. Ai esse erro eh normal
            
        #print comando
        #foo = pexpect.spawn(comando)
        #foo.expect('[Pp]assword: ')
        #foo.sendline(senha)
        #foo.expect (self.COMMAND_PROMPT)
        #foo.interact()
        foo=None


    def run_command(self, cmd):
    
        self.child.sendline(cmd) 
        self.child.expect (self.COMMAND_PROMPT)
        return self.__strip_output(cmd, self.child.before)
        
    def run_sqjobs(self):
        return self.run_command('sqjobs -qa')
    
    def run_atomic_sqjobs(self, host, user, password):
        resposta=self.run_atomic_command(host, user, password, 'sqjobs -qa')
        if resposta=="":#Nao tinha ng na fila e retornou vazio
            resposta=self.run_atomic_command(host, user, password, 'sqjobs -n')#colcoa so as infos gerais do host
        return resposta
    
    def run_atomic_command(self, host, user, password, command):
        """Connect to a remote host, login, run a command, and close the connection.
            
        @param command: Unix command
        @return: Command output
        @rtype: String
        """
        self.login(host, user, password)
        command_output = self.run_command(command)
        self.logout()
        return command_output
    
    def __strip_output(self, command, response):
        """Strip everything from the response except the actual command output.
            
        @param command: Unix command        
        @param response: Command output
        @return: Stripped output
        @rtype: String
        """
        lines = response.splitlines()
        # if our command was echoed back, remove it from the output
        if command in lines[0]:
            lines.pop(0)
        # remove the last element, which is the prompt being displayed again
        lines.pop()
        # append a newline to each line of output
        lines = [item + '\n' for item in lines]
        # join the list back into a string and return it
        return ''.join(lines)

def main():

    connection=SSHController()
    connection.login('bull.sharcnet.ca', 'login', 'password')
    #print connection.run_command("sqsub -q mpi -n 7 -r 4 -o hello2.log ./hello2")
    print connection.run_sqjobs()
    connection.logout()
    

if __name__ == '__main__':
    try:
        main()
    except pexpect.ExceptionPexpect, e:
        print str(e)
