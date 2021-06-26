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
        self.currChar = 0
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
    
    def returnToCharSelect(self):
        exited = False
        while not self.scanThisROI(self.templateDict['resetexitmenu'],108,158,409,555, 0.8, True) and not exited:
            self.toggleKeyCMD(keyCodes.ESC_KEY)
            BotTools.time.sleep(0.7)

            if self.scanThisROI(self.templateDict['resetexitmenu'],108,158,409,555, 0.8, True):
                BotTools.time.sleep(4)
                self.sendTimedTap(430,537,381,417,  keyConstants.SHORT_TAP_DURATION)
                exited = True

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
        else:
            exit()

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
    

    def whichCharSelected2(self, cAvg):
        xBound = cAvg[0][0] + 73 #self.matchCoords.xyLoc[0] #+ coords.LOBBY_CHARS[0][0]
        yBound = cAvg[0][1] + 82#self.matchCoords.xyLoc[1] #+ coords.LOBBY_CHARS[0][1]
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
        roi = self.grabROI(82,483,73,645, False)
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

            #cv.imwrite("ok.png", roi)
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

    def getCharLevelLobby(self):
        first = -1
        second = -1
        for x in range(0,10):
            tempName = 'charLobbyLevel' + str(x)
            if self.scanThisROI(self.templateDict[tempName],153,167,743,753,0.8, True):
                first = x 
            if self.scanThisROI(self.templateDict[tempName],153,167,753,763,0.8, True):
                second = x
        
        if second != -1:
            level = (first*10)
            level += second
        else:
            level = first
        
        print("level is: " + str(level))
        return level


    def findSelectedChar(self):
        roi1 = self.grabROI(82,483,73,645, False)
        blurred = cv.GaussianBlur(roi1, (11, 11), 0)
        thresh11 = cv.threshold(blurred, 245, 255, cv.THRESH_BINARY)[1]
        thresh11 = cv.erode(thresh11, None, iterations=2)
        thresh11 = cv.dilate(thresh11, None, iterations=4)
        ok = cv.findNonZero(thresh11)
        avg = np.average(ok, axis = 0)
        self.whichCharSelected2(avg)




    def AQ_closeAdvicePopup(self):
        if self.scanThisROI(self.templateDict['advicePopupPic'], 175,249,259,337, 0.85, False):
            popupFound = True
            while popupFound:
                self.sendTimedTap(525,544,146,164, keyConstants.SHORT_TAP_DURATION)
                BotTools.time.sleep(2)
                if not self.scanThisROI(self.templateDict['advicePopupPic'], 175,249,259,337, 0.85, False):
                    popupFound = False

    def AQ_indialog(self):
        if not self.scanThisROI(self.templateDict['nextdialog'],342, 405,792,960, 0.85, False) and not self.scanThisROI(self.templateDict['questaccept'],275, 365,695,951, 0.8,False) \
        and not self.scanThisROI(self.templateDict['questcomplete'], 275, 365,695,951, 0.8,False) and not self.scanThisROI(self.templateDict['questconfirm'], 275, 365,695,951, 0.8,False)\
        and not self.scanThisROI(self.templateDict['questclaimreward'], 443,522,350,602, 0.9,False):
            return False

        return True

    def AQ_questObtained(self):
        if self.gameState.currState[stateConstants.S23_quest_inprogress] or self.gameState.currState[stateConstants.S31_quest_accepted]:
            return True
        
        return False
    
    def AQ_claimRewardIfGiven(self):
        if self.scanThisROI(self.templateDict['questclaimreward'], 443,522,350,602, 0.8, False):
            print("not doing quest/forced quest but claiming reward")
            self.gameState.updateStatus(stateConstants.S23_quest_inprogress, False)
            self.gameState.updateStatus(stateConstants.S24_in_dialog, False)
            self.gameState.updateStatus(stateConstants.S25_on_route, False)
            self.gameState.updateStatus(stateConstants.S31_quest_accepted, False)
            self.sendTimedTap(382,577, 461,504,  keyConstants.SHORT_TAP_DURATION)
            BotTools.time.sleep(2)
        
    
    def AQ_isIdle(self):
        if not self.gameState.currState[stateConstants.S23_quest_inprogress] and \
        not self.AQ_indialog() and not self.gameState.currState[stateConstants.S25_on_route] \
        and not self.gameState.currState[stateConstants.S31_quest_accepted]:
            return True
        
        return False
    
    def AQ_inMultiQDialog(self):
        if self.scanThisROI(self.templateDict['newmultiqstart'],392, 509,219,370, 0.85, True) \
        or self.scanThisROI(self.templateDict['newmultiqend'],392, 509,219,370, 0.85, True): 
            return True
        
        return False
    
    def AQ_startForcedTut(self):
        self.scanThisROI(self.templateDict['newtuticon'],90,120,20,345,0.83, True)
        x = self.matchCoords.xyLoc[0] + 20
        y = self.matchCoords.xyLoc[1] + 90
        self.sendTimedTap(x,x + 5, y, y+5,keyConstants.SHORT_TAP_DURATION)
        print(x)
        print(y)
        BotTools.time.sleep(3)
        if self.scanThisROI(self.templateDict['inNewTut'],124,180,423,523, 0.85, False):
            self.gameState.buttonPressed = True 
            self.gameState.updateStatus(stateConstants.S30_new_forced_visible, True)  #255,272, 110,125
    
    def AQ_foundForcedIcon(self):
        if self.scanThisROI(self.templateDict['newtuticon'],90,120,20,345,0.83, True) and not self.scanThisROI(self.templateDict['inNewTut'],124,180,423,523, 0.8, False):
            x = self.matchCoords.xyLoc[0] + 20
            y = self.matchCoords.xyLoc[1] + 90
            print(x)
            print(y)
            return True
        
        return False
    
    def AQ_handleDialog(self):
        print("man da fuk goinon")
        if self.scanThisROI(self.templateDict['newmultiqstart'],392, 509,219,370, 0.85, True) or self.scanThisROI(self.templateDict['newmultiqend'],392, 509,219,370, 0.85, True):
            self.gameState.updateStatus(stateConstants.S24_in_dialog, True)
            minX = 219 + self.matchCoords.xyLoc[0]
            maxX = minX + 70
            minY = 392+ self.matchCoords.xyLoc[1] + 10
            maxY = minY + 25
            self.sendTimedTap(minX,maxX,minY,maxY,  keyConstants.SHORT_TAP_DURATION) #219-370 x 392-509 y

        elif self.scanThisROI(self.templateDict['nextdialog'],342, 405,792,960, 0.85, False):
            self.gameState.updateStatus(stateConstants.S23_quest_inprogress, True)
            self.gameState.updateStatus(stateConstants.S24_in_dialog, True)
            self.sendTimedTap(863,937,365,387, keyConstants.SHORT_TAP_DURATION)
        elif self.scanThisROI(self.templateDict['questaccept2'], 275, 365,695,951, 0.9, False) or self.scanThisROI(self.templateDict['questconfirm'], 275, 365,695,951, 0.8, False):
            self.sendTimedTap(765,890, 300,323, keyConstants.SHORT_TAP_DURATION)
            self.gameState.updateStatus(stateConstants.S23_quest_inprogress, True)
            self.gameState.updateStatus(stateConstants.S24_in_dialog, False)
            self.gameState.updateStatus(stateConstants.S31_quest_accepted, True)
        elif self.scanThisROI(self.templateDict['questcomplete'], 275, 365,695,951, 0.8, False):
            self.gameState.updateStatus(stateConstants.S23_quest_inprogress, False)
            self.gameState.updateStatus(stateConstants.S24_in_dialog, False)
            self.sendTimedTap(740,915, 297,332, keyConstants.SHORT_TAP_DURATION)
    
    #look for better templates
    '''
    def AQ_routeIsShort(self): #(142,154,547,556)

        tempImg = self.grabROI(140,156,545,558)
        tempArr1=cv.matchTemplate(tempImg ,self.templateDict['0leftrock'], eval('cv.TM_CCOEFF_NORMED'))
        tempArr2=cv.matchTemplate(tempImg ,self.templateDict['1leftrock'], eval('cv.TM_CCOEFF_NORMED'))
        tempArr3=cv.matchTemplate(tempImg ,self.templateDict['2leftrock'], eval('cv.TM_CCOEFF_NORMED'))
        tempArr4=cv.matchTemplate(tempImg ,self.templateDict['3leftrock'], eval('cv.TM_CCOEFF_NORMED'))
    
        if np.amax(tempArr1) > 0.81:
            return True
        elif np.amax(tempArr2) > 0.81:
            return True
        elif np.amax(tempArr3) > 0.81:
            return True
        elif np.amax(tempArr4) > 0.81:
            return True
        
        return False
    '''

    def AQ_autoAssignSP(self):
        if self.scanThisROI(self.templateDict['autoassign'], 253,273,539,645,0.85, True):
            minX = 539 + self.matchCoords.xyLoc[0] - 5
            maxX = minX + 40
            minY = 253 + self.matchCoords.xyLoc[1] - 3
            maxY = minY + 7
            self.sendTimedTap(minX,maxX,minY,maxY, keyConstants.SHORT_TAP_DURATION)
            BotTools.time.sleep(3)

        if self.scanThisROI(self.templateDict['autoskillpopup'], 382,418,497,685, 0.85, True):
            minX = 497 + self.matchCoords.xyLoc[0] - 20
            maxX = minX + 100
            minY = 382 + self.matchCoords.xyLoc[1] - 7
            maxY = minY + 15
            self.sendTimedTap(minX,maxX,minY,maxY, keyConstants.SHORT_TAP_DURATION)


    def AQ_purpleQuestLevel(self):
        screen = self.returnGraySS().copy()
        tensDigit = screen[self.adjustYoffset(142):self.adjustYoffset(155), 116:123]
        onesDigit = screen[self.adjustYoffset(142):self.adjustYoffset(155), 123:130]
        str_1 = ""
        str_2 = ""

        for x in range(10):
            tempName = "questpurplv" + str(x)
            matchOne = cv.matchTemplate(tensDigit ,self.templateDict[tempName], eval('cv.TM_CCOEFF_NORMED'))
            matchTwo = cv.matchTemplate(onesDigit ,self.templateDict[tempName], eval('cv.TM_CCOEFF_NORMED'))

            if np.amax(matchOne) > 0.81:
                str_1 = str(x)
            if np.amax(matchTwo) > 0.81:
                str_2 = str(x)
        
        result = str_1 + str_2 
        if result == "":
            return -1
        
        return int(result)
    
    def AQ_checkAndReturnLevel(self):
        screen = self.returnGraySS().copy()
        oneDigitLevel = screen[self.adjustYoffset(5):self.adjustYoffset(22), 32:41]
        twoDigitLevel = screen[self.adjustYoffset(5):self.adjustYoffset(22), 40:48]
        threeDigitLevel = screen[self.adjustYoffset(5):self.adjustYoffset(22), 46:55]
        str_1 = ""
        str_2 = ""
        str_3 = ""

        for x in range(10):
            tempName = "leveltext" + str(x)
            matchOne = cv.matchTemplate(oneDigitLevel ,self.templateDict[tempName], eval('cv.TM_CCOEFF_NORMED'))
            matchTwo = cv.matchTemplate(twoDigitLevel ,self.templateDict[tempName], eval('cv.TM_CCOEFF_NORMED'))
            matchThree = cv.matchTemplate(threeDigitLevel ,self.templateDict[tempName], eval('cv.TM_CCOEFF_NORMED'))

            if np.amax(matchOne) > 0.81:
                str_1 = str(x)
            if np.amax(matchTwo) > 0.81:
                str_2 = str(x)
            if np.amax(matchThree) > 0.81:
                str_3 = str(x)
        
        result = str_1 + str_2 + str_3 
        if result == "":
            return -1

        return int(result)

    
    def AQ_isEmptySlot(self, slotNum):
        s0Empty = s1Empty = s2Empty = s3Empty = s4Empty = False
        if slotNum == 0 and self.scanThisROI(self.templateDict['skill_btn_slot_0'],315,385,167, 235 , 0.8, True):
            print("button 0 empty")
            return True
        elif slotNum == 1 and self.scanThisROI(self.templateDict['skill_btn_slot_0'],233,300,167, 235 , 0.8, True):
            print("button 1 empty")
            return True
        elif slotNum == 2 and self.scanThisROI(self.templateDict['skill_btn_slot_0'],182,250,233, 300 , 0.8, True):
            print("button 2 empty")
            return True
        elif slotNum == 3 and self.scanThisROI(self.templateDict['skill_btn_slot_0'],182,250,318, 386 , 0.8, True):
            print("button 3 empty")
            return True
        elif slotNum == 4 and self.scanThisROI(self.templateDict['skill_btn_slot_0'],270,370,247, 343 , 0.8, True):
            print("button 4 empty")
            return True
        
        return False

    
    def AQ_frontOrBackSkillPage(self):
        if self.scanThisROI(self.templateDict['skill_pg_front'],192,206,404,441, 0.96, True):
            print("FRONT")
        elif self.scanThisROI(self.templateDict['skill_pg_back'],192,206,404,441, 0.96, True):
            print("BACK")

    def AQ_whichPageNumber(self):
        if self.scanThisROI(self.templateDict['skill_pg_1'],93,129,150,250, 0.93, True):
            print("1")
        elif self.scanThisROI(self.templateDict['skill_pg_2'],93,129,150,250, 0.93, True):
            print("2")
        elif self.scanThisROI(self.templateDict['skill_pg_3'],93,129,150,250, 0.93, True):
            print("3")

    
    def AQ_placeSkills(self):
        if self.scanThisROI(self.templateDict['skillpgequip'],175,206,765, 842 , 0.8, True):
            self.sendTimedTap(770,835,180,200, keyConstants.SHORT_TAP_DURATION)
            BotTools.time.sleep(2)
            self.sendTimedTap(180,210,340,360, keyConstants.SHORT_TAP_DURATION)
            print("skill 1 equip location")
            BotTools.time.sleep(2)
        if self.scanThisROI(self.templateDict['skillpgequip'],271,303,765, 842, 0.8, True):
            self.sendTimedTap(770,835,280,295, keyConstants.SHORT_TAP_DURATION)
            BotTools.time.sleep(2)
            self.sendTimedTap(190,210,253,273, keyConstants.SHORT_TAP_DURATION)
            print("skill 2 equip location")
            BotTools.time.sleep(2)
        if self.scanThisROI(self.templateDict['skillpgequip'],369,401,765, 842 , 0.8, True):
            self.sendTimedTap(770,835,377,390, keyConstants.SHORT_TAP_DURATION)
            BotTools.time.sleep(2)
            self.sendTimedTap(250,270,200,220, keyConstants.SHORT_TAP_DURATION)
            print("skill 3 equip location")
            BotTools.time.sleep(2)
        if self.scanThisROI(self.templateDict['skillpgequip'],466, 494,765, 842 , 0.8, True):
            self.sendTimedTap(770,835,475,485, keyConstants.SHORT_TAP_DURATION)
            BotTools.time.sleep(2)
            self.sendTimedTap(340,360,200,220, keyConstants.SHORT_TAP_DURATION)
            print("skill 4 equip location")
            BotTools.time.sleep(2)

    def AQ_countActiveSkills(self):
        #return n-1 b/c each section has "dummy skill" - preset button - which isnt skill but is accounted for in the #
        if self.scanThisROI(self.templateDict['6skillsavail'],97, 116,613, 630 , 0.8, True):
            print("5 skills baby")
            return 5
        elif self.scanThisROI(self.templateDict['5skillsavail'],97, 116,613, 630 , 0.8, True):
            print("4 skills baby")
            return 4
        elif self.scanThisROI(self.templateDict['4skillsavail'],97, 116,613, 630 , 0.8, True):
            print("3 skills baby")
            return 3
        elif self.scanThisROI(self.templateDict['3skillsavail'],97, 116,613, 630 , 0.8, True):
            print("2 skills baby")
            return 2
        elif self.scanThisROI(self.templateDict['2skillsavail'],97, 116,613, 630 , 0.8, True):
            print("1 skills baby")
            return 1
        elif self.scanThisROI(self.templateDict['1skillsavail'],97, 116,613, 630 , 0.8, True):
            print("0 skills baby")
            return 0


    def AQ_removeSkill(self, skillNum):
        if skillNum == 0 and self.scanThisROI(self.templateDict['removeSkillFromWheel'],313,335,200, 226 , 0.8, True):
            #205-211 x y 235-240
            self.sendTimedTap(210,215,320,325, keyConstants.SHORT_TAP_DURATION)
            print("skill 1 equip location")
        if skillNum == 1 and  self.scanThisROI(self.templateDict['removeSkillFromWheel2'],225,250,200, 226, 0.8, True):
            self.sendTimedTap(205,211,235,240, keyConstants.SHORT_TAP_DURATION)
            print("skill 2 equip location")
        if skillNum == 2 and  self.scanThisROI(self.templateDict['removeSkillFromWheel'],176,197,268, 292 , 0.8, True):
            self.sendTimedTap(277,282,182,187, keyConstants.SHORT_TAP_DURATION)
            print("skill 3 equip location")
        if skillNum == 3 and  self.scanThisROI(self.templateDict['removeSkillFromWheel'],176, 197,355, 378 , 0.8, True):
            self.sendTimedTap(363,368,185,190, keyConstants.SHORT_TAP_DURATION)
            print("skill 4 equip location")
        if skillNum == 4 and  self.scanThisROI(self.templateDict['removeSkillFromWheelBig'],277, 302,299, 323 , 0.8, True):
            self.sendTimedTap(307,312,287,292, keyConstants.SHORT_TAP_DURATION)
            print("skill 5 equip location")


    def AQ_equipNewSkills(self, level):
        self.openInGameMenu()
        if self.checkIfInMenu():
            self.enterSubMenu('skillicon', cMenuOption.SKILL_MENU)
        if self.checkIfRightSubMenu('skillpage'): #we at skill page. now check status of skill slots.
            chosenTab = self.whichSkillTab()
            if chosenTab == level:
                for x in range(5):
                    if not self.AQ_isEmptySlot(x):
                        self.AQ_removeSkill(x)
                self.AQ_placeSkills()
                while not self.scanThisROI(self.templateDict['newmenuicon'],7,47,900, 954, 0.83, True):
                    self.toggleKeyCMD(keyCodes.ESC_KEY)
                    BotTools.time.sleep(2)


            if self.scanThisROI(self.templateDict['bottom_left_skillbtn'],2,35,167, 235 , 0.8, True):
                pass
    
    def whichSkillTab(self):
        roi = self.grabROIColor(71,534,30,95)
        hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv,(5,50,50), (15, 255, 255) )
        mm = cv.findNonZero(mask)
        avg = np.average(mm, axis = 0) #71 corresponds to y starting point of ROI so have to adjust for it [since everything done w/ respect to (0,0)]
        selectedTab = avg[0][1] + 71
        print(type(avg))
        print(avg[0][0] + 30)
        if selectedTab >= 71 and selectedTab <= 131:
            print("lv 1")
            return 1
        elif selectedTab >= 132 and selectedTab <= 199:
            print("lv 30")
            return 30
        elif selectedTab >= 200 and selectedTab <= 265:
            print("lv 60")
            return 60
        elif selectedTab >= 266 and selectedTab <= 333:
            print("lv 100")
            return 100
        
        return -1 #ruh roh
    
    def AQ_autoEquip(self):
        runOnce = True
        while runOnce:
            if self.scanThisROI(self.templateDict['equipbtn'], 285,305,535,616, 0.8, True):
                self.sendTimedTap(535+ self.matchCoords.xyLoc[0] - 10, 535 + self.matchCoords.xyLoc[0] + 10, 285 + self.matchCoords.xyLoc[1] - 5, 285 + self.matchCoords.xyLoc[1], keyConstants.SHORT_TAP_DURATION)
                BotTools.time.sleep(3)
            if not self.scanThisROI(self.templateDict['equipbtn'], 285,305,535,616, 0.8, True):
                runOnce = False


    
    def forcedQtest(self): #replace forcedtut with this
        roi = self.grabROIColor(220,330,195,815)
        hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv,(5,25,50), (25, 255, 255) )
        mm = cv.findNonZero(mask)
        t = mask[0:110, 5:105] # + 20 - 20
        #t = mask[0:110, 110:215]
        #t = mask[0:110, 220:325]
        #t = mask[0:110, 340:435]
        #t = mask[0:110, 450:550]
        #t = mask[0:110, 560:620]
        s = cv.findNonZero(t)
        avg = np.average(s, axis = 0)
        print(avg)
        print(s)
        print(t)
        #avg = np.average(mm, axis = 0) #71 corresponds to y starting point of ROI so have to adjust for it [since everything done w/ respect to (0,0)]
        #selectedTab = avg[0][1] + 71
        #print(len(mm))
        cv.imshow("oj", mask)
        cv.imshow("oj2", t)
        #cv.imshow("oj2", t)
        cv.waitKey(0)

    
    def freeABTaken(self):
        roi = self.grabROI(280,320,655, 745, True)
        hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv,(0,5,20), (5, 255, 255) )
        mm = cv.findNonZero(mask)
        cv.imshow("oj", mask)
        cv.waitKey(0)

        if mm is not None:
            return True
        return False #false if not famed, true if famed


    def currAmtABold(self):
        minutes = 0
        seconds = 0
        for x in range(0,10):
            tempName = 'abtimer' + str(x)
            if self.scanThisROI(self.templateDict[tempName],263,288,295,310,0.89, True):
                minutes += pow(10,2)*x
            if self.scanThisROI(self.templateDict[tempName],263,288,308,324,0.89, True):
                minutes += 10*x
            if self.scanThisROI(self.templateDict[tempName],263,288,322,338,0.89, True):
                minutes += x
            if self.scanThisROI(self.templateDict[tempName],263,288,345,362,0.89, True):
                seconds += 10*x
            if self.scanThisROI(self.templateDict[tempName],263,288,363,376,0.89, True):
                seconds += x   
            '''
            if self.scanThisROI(self.templateDict[tempName],265,290,286,300,0.9, True):
                minutes += pow(10,2)*x
            if self.scanThisROI(self.templateDict[tempName],265,290,299,313,0.9, True):
                minutes += 10*x
            if self.scanThisROI(self.templateDict[tempName],265,290,311,327,0.9, True):
                minutes += x
            if self.scanThisROI(self.templateDict[tempName],265,290,344,358,0.9, True):
                seconds += 10*x
            if self.scanThisROI(self.templateDict[tempName],265,290,357,375,0.9, True):
                seconds += x   
            '''
        
        res = str(minutes) + ":" + str(seconds)
        print(res)
    
    def currAmtAB(self):
        minutes = 0
        seconds = 0
        for x in range(0,10):
            tempName = 'abtimer' + str(x)
            if self.scanThisROI(self.templateDict[tempName],263,288,295,310,0.89, True):
                minutes += pow(10,2)*x
            if self.scanThisROI(self.templateDict[tempName],263,288,308,324,0.89, True):
                minutes += 10*x
            if self.scanThisROI(self.templateDict[tempName],263,288,322,338,0.89, True):
                minutes += x
            if self.scanThisROI(self.templateDict[tempName],263,288,345,362,0.89, True):
                seconds += 10*x
            if self.scanThisROI(self.templateDict[tempName],263,288,362,379,0.89, True):
                seconds += x   
            '''
            if self.scanThisROI(self.templateDict[tempName],265,290,286,300,0.9, True):
                minutes += pow(10,2)*x
            if self.scanThisROI(self.templateDict[tempName],265,290,299,313,0.9, True):
                minutes += 10*x
            if self.scanThisROI(self.templateDict[tempName],265,290,311,327,0.9, True):
                minutes += x
            if self.scanThisROI(self.templateDict[tempName],265,290,344,358,0.9, True):
                seconds += 10*x
            if self.scanThisROI(self.templateDict[tempName],265,290,357,375,0.9, True):
                seconds += x   
            '''
        
        res = str(minutes) + ":" + str(seconds)
        print(res)

    def useAB(self):
        if not self.confirmedAQ2():
            print("AB not used; checking AB")
            self.pressMatchCoords(305,330,480,502)
    
    def checkFreeAB(self):
        if self.scanThisROI(self.templateDict['abtaken'], 280,330,643,754, 0.99, False):
            print("free ab taken")

    def checkKickSave(self):
        if self.scanThisROI(self.templateDict['kicksavenotenabled'], 368,410,728,765, 0.8, False):
            print("not enabled")
        else:
            print("on")
    

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
                        print("made it! we in game baby")
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
                print("in game")
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