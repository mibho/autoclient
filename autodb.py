import sqlite3
import DateManager as dmtime 
import datetime
import pytz
import cProfile
'''
PRAGMA table_info(your_table_name)

If the resulting table is empty then your_table_name doesn't exist.
'''

class clientDB:
    UTC_7_TZ = "America/Los Angeles"
    UTC_8_TZ = "America/Juneau"
    CHAR_TBL_TITLE = "charTable"
    FAME_TBL_TITLE = "fameTable"
    #CREATE_MAIN_TABLE_CMD = "CREATE TABLE IF NOT EXISTS MAIN_CLI_TBL (clientID INTEGER PRIMARY KEY, clientName TEXT NOT NULL, botLastOpened timestamp);"
    #CREATE_CLIENT_CHAR_TABLE_CMD =  "CREATE TABLE IF NOT EXISTS " + tableName + " (clientID INTEGER PRIMARY KEY, clientName TEXT NOT NULL, botLastOpened timestamp);"

    def __init__(self, dbFileName, winName, noxClientID):
        self.noxNum = noxClientID + 1
        self.clientName = winName
        self.connectToDB(dbFileName)
        self.initMainTable()
        self.dailyReset = False
        self.reobtainCharInfo = False #have this be like a checkbox setting; enabled if user clicks button or something for gui pt later...
        #self.checkIfDataRegistered(self.noxNum)
        #self.getNumberOfEntries()
        self.resetDailyStatus()
        self.registerClientInMain()
        print("clientDB object created.")

    
    def connectToDB(self, dbFileName):
        print("checking for DB file...")
        self.sqlConnection = sqlite3.connect(dbFileName)
        self.sqlCursor = self.sqlConnection.cursor()
        print("Connected to SQLite")
    

    def executeCMD(self, *args):
        if len(args) == 0:
            return

        elif len(args) == 1:
            self.sqlCursor.execute(args[0])
        else:
            self.sqlCursor.execute(args[0], args[1])

        self.sqlConnection.commit()

    def updateSingleVar(self,tableName, columnToChange, value):
        cmd = "UPDATE " + tableName + " SET " + columnToChange + " = ? WHERE clientID = " + str(self.noxNum)
        self.executeCMD(cmd, value)  

    def insertOrUpdateMultiple(self, *args): #args[0] = tbl_name, args[1] = colVals, args[2] = valuestoinsert
        temp = '?'*(len(args[2]))
        s_tuple = tuple(temp)
        s_tuple = str(s_tuple)
        s_tuple = s_tuple.replace("'", "")
        cmd = "INSERT OR REPLACE INTO " + args[0] + " " + args[1] + " VALUES " + s_tuple# + ";"
        self.executeCMD(cmd, args[2] )
        
    def getSingleVal(self, colName, tableName, cID):
        sqlCMD = "SELECT " + colName + " FROM " + tableName + " where clientID " + "= ?"
        self.executeCMD(sqlCMD, str(cID))


    def doesTableExist(self, tableName):
        sqlCMD = "PRAGMA table_info(" + tableName + ");"
        self.executeCMD(sqlCMD)

        return (self.sqlCursor.fetchone() is not None)

    '''
    createTableIfDNE absolute shitfest of a func; need rewrite
    2 ways to call:
        1) createTableIfDNE(tableName, tupleNeeded, dataTuple) which takes name of the table(string), 1 (if tuple not needed, else omit), tuple w/ data.
        2) createTableIfDNE(tableName, dataTuple) 
        difference being dataTuple in 2nd call requires caller to add parentheses. [alr included in 1)]
    '''
    def createTableIfDNE(self, *args): #args[0] = tbl_name, args[1] = column contents of tbl
        if args[1] == 1: #tuple not needed
            sqlCMD = "CREATE TABLE IF NOT EXISTS "+ args[0] + " " + args[2] + ";"
            self.executeCMD(sqlCMD)
        else:
            sqlCMD = "CREATE TABLE IF NOT EXISTS "+ args[0] + " (" + args[1] + ");"
            self.executeCMD(sqlCMD)
        
    
    def resetDailyStatus(self):
        print("ENTERING RESETDAILY")
        sqlCMD = "SELECT * FROM sqlite_master where type='table'"
        self.executeCMD(sqlCMD)
        for tbl in self.sqlCursor.fetchall():
            if self.checkIfDataRegistered(self.noxNum) == 1:
                print("line 84")
            print(tbl)
            print("1")
        print("EXITED RESETDAILY")
    
    def verifyValidTable(self, tableName):
        if self.doesTableExist(tableName): #table does exist, 
            if self.checkIfDataRegistered(self.noxNum) == 1:
                return True
                #since we verified it is valid table, trust that accdata was registered and tbl has data regarding chars that we can now reset.
        
        return False
    

    def getSingleValAccData(self, colName, cID):
        table = self.CHAR_TBL_TITLE + str(self.noxNum)
        sqlCMD = "SELECT " + colName + " FROM " + table + " where charNum " + "= ?"
        self.executeCMD(sqlCMD, str(cID))

                                        #  0        1               2               3                   4               5               6           7           8
    def createClientAccDataTable(self, clientTitle): #char# | jobs done? | ed tix take? | daily dung done? | elite dung done? | netts dung done? | ab taken? | can take AB | TY done
        self.createTableIfDNE(clientTitle, "charNum INTEGER PRIMARY KEY, charDone INTEGER, extraEDTixTaken INTEGER, dailyDungDone INTEGER, eliteDungDone INTEGER, nettsDungDone INTEGER, dailyABTaken INTEGER, dailyABAvail INTEGER, cookDungDone INTEGER, allFamed INTEGER")

    def getNumOfClientsRegistered(self):
        sqlCMD = "SELECT * FROM MAIN_TBL_CLIENTS"
        self.executeCMD(sqlCMD)
        print(len(self.sqlCursor.fetchall()))
        print("TOTAL")

    def registerFameAccData(self,names, data_tuple, numChars):
        table = self.FAME_TBL_TITLE + str(self.noxNum)
        prefix = ('charNum',)
        t1 = prefix + names
        print(type(t1))
        print(t1)
        for x in range(0, numChars):
            t2 = (x,) + data_tuple
            self.insertOrUpdateMultiple(table, str(t1), t2)
        

    def registerClientAccData(self,charNum):
        table = self.CHAR_TBL_TITLE + str(self.noxNum)
        data_tuple = (charNum, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.insertOrUpdateMultiple(table,"(charNum, charDone, extraEDTixTaken, dailyDungDone, eliteDungDone, nettsDungDone, dailyABTaken, dailyABAvail, cookDungDone, allFamed )", data_tuple)
    #return -1 if entry DNE, ie, current clientID isn't even in main table... otherwise return 0 or 1.
    #                                                                         returns 0 by default [not registered], 1 if we obtained acc data via char lobby already.
    def checkIfDataRegistered(self, cID):
        self.getSingleVal("accDataRegistered", "MAIN_TBL_CLIENTS", cID)
        registered = self.sqlCursor.fetchone()
        if registered is None:
            return -1
        else:
            return registered[0]
    
    def checkSetup(self):
        state = self.checkIfDataRegistered(self.noxNum)
        if state != -1:
            return state
        else:
            return -1
    
    '''
    if accData is registered, then either 1) table for client exists or 2) doesnt
    if NOT registered (0), then clearly the

    '''
    def registerClientInMain(self):
        timeData = datetime.datetime.now(tz=pytz.timezone(self.UTC_8_TZ))
        data_tuple = (self.noxNum, self.clientName, timeData, 0, 0)
        self.insertOrUpdateMultiple("MAIN_TBL_CLIENTS","(clientID, clientName, botLastOpened, accDataRegistered, jobsFinished)", data_tuple)

    def initMainTable(self):
        if not self.doesTableExist("MAIN_TBL_CLIENTS"): #creates main table if DNE
            self.createTableIfDNE("MAIN_TBL_CLIENTS", "clientID INTEGER PRIMARY KEY,clientName TEXT NOT NULL, botLastOpened timestamp,accDataRegistered INTEGER,jobsFinished INTEGER")
            self.registerClientInMain()
        else: #main tbl exists already 
            pass

    

    def updateStoredWindowName(self, tableName, windowName):
        cmd = "UPDATE " + tableName + " SET clientName = ? WHERE clientID = " + str(self.noxNum)
        self.executeCMD(cmd, windowName)  


    def getColName(self, tableName):
        check_exist_str = "SELECT * FROM " + tableName #+ " LIMIT 1;"
        self.sqlCursor.execute(check_exist_str)
        for a in self.sqlCursor.fetchall():
            print(a)

    def updateNameIfNeeded(self,cID):
        check_exist_str = "SELECT * FROM MAIN_TBL_CLIENTS where " + "clientName " + "= ?"
        self.sqlCursor.execute(check_exist_str, (cID,))
        for value in self.sqlCursor.fetchall():
            if value[0] == cID and value[1] != self.windowName:
                self.updateStoredWindowName("MAIN_TBL_CLIENTS", self.windowName)
        print("done")


    
