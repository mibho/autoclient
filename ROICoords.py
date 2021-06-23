# ( (x1,x2), (y1,y2) )
class cScanCoords:
    
    PATCH_DOWNLOAD = ((356,602),(105,166))
    PATCH_CONFIRM  = ((392,559), (382,417))

    #checkStage coords 237,309,485, 555
    WORLD_INOSYS = ((485,555),(237,309))
    LOBBY_START = ((685,930),(430,497))
    LOBBY_CHARS = ((73,645),(82,483))
    LOBBY_CHAR0POS = ((120,279), (115,250))
    LOBBY_CHAR1POS = ((285,431), (115,250))
    LOBBY_CHAR2POS = ((431,580), (115,250))
    LOBBY_CHAR3POS = ((52,218), (333,468))
    LOBBY_CHAR4POS = ((209,356), (333,468))
    LOBBY_CHAR5POS = ((357,503), (333,468))
    LOBBY_CHAR6POS = ((508,654), (333,468))
    



    #checkforpopups coords
    REVIVE_BUTTON = ((200,391), (345,445)) #ROI scan loc of revive btn 
    POPUP_MAPLEVIEW = ((793,909), (49,80)) #scans certain part of text b/c most consistent
    POPUP_ADS = ((620,912), (19,104))
    POPUP_NEWCONFIRM = ((346,615),(365,455))
    POPUP_VIOLETTA = ((228,763), (110,420))

    #locate quest coords
    QUEST_ARROW = ((150,240), (155,210))
    QUEST_NEWUI_DOT = ((55,90), (140,240))


    
    RESET_EXIT_MENU = ((409,555),(108,158))



    MAIL_IN_DEFAULT = ((457,478),(92,133)) 
    MAIL_IN_PERSONAL = ((765,786),(92,133))


    #handling quest
    USE_TELEROCK = ((537,649), (163,210))
    QUEST_CLAIMREWARD = ((350,602),(443,522)) #questclaimreward
    QUEST_NEXTDIALOG = ((792,960),(342,405))
    QUEST_COMPLETE = ((695,951),(275,365))


    INGAMEMENU_SHOP = ((695,951),(275,365))




    
#self.scanThisROI(self.templateDict['mailnotif'],92,133,457,478, 0.8, True) or self.scanThisROI(self.templateDict['mailnotif'],92,133,765,786, 0.8, True):


class cTouchCoords:
    
    REVIVE_BUTTON = ((214,378), (370,420))
    POPUP_MAPLEVIEW = ((915,940), (18,34)) # targets actual exit 
    POPUP_NEWCONFIRM = ((383,575),(391,438))  #newcontentconfirm
    # (X,Y) are the BASE coords, ie, top left corner of ROI.
    # matchCoords returned w/ respect to BASE coords
    POPUP_ADS = ((750,750), (11,11)) 
    
    RESET_EXIT_MENU = ((275,386),(381,417))

    MAIL_GET_ALL = ((670,770),(466,500))
    
    QUEST_NEWUI_DOT = ((55,90), (140,240))
    USE_TELEROCK = ((488,640), (175,201))
    QUEST_CLAIMREWARD = ((382,577), (461,504))# questclaimreward
    

135,207,489,561
class cSkillCoords:
    SKILLEQ_0TOP = ((756,849),(172,207)) #equip the skill 
    SKILLPIC_0TOP = ((489,561), (135,207)) #'skillpgpreset' : cv.imread('skillpgpreset.png', 0), if scanROI matches, then the topmost skill is the "skill preset" aka not a skill

    SKILLEQ_1TOP = ((756,849),(270,302))
    SKILLPIC_1TOP = ((489,561), (231,302))

    SKILLEQ_2TOP = ((756,849),(367,399))
    SKILLPIC_2TOP = ((489,561), (135,207))

    SKILLEQ_3TOP = ((756,849),(465,496))
    SKILLPIC_3TOP = ((489,561), (427,496))

    #count clockwise from bottom left-most slot. (ie, one above is slot 1, top-most right under #3 is slot 2, top-most near the flip symbol is slot 3, biggest circle is slot 4)
    SKILL_SLOT0 = ((205,242),(313,351)) # tempname = skillslot0
    SKILL_SLOT1 = ((187,224),(230,270)) #skillslot1
    SKILL_SLOT2 = ((235,271),(156,200))
    SKILL_SLOT3 = ((317,358),(165,211))
    SKILL_SLOT4 = ((266,322),(235,304))




print(cTouchCoords.REVIVE_BUTTON[0])