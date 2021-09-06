class colorCode:
    GRAYSCALE = False
    RGB_DEFAULT = True

class eventType:
    EV_REPORTCMD = "0 "
    EV_KEYPRESS  = "1 "
    EV_INPUT     = "3 "

class inputCodes:
    TOUCH_REPORT   = "2 "
    TOUCH_SIZE     = "48 "
    TOUCH_COORD_X  = "53 "
    TOUCH_COORD_Y  = "54 "
    TOUCH_ID       = "57 "   
    TOUCH_PRESSURE = "58 "

class keyCodes:
    UP_KEY             = "103"
    DOWN_KEY           = "108"
    LEFT_KEY           = "105"
    RIGHT_KEY          = "106"
    ESC_KEY            = "158"
    PG_UP_KEY          = "221"
    TOUCH_KEY          = "330"
    HOMETEST_KEY       = "102"
    KPRESS_DOWN_EOL    = "1 ;"
    KPRESS_RELEASE_EOL = "0 ;"

    KTYPE_ON           = "1"
    KTYPE_OFF          = "0"
    
class keyConstants: #EOL = END OF LINE 

    SEND_EVENTCMD      = "sendevent dev/input/event7 "
    INPUT_SWIPECMD     = "input swipe"
    TOUCH_CONFIRM_CMD        = "0 2 0 ;"
    CONFIRM_CMD        = "0 0 0 ;"
    QUICK_TAP_DURATION = 0.07
    SHORT_TAP_DURATION = 0.15
    SWIPE_UP           = 0
    SWIPE_DOWN         = 1
    SWIPE_LEFT         = 2
    SWIPE_RIGHT        = 3
    OP_INC             = 1
    OP_DEC             = 0

class stateConstants:
    RUH_ROH                      = -3
    LOADING_TITLE                = -2
    NOTHING_FOUND                = -1
    L0_at_home_scr               = 0
    L1_at_start_ban              = 1 # start_ban_exit pic. |
    L2_at_title_screen           = 2
    L3_load_entering_game        = 3
    L4_at_char_lobby             = 4
    L5_ingame                    = 5
    L6_mulung                    = 6
    L7_collect_week_rewards      = 7    #getting all stuff from achievements
    L8_daily_dung                 = 8
    L9_elite_dung                = 9
    L10_auto_fame                = 10
    L11_mini_dung                = 11
    L12_exped_leech              = 12
    L13_auto_quest               = 13
    L14_auto_autobattle          = 14
    L15_macro                    = 15
    L16_loading_wait             = 16
    #L16
    

    S20_isdead                    = 20
    S21_new_char_intro            = 21
    S22_popup_visible             = 22
    S23_quest_inprogress          = 23
    S24_in_dialog                 = 24
    S25_on_route                  = 25
    S26_in_menu                   = 26
    S27_in_bag                    = 27
    S28_in_mailbox                = 28
    S29_auto_mail_on              = 29
    S30_new_forced_visible        = 30
    S31_new_confirm_popup         = 31
    S32_mapleview_visible         = 32
    S33_violetta                  = 33


# scan loc for submenu pages    x = 5-91        y = 13-53

class cSwipeCoords:
    LR_DUNGPAGE_YRANGE = (131,530)
    LR_DUNGPAGE_REFPT1 = 533

    UD_SKILLS_XRANGE = (493,931)
    UD_INGAME_MENU_XRANGE = (605, 942)


class pageInfo:        #templateName, menuLoc, pageSign
    dung_page = ('dungeonicon', (614,265), 'dungpage' )
    skill_page = ('skillicon', (865,60),  'skillpage')#skill_page = ('skillicon', (614,130),  'skillpage')
    tasks_page = ('tasksicon', (695,192), 'taskpage' )
    event_page = ('eventicon', (695,130), 'eventpage')

#x length = 60
#y length = 60ish
# data is as follows:
#   (x,y) | x is horizontal loc. of top left corner of the icon, y is vert. [each point to x,y loc]
class cMenuOption:
    #COLUMN 1 
    ICON_LENGTH     = (60,55),

    CHAR_INFO_MENU  = (614,60),  #ROW1   115 MAX y 
    SKILL_MENU      = (865,60), #SKILL_MENU      = (614,130), #ROW2
    QUEST_MENU      = (614,192),            #ROW3    #Y END = 250    614-675 x  
    DUNG_MENU       = (865,196), #(614,265),          #ROW4  END AT 315 
    EVENT_SHOP_MENU = (614,330), 
    GUILD_MENU      = (614,405),  
    TASKS_MENU      = (614,192),         #ROW3
    #X END 675

    #COLUMN 2
    #TASKS_MENU      = (695,192),         #ROW3
    FORGE_MENU      = (695,265),        #ROW4

    #COLUMN 3
    PET_MENU        = (785,130),        #ROW2
    EVENT_MENU      = (695,192),#(785,195),        #ROW3

    #COLUMN 4 

    SOUL_MENU       = (865,60),         #ROW1
    JEWEL_MENU      = (865,130),        #ROW2
    MAPLE_ADV_MENU  = (865,196),        #ROW3
    SHOP_MENU       = (865,264),        #ROW4
    COMMUNITY_MENU       = (865,395),        #ROW4
    

class gameConstants:        #in same order as game, ie: 1st/top-most item is phydmg buff, 2nd is bossatt, 3rd is meso, etc
    
    DAILY_FAME_LIMIT        = 10

    NOT_FOUND               = -3 
    TANG_YOON_PHYDMG        = ('phydmgtang.png', 0)
    TANG_YOON_BOSSATT       = ('bossattacktang.png', 1)
    TANG_YOON_MESO          = ('mesoxptang.png', 2)
    TANG_YOON_MAGDMG        = ('magdmgtang.png', 3)
    TANG_YOON_CRITRATE      = ('critratetang.png', 4)

    TANG_YOON_PREV_OPTION = 5 #DIR = LEFT
    TANG_YOON_NEXT_OPTION = 6 #DIR = RIGHT

    TANG_YOON_START_PT_LEFT = 7
    TANG_YOON_START_PT_RIGHT = 8


'''
        topLCX = locOfMenu[0]
        topLCY = locOfMenu[1]
        xMax = topLCX + cMenuOption.ICON_LENGTH[0]
        yMax = topLCY +cMenuOption.ICON_LENGTH[1]
        if scanThisROI(self.templateDict[tempName],)

'''