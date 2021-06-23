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
        if np.amax(homeStage) > self.DEFAULT_THRESHOLD:
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
                
                elif stageTitleRegionVisible and stageTitleMSNameVisible and (stageTitleServerIconVisible or stageTitleCharDetectedVisible): #at titlescreen LOADED #how we know if title is loaded?
                    self.gameState.toggleOtherStatesOff(stateConstants.L2_at_title_screen)
            
                elif loadingPageVisible and not (stageTitleServerIconVisible or stageTitleRegionVisible):
                    self.gameState.toggleOtherStatesOff(stateConstants.L3_load_entering_game)
                    if self.gameState.startPressed:
                        self.gameState.toggleOtherStatesOff(stateConstants.L5_ingame)
                    #elif self.gameState.goingBackToLobby:
                    #    self.gameState.toggleOtherStatesOff(stateConstants.L4_at_char_lobby)                
                
                
                elif charStartPageVisible:
                    self.gameState.toggleOtherStatesOff(stateConstants.L4_at_char_lobby)
                else:
                    
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