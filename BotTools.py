#--------------------------------------
# system/native imports 
#--------------------------------------
import time
#--------------------------------------
# public/3rd-party imports 
#--------------------------------------
import win32gui, win32con, win32ui
import numpy as np
import cv2 as cv
#--------------------------------------
# project specific imports  
#--------------------------------------
#from NoxClientHandler import cNoxClientHandler
from Constants import *
from Constants import keyCodes
import Coords
import processTools
#--------------------------------------s

class cBotTools:

    CLIENT_HEIGHT = 540 + 33
    CLIENT_WIDTH  = 960 

    def __init__(self, pID, windowName, clientNum, deviceObj, adbSockInfo):
        #super(cBotTools,self).__init__(pID, windowName, clientNum, deviceObj, adbSockInfo)
        print("cBotTools start of ctor")
        self.windowName = windowName

        self.hwnd = processTools.getHWNDFromTitle(windowName)
        self.device = deviceObj#.device(adbSockInfo)
        self.cNum = clientNum + 1
        
        self.matchCoords = Coords.cCoords(0,0)

        self.afkTimerStarted = False
        self.popupDetected = False
        
        print("cBotTools init success; end of ctor")
    
    def returnColorSS(self, colormode):

        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.CLIENT_WIDTH, self.CLIENT_HEIGHT)
        cDC.SelectObject(dataBitMap)
            
        cDC.BitBlt((0,0),(self.CLIENT_WIDTH, self.CLIENT_HEIGHT) , dcObj, (0,0), win32con.SRCCOPY)


            
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype = 'uint8')
        img.shape = (self.CLIENT_HEIGHT, self.CLIENT_WIDTH,4)

            # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

            # store img as data in numpy array then convert to grayscale
        img = np.ascontiguousarray(img)
        if not colormode:
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        return img
    
    def grabROI(self, minY, maxY, minX, maxX, colormode):
        img = self.returnColorSS(colormode)
        roi = img[minY + 33:maxY + 33, minX : maxX]
        return roi

    def getTemplate(self, minY, maxY, minX, maxX, colormode):
        self.preClickImg = self.returnColorSS(colormode)
        roi = self.preClickImg[minY + 33:maxY + 33, minX : maxX].copy() #still need orig full img to 
        print("saving")
            #res = cv.matchTemplate(roi ,temp, eval('cv.TM_CCOEFF_NORMED')) #cv.TM_CCOEFF_NORMED
        #res = cv.matchTemplate(roi ,self.templateDict['questavail'], eval('cv.TM_CCOEFF_NORMED')) #cv.TM_CCOEFF_NORMED
        cv.imwrite("ok.png", roi)
        cv.imwrite("ok1.png", self.preClickImg)
        time.sleep(1)

    def saveImageAs(self, minY, maxY, minX, maxX, colormode, picName):
        picName += ".png"
        self.preClickImg = self.returnColorSS(colormode)
        #self.preClickImg = cv.cvtColor(self.preClickImg, cv.COLOR_RGB2BGR)
            #487-515 y 263-302 516-490
        roi = self.preClickImg[minY + 33:maxY + 33, minX : maxX].copy() #still need orig full img to 
        print("saving")
        cv.imwrite(picName, roi)
        time.sleep(1)
    

    
    def scanROIAndGetMatches(self, temp, y1,y2,x1,x2 ,threshold, ptsneeded):
        ptsList = []
        roi = self.grabROI(y1,y2,x1,x2)
        res = cv.matchTemplate(roi ,temp, eval('cv.TM_CCOEFF_NORMED')) #cv.TM_CCOEFF_NORMED
        loc = np.where( res >= threshold)

        if np.amax(res) > threshold:
            if ptsneeded:
                for pt in zip(*loc[::-1]):
                    ptsList.append(pt)
            
        
        return ptsList
    

    


    
    def adjustYoffset(self, yC):
        return yC + 33


    

    def getTemplateRet(self, minY, maxY, minX, maxX, n):
        
            #res = cv.matchTemplate(roi ,temp, eval('cv.TM_CCOEFF_NORMED')) #cv.TM_CCOEFF_NORMED
        #res = cv.matchTemplate(roi ,self.templateDict['questavail'], eval('cv.TM_CCOEFF_NORMED')) #cv.TM_CCOEFF_NORMED
        for x in range(0,n):
            self.preClickImg = self.returnGraySS()
            #487-515 y 263-302 516-490
            roi = self.preClickImg[minY + 33:maxY + 33, minX : maxX].copy() #still need orig full img to 
            name = "z" + str(x) + ".png"
            cv.imwrite(name, roi)
            print("captured " + str(x))
        time.sleep(1)

    def sendKeyCMD(self, whatKeyCode, onOrOff):
        completeCMD = keyConstants.SEND_EVENTCMD + eventType.EV_KEYPRESS + " " + whatKeyCode \
                        + " " + onOrOff + keyConstants.SEND_EVENTCMD + keyConstants.CONFIRM_CMD
        self.device.shell(completeCMD)
    
    def toggleKeyCMD(self, whatKeyCode):
        self.sendKeyCMD(whatKeyCode, keyCodes.KPRESS_DOWN_EOL)
        self.sendKeyCMD(whatKeyCode, keyCodes.KPRESS_RELEASE_EOL)

    def sendTouchCMD(self, x, y, onOrOff):
        if onOrOff == keyCodes.KTYPE_OFF:
            x = y = 0
            mCMD = ""
        else:
            mCMD = keyConstants.SEND_EVENTCMD + " 3 48 5 ;"
        queueCMD = keyConstants.SEND_EVENTCMD + eventType.EV_KEYPRESS + keyCodes.TOUCH_KEY + " " + onOrOff + " ;"
        pressXCMD = keyConstants.SEND_EVENTCMD + eventType.EV_INPUT + inputCodes.TOUCH_COORD_X + str(x) + " ;"
        pressYCMD = keyConstants.SEND_EVENTCMD + eventType.EV_INPUT + inputCodes.TOUCH_COORD_Y + str(y) + " ;"
        confirmCMD = keyConstants.SEND_EVENTCMD + keyConstants.TOUCH_CONFIRM_CMD \
                    + keyConstants.SEND_EVENTCMD + keyConstants.CONFIRM_CMD
        
        completeCMD = queueCMD + pressXCMD + pressYCMD + mCMD + confirmCMD
       #print(completeCMD)
        self.device.shell(completeCMD)
    
    def sendResetCMD(self):
        confirmCMD = keyConstants.SEND_EVENTCMD + keyConstants.TOUCH_CONFIRM_CMD \
                    + keyConstants.SEND_EVENTCMD + keyConstants.CONFIRM_CMD
        self.device.shell(confirmCMD)
    
    def inputTap(self, xC1, xC2, yC1, yC2, delay):
        tempCoords = Coords.randPoint(xC1,xC2, yC1,yC2)
        randX = str(tempCoords[0])
        randY = str(tempCoords[1])
        event_string =  "input tap " + randX + " " + randY  # 1 330 108 
        self.device.shell(event_string)

    def sendTimedTap(self, xC1, xC2, yC1, yC2, delay):
        smoldelay = Coords.randTime(0.8, 2.4)
        time.sleep(smoldelay)
        tempCoords = Coords.randPoint(xC1,xC2, yC1,yC2)
        randX = tempCoords[0]
        randY = tempCoords[1]
        self.sendTouchCMD(randX,randY, keyCodes.KTYPE_ON)
        time.sleep(delay)
        self.sendResetCMD()
        self.sendTouchCMD(randX,randY, keyCodes.KTYPE_OFF)

    def enterText(self, content):
        event_string = "input text " + content 
        self.device.shell(event_string)

    def sendDragCMD(self, swipeDirection, duration, refPoint, startPoint, endPoint): # UP,DOWN,LEFT,RIGHT 
        if swipeDirection == keyConstants.SWIPE_UP or swipeDirection == keyConstants.SWIPE_DOWN:
            xC1 = xC2 = str(refPoint)
            yC1 = str(startPoint)
            yC2 = str(endPoint)
        elif swipeDirection == keyConstants.SWIPE_LEFT or swipeDirection == keyConstants.SWIPE_RIGHT:
            yC1 = yC2 = str(refPoint)
            xC1 = str(startPoint)
            xC2 = str(endPoint)

        completeCMD = keyConstants.INPUT_SWIPECMD + " " + xC1 + " " + yC1 \
                     + " " + xC2 + " " + yC2 + " " + str(duration)     #Swipe X1 Y1 X2 Y2 [duration(ms)]
        self.device.shell(completeCMD)


#for testing only
