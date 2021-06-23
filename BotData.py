import cv2 as cv 

#import AccInfo
#import States
#import ByteStrings



class cBotData:
    def __init__(self):
        self.templateDict = {

            #stageCheck() function template files
            'SCHK_0atHomeScreen'   : cv.imread('sCHK_0atHomeScreen2.png', 0),
            'SCHK_1exitbanner'   : cv.imread('SCHK_1exitbanner.png', 0),
            'SCHK_vivoxTitleRegion'   : cv.imread('SCHK_vivoxTitleRegion.png', 0), #820-930 X | 400-510 Y
            'SCHK_12newTitleRegion' : cv.imread('SCHK_12newTitleRegion.png', 0), #10-45 x     492-523 y
            'SCHK_12titleScreen'   : cv.imread('SCHK_12titleScreen.png', 0), 
            'SCHK_1roiTitleInosys'   : cv.imread('SCHK_1roiTitleInosys.png', 0), 
            'SCHK_20roiTitleCharDetected' : cv.imread('SCHK_20roiTitleCharDetected.png', 0),
            'SCHK_30loadingPage' : cv.imread('SCHK_302loadingPage.png', 0), 
            'SCHK_40charStart' : cv.imread('SCHK_40charStart.png', 0),  
            'bannerexit2' : cv.imread('bannerexit2.png', 0),  

            #template files for update/download stage
            'updateReqPopup' : cv.imread('updateReqPopup.png', 0), #400-550 x 100-165 y
            'updateReqPopup2' : cv.imread('updateReqPopup2.png', 0),
            'updateReqPopup3' : cv.imread('updateReqPopup3.png', 0),
            'updateReqPopup31' : cv.imread('updateReqPopup31.png', 0),
            'updateReqPopup4GooglePlay' : cv.imread('updateReqPopup4GooglePlay.png', 0),
            'updateReqPopup4GooglePlayReady' : cv.imread('updateReqPopup4GooglePlayReady.png', 0),
            'updateReqPopup4GooglePlayReady2' : cv.imread('updateReqPopup4GooglePlayReady2.png', 0),
            'downloadwarning' : cv.imread('downloadwarning.png', 0),
            'msmstoppedmsgbox' : cv.imread('msmstoppedmsgbox.png', 0),
            

            #checkForPopups() function template files
            'revivebtn'   : cv.imread('revivebtn.png', 0),  
            'mapleviewpopup' : cv.imread('mapleviewpopup.png', 0), 
            'exitpic'   : cv.imread('exitpic.png', 0),  
            'exitpic2' : cv.imread('exitpic2.png', 0), 
            'adexit3'   : cv.imread('adexit3.png', 0),  
            'newmenuexit' : cv.imread('newmenuexit.png', 0), 
            'newmenuexit2'   : cv.imread('newmenuexit2.png', 0),  
            'newcontentconfirm' : cv.imread('newcontentconfirm.png', 0), 
            'violettabotpopup' : cv.imread('violettabotpopup.png', 0), 
            'newtuticon' : cv.imread('newtuticon.png', 0), 



                 }
        page_elite_dung = ['']                   
        self.pageInfoDict = {

        }