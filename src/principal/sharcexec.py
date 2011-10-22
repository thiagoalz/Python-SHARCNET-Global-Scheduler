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

class Principal:

    def __init__(self):    
        pass    
        
    def executaComandoAuto(self, login, senha, comando, features):
        self._iniServerList(login, senha)
        servidor=self._servidores.getBestServer(features)
        print "Executando comando em->",servidor
        ssh= SSHController()
        resposta=ssh.run_atomic_command(servidor.getHost(), login, senha, comando)
        print "====RESPOSTA===="
        print resposta,servidor.getHost()
        
    def executaComando(self, host, login, senha, comando):
        print "Executando comando em->",host,"[FORCADO]"
        ssh= SSHController()
        resposta=ssh.run_atomic_command(host, login, senha, comando)
        print "====RESPOSTA===="
        print resposta,servidor.getHost()
        
    def _iniServerList(self, user, password):
        self._servidores= ServerList(user, password)
        
def main():
    host="auto"
    login="login"
    senha="password"
    features="N"
    comando="sqsub -q mpi -n 7 -r 4 -o hello2.log ./hello2"
    
    if (len(sys.argv) < 6):#nao passou todos os parametros
        print "Usage"
        print "python sharcexec.py host|auto login password features|N command"
        
        print "MODULO DE TESTE, EXECUTANDO OPCAO PADRAO"        
    else:
        host=sys.argv[1]        
        login=sys.argv[2]
        senha=sys.argv[3]
        features=sys.argv[4]
        comando = [item + ' ' for item in sys.argv[5:]]
        comando=''.join(comando)
        
    if features=="N" or features=="n": #Faco assim so para garantir que conheco a quantidade de parametros sempre
        features=""                
            
    programa=Principal()
    if host.upper()=="AUTO":
        programa.executaComandoAuto(login, senha, comando,features)
    else:
        if (not host.endswith(".ca")):
            host=host+".sharcnet.ca"            
        programa.executaComando(host, login, senha, comando)    
    
    

if __name__ == '__main__':
    try:
        main()
    except pexpect.ExceptionPexpect, e:
        print str(e)
