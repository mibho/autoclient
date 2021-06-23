#--------------------------------------
# system/native imports 
#--------------------------------------
import subprocess
import time
import psutil
#--------------------------------------
# public/3rd-party imports 
#--------------------------------------
import win32gui, win32con, win32ui

from ppadb.client import Client as AdbClient
#--------------------------------------
# project specific imports  
#--------------------------------------
import processTools
#--------------------------------------

class NoxClientManager():

    #process's socket index constants
    PROC_SOCK_ADDR_DATA = 3
    PROC_SOCK_TCP_STATUS = 5

    SOCK_ADDR_IP = 0
    SOCK_ADDR_PORT = 1

    

    PROC_ID = 0
    TITLE_INDEX = 1
    HWND_ID = 2
    NOX_EXE = 1
    NOX_VM_HANDLE_EXE = 2

    # {portNumber : }
    def __init__(self):
        self.connectedDevicesList = {}
        self.detectedDevicesADBList = {} # if N devices, and m connected,
        self.waitingDevicesList = {}
        self.adbConnectedDevs = {}
        self.initADB()
    
    def initADB(self):
        self.client = AdbClient(host="127.0.0.1", port=5037) #Nox
       # else:
         #   self.client = AdbClient(host="127.0.0.1", port=5555)
    
    #def getWindowNameFromPID(self, processID):
    #processID, => clientNum, 


    def findNoxInstanceID(self, procObj, pNum): #pNum == 0 thenn "Nox.exe" | 1 then NoxVMHandle.exe
        arg = procObj.cmdline()[pNum]
        clientNum = arg.split("_", 1)
        if(len(clientNum) == 1):
            return 0

        return int(clientNum[1])
    
    def getUsedPorts(self, procObj, portsDict, nID):
        #portsDict = {}
        for proc in procObj.connections("tcp4"):
            if len(proc[self.PROC_SOCK_TCP_STATUS]) == 11: #ESTABLISHED is 11 chars long LOL
                if(proc[self.PROC_SOCK_ADDR_DATA][self.SOCK_ADDR_IP] == "127.0.0.1"):
                    portNo = int(proc[self.PROC_SOCK_ADDR_DATA][self.SOCK_ADDR_PORT])
                    if portNo not in portsDict:
                        portsDict[portNo] = nID

    def returnDetectedPortDict(self):
        tempDict = {}
        for dev in self.client.devices():
            devicePortNo = processTools.getPortFromSockAddress(dev.serial)
            if devicePortNo not in self.adbConnectedDevs:
                self.adbConnectedDevs[devicePortNo] = dev
            tempDict[devicePortNo] = dev 
        
        return tempDict


    def autoDetectNoxProcesses(self):
        noxExeDict = {}
        tcp_addrDict = {}
        adbDevicesDict = {}
        lostDeviceList = []

        for proc in psutil.process_iter():
            if proc.name() == "Nox.exe":
                noxID = self.findNoxInstanceID(proc, self.NOX_EXE)
                nameList = processTools.getWindowNameFromPID(proc.pid)
                name = nameList[0]
                noxExeDict[noxID] = (proc.pid, name)

            elif proc.name() == "NoxVMHandle.exe":
                noxID = self.findNoxInstanceID(proc, self.NOX_VM_HANDLE_EXE)
                self.getUsedPorts(proc, tcp_addrDict, noxID)        


        adbDevicesDict = self.returnDetectedPortDict()
        if len(self.detectedDevicesADBList) > 0:
            for key in self.detectedDevicesADBList:
                if key not in adbDevicesDict:
                    lostDeviceList.append(key)
            if len(lostDeviceList) > 0:
                for lostPort in lostDeviceList:
                    if lostPort in self.detectedDevicesADBList:
                        del self.detectedDevicesADBList[lostPort]
                    if lostPort in self.adbConnectedDevs:
                        del self.adbConnectedDevs[lostPort]


        for devicePortNo in adbDevicesDict:    
            if devicePortNo in tcp_addrDict: #match found!
                clientNo = tcp_addrDict[devicePortNo]
                noxProcInfo = noxExeDict[clientNo]
                if devicePortNo not in self.detectedDevicesADBList:
                    self.detectedDevicesADBList[devicePortNo] = (noxProcInfo[self.PROC_ID], \
                                                                noxProcInfo[self.TITLE_INDEX], \
                                                                clientNo, \
                                                                adbDevicesDict[devicePortNo].serial) 
    
    

    



    def refreshAvailable(self):
        detectedDevices = len(self.client.devices())
        if detectedDevices == 0:
            win32ui.MessageBox("Unable to detect any running clients.", "Error - No instances found")
        else:
            for d in self.client.devices():
                self.deviceInfo = d.serial     
                print("current device info: ")
                print(self.deviceInfo + "\n")
            self.device = self.client.device(self.deviceInfo)


