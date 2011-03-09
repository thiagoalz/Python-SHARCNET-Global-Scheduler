#  Copyright (c) 2009, Thiago Lechuga
#
#  ServerList.py is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

 
"""

@author: Thiago Lechuga
@copyright: (C) 2009 Thiago Lechuga
@license: GNU General Public License (GPL)
"""

from Servers.Server import *
from datetime import *
import ConfigParser
import sys
import time
from SSH.SSHControllerMod import *


class ServerList:
    _servers=[]
    _ultima_atualizacao=None
    _tempo_atualizacao=None    

    def __init__(self, user, password):
        #Obtendo configuracoes do arquivo ini       
        configdict = ConfigParser.ConfigParser()
        configdict.read('/home/thiago/workspace/Escalonador/src/principal/Servers/servers.conf')
        datasalva=configdict.getfloat('DEFAULT','last_upate')
        self._ultima_atualizacao=datetime.fromtimestamp(datasalva)
        self._tempo_atualizacao=configdict.getint('DEFAULT','update_time')
        self._carregaServers(user, password)
        
    def _carregaServers(self, user, password):
        delta=datetime.now()-self._ultima_atualizacao
        if(delta.days>0 or delta.seconds>self._tempo_atualizacao):
            print "Status NAO Atualizado"
            print "Atualizando informacoes dos Servidores"
            self._atualizar(user, password)
        else:
            print "Status Atualizado"
            print "Carregando informacoes do arquivo"
            
            configdict = ConfigParser.ConfigParser()
            configdict.read('/home/thiago/workspace/Escalonador/src/principal/Servers/servers.conf')
            self._servers=[]
            sections=configdict.sections()
            for atual in sections:
                name=configdict.get(atual,'name')
                host=configdict.get(atual,'host')
                status=configdict.get(atual,'status')
                CPU_total=configdict.getint(atual,'CPU_total')
                CPU_idle=configdict.getint(atual,'CPU_idle')
                CPU_busy=configdict.getint(atual,'CPU_busy')
                CPU_queued=configdict.getint(atual,'CPU_queued')
                jobs_runing=configdict.getint(atual,'jobs_runing')
                jobs_queued=configdict.getint(atual,'jobs_queued')
                features=configdict.get(atual,'features')
                server=Server(name, host, status, CPU_total, CPU_idle, CPU_busy, CPU_queued, jobs_queued, jobs_runing,features)
                self._servers.append(server)                
                
            self._servers.sort(self._comparaServers)            
        
        
    def _atualizar(self, user, password):
        configServers = ConfigParser.RawConfigParser() #Criando o novo arquivo de servers
        delta=datetime.now()-self._ultima_atualizacao
        if(delta.days>0 or delta.seconds>self._tempo_atualizacao):
            #Lendo o qrquivo ini com os servers
            configIni = ConfigParser.ConfigParser()
            configIni.read('/home/thiago/workspace/Escalonador/src/principal/config.ini')
            servers=configIni.items("servers")
            self._servers=[]
            
            ssh= SSHController()
            
            for atual in servers:
                name=atual[0]
                split=atual[1].split(" ")#aqui tem infos de host e caracteristicas
                host=split[0]
                try:
                    features=split[1]
                except IndexError:
                    features=""
                
                #Conecta ao servidor e salva a resposta
                try:                    
                    resposta=ssh.run_atomic_sqjobs(host, user, password)   
                    
                    #separando informacao util
                    lines = resposta.splitlines()
                    if len(lines) > 3: #Se nao tiver ng na fila vem so com as ultimas linhas
                        del lines[0:2] #sem nada que presta nas 2 primeiras linhas
                    
                    lastLine=lines.pop() # a ultima linha nunca eh importante
                    lastLine=lines.pop() # as vezes eh importante e as vezes nao                    
                    if lastLine.find("reserved cpus") > -1:#verifica se deve tirar mais uma linha
                        lastLine=lines.pop()
                    
                    print name+"--->"+ lastLine                
                                        
                    #lendo a fila para contar as CPUs 
                    CPU_queued=0;
                    for linhaAtual in lines:
                        split=linhaAtual.split(" ")
                        
                        #removendo linhas sm nada
                        qtd=split.count('')
                        for i in range(qtd):
                            split.remove('')
                                
                        #print split
                        #ESSE ALGORITMO ESTA ERRADO... porque mode ter omitido caras com CPU diferente
                        #Como 99% dos casos funciona deixei assim e depois tento arrumar
                        if split[2]=="omitted":#ARMENGUE DOS INFERNOS, TEM SERVER QUE APARECE 'MORE JOBS omitted' e tem server que aparece 'JOBS omitted'
                            split.insert(2,"MORE")
                        if split[3]=="omitted": #mostrou 5 do usuario e omitiu o resto
                            split[4]=split[4][1:]
                            qtdOmitido=int(split[4])-5
                            CPU_queued+=( qtdOmitido *  anterior) #To assumindo que todos sao iguais ao anterior
                        else:
                            CPU_queued+=int(split[4])
                            anterior=int(split[4])
                                
                    split=lastLine.split(" ")
                                
                    CPU_total=int(split[0])    
                    CPU_idle=int(split[3])
                    CPU_busy=int(split[5])
                    jobs_runing=int(split[7])
                    jobs_queued=int(split[12])                
                    status="busy"
                    if(jobs_queued==0):
                        status="idle"                    
                    
                    #Coloca o objeto na lista
                    self._servers.append(Server(name, host, status, CPU_total, CPU_idle, CPU_busy, CPU_queued, jobs_queued, jobs_runing, features))
                    
                    #Coloca o objeto para ser escrito no arquivo
                    configServers.add_section(name)
                    configServers.set(name,'name', name)
                    configServers.set(name,'host', host)
                    configServers.set(name,'status', status)
                    configServers.set(name,'CPU_total', CPU_total)
                    configServers.set(name,'CPU_idle', CPU_idle)
                    configServers.set(name,'CPU_busy', CPU_busy)
                    configServers.set(name,'CPU_queued', CPU_queued)
                    configServers.set(name,'jobs_runing', jobs_runing)
                    configServers.set(name,'jobs_queued', jobs_queued)
                    configServers.set(name,'features', features)
                except:
                    print "Erro ao contactar",name
                
            self._servers.sort(self._comparaServers)
            
            #Escreve o arquivo de configuracao dos servidores
    
            configServers.set('DEFAULT','last_upate', time.time())
            configServers.set('DEFAULT','update_time', self._tempo_atualizacao)
                    
            # Writing our configuration file
            configfile = None
            try:
                configfile = open('/home/thiago/workspace/Escalonador/src/principal/Servers/servers.conf', 'wb')
                configServers.write(configfile)
            except IOError:
                print "Cannot find open the file", '/home/thiago/workspace/Escalonador/src/principal/Servers/servers.conf'
        else:
            print "Servidores ja estavam atualizados" 

    
    def getBestServer(self, features):        
        #self._servers.sort(self._comparaServers) # ja estou chamando essa funcao quando  crio a lista de servers
        melhor=None
        contrMelhor=-1
        for serverAtual in self._servers:
            contLetras=0
            
            for letra in features:
                if serverAtual.getFeatures().find(letra)>=0 or serverAtual.getFeatures().find(letra. upper())>=0:
                    contLetras+=1
                    
            if contLetras>contrMelhor:
                contrMelhor=contLetras
                melhor=serverAtual
            
            if contLetras==len(features):
                #Encontrou um perfeito
                print "Requisitos preenchidos"
                return melhor
                
        print "Nao foi encontrado um servidor com os requisitos. Retornando o mais proximo"
        return melhor
    
    def _comparaServers(self, server1, server2):
        filaRelativaServer1=float(server1.getCPU_queued())/float(server1.getCPU_total())
        filaRelativaServer2=float(server2.getCPU_queued())/float(server2.getCPU_total())
        
        if filaRelativaServer1< filaRelativaServer2:
            return -1 # Se o primeiro tem menos fila, ele e melhor
        elif filaRelativaServer2< filaRelativaServer1:
            return 1 # Se o segundo que tem menor fila, ele e o melhor
        else: #nesse caso a fila dos dois e igual        
            #Campara pela quantidade de processadores de casa um
            if server1.getCPU_total()> server2.getCPU_total():
                return -1 # Se o primeiro tem mais processadores, ele e melhor
            elif server2.getCPU_total()> server1.getCPU_total():
                return 1 # Se o segundo que tem mais processadores, ele e o melhor
            else:
                return 0
        #nao deve chegar aqui nunca
        return 0
        