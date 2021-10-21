
import BotFunctions as AutoClient
from Constants import *
from ROICoords import cScanCoords as coords
from pdb import set_trace as bp
import random
import NoxClientManager as NoxMgr

import multiprocessing
import time
if __name__ == '__main__':   
    nprocs = multiprocessing.cpu_count()
    print(nprocs)
    n_mgr = NoxMgr.NoxClientManager()
    n_mgr.autoDetectNoxProcesses()
    print(n_mgr.detectedDevicesADBList)
    
    z = {} 
    pList = {}
    for key in n_mgr.detectedDevicesADBList:
        z[key] = AutoClient.cBotFunctions( n_mgr.detectedDevicesADBList[key][0], n_mgr.detectedDevicesADBList[key][1], \
                                            n_mgr.detectedDevicesADBList[key][2], n_mgr.adbConnectedDevs[key], "lol")
    '''
    for key in n_mgr.detectedDevicesADBList:
        test = AutoClient.cBotFunctions( n_mgr.detectedDevicesADBList[key][0], n_mgr.detectedDevicesADBList[key][1], \
                                            n_mgr.detectedDevicesADBList[key][2], n_mgr.adbConnectedDevs[key], "lol")
    '''
    #while 1:
    #test.doEliteDung(0)
    #print(z)
    #time.sleep(2)
    #print(n_mgr.adbConnectedDevs)
    #print("ok these adb connected")
    #time.sleep(3)
    #(self, pID, windowName, clientNum, deviceObj, adbSockInfo):
    #cObj = AutoClient.cBotFunctions(740, "iceyooh lsmurf 3118", 6, n_mgr.adbConnectedDevs[62030], "127.0.0.1:62030" )
    #cObj2 = AutoClient.cBotFunctions(17812, "iceyay lsmurf6618", 5, n_mgr.adbConnectedDevs[62029], "127.0.0.1:62029" )
    
    print("OK WE MADE AST THIS")
    for i in z:
        pList[i] = multiprocessing.Process(target=z[i].botLoop)
        print("GOT OBJ: " + str(i))
    
    for i in pList:
        pList[i].start()
    
    for i in pList:
        pList[i].join()
    print("started")
    print("HOLY WAT")
     