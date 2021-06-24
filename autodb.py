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
    #CREATE_MAIN_TABLE_CMD = "CREATE TABLE IF NOT EXISTS MAIN_CLI_TBL (clientID INTEGER PRIMARY KEY, clientName TEXT NOT NULL, botLastOpened timestamp);"
    #CREATE_CLIENT_CHAR_TABLE_CMD =  "CREATE TABLE IF NOT EXISTS " + tableName + " (clientID INTEGER PRIMARY KEY, clientName TEXT NOT NULL, botLastOpened timestamp);"

    def __init__(self, dbFileName, winName, noxClientID):
        self.noxNum = noxClientID + 1
        self.clientName = winName
        self.connectToDB(dbFileName)
        self.initTables()
        self.dailyReset = False
        self.reobtainCharInfo = False #have this be like a checkbox setting; enabled if user clicks button or something for gui pt later...
        self.checkIfDataRegistered(self.noxNum)
        #self.getNumberOfEntries()
        #self.resetDailyStatus()

    
    def connectToDB(self, dbFileName):
        print("checking for DB file...")
        self.sqlConnection = sqlite3.connect(dbFileName)
        self.sqlCursor = self.sqlConnection.cursor()
        print("Connected to SQLite")
    

    def executeCMD(self, *args):
        print("this being run: ")
        print(args)
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

    def createTableIfDNE(self, *args):
        sqlCMD = "CREATE TABLE IF NOT EXISTS "+ args[0] + " (" + args[1] + ");"
        self.executeCMD(sqlCMD)
    
    def resetDailyStatus(self):
        print("ENTERING RESETDAILY")
        sqlCMD = "SELECT * FROM sqlite_master where type='table'"
        self.executeCMD(sqlCMD)
        for tbl in self.sqlCursor.fetchall():
            print(tbl)
        print("EXITED RESETDAILY")
    
    def verifyValidTable(self, tableName):
        if self.doesTableExist(tableName): #table does exist, 
            if self.checkIfDataRegistered(self.noxNum) == 1:
                return True
                #since we verified it is valid table, trust that accdata was registered and tbl has data regarding chars that we can now reset.
        
        return False

    def getNumOfClientsRegistered(self):
        sqlCMD = "SELECT * FROM MAIN_TBL_CLIENTS"
        self.executeCMD(sqlCMD)
        print(len(self.sqlCursor.fetchall()))
        print("TOTAL")

    
    #return -1 if entry DNE, ie, current clientID isn't even in main table... otherwise return 0 or 1.
    #                                                                         returns 0 by default [not registered], 1 if we obtained acc data via char lobby already.
    def checkIfDataRegistered(self, cID):
        self.getSingleVal("accDataRegistered", "MAIN_TBL_CLIENTS", cID)
        registered = self.sqlCursor.fetchone()
        if registered is None:
            return -1
        else:
            return registered[0]
    
    def setup(self):
        state = self.checkIfDataRegistered(self.noxNum)
        if state == 1:
            print("it registered")
        elif state == 0: 
            print("not registered but client info was recognized. jst need to read during char lobby now...")
        elif state == -1:
            print("doesnt exist")
    
    '''
    if accData is registered, then either 1) table for client exists or 2) doesnt
    if NOT registered (0), then clearly the

    '''


    def initTables(self):
        if not self.doesTableExist("MAIN_TBL_CLIENTS"): #creates main table if DNE
            self.createTableIfDNE("MAIN_TBL_CLIENTS", "clientID INTEGER PRIMARY KEY,clientName TEXT NOT NULL, botLastOpened timestamp,accDataRegistered INTEGER,jobsFinished INTEGER")

        else:
            timeData = datetime.datetime.now(tz=pytz.timezone(self.UTC_8_TZ))
        
            if self.doesTableExist("MAIN_TBL_CLIENTS"): #clientID registered, make changes to windowname as needed
                print("REGISTERED YAYAYA")
                self.updateNameIfNeeded(self.noxNum)
                data_tuple = (self.noxNum, self.clientName, timeData, "1")
                self.insertOrUpdateMultiple("MAIN_TBL_CLIENTS","(clientID, clientName, botLastOpened, accDataRegistered)", data_tuple, 1)
                #self.insertOrUpdateTable("MAIN_TBL_CLIENTS","accDataRegistered", "1")
                #self.updateSingleVar("MAIN_TBL_CLIENTS", "jobsFinished", "0")
                self.updateSingleVar("MAIN_TBL_CLIENTS", "botLastOpened", (timeData,))
                #self.insertOrUpdateMultiple("MAIN_TBL_CLIENTS", "botLastOpened", timeData, 0)
                print("aasd done")
            
            pass
        #now check if clientID registered:
    

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


    
