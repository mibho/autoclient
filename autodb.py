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
    #CREATE_MAIN_TABLE_CMD = "CREATE TABLE IF NOT EXISTS MAIN_CLI_TBL (clientID INTEGER PRIMARY KEY, clientName TEXT NOT NULL, botLastOpened timestamp);"
    #CREATE_CLIENT_CHAR_TABLE_CMD =  "CREATE TABLE IF NOT EXISTS " + tableName + " (clientID INTEGER PRIMARY KEY, clientName TEXT NOT NULL, botLastOpened timestamp);"

    def __init__(self, dbFileName, winName, noxClientID):
        self.noxNum = noxClientID + 1
        self.clientName = winName
        self.connectToDB(dbFileName)
        #self.initTables()
        self.dailyReset = False
        self.checkIfDataRegistered(3)
        #self.MT_createtbl()

        #self.MT_insertOrUpdate("A")
        #self.insertOrUpdate("MAIN_CLI_TBL")
        #self.confirmMainTableExists()
        #self.checkRows("MAIN_CLI_TBL")
        #print(self.doesTableExist("MAIN_CLI_TBL"))
        #self.getColName("MAIN_CLI_TBL")
        #self.getIDFromMain(self.noxNum)
        #self.checkRows("basic_data")
    
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
        
        

    def doesTableExist(self, tableName):
        check_exist_str = "PRAGMA table_info(" + tableName + ");"
        self.executeCMD(check_exist_str)
        return (self.sqlCursor.fetchone() is not None)

    def clientInfoRegistered(self, tableName):
        check_exist_str = "PRAGMA table_info(" + tableName + ");"
        self.executeCMD(check_exist_str)
        for a in self.sqlCursor.fetchall():
            print(a)
            
            if a[0] == self.noxNum:
                return True
        
        return False
    
    def getSingleVal(self, colName, tableName, cID):
        check_exist_str = "SELECT " + colName + " FROM " + tableName + " where clientID " + "= ?"
        #self.sqlCursor.execute(check_exist_str, (cID,))
        self.executeCMD(check_exist_str, str(cID))
    
    
    def checkIfDataRegistered(self, cID):
        self.getSingleVal("accDataRegistered", "MAIN_TBL_CLIENTS", cID)
        registered = self.sqlCursor.fetchone()
        if registered is None:
            return -1
        else:
            return registered[0]


    def initTables(self):
        if not self.doesTableExist("MAIN_TBL_CLIENTS"): #creates main table if DNE
            self.createTableIfDNE("MAIN_TBL_CLIENTS", "clientID INTEGER PRIMARY KEY,clientName TEXT NOT NULL, botLastOpened timestamp,accDataRegistered INTEGER,jobsFinished INTEGER")

        else:
            timeData = datetime.datetime.now(tz=pytz.timezone('America/Los_Angeles'))
        
            if self.doesTableExist("MAIN_TBL_CLIENTS"): #clientID registered, make changes to windowname as needed
                print("REGISTERED YAYAYA")
                self.updateNameIfNeeded(self.noxNum)
                data_tuple = (self.noxNum, self.clientName, timeData, "1")
                self.insertOrUpdateMultiple("MAIN_TBL_CLIENTS","(clientID, clientName, botLastOpened, accDataRegistered)", data_tuple, 1)
                #self.insertOrUpdateTable("MAIN_TBL_CLIENTS","accDataRegistered", "1")
                self.updateSingleVar("MAIN_TBL_CLIENTS", "jobsFinished", "0")
                #self.insertCurrentTime("MAIN_TBL_CLIENTS", "botLastOpened", timeData)
                #self.insertOrUpdateMultiple("MAIN_TBL_CLIENTS", "botLastOpened", timeData, 0)
                print("aasd done")
            
            pass
        #now check if clientID registered:

    def createTableIfDNE(self, *args):
        basic_dataTB_str = "CREATE TABLE IF NOT EXISTS "+ args[0] + " (" + args[1] + ");"
        self.executeCMD(basic_dataTB_str)



    def initRecord(self, tableName):
        self.initMainTable() #ensures main tbl exists 
        if self.checkForRecord("MAIN_CLI_TBL"): #clientID logged before 
            pass
        else:
            self.inputRecordEntryWithTime(self.noxNum, self.clientName )
    
    

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

           
    
    def insertCurrentTime(self, tableName, newValue, valueToChange):
        #timeData = datetime.datetime.now(tz=pytz.timezone('America/Los_Angeles'))
        #updateCMD = "UPDATE " + tableName + " SET " + newValue + " = ?" + " WHERE " + valueToChange + " = ?"
        updateCMD = "UPDATE " + tableName + " SET " + "botLastOpened" + " = ?" + " WHERE " + "clientID" + " = ?"
        self.executeCMD(updateCMD, (newValue, valueToChange))
        #self.sqlCursor.execute(updateCMD, (newValue, valueToChange))
        #self.sqlConnection.commit()

    
    def createClientCharTable(self, cID): #createTableIfDoesNot Exist
        createCMD = "CREATE TABLE IF NOT EXISTS charData_client" + str(cID) + " (charNumber INTEGER PRIMARY KEY, clientName TEXT NOT NULL, botLastOpened timestamp);"
        basic_dataTB_str = '''CREATE TABLE IF NOT EXISTS basic_data
                                      (clientID INTEGER PRIMARY KEY,
                                       clientName TEXT NOT NULL,
                                       botLastOpened timestamp);'''
    
