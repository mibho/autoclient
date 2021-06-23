#--------------------------------------
# system/native imports 
#--------------------------------------
import time
#--------------------------------------
# public/3rd-party imports 
#--------------------------------------
import numpy as np
import cv2 as cv
#--------------------------------------
# project specific imports  
#--------------------------------------

from BotFunctionsTools import cBotFunctionsTools
from Constants import *
from autodb import clientDB
from ROICoords import cScanCoords as coords
#--------------------------------------



#class cBotFunctions(c cBotData):
class cBotFunctions(cBotFunctionsTools):
    def __init__(self, pID, windowName, clientNum, deviceObj, adbSockInfo):
        cBotFunctionsTools.__init__(self, pID, windowName, clientNum, deviceObj, adbSockInfo)
        print("loading..")
        self.dbConn = clientDB("autoTest.db", windowName, clientNum)
        print("successfully passed clientDB obj creation!")
        self.updateRequired = False
        self.patchSuccess = False
    
    def update():
        pass
    
    def botLoop(self, whichFeature, enabled):
        while enabled:
            time.sleep(1)
            #load data from db
            level = self.gameState.returnStageNum()
            self.gameState.printTest()
            if level == stateConstants.L0_at_home_scr:
                if self.errorMsgFound:
                    print("Error lol")
                    #send touch. 
                if self.scanThisROI(self.templateDict['SCHK_0atHomeScreen'],0,457, 0, 865, 0.8, True):
                    print("MSM located! opening...")
                    self.sendTimedTap(self.matchCoords.xyLoc[0] + 5, self.matchCoords.xyLoc[0] + 20, self.matchCoords.xyLoc[1] - 45, self.matchCoords.xyLoc[1] - 30, 0.03)
                    if self.gameState.crashed:
                        self.gameState.resetOnCrash()
            elif level == stateConstants.L1_at_start_ban:
                self.patchSuccess = True
                if self.scanThisROI(self.templateDict['bannerexit2'],2,52,900,960,0.8,True):
                    self.sendTimedTap(919,949, 10, 41, keyConstants.SHORT_TAP_DURATION)
                    print("sent CMD, banner should be closing...")
            elif level == stateConstants.L2_at_title_screen:
                #roiLoading = screen[self.adjustYoffset(48):self.adjustYoffset(98), 675:720]
                if not self.scanThisROI(self.templateDict['SCHK_30loadingPage'], 48,98,685,735, 0.8, False):
                    self.sendTimedTap(183, 940, 28, 460, keyConstants.SHORT_TAP_DURATION)
                    time.sleep(3)
                    print("sent CMD, should pass title screen")
            elif level == stateConstants.L3_load_entering_game:
                self.closeAnyLobbyPopup()
            elif level == stateConstants.L4_at_char_lobby:
    
                self.closeAnyLobbyPopup()
                print("at lvl 4 now baybee")
            elif level == stateConstants.L16_loading_wait:
                if not self.updateRequired:
                    if self.scanThisROI(self.templateDict['SCHK_1exitbanner'],2,52,900,960,0.8,True):
                        self.sendTimedTap(919,949, 10, 41, keyConstants.SHORT_TAP_DURATION)
                        time.sleep(2)
                    elif self.scanThisROI(self.templateDict['downloadwarning'],coords.PATCH_DOWNLOAD[1][0], coords.PATCH_DOWNLOAD[1][1], coords.PATCH_DOWNLOAD[0][0], coords.PATCH_DOWNLOAD[0][1], 0.8, True):
                        self.sendTimedTap(coords.PATCH_CONFIRM[0][0], coords.PATCH_CONFIRM[0][1], coords.PATCH_CONFIRM[1][0], coords.PATCH_CONFIRM[1][1], keyConstants.SHORT_TAP_DURATION)
                    
                    #
                    elif self.scanThisROI(self.templateDict['downloadwarning'],coords.PATCH_DOWNLOAD[1][0], coords.PATCH_DOWNLOAD[1][1], coords.PATCH_DOWNLOAD[0][0], coords.PATCH_DOWNLOAD[0][1], 0.8, True):
                        pass
                    elif self.scanThisROI(self.templateDict['updateReqPopup'],100,165,400,550,0.8,True):
                        self.updateRequired = True
                        self.sendTimedTap(400,555, 383, 414, keyConstants.SHORT_TAP_DURATION)
                else:
                    if self.scanThisROI(self.templateDict['updateReqPopup2'], 110,200,195,600 ,0.8, True):
                        if self.scanThisROI(self.templateDict['updateReqPopup3'], 110,420,195,775 ,0.8, True):
                            self.sendTimedTap(self.matchCoords.xyLoc[0] + 195, self.matchCoords.xyLoc[0] + 500, self.matchCoords.xyLoc[1] + 110, self.matchCoords.xyLoc[1] + 200, 0.03)
                            time.sleep(1)
                            self.sendTimedTap(222, 450, 360, 410, 0.05)
                    else:
                        if self.scanWindow2(self.templateDict['updateReqPopup4GooglePlay'], 0.8):
                            self.sendTimedTap(self.matchCoords.xyLoc[0] - 100, self.matchCoords.xyLoc[0] + 100, self.matchCoords.xyLoc[1] - 50, self.matchCoords.xyLoc[1], 0.03)
                        elif self.scanWindow2(self.templateDict['updateReqPopup4GooglePlayReady'], 0.8) or self.scanWindow2(self.templateDict['updateReqPopup4GooglePlayReady2'], 0.8):
                            print("FOUND")
                            self.updateRequired = False
                            self.sendTimedTap(self.matchCoords.xyLoc[0] - 100, self.matchCoords.xyLoc[0] + 100, self.matchCoords.xyLoc[1] - 50, self.matchCoords.xyLoc[1], 0.03)
                        #(332 - 50, 332, 656 - 100,656 + 100, True)
            
            elif level == stateConstants.L5_ingame:
                    

            
        