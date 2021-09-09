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
        print("DB File created or already exists. loading..")
        self.startPressed = False
        self.updateRequired = False
        self.gplayPressedPlayed = False
        self.patchSuccess = False
        self.inputAccData = False
        self.reScanLobbyData = False # toggle 
        self.dbDataCheck()
    
    def dbDataCheck(self):
        tblName = self.dbConn.CHAR_TBL_TITLE + str(self.cNum)

        if self.dbConn.checkSetup() == 0: #need to register accData. 1st check if client table exists..
            
            if not self.dbConn.doesTableExist(tblName):
                self.dbConn.createClientAccDataTable(tblName)
            self.inputAccData = True
                
        elif self.dbConn.checkSetup() == -1: #row not registered so... 
            self.dbConn.registerClientInMain()
            self.dbConn.createClientAccDataTable(tblName)
            self.inputAccData = True
        else: #good to go
            if not self.dbConn.verifyValidTable(tblName):
                print("OH NO SOMETHING BIG WRONG BIG BIG WRONG")
                print("HELP!")
                print("---------------------------------------")
            self.inputAccData = False
    
    def getCharLobbyData(self):
        #make sure in char select lobby.. do on first run only?
        currPage = -1
        total = -1
        first = False
        while currPage != 1:
            currPage = self.whichCharPage()
            if currPage != 1:
                if currPage <= 3:
                    self.movePage(0) #move left
                else:
                    self.movePage(1)
            else:
                print("we are on page 1. continuing...")
                first = True

        while first == True or total == 7:
            total = self.returnCharAmtOnPage()
            if total == 7:
                self.movePage(1)
                first = False
        currPage = self.whichCharPage()

        if currPage != 1: 
            amt = total
            total = (currPage - 1) * 7
            total += amt
        
        print("ok so total is: " + str(total))
        return total
    
    def getNamesFromFile(self, filename):
        with open(filename, encoding= 'utf-8') as nameList:
            tempList = nameList.readlines()
        
        data_tup = tuple(name.rstrip('\n') for name in tempList)

        return str(data_tup)

    def initFameDB(self):
        tbl_name = "fameTable" + str(self.dbConn.noxNum)
        if not self.dbConn.doesTableExist(tbl_name):    #if tbl doesnt exist, lets set it up
            names = self.getNamesFromFile('fameNames.txt')
            self.dbConn.createTableIfDNE(tbl_name, 1, names)
            # get char names from user input in pyqt (user enters 10 names, those are read in. store data after)
        else:
            pass
            # tbl exists so go thru tbl and fame
            

    def update():
        pass

    def startAQ(self):
        pass

    

    def doFame(self, charName, preSS, postSS):
        jobDone = False
        if self.scanThisROI(self.templateDict['searchplayersbtn'],480, 517, 135,238, 0.8, False) and not self.scanThisROI(self.templateDict['searchplayersbox'],110, 153, 390,570, 0.8, False):
            self.sendTimedTap(146,226, 485, 510,  keyConstants.SHORT_TAP_DURATION)
            time.sleep(2)
        if self.scanThisROI(self.templateDict['searchplayersbox'],110, 153, 390,570, 0.8, False):
            if self.scanThisROI(self.templateDict['emptynamebox'],280, 310, 365,590, 0.8, False):
                self.sendTimedTap(370,580, 290, 305, keyConstants.SHORT_TAP_DURATION)
                time.sleep(1)
                self.enterText(charName)
                time.sleep(2.5)
        print("y")
        if not self.scanThisROI(self.templateDict['emptynamebox'],289, 305, 455,485, 0.8, False):
            print("a")
            while not self.scanThisROI(self.templateDict['emptynamebox'],289, 305, 455,485, 0.8, False) and self.scanThisROI(self.templateDict['confirmbtn'],380, 415, 530,655, 0.8, False):
                print("s")
                self.sendTimedTap(525,640, 383, 414, keyConstants.SHORT_TAP_DURATION)
                time.sleep(2)
        if self.scanThisROI(self.templateDict['searchresults'],115, 152, 431,600, 0.8, False):
            self.sendTimedTap(280,400, 220, 315, keyConstants.SHORT_TAP_DURATION)
            time.sleep(2)
        
        if self.checkIfRightSubMenu('playerinfopage'):
            time.sleep(2)
            #self.saveImageAs(65,460,620,950, 1, preSS)
            while not self.fameIsUsed():
                self.sendTimedTap(645,660,85, 105, keyConstants.SHORT_TAP_DURATION)
                time.sleep(2)
            if self.fameIsUsed():
                #self.saveImageAs(65,460,620,950, 1, postSS)
                jobDone = True
                print("done")
                #self.returnToCharSelect()
    
    def fameLoop(self, charName1, ss1, ss2):
        done = False
        self.openInGameMenu()
        if self.checkIfInMenu():
            self.enterSubMenu('communityicon')
            time.sleep(2)
        if self.checkIfRightSubMenu('communitypage'):
            done = self.doFame(charName1, ss1, ss2)
        if self.checkIfRightSubMenu('playerinfopage'):
            time.sleep(2)
            #self.saveImageAs(65,460,620,950, 1, ss1)
            while not self.fameIsUsed():
                self.sendTimedTap(645,660,85, 105, keyConstants.SHORT_TAP_DURATION)
                time.sleep(2)
            if self.fameIsUsed():
                #self.saveImageAs(65,460,620,950, 1, ss2)
                done = True
                print("done")
                #self.returnToCharSelect()

        
        return done

    #fameList consist of list of strings (names of chars)
    def startFame(self, fameList):
        #get name data from DB [separate table]
        #each char should have own tbl keeping track of which chars successfully famed.
        timestamp = time.strftime('_%H_%M_%S_')

        ssName1 = "preFame" + timestamp 
        ssName2 = "postFame" + timestamp  
        if self.fameLoop("Meowkins", ssName1, ssName2):
            famed = True
        
        if famed:
            print("famed, switching chars")
            self.returnToCharSelect()
            self.updateStageNum(stateConstants.L4_at_char_lobby)
            atLevel = stateConstants.L4_at_char_lobby
            self.gameState.updateStatus(stateConstants.L13_auto_quest, False)
            self.gameState.goingBackToLobby = True
            someVal += 1
            famed = False
    

    



    def botLoop(self, whichFeature, enabled):
        firstrun = True
        while enabled:
            time.sleep(1)
            #load data from db
            level = self.gameState.returnStageNum()
            self.gameState.printTest()
            if level == stateConstants.L0_at_home_scr:
                print("level 0")
                if self.errorMsgFound:
                    print("Error lol")
                    #send touch. 
                if self.scanThisROI(self.templateDict['SCHK_0atHomeScreen'],0,457, 0, 865, 0.8, True):
                    print("MSM located! opening...")
                    self.sendTimedTap(self.matchCoords.xyLoc[0] + 5, self.matchCoords.xyLoc[0] + 20, self.matchCoords.xyLoc[1] - 45, self.matchCoords.xyLoc[1] - 30, 0.03)
                    if self.gameState.crashed:
                        self.gameState.resetOnCrash()
            elif level == stateConstants.L1_at_start_ban:
                print("level 1")
                self.patchSuccess = True
                if self.scanThisROI(self.templateDict['bannerexit2'],2,52,900,960,0.8,True):
                    self.sendTimedTap(919,949, 10, 41, keyConstants.SHORT_TAP_DURATION)
                    print("sent CMD, banner should be closing...")
            elif level == stateConstants.L2_at_title_screen:
                print("level 2")
                #roiLoading = screen[self.adjustYoffset(48):self.adjustYoffset(98), 675:720]
                if not self.scanThisROI(self.templateDict['SCHK_30loadingPage'], 48,98,685,735, 0.8, False):
                    self.sendTimedTap(183, 940, 28, 460, keyConstants.SHORT_TAP_DURATION)
                    time.sleep(3)
                    print("sent CMD, should pass title screen")
            elif level == stateConstants.L3_load_entering_game:
                print("level 3")
                self.closeAnyLobbyPopup()
            elif level == stateConstants.L4_at_char_lobby:
                print("level 4")

                if self.inputAccData:
                    done = False
                    while not done:
                        self.closeAnyLobbyPopup()
                        if self.gameState.returnStageNum() == stateConstants.L4_at_char_lobby:
                            charAmt = self.countEmptySlots()
                            for x in range(0, charAmt):
                                self.dbConn.registerClientAccData(x)
                            self.dbConn.updateSingleVar("MAIN_TBL_CLIENTS", "accDataRegistered", (1,) )
                            done = True
                            self.inputAccData = False
                else:
                    self.findSelectedChar()
                    if firstrun and self.currChar != 0:
                        self.selectChar(0)
                        self.findSelectedChar()
                        if self.currChar == 0:
                            firstrun = False
                    elif firstrun and self.currChar == 0:
                        firstrun = False
                    
                    if not firstrun:
                        if self.dbConn.getSingleValAccData("charDone", self.currChar):
                            self.selectChar(self.currChar + 1)
                        else:
                            if self.gameState.returnStageNum() == stateConstants.L4_at_char_lobby:
                                print("no popup detected! going in game")
                                self.sendTimedTap(707,899,445,479, keyConstants.SHORT_TAP_DURATION)
                                self.gameState.startPressed = True
                                time.sleep(2)

                #check table exists.
    
                self.closeAnyLobbyPopup()
                print("at lvl 4 now baybee")
            elif level == stateConstants.L16_loading_wait:
                print("level 16")
                if not self.updateRequired:

                    #if self.gplayPressedPlayed:
                    #    if self.scanWindow2(self.templateDict['updateReqPopup4GooglePlayReady'], 0.8) or self.scanWindow2(self.templateDict['updateReqPopup4GooglePlayReady2'], 0.8):
                    #        print("CRASHED BUT IT'S OK. RE-PRESSING PLAY.")

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
                            self.gplayPressedPlayed = True
                            self.sendTimedTap(self.matchCoords.xyLoc[0] - 100, self.matchCoords.xyLoc[0] + 100, self.matchCoords.xyLoc[1] - 50, self.matchCoords.xyLoc[1], 0.03)
                        #(332 - 50, 332, 656 - 100,656 + 100, True)
            
            elif level == stateConstants.L5_ingame:
                self.gameState.atLobby = False
                if self.gameState.currState[stateConstants.L13_auto_quest]:
                    while self.gameState.currState[stateConstants.L13_auto_quest]:
                        pass
                        '''
                        check level
                        '''


                pass
                    

            
        