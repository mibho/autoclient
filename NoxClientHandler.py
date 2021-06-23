#--------------------------------------
# system/native imports 
#--------------------------------------
import subprocess
import time

#--------------------------------------
# public/3rd-party imports 
#--------------------------------------
import win32gui, win32con, win32ui

from ppadb.client import Client as AdbClient
#--------------------------------------
# project specific imports  
#--------------------------------------

#--------------------------------------
class cNoxClientHandler():
    def __init__(self, clientNo, wName, width, height, whichEmu):

        #self.deviceList = {} #implement multi-process 

        self.noxInfoDict = { 'clientNum'    : clientNo,
                             'windowName'   : wName,
                             'isNoxOn'      : False,
                             'clientWidth'  : width,
                             'clientHeight' : height + 33, 
                             'emuType'      : whichEmu  #0 = Nox, #1 = BlueStacks
                            }
        self.hwnd = win32gui.FindWindow(None, wName)
        self.connectADB()


    
    def initCheck(self):
        # if handle to window not found (ie, app isnt running), start it
        if self.noxInfoDict['emuType'] == 0:
            if not self.hwnd:
                win32ui.MessageBox("Starting up Nox, please wait...", "Error - Nox Client not found")
                subprocess.Popen(["Nox.exe", "-clone:Nox_" + str(self.noxInfoDict['clientNum'])  ])
                # if nox opens late due to lag or w/e, keep looking until found
                while not self.hwnd:
                    time.sleep(1)
                    self.hwnd = win32gui.FindWindow(None, self.noxInfoDict['windowName'])
        else:
            if not self.hwnd:
                win32ui.MessageBox("Please launch Bluestacks!", "Error - BlueStacks Client not found")
                while not self.hwnd:
                    print("checking for BlueStacks instance...")
                    time.sleep(1)
                    self.hwnd = win32gui.FindWindow(None, self.noxInfoDict['windowName'])


    def connectADB(self):
        #if self.noxInfoDict['isNoxOn'] and self.noxInfoDict['emuType'] == 0: 
            self.client = AdbClient(host="127.0.0.1", port=5037)
       # else:
         #   self.client = AdbClient(host="127.0.0.1", port=5555)

            for d in self.client.devices():
                self.deviceInfo = d.serial     
                print("current device info: ")
                print(self.deviceInfo + "\n")
            self.device = self.client.device(self.deviceInfo)

#           device2 = client.device("127.0.0.1:62001")

    def checkNoxStillRunning(self):
        if not self.hwnd:
           self.noxInfoDict['isNoxOn'] = False
           win32ui.MessageBox("Exiting. Please restart the client.", "Error - Nox Client not found")
           exit()