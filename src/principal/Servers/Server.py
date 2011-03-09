#  Copyright (c) 2009, Thiago Lechuga
#
#  Server.py is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

 
"""

@author: Thiago Lechuga
@copyright: (C) 2009 Thiago Lechuga
@license: GNU General Public License (GPL)
"""


class Server:

    def __init__(self, name, host, status, CPU_total, CPU_idle, CPU_busy, CPU_queued, jobs_queued, jobs_runing, features):
        
        self._name=name
        self._host=host
        self._status=status
        self._CPU_total=CPU_total
        self._CPU_idle=CPU_idle
        self._CPU_busy=CPU_busy
        self._CPU_queued=CPU_queued
        self._jobs_queued=jobs_queued
        self._jobs_runing=jobs_runing        
        self._features=features
        print self

    def getCPU_total(self):
        return self._CPU_total


    def setCPU_total(self, value):
        self._CPU_total = value


    def delCPU_total(self):
        del self._CPU_total


    def getCPU_queued(self):
        return self._CPU_queued


    def setCPU_queued(self, value):
        self._CPU_queued = value


    def delCPU_queued(self):
        del self._CPU_queued


    def getFeatures(self):
        return self._features


    def setFeatures(self, value):
        self._features = value


    def delFeatures(self):
        del self._features

        
        
    def __str__(self):
        return str(self._name+ " " +self._host+ " " +self._status+
                   "\n CPU_total:" +str(self._CPU_total)+
                   "\n CPU_idle:" +str(self._CPU_idle)+
                   "\n CPU_busy:" +str(self._CPU_busy)+
                   "\n CPU_queued:" +str(self._CPU_queued)+
                   "\n jobs_queued:" +str(self._jobs_queued)+
                   "\n jobs_runing:" +str(self._jobs_runing)+                   
                   "\n features:" + str(self._features))

    def getStatus(self):
        return self._status


    def getCPU_idle(self):
        return self._CPU_idle


    def getCPU_busy(self):
        return self._CPU_busy


    def getJobs_runing(self):
        return self._jobs_runing


    def getJobs_queued(self):
        return self._jobs_queued


    def setStatus(self, value):
        self._status = value


    def setCPU_idle(self, value):
        self._CPU_idle = value


    def setCPU_busy(self, value):
        self._CPU_busy = value


    def setJobs_runing(self, value):
        self._jobs_runing = value


    def setJobs_queued(self, value):
        self._jobs_queued = value


    def delStatus(self):
        del self._status


    def delCPU_idle(self):
        del self._CPU_idle


    def delCPU_busy(self):
        del self._CPU_busy


    def delJobs_runing(self):
        del self._jobs_runing


    def delJobs_queued(self):
        del self._jobs_queued
    

    def getName(self):
        return self._name


    def getHost(self):
        return self._host


    def setName(self, value):
        self._name = value


    def setHost(self, value):
        self._host = value


    def delName(self):
        del self._name


    def delHost(self):
        del self._host


    name = property(getName, setName, delName, "Name's Docstring")

    host = property(getHost, setHost, delHost, "Host's Docstring")
    
    status = property(getStatus, setStatus, delStatus, "Status's Docstring")

    CPU_idle = property(getCPU_idle, setCPU_idle, delCPU_idle, "CPU_idle's Docstring")

    CPU_busy = property(getCPU_busy, setCPU_busy, delCPU_busy, "CPU_busy's Docstring")

    jobs_runing = property(getJobs_runing, setJobs_runing, delJobs_runing, "Jobs_runing's Docstring")

    jobs_queued = property(getJobs_queued, setJobs_queued, delJobs_queued, "Jobs_queued's Docstring")

    features = property(getFeatures, setFeatures, delFeatures, "Features's Docstring")

    CPU_queued = property(getCPU_queued, setCPU_queued, delCPU_queued, "CPU_queued's Docstring")

    CPU_total = property(getCPU_total, setCPU_total, delCPU_total, "CPU_total's Docstring")
