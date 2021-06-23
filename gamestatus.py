
from Constants import stateConstants


class GameStatus:
    
    def __init__(self):
        self.currState ={ 
                  0  : False,   11: False,        21: False,   31: False,   41: False,         
                  1  : False,   12: False,        22: False,   32: False,   42: False,
                  2  : False,   13: False,        23: False,   33: False,   43: False,
                  3  : False,   14: False,        24: False,   34: False,
                  4  : False,   15: False,        25: False,   35: False,     
                  5  : False,   16: False,        26: False,   36: False,
                  6  : False,   17: False,        27: False,   37: False, 
                  7  : True,    18: False,        28: False,   38: False,  
                  8  : False,   19: False,        29: False,   39: False,
                  9  : False,   20: False,        30: False,   40: False,
                  10 : False                                                   


                }
        self.stageNum = 0
        self.buttonPressed = False
        self.distanceGrabbed = False
        self.startPressed = False
        self.goingBackToLobby = False

        self.crashed = False
        self.charLocated = False
        self.atLobby = False
    
    def startBtnState(self, pressedOrNot):
        self.startPressed = pressedOrNot
    
    def wasRunning(self): #on first run every relevant level is "False"
        return (self.currState[0] | self.currState[1] | self.currState[2] | self.currState[3] | self.currState[4] | self.currState[5] | self.currState[16]) 
    
    def returnStageNum(self):
        return self.stageNum

    def printTest(self):
        print("we are at: " + str(self.stageNum))
        
    def toggleOtherStatesOff(self, levelExcluded):
        self.stageNum = levelExcluded
        for x in range(0,6):
            if x != levelExcluded:
                self.currState[x] = False
            else:
                self.currState[x] = True
        if levelExcluded == 16:
            self.currState[16] = True
        else:
            self.currState[16] = False

    def returnAppState(self):
        pass
      
    
    def detected(self):
        if self.currState[stateConstants.L0_at_home_scr]:
            return 0
        elif self.currState[stateConstants.S32_mapleview_visible]:
            return 32
        elif self.currState[stateConstants.S20_isdead]:
            return 20 
        elif self.currState[stateConstants.S22_popup_visible]:
            return 22 
        elif self.currState[stateConstants.S30_new_forced_visible]:
            return 30 
        elif self.currState[stateConstants.S33_violetta]:
            return 33
           # return 43
        else:
            return -1
    
    def resetOnCrash(self): #dtype = np.int8
        for x in range(6):
            self.currState[x] = False
        self.currState[16] = False #loading 
        for x in range(20,44):
            self.currState[x] = False
        self.charLocated = False
        self.atLobby = False
        self.buttonPressed = False
        self.startPressed = False
    
    def resetOnDeath(self):
        #23,25,31
        self.currState[stateConstants.S20_isdead] = False
        self.currState[stateConstants.S23_quest_inprogress] = False
        self.currState[stateConstants.S25_on_route] = False
        self.currState[stateConstants.S31_quest_accepted] = False



    def updateStatus(self, codeNum, res):
        self.currState[codeNum] = res






'''


from enum import Enum



class appStatus():
    L0_at_home_scr               = 0
    L1_at_start_ban              = 1 # start_ban_exit pic. |
    L2_at_title_screen           = 2
    L3_at_server_sel             = 3
    L4_at_char_lobby             = 4
    L5_ingame                    = 5

class botFeatures():
    L6_mulung                    = 6
    L7_collect_week_rewards      = 7    #getting all stuff from achievements
    L8_daily_dung                 = 8
    L9_elite_dung                = 9
    L10_netts                    = 10
    L11_mini_dung                = 11
    L12_exped_leech              = 12
    L13_auto_quest               = 13
    L14_auto_autobattle          = 14
    L15_macro                    = 15
    #L16
    


class states():
    L20_isdead                   = 20
    L21_autoeq_isvisible         = 21
    L22_autosp_isvisible         = 22
    L23_cspopup_isvisible        = 23
    L24_exitIcon_isvisible       = 24
    L25_newCharIntro_isvisible   = 25
    L26_ruhroh                   = 26
    L27_questingOn               = 27
    L28_automailOn               = 28
    L29_doingQuest               = 29
    L30_onroute                  = 30
    L31_inBag                    = 31
    L32_inMailBox                = 32
    L33_inSkillMenu              = 33
    L34_inDialog                 = 34
    L35_forcedtutexitbtn         = 35
    L36_doingForcedQuest         = 36         #all flags false/failed
    L37_ForcedQuestArrow         = 37         #forced tut stuff    
    L38_FairyLeft                = 38         #fairy popup
    L39_FairyRight               = 39
    L40_radio                    = 40
    L41_boogie                   = 41
    L42_guildpopup               = 42
    L43_mapleview                = 43

class GameStatus:
    
    def __init__(self):
        self.currState ={ 
                  0  : False,   11: False,        21: False,   31: False,   41: False,         
                  1  : False,   12: False,        22: False,   32: False,   42: False,
                  2  : False,   13: False,        23: False,   33: False,   43: False,
                  3  : False,   14: False,        24: False,   34: False,
                  4  : False,   15: False,        25: False,   35: False,     
                  5  : False,   16: False,        26: False,   36: False,
                  6  : False,   17: False,        27: False,   37: False, 
                  7  : True,    18: False,        28: False,   38: False,  
                  8  : False,   19: False,        29: False,   39: False,
                  9  : False,   20: False,        30: False,   40: False,
                  10 : False                                                   


                }
    
    def detected(self):
        if self.currState[appStatus.L0_at_home_scr]:
            return 0
        elif self.currState[states.L23_cspopup_isvisible]:
            return 23 
        elif self.currState[states.L37_ForcedQuestArrow]:
            return 37
        elif self.currState[states.L38_FairyLeft]:
            return 38
        elif self.currState[states.L39_FairyRight]:
            return 39
        elif self.currState[states.L40_radio]:
            return 40
        elif self.currState[states.L41_boogie]: 
            return 41
        elif self.currState[states.L42_guildpopup]:
            return 42
        elif self.currState[states.L43_mapleview]:
            return 43
        else:
            return -1
    
    def resetOnCrash(self): #dtype = np.int8
        for x in range(6):
            self.currState[x] = False
        for x in range(20,44):
            self.currState[x] = False



    def updateStatus(self, codeNum, res):
        self.currState[codeNum] = res

    def errorCheck(self):
        for i in range(len(self.currState)):
            if self.currState[i]:
                self.countToggled = self.countToggled - 1
        
        if self.countToggled != 0:
            self.stop = True
        
        self.countToggled = 1
    
    def increaseLevel(self):
        if self.atLevel >= 0 and self.atLevel < 5:
            self.currState[self.atLevel] = not self.currState[self.atLevel]
            self.atLevel += 1
            self.currState[self.atLevel] = not self.currState[self.atLevel]

'''