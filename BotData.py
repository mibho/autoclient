import cv2 as cv 

#import AccInfo
#import States
#import ByteStrings



class cBotData:
    def __init__(self):
        self.templateDict = {

            #stageCheck() function template files
            'SCHK_0atHomeScreen'   : cv.imread('SCHK_0atHomeScreen.png', 0),
            'SCHK_1exitbanner'   : cv.imread('SCHK_1exitbanner.png', 0),
            'SCHK_vivoxTitleRegion'   : cv.imread('SCHK_vivoxTitleRegion.png', 0), #820-930 X | 400-510 Y
            'SCHK_12newTitleRegion' : cv.imread('SCHK_12newTitleRegion.png', 0), #10-45 x     492-523 y
            'SCHK_12titleScreen'   : cv.imread('SCHK_12titleScreen.png', 0), 
            'SCHK_1roiTitleInosys'   : cv.imread('SCHK_1roiTitleInosys.png', 0), 
            'SCHK_20roiTitleCharDetected' : cv.imread('SCHK_20roiTitleCharDetected.png', 0),
            'SCHK_30loadingPage' : cv.imread('SCHK_30loadingPage.png', 0), 
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


            #char lobby counting 
            'botleft1'   : cv.imread('botleft1.png', 0),
            'botleft2'  : cv.imread('botleft2.png', 0),
            'botright1' : cv.imread('botright1.png', 0),
            'botright2' : cv.imread('botright2.png', 0),

            'topleft1': cv.imread('topleft1.png',0),
            'topleft2'        :  cv.imread('topleft2.png',0),
            'topright1'      :   cv.imread('topright1.png',0),

            'charLobbyLevel0' : cv.imread('charLobbyLevel0.png', 0),#char lobby level leftmost-digit eg: 74 <- location of the 7 
            'charLobbyLevel1' : cv.imread('charLobbyLevel1.png', 0),# x: 743-752 | y: 153,167
            'charLobbyLevel2' : cv.imread('charLobbyLevel2.png', 0),
            'charLobbyLevel3' : cv.imread('charLobbyLevel3.png', 0),#char lobby level middle digit eg: 63 <- location of the 3
            'charLobbyLevel4' : cv.imread('charLobbyLevel4.png', 0),# x: 753-763 | y: 153,167
            'charLobbyLevel5' : cv.imread('charLobbyLevel5.png', 0),
            'charLobbyLevel6' : cv.imread('charLobbyLevel6.png', 0),
            'charLobbyLevel7' : cv.imread('charLobbyLevel7.png', 0),
            'charLobbyLevel8' : cv.imread('charLobbyLevel8.png', 0),
            'charLobbyLevel9' : cv.imread('charLobbyLevel9.png', 0),


            '''
            -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------






            '''

            #returnToCharSelect template
            'resetexitmenu' : cv.imread('resetexitmenu.png', 0),

            #AQ_closeAdvicePopup template
            'advicePopupPic' : cv.imread('advicePopupPic.png', 0), #259,337 x   175,249 y   525,544 x  146,164 y

            #AQ_inDialog templates | also for AQ_questObtained, AQ_claimRewardIfGiven
            'nextdialog' : cv.imread('nextdialog.png', 0), # coords: 866-954 x 360-390 y |     scan area: 820-960 x 318-420 y
            'questconfirm'   : cv.imread("questconfirm.png", 0),
            'questaccept'   : cv.imread("questaccept.png", 0),
            'questcomplete'   : cv.imread("questcomplete.png", 0),
            'questclaimreward'   : cv.imread("questclaimreward.png", 0),

            #AQ_inMultiQDialog templates
            'newmultiqstart' : cv.imread('newmultiqstart.png' ,0),   #219-370 x 392-509 y
            'newmultiqend' : cv.imread('newmultiqend.png' ,0),


            #AQ_startForcedTut templates
            'newtuticon' : cv.imread('newtuticon0.png', 0),
            'inNewTut' : cv.imread('inNewTut.png', 0),
            
            #AQ_handleDialog templates
            'questaccept2' : cv.imread('questaccept2.png', 0),

            #AQ_autoassignSP
            'autoassign' : cv.imread('autoassign.png', 0),
            'autoskillpopup' : cv.imread('autoskillpopup.png', 0),


            #quest detector for purple quests that required travel to veritas 

            'questpurplv1' : cv.imread('questpurplv1.png', 0),
            'questpurplv2' : cv.imread('questpurplv2.png', 0),
            'questpurplv3' : cv.imread('questpurplv3.png', 0),
            'questpurplv4' : cv.imread('questpurplv4.png', 0),
            'questpurplv5' : cv.imread('questpurplv5.png', 0),
            'questpurplv6' : cv.imread('questpurplv6.png', 0),
            'questpurplv7' : cv.imread('questpurplv7.png', 0),
            'questpurplv8' : cv.imread('questpurplv8.png', 0),
            'questpurplv9' : cv.imread('questpurplv9.png', 0),
            'questpurplv0' : cv.imread('questpurplv0.png', 0),


            #AQ_checkAndReturnLevel
            'leveltext0' : cv.imread("leveltext0.png", 0), 
            'leveltext1' : cv.imread("leveltext1.png", 0),
            'leveltext2' : cv.imread("leveltext2.png", 0), 
            'leveltext3' : cv.imread("leveltext3.png", 0),
            'leveltext4' : cv.imread("leveltext4.png", 0), 
            'leveltext5' : cv.imread("leveltext5.png", 0),
            'leveltext6' : cv.imread("leveltext6.png", 0), 
            'leveltext7' : cv.imread("leveltext7.png", 0),
            'leveltext8' : cv.imread("leveltext8.png", 0), 
            'leveltext9' : cv.imread("leveltext9.png", 0),

            #AQ_isEmptySlot()
            'skill_btn_slot_0' : cv.imread('skill_btn_slot_0.png', 0),
            
            #AQ_frontOrBackSkillPage()

            'skill_pg_front' : cv.imread('skill_pg_front.png', 0), #405-441 x  192,206 y 
            'skill_pg_back' : cv.imread('skill_pg_back.png', 0),

            #AQ_whichPageNumber
            'skill_pg_1' : cv.imread('skill_pg_1.png', 0), # y 96-126 x 152-181
            'skill_pg_2' : cv.imread('skill_pg_2.png', 0), #186-215
            'skill_pg_3' : cv.imread('skill_pg_3.png', 0), #218-247

            #AQ_placeSkills
            'skillpgequip' : cv.imread('skillpgequip.png', 0), 

            #AQ_countActiveSkills
            '6skillsavail' : cv.imread('6skillsavail.png', 0),
            '5skillsavail' : cv.imread('5skillsavail.png', 0),
            '4skillsavail' : cv.imread('4skillsavail.png', 0),
            '3skillsavail' : cv.imread('3skillsavail.png', 0),
            '2skillsavail' : cv.imread('2skillsavail.png', 0),
            '1skillsavail' : cv.imread('1skillsavail.png', 0),
            '0skillsavail' : cv.imread('0skillsavail.png', 0),

            'removeSkillFromWheel' : cv.imread('removeSkillFromWheel.png', 0),
            'removeSkillFromWheel2' : cv.imread('removeSkillFromWheel2.png', 0),
            'removeSkillFromWheelBig' : cv.imread('removeSkillFromWheelBig.png', 0),

            'skillpage' : cv.imread('skillpage.png', 0),
            'skillicon' : cv.imread('skillicon.png', 0),

            #AQ_autoequip
            'equipbtn' : cv.imread('equipbtn.png', 0),


            'forcedtutblueskip' : cv.imread('forcedtutblueskip.png', 0),
            'newtutlight' : cv.imread('newtutlight.png', 0),


            'dungeonicon' : cv.imread('dungeonicon.png', 0),
            'dungpage' : cv.imread('dungpage2.png', 0),

            'elitedungpic' : cv.imread('elitedungpic.png', 0),
            'elitedungpage' : cv.imread('elitedungpage.png', 0),
            'elitedungFinishedPage' : cv.imread('elitedungFinishedPage.png', 0),
            'elitedungOption0Exit' : cv.imread('elitedungOption0Exit.png', 0), #465,502 Y  235-282 x
            'elitedungOption1Menu' : cv.imread('elitedungOption1Menu.png', 0), #420,540 x
            'elitedungOption2Again' : cv.imread('elitedungOption2Again.png', 0), #620-775 x
            'elitedungWeeklyRewardDone' : cv.imread('elitedungWeeklyRewardDone.png', 0), #171,271 x  255,376 y
            
            'tasksicon' : cv.imread('tasksicon.png', 0),
            'taskpage' : cv.imread('taskpage.png', 0),
            
            'weeklyrewardclaimed' : cv.imread('weeklyrewardclaimed.png', 0),
            'weeklyedtixreward' : cv.imread('weeklyedtixreward.png', 0),
            'edtixclaimed' : cv.imread('edtixclaimed.png', 0),


            'addTix' : cv.imread('addTix.png', 0),  #572-603    314-345 y 
            'minusTix' : cv.imread('minusTix.png', 0), #413-444 
            '1tixselected' : cv.imread('1tixselected.png', 0),
            '2tixselected' : cv.imread('2tixselected.png', 0),  #  498-522  314-345 y 
            '3tixselected' : cv.imread('3tixselected.png', 0), #  
            'confirmTixUse' : cv.imread('confirmTixUse.png', 0), # 363-600 x 171-207 y 
            'tixconfirm' : cv.imread('tixconfirm.png', 0),


            'dungabon' : cv.imread('dungabon.png', 0),
            'dungaboff' : cv.imread('dungaboff.png', 0),
            'dungcreateroom' : cv.imread('dungcreateroom.png', 0),



            'kicksavenotenabled' : cv.imread('kicksavenotenabled.png', 0),
            'freefullab' : cv.imread('freefullab.png', 0),
            'abtaken' : cv.imread('abtaken.png', 0),

            'abtimer0' : cv.imread('abtimer0.png', 0),
            'abtimer1' : cv.imread('abtimer1.png', 0),
            'abtimer2' : cv.imread('abtimer2.png', 0),
            'abtimer3' : cv.imread('abtimer3.png', 0),
            'abtimer4' : cv.imread('abtimer4.png', 0),
            'abtimer5' : cv.imread('abtimer5.png', 0),
            'abtimer6' : cv.imread('abtimer6.png', 0),
            'abtimer7' : cv.imread('abtimer7.png', 0),
            'abtimer8' : cv.imread('abtimer8.png', 0),
            'abtimer9' : cv.imread('abtimer9.png', 0),


            'havemailnotif' : cv.imread('havemailnotif.png', 0),
            'mailbox' : cv.imread('mailbox.png', 0),
            'havemail2' : cv.imread('havemail2.png', 0),
            'mailconfirmreward' : cv.imread('mailconfirmreward.png', 0),
            'nomail' : cv.imread('nomail.png', 0),
            'mailnotif' : cv.imread('mailnotif.png', 0),

            'ed3tix' : cv.imread('ed3tix.png', 0),
            'ed2tix' : cv.imread('ed2tix.png', 0),
            'ed1tix' : cv.imread('ed1tix.png', 0),
            'ed0tix' : cv.imread('ed0tix.png', 0),

            'newtelebtn'  : cv.imread('newtelebtn.png',0),

            'questbulb' : cv.imread('questbulbicon.png', 0),
            'questbookicon' : cv.imread('questbookicon.png', 0),
            'questavail' : cv.imread('questavail.png', 0),
            'xenonshipmenu' : cv.imread('xenonshipmenu.png', 0),
            'regquestarrow'  : cv.imread('regquestarrow.png',0),

            'psreviewicon' : cv.imread('psreviewicon.png', 0),
            'exitreviewbtn' : cv.imread('exitreviewbtn.png', 0),

            'bottom_left_skillbtn' : cv.imread('bottom_left_skillbtn.png', 0),
            'communityicon' : cv.imread('communityicon.png', 0),
            'communitypage' : cv.imread('communitypage.png', 0),
            'searchplayersbtn' : cv.imread('searchplayers.png', 0),
            'searchplayersbox' : cv.imread('searchplayersbox.png', 0),
            'emptynamebox' : cv.imread('emptynamebox.png', 0),
            'confirmbtn' : cv.imread('confirmbtn.png', 0),
            'searchresults' : cv.imread('searchresults.png', 0),
            'playerinfopage' : cv.imread('playerinfopage.png', 0),

            'newmenuicon' : cv.imread('newmenuicon.png', 0),
            'inmenucheck' : cv.imread('inmenucheck.png', 0),
                 }
        page_elite_dung = ['']                   
        self.pageInfoDict = {

        }
'''

            #ROI of weekly mission tasks (all): 171- 698 x |  121,376 y 
            # top half Y: 121,246. bottom half Y: 255,376 mailconfirmreward
            
                #press y| 473,493 x| 136,390
            
'''