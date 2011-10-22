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

class Resultado:

    def __init__(self):    
        pass    
        
    def readResult(self, host, login, senha, arquivo):
        comando="cat "+arquivo       
        ssh= SSHController()
        resposta=ssh.run_atomic_command(host, login, senha, comando)
        print resposta
        
    def downloadResult(self, host, login, senha, arquivoRem, arquivoLoc):        
        ssh= SSHController()
        ssh.scp(host, login, senha, arquivoRem, arquivoLoc)
        print arquivoLoc
        
def main():
    option="READ"
    host="narwhal"
    login="login"
    senha="password"
    arquivo="/home/tlechuga/hello2.log"
    arquivoLoc="/tmp/sharcnet.result"
    
    if (len(sys.argv) < 6):#nao passou todos os parametros
        print "Usage"
        print "python sharcresult.py READ|GET host login password archive [localArchive]"
        
        print "MODULO DE TESTE, EXECUTANDO OPCAO PADRAO"        
    else:
        option=sys.argv[1]
        host=sys.argv[2]
        login=sys.argv[3]
        senha=sys.argv[4]
        arquivo=sys.argv[5]
        
        if (len(sys.argv) >=7):         
            arquivoLoc=sys.argv[6]
        
    programa=Resultado()
    
    if (not host.endswith(".ca")):
        host=host+".sharcnet.ca"    
               
    if(option.upper()=="READ"):     
        programa.readResult(host, login, senha, arquivo)
    else:
        programa.downloadResult(host, login, senha, arquivo, arquivoLoc)
    
    

if __name__ == '__main__':
    try:
        main()
    except pexpect.ExceptionPexpect, e:
        print str(e)
