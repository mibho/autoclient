import numpy as np
import cv2 as cv

import BotTools
from ROICoords import cScanCoords as coords
from Constants import *
from BotTools import cBotTools
from BotData import cBotData
import gamestatus as gs

class cBotFunctionsTools(cBotTools, cBotData):
    DEFAULT_THRESHOLD = 0.8

    def __init__(self, pID, windowName, clientNum, deviceObj, adbSockInfo):
        cBotTools.__init__(self, pID, windowName, clientNum, deviceObj, adbSockInfo)
        cBotData.__init__(self)
        self.gameState = gs.GameStatus()

        self.dataGrabbed = False
        self.afkStart = 0
        self.timerStarted = False
        self.popupDetected = False
        self.errorMsgFound = False

    def OOG_pressAndroidTasksMenu(self):
        self.toggleKeyCMD(keyCodes.PG_UP_KEY)
    
    def OOG_forceCloseMapleApp(self):
        while self.scanThisROI(self.templateDict['msmTitleAndroidMenu'], 405,460,50,950 ,0.8, True):
            x1 = self.matchCoords.xyLoc[0] + 80
            y1 = self.matchCoords.xyLoc[1] + 350
            self.sendDragCMD(keyConstants.SWIPE_UP,100, x1, y1, y1 - 250)
            BotTools.time.sleep(1)

    def confirmPatchIfNeeded(self):
        if self.scanThisROI(self.templateDict['downloadwarning'],coords.PATCH_DOWNLOAD[1][0], coords.PATCH_DOWNLOAD[1][1], coords.PATCH_DOWNLOAD[0][0], coords.PATCH_DOWNLOAD[0][1], 0.8, True):
            self.sendTimedTap(coords.PATCH_CONFIRM[0][0], coords.PATCH_CONFIRM[0][1], coords.PATCH_CONFIRM[1][0], coords.PATCH_CONFIRM[1][1], keyConstants.SHORT_TAP_DURATION)
            BotTools.time.sleep(5)


    def getCharPos(self, whichCharNum):
        if whichCharNum == 0: return coords.LOBBY_CHAR0POS
        elif whichCharNum == 1: return coords.LOBBY_CHAR1POS
        elif whichCharNum == 2: return coords.LOBBY_CHAR2POS
        elif whichCharNum == 3: return coords.LOBBY_CHAR3POS
        elif whichCharNum == 4: return coords.LOBBY_CHAR4POS
        elif whichCharNum == 5: return coords.LOBBY_CHAR5POS
        elif whichCharNum == 6: return coords.LOBBY_CHAR6POS

    def selectChar(self, whichCharNum):
        BotTools.time.sleep(0.3)
        charLoc = self.getCharPos(whichCharNum)
        self.sendTimedTap(charLoc[0][0] + 40, charLoc[0][1] - 45, charLoc[1][0], charLoc[1][1], keyConstants.SHORT_TAP_DURATION)


    def setTotalChars(self, num):
        self.totalChars = num
    
    def updateStageNum(self, state):
        self.gameState.stageNum = state
    
    def setDataGrabbedTrue(self):
        self.dataGrabbed = True
    
    def returnToCharSelect(self):
        exited = False
        while not self.scanThisROI(self.templateDict['resetexitmenu'],108,158,409,555, 0.8, True) and not exited:
            self.toggleKeyCMD(keyCodes.ESC_KEY)
            BotTools.time.sleep(0.7)

            if self.scanThisROI(self.templateDict['resetexitmenu'],108,158,409,555, 0.8, True):
                BotTools.time.sleep(4)
                self.sendTimedTap(430,537,381,417,  keyConstants.SHORT_TAP_DURATION)
                exited = True
    
    
    

    def whichCharSelected(self):
        xBound = self.matchCoords.xyLoc[0] #+ coords.LOBBY_CHARS[0][0]
        yBound = self.matchCoords.xyLoc[1] #+ coords.LOBBY_CHARS[0][1]
        #topleft    0
        if xBound >= coords.LOBBY_CHAR0POS[0][0] and xBound <= coords.LOBBY_CHAR0POS[0][1] \
            and   yBound >= coords.LOBBY_CHAR0POS[1][0] and   yBound <= coords.LOBBY_CHAR0POS[1][1]:
            self.currChar = 0
            print("Char 0 [top left] selected.")
        #topmid     1
        elif xBound >= coords.LOBBY_CHAR1POS[0][0] and xBound <= coords.LOBBY_CHAR1POS[0][1] \
            and   yBound >= coords.LOBBY_CHAR1POS[1][0] and   yBound <= coords.LOBBY_CHAR1POS[1][1]:
            self.currChar = 1
            print("Char 1 [top middle] selected.") 
        #topright   2
        elif xBound >= coords.LOBBY_CHAR2POS[0][0] and xBound <= coords.LOBBY_CHAR2POS[0][1] \
            and   yBound >= coords.LOBBY_CHAR2POS[1][0] and   yBound <= coords.LOBBY_CHAR2POS[1][1]:
            self.currChar = 2
            print("Char 2 [top right] selected.") 
        #botleft1   3
        elif xBound >= coords.LOBBY_CHAR3POS[0][0] and xBound <= coords.LOBBY_CHAR3POS[0][1] \
            and   yBound >= coords.LOBBY_CHAR3POS[1][0] and   yBound <= coords.LOBBY_CHAR3POS[1][1]:
            self.currChar = 3
            print("Char 3 [bottom leftmost] selected.") 
        #botleft2   4
        elif xBound >= coords.LOBBY_CHAR4POS[0][0] and xBound <= coords.LOBBY_CHAR4POS[0][1] \
            and   yBound >= coords.LOBBY_CHAR4POS[1][0] and   yBound <= coords.LOBBY_CHAR4POS[1][1]:
            self.currChar = 4
            print("Char 4 [bottom left close to the center] selected.") 
        #botright2  5
        elif xBound >= coords.LOBBY_CHAR5POS[0][0] and xBound <= coords.LOBBY_CHAR5POS[0][1] \
            and   yBound >= coords.LOBBY_CHAR5POS[1][0] and   yBound <= coords.LOBBY_CHAR5POS[1][1]:
            self.currChar = 5
            print("Char 5 [bottom right close to the center] selected.")  
        #botright1  6
        elif xBound >= coords.LOBBY_CHAR6POS[0][0] and xBound <= coords.LOBBY_CHAR6POS[0][1] \
            and   yBound >= coords.LOBBY_CHAR6POS[1][0] and   yBound <= coords.LOBBY_CHAR6POS[1][1]:
            self.currChar = 6
            print("Char 6 [bottom right] selected.") 
        else:
            print("ruh roh error")
    

    def countEmptySlots(self):
        roi = self.grabROI(82,483,73,645)
        count = 0
        
        for x in range(1,3):
            leftLocsBot = 'botleft'
            rightLocsBot = 'botright'
            leftLocsTop = 'topleft'
            rightLocsTop = 'topright'
            if x == 1: 
                leftLocsBot = leftLocsBot + str(x)
                leftLocsTop = leftLocsTop + str(x)
                rightLocsBot = rightLocsBot + str(x)
                rightLocsTop = rightLocsTop + str(x)
            elif x == 2:
                leftLocsBot = leftLocsBot + str(x)
                leftLocsTop = leftLocsTop + str(x)
                rightLocsBot = rightLocsBot + str(x)

            resLB = cv.matchTemplate(roi,self.templateDict[leftLocsBot], eval('cv.TM_CCOEFF_NORMED')) #cv.TM_CCOEFF_NORMED
            resLT = cv.matchTemplate(roi,self.templateDict[leftLocsTop], eval('cv.TM_CCOEFF_NORMED')) #cv.TM_CCOEFF_NORMED
            resRB = cv.matchTemplate(roi,self.templateDict[rightLocsBot], eval('cv.TM_CCOEFF_NORMED')) #cv.TM_CCOEFF_NORMED
            if x != 2:    
                resRT = cv.matchTemplate(roi,self.templateDict[rightLocsTop], eval('cv.TM_CCOEFF_NORMED')) #cv.TM_CCOEFF_NORMED

            cv.imwrite("ok.png", roi)
            #cv.imwrite("ok1.png", self.preClickImg)
            #time.sleep(1)
            if np.amax(resLT) > 0.85:
                count += 1
            if np.amax(resLB) > 0.85:
                count += 1
            if x != 2 and np.amax(resRT) > 0.85:
                count += 1
            if np.amax(resRB) > 0.85:
                count += 1
        
        return (7 - count)
    
    def filterUIBlockedMatches(self, xC1, xC2, yC1, yC2):#y range 323, 515, x = 11,200
        if not ((yC1 >= 323 and yC1 <= 515) and (yC2 >= 323 and yC2 <= 515) and \
        (xC1 >= 11 and xC1 <= 200) and (xC2 >= 11 and xC2 <= 200)):
            return True
        
        return False

    def closeAnyLobbyPopup(self):
        if self.scanWindow2(self.templateDict['exitpic'], 0.9) or self.scanWindow2(self.templateDict['exitpic2'], 0.9):
            print("popup located! sending touch...")
            self.sendTimedTap(self.matchCoords.xyLoc[0]+2,self.matchCoords.xyLoc[0]+20,self.matchCoords.xyLoc[1]-20,self.matchCoords.xyLoc[1]-5,  keyConstants.SHORT_TAP_DURATION)
            print("touch sent!")

        #findTemplateMatch2
    def scanWindow2(self, temp, threshold):
        filteredPic = self.checkForPopups()
        if not self.popupDetected:
            res = cv.matchTemplate(filteredPic ,temp, eval('cv.TM_CCOEFF_NORMED')) #cv.TM_CCOEFF_NORMED
            
            loc = np.where( res >= threshold)
        
            if np.amax(res) > threshold:
                for pt in zip(*loc[::-1]):
                    self.matchCoords.setPoints(pt[0], pt[1])    
                return True

        return False
    
        #by default it grabs gray ROIs
    def scanThisROI(self, temp, y1,y2,x1,x2 ,threshold, ptsneeded):
        filteredPic = self.checkForPopups()
        if not self.popupDetected:
            roi = filteredPic[self.adjustYoffset(y1):self.adjustYoffset(y2), x1 : x2]
            res = cv.matchTemplate(roi ,temp, eval('cv.TM_CCOEFF_NORMED')) #cv.TM_CCOEFF_NORMED
            loc = np.where( res >= threshold)

            if np.amax(res) > threshold:
                if ptsneeded:
                    for pt in zip(*loc[::-1]):
                        self.matchCoords.setPoints(pt[0], pt[1])
                
                return True
            
        return False
    
    def checkStage(self):
        screen = self.returnColorSS(False)
        homeStage = cv.matchTemplate(screen, self.templateDict['SCHK_0atHomeScreen'], eval('cv.TM_CCOEFF_NORMED'))
        crashMsg = cv.matchTemplate(screen, self.templateDict['msmstoppedmsgbox'], eval('cv.TM_CCOEFF_NORMED'))
        if np.amax(crashMsg > self.DEFAULT_THRESHOLD):
            self.errorMsgFound = True
        else:
            self.errorMsgFound = False

        if np.amax(homeStage) > self.DEFAULT_THRESHOLD or np.amax(crashMsg) > self.DEFAULT_THRESHOLD:
            self.gameState.toggleOtherStatesOff(stateConstants.L0_at_home_scr)
        else: #not home screen so in game or buggd
            if not (self.gameState.currState[stateConstants.L5_ingame]):
                vivoxBanner = screen[self.adjustYoffset(450):self.adjustYoffset(477), 830:925]
                roiBanner = screen[self.adjustYoffset(2):self.adjustYoffset(52), 900:955]
                

                roiTitleRegionIcon = screen[self.adjustYoffset(495):self.adjustYoffset(530),8:48]  # #titlescreen loaded and ready
                roiTitleMSName = screen[self.adjustYoffset(120):self.adjustYoffset(160), 250:680]

                
                roiLoading = screen[self.adjustYoffset(48):self.adjustYoffset(98), 685:735]
                roiCharStart = screen[self.adjustYoffset(430):self.adjustYoffset(497), 685:930]

                roiTitleScreenReady1 = screen[self.adjustYoffset(420):self.adjustYoffset(460), 286:330] #roiTitleInosys
                roiTitleScreenReady2 = screen[self.adjustYoffset(425):self.adjustYoffset(455), 565:592] #roiTitleCharDetected

                vivoxMatch = cv.matchTemplate(vivoxBanner, self.templateDict['SCHK_vivoxTitleRegion'], eval('cv.TM_CCOEFF_NORMED'))

                stageTitleRegion = cv.matchTemplate(roiTitleRegionIcon, self.templateDict['SCHK_12newTitleRegion'], eval('cv.TM_CCOEFF_NORMED'))
                stageTitleServerIcon = cv.matchTemplate(roiTitleScreenReady1, self.templateDict['SCHK_1roiTitleInosys'], eval('cv.TM_CCOEFF_NORMED'))
                stageTitleCharDetected = cv.matchTemplate(roiTitleScreenReady2, self.templateDict['SCHK_20roiTitleCharDetected'], eval('cv.TM_CCOEFF_NORMED'))
                stageTitleMSName = cv.matchTemplate(roiTitleMSName ,self.templateDict['SCHK_12titleScreen'], eval('cv.TM_CCOEFF_NORMED'))

                stageCharStart = cv.matchTemplate(roiCharStart ,self.templateDict['SCHK_40charStart'], eval('cv.TM_CCOEFF_NORMED')) 


                stageBanner = cv.matchTemplate(roiBanner, self.templateDict['bannerexit2'], eval('cv.TM_CCOEFF_NORMED'))

                stageLoading = cv.matchTemplate(roiLoading ,self.templateDict['SCHK_30loadingPage'], eval('cv.TM_CCOEFF_NORMED'))

                stageTitleRegionVisible = np.amax(stageTitleRegion) > self.DEFAULT_THRESHOLD
                stageTitleServerIconVisible = np.amax(stageTitleServerIcon) > self.DEFAULT_THRESHOLD
                stageTitleCharDetectedVisible = np.amax(stageTitleCharDetected) > self.DEFAULT_THRESHOLD
                stageTitleMSNameVisible = np.amax(stageTitleMSName) > self.DEFAULT_THRESHOLD

                exitBannerVisible = np.amax(stageBanner) > self.DEFAULT_THRESHOLD

                vivoxBannerVisible = np.amax(vivoxMatch) > self.DEFAULT_THRESHOLD

                loadingPageVisible = np.amax(stageLoading) > self.DEFAULT_THRESHOLD
                charStartPageVisible = np.amax(stageCharStart) > self.DEFAULT_THRESHOLD
                '''
                print("stageTitleRegionVisible = " + str(stageTitleRegionVisible))
                print("stageTitleServerIconVisible = " + str(stageTitleServerIconVisible))
                print("stageTitleCharDetectedVisible = " + str(stageTitleCharDetectedVisible))
                print("stageTitleMSNameVisible = " + str(stageTitleMSNameVisible))
                print("exitBannerVisible = " + str(exitBannerVisible))
                print("vivoxBannerVisible = " + str(vivoxBannerVisible))
                print("loadingPageVisible = " + str(loadingPageVisible))
                print("charStartPageVisible = " + str(charStartPageVisible))
                '''

            
                if exitBannerVisible: 
                    self.gameState.toggleOtherStatesOff(stateConstants.L1_at_start_ban)
                    self.gameState.atLobby = False

                elif stageTitleRegionVisible and stageTitleMSNameVisible and (stageTitleServerIconVisible or stageTitleCharDetectedVisible): #at titlescreen LOADED #how we know if title is loaded?
                    self.gameState.toggleOtherStatesOff(stateConstants.L2_at_title_screen)
                    self.gameState.atLobby = False
            
                elif loadingPageVisible and not (stageTitleServerIconVisible or stageTitleRegionVisible):
                    self.gameState.toggleOtherStatesOff(stateConstants.L3_load_entering_game)
                    if self.gameState.startPressed:
                        self.gameState.toggleOtherStatesOff(stateConstants.L5_ingame)
                    self.gameState.atLobby = False
                    #elif self.gameState.goingBackToLobby:
                    #    self.gameState.toggleOtherStatesOff(stateConstants.L4_at_char_lobby)                
                
                
                elif charStartPageVisible:
                    self.gameState.atLobby = True
                    self.gameState.toggleOtherStatesOff(stateConstants.L4_at_char_lobby)
                else:
                    if not self.gameState.atLobby:
                        self.gameState.toggleOtherStatesOff(stateConstants.L16_loading_wait)
                    #if start button was pressed then we going in game
            
                
            else: #not in game not in app somewhere
                pass
            
        return screen

    

    def checkForPopups(self): #get ss, grab ea region of interest and scan for any of those.
        screen = self.checkStage()
        roiRevive   = screen[self.adjustYoffset(345):self.adjustYoffset(445), 200:391] #345, 445, 200, 391,0.85):
        roiMapleView = screen[self.adjustYoffset(49):self.adjustYoffset(80), 793:909] #49,80,793,909
        roiRandAds = screen[self.adjustYoffset(11):self.adjustYoffset(120), 750:900]
        roiNewConfirm = screen[self.adjustYoffset(365):self.adjustYoffset(455), 346:615]
        roiVioletta = screen[self.adjustYoffset(110):self.adjustYoffset(420),228:763]
        roiNewForced = screen[self.adjustYoffset(90):self.adjustYoffset(120), 20:345] #297-323 90-120

        resRev = cv.matchTemplate(roiRevive, self.templateDict['revivebtn'], eval('cv.TM_CCOEFF_NORMED'))
        resMapleView = cv.matchTemplate(roiMapleView, self.templateDict['mapleviewpopup'], eval('cv.TM_CCOEFF_NORMED'))
        resAds1 = cv.matchTemplate(roiRandAds ,self.templateDict['exitpic'], eval('cv.TM_CCOEFF_NORMED'))
        resAds2 = cv.matchTemplate(roiRandAds ,self.templateDict['exitpic2'], eval('cv.TM_CCOEFF_NORMED'))
        
        resAds3 = cv.matchTemplate(roiRandAds ,self.templateDict['adexit3'], eval('cv.TM_CCOEFF_NORMED'))

        resExit1 = cv.matchTemplate(roiRandAds ,self.templateDict['newmenuexit'], eval('cv.TM_CCOEFF_NORMED'))
        resExit2 = cv.matchTemplate(roiRandAds ,self.templateDict['newmenuexit2'], eval('cv.TM_CCOEFF_NORMED'))

        resNewConfirm = cv.matchTemplate(roiNewConfirm ,self.templateDict['newcontentconfirm'], eval('cv.TM_CCOEFF_NORMED'))
        resVioletta = cv.matchTemplate(roiVioletta ,self.templateDict['violettabotpopup'], eval('cv.TM_CCOEFF_NORMED'))
        resNewForced = cv.matchTemplate(roiNewForced ,self.templateDict['newtuticon'], eval('cv.TM_CCOEFF_NORMED'))
              
        if np.amax(resRev) > self.DEFAULT_THRESHOLD:
            self.gameState.updateStatus(stateConstants.S20_isdead, True)
            print("we dead")
        
        elif (np.amax(resAds1) > self.DEFAULT_THRESHOLD or np.amax(resAds2) > self.DEFAULT_THRESHOLD or np.amax(resAds3) > self.DEFAULT_THRESHOLD or np.amax(resExit1) > self.DEFAULT_THRESHOLD or np.amax(resExit2) > self.DEFAULT_THRESHOLD) and \
            (not self.gameState.currState[stateConstants.S24_in_dialog] and not self.gameState.currState[stateConstants.S27_in_bag] and not self.gameState.currState[stateConstants.S28_in_mailbox]):
            print("closeable popup detected!")

            if np.amax(resAds1) > self.DEFAULT_THRESHOLD:
                res = resAds1 
                print("exitpic [resAds1] detected")
            elif np.amax(resAds2) > self.DEFAULT_THRESHOLD:
                res = resAds2
                print("exitpic2 [resAds2] detected")
            elif np.amax(resAds3) > self.DEFAULT_THRESHOLD:
                res = resAds3
                print("adexit3 [resAds3] detected")
            elif np.amax(resExit1) > self.DEFAULT_THRESHOLD:
                res = resExit1
                print("newmenuexit [resExit1] detected")
            elif np.amax(resExit2) > self.DEFAULT_THRESHOLD:
                res = resExit2
                print("newmenuexit2 [resExit2] detected")
            
            loc = np.where( res >= self.DEFAULT_THRESHOLD)
            for pt in zip(*loc[::-1]):
                self.matchCoords.setPoints(pt[0], pt[1])   

            
            self.gameState.updateStatus(stateConstants.S22_popup_visible, True)
        elif np.amax(resNewForced) > self.DEFAULT_THRESHOLD: #and self.gameState.buttonPressed:
            self.gameState.updateStatus(stateConstants.S30_new_forced_visible, True)
            print("new forced tut visible")
        elif np.amax(resNewConfirm) > self.DEFAULT_THRESHOLD: #and self.gameState.buttonPressed:
            self.gameState.updateStatus(stateConstants.S31_new_confirm_popup, True)
            print("new confirm popup detected")
        elif np.amax(resMapleView) > self.DEFAULT_THRESHOLD:
            self.gameState.updateStatus(stateConstants.S32_mapleview_visible, True)
            print("Mapleview popup detected!")
            
        elif np.amax(resVioletta) > self.DEFAULT_THRESHOLD:
            self.gameState.updateStatus(stateConstants.S33_violetta, True)
            print("VIOLETTA DETECTED")
        
        if self.gameState.detected() != -1 and self.gameState.detected() != 0:
            self.popupDetected = True
        else:
            self.popupDetected = False

        return screen