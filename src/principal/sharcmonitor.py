#  Copyright (c) 2009, Thiago Lechuga
#
#  Principal.py is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

 
"""

@author: Thiago Lechuga
@copyright: (C) 2009 Thiago Lechuga
@license: GNU General Public License (GPL)
"""

from Servers.ServerList import *
from SSH.SSHControllerMod import *
import pexpect
import sys
import time

class Monitor:

    def __init__(self):    
        pass        
        
    def monitorar(self, host, login, senha, jobID):
        comando="sqjobs"
        
        print "Monitorando Job: ",jobID," Em: ",host
        ssh= SSHController()
        
        ssh.login(host, login, senha)
        
        terminou=False
        while (not terminou):
            resposta=ssh.run_command(comando)
            pos=resposta.find(jobID)
            
            if (pos!=-1):
                print "Processo Ainda na fila"
                time.sleep(60)
            else:
                print "Processo Concluido"
                terminou=True
                
        ssh.logout()

        print resposta
        
def main():
    host="narwhal"
    login="login"
    senha="password"
    jobID="1234"
    
    if (len(sys.argv) < 5):#nao passou todos os parametros
        print "Usage"
        print "python sharcmonitor.py host login password JobID"
        
        print "MODULO DE TESTE, EXECUTANDO OPCAO PADRAO"        
    else:
        host=sys.argv[1]        
        login=sys.argv[2]
        senha=sys.argv[3]
        jobID=sys.argv[4]                
            
    programa=Monitor()
    
    if (not host.endswith(".ca")):
        host=host+".sharcnet.ca"
           
    programa.monitorar(host, login, senha, jobID)    
    
    

if __name__ == '__main__':
    try:
        main()
    except pexpect.ExceptionPexpect, e:
        print str(e)
