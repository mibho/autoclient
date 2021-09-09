
import BotFunctions as AutoClient
from Constants import *
from ROICoords import cScanCoords as coords
from pdb import set_trace as bp
import random
import NoxClientManager as NoxMgr

import multiprocessing
import time
if __name__ == '__main__':   
    key = 0
    nprocs = multiprocessing.cpu_count()
    print(nprocs)
    n_mgr = NoxMgr.NoxClientManager()
    n_mgr.autoDetectNoxProcesses()
    print(n_mgr.detectedDevicesADBList)
    for k in n_mgr.detectedDevicesADBList:
        key = k
    test = AutoClient.cBotFunctions( n_mgr.detectedDevicesADBList[key][0], n_mgr.detectedDevicesADBList[key][1], \
                                            n_mgr.detectedDevicesADBList[key][2], n_mgr.adbConnectedDevs[key], "lol")
            
    
    #test.getInputDeviceID()
    #while 1:
    #    test.charSelectTest()
    #    AutoClient.time.sleep(0.5)
    #test.closePlayStoreReview()
    #if test.freeABTaken():
    #test.OOG_pressAndroidTasksMenu()
    #if test.scanThisROI(test.templateDict['updateReqPopup2'], 110,200,195,600 ,0.8, True):
    #if test.scanThisROI(test.templateDict['updateReqPopup3'], 110,420,195,775 ,0.8, True):
    #test.findSelectedChar
    #    print(test.matchCoords.xyLoc[1] + 405)
    #    test.OOG_forceCloseMapleApp()#[self.adjustYoffset(125):self.adjustYoffset(155), 250:670]screen[self.adjustYoffset(48):self.adjustYoffset(98), 675:720]
    #test.getTemplate(327 - 50, 327, 641 - 100,641 + 100, True)
    #test.fameLoop("QWEASDZXC123", "lol", "lol2") #610-945    y 50-440
    #test.botLoop(0, 1)
    test.botLoop(0,1)
    #if test.scanThisROI(test.templateDict['communityicon'], 50,440,610,945 ,0.8, True):
    #    print("yeah we found baby")
    #    print(test.matchCoords.xyLoc) #x = 24 | + 610, y = 355 | + 50

    #test.botLoop(0, True)
    #test.getTemplate(263,288,290,337, False) x 208-450  145-370 y 
    #test.checkKickSave()
    #test.getTemplate(368,410,728,765, True)#263,288,295,309, False)
    #test.currAmtAB()
    #test.dbConn.updateSingleVar("MAIN_TBL_CLIENTS", "accDataRegistered", (1,))
        
    #while 1:
        #if (test.findTemplateMatch2(test.templateDict['questbulb'], 0.85) or test.findTemplateMatch2(test.templateDict['questbookicon'], 0.85)):
        #    print (test.matchCoords.xyLoc)
    #    test.sendTimedTap(300,300,300,300, 0.15)
        #test.doEliteDung(0)
        #print("doEliteDung finished")
    #    time.sleep(1)
    #test.toggleKeyCMD(keyCodes.PG_UP_KEY)
    #test.OOG_forceCloseMapleApp()
    #test.forcedQtest()
    #while 1:
        #test.checkForPopups()
        #AutoClient.time.sleep(1)
        #test.confirmedAQ2()
        #AutoClient.time.sleep(1.5)
    '''
    coords for communitypage #6-152 x   | 10-50 y

    coords for search players btn press   # 147-227 x  | 480-510 y 

    coords for search players box sign 388-568 x | 110-150 y

    coords for entering name press  x 370-580 | 290-305 y

                365-590 x    284-310 y [empty name box]
    
    coords for confirm btn  510-660 x 380-415 y

    coords for player search results 355-605 x  115-150 y 

    280-400 x 220-315 y [press location to get to player info page]

    coords for player info page: 5-145 x | 10-50 y 

    638-670 x  81-113 y 


    '''
    #test.yes()
    #test.enterText("hi")
    #test.getColorSS2(65,460,620,950, "ok.png")
    #he = test.getTemplate2(65,460,620,950)
    #AutoClient.cv.imwrite("ok.png", he)
    print("ok done")
    x = 1
    while x == 2:
        #test.fameNotUsed()
        #test.getTemplate(18, 43,15,143) #143,154,116,123 <- loc of 7 in 74
        #test.whichSkillTab()
        #test.AQ_returnEmptySlots()
        #test.getTemplate(153,167,743,752) #char lobby level leftmost-digit eg: 74 <- location of the 7
        #test.getTemplate(153,167,753,763) #char lobby level middle digit eg: 63 <- location of the 3
        
        #test.getTemplate(122,140,396,567) #144, 153,123,130 <- loc of 4 in 74
        #print(test.AQ_purpleQuestLevel())
        '''
        if test.scanThisROI(test.templateDict['questlv5purpL'], 142, 155, 116, 123, 0.8, True): #142, 155, 123, 130 scan loc for top quest
            print("1st 5 detected!")
        if test.scanThisROI(test.templateDict['questlv5purpL'], 142, 155, 123, 130, 0.8, True): #142, 155, 123, 130 scan loc for top quest
            print("2nd 5 detected!")
        
        if test.scanThisROI(test.templateDict['xenonshipmenu'], 117, 145, 391, 572, 0.8, True):
            print("intheshipmenu")

            #press confirm button coords:
            #506-666 x   380-410 y
        '''
        AutoClient.time.sleep(1)
    

    