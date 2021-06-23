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
        self.noxNum = noxClientID
        self.clientName = winName
        self.connectToDB(dbFileName)
        #self.initTables()
        self.dailyReset = False
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

    
    def insertOrUpdateTable(self, *args): #args[0] = tbl_name, args[1] = colVals, args[2] = valuestoinsert
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
            if a[0] == self.noxNum:
                return True
        
        return False
    


    def initTables(self):
        if self.doesTableExist("MAIN_TBL_CLIENTS"): #creates main table if DNE
            pass
            #check what if 
        else:
            self.createMainTable()

        if self.clientInfoRegistered("MAIN_TBL_CLIENTS"): #clientID registered, make changes to windowname as needed
            self.updateNameIfNeeded()
            timeData = datetime.datetime.now(tz=pytz.timezone('America/Los_Angeles'))
            self.insertCurrentTime("MAIN_TBL_CLIENTS", timeData, "botLastOpened")

        else:
            pass
        #now check if clientID registered:

    def createTableIfDNE(self, *args):
        pass
        

    def createMainTable(self):
        basic_dataTB_str = '''CREATE TABLE IF NOT EXISTS MAIN_TBL_CLIENTS
                                      (clientID INTEGER PRIMARY KEY,
                                       clientName TEXT NOT NULL,
                                       botLastOpened timestamp);'''
        self.executeCMD(basic_dataTB_str)
    
    def initMainTable(self):
        if self.doesTableExist("MAIN_CLI_TBL"): #if main table exists,
            print("yay")
        else:
            self.createMainTable()




    def inputRecordEntryWithTime(self, id, name):
        sqlite_insert_with_param = """INSERT INTO 'MAIN_CLI_TBL'
                            ('clientID', 'clientName', 'botLastOpened') 
                            VALUES (?, ?, ?);"""
        timeData = datetime.datetime.now(tz=pytz.timezone('America/Los_Angeles'))
        data_tuple = (id, name, timeData)
        self.sqlCursor.execute(sqlite_insert_with_param, data_tuple)
        self.sqlConnection.commit()

    def initRecord(self, tableName):
        self.initMainTable() #ensures main tbl exists 
        if self.checkForRecord("MAIN_CLI_TBL"): #clientID logged before 
            pass
        else:
            self.inputRecordEntryWithTime(self.noxNum, self.clientName )
    
    def updateStoredWindowName(self, tableName, windowName):
        cmd = "UPDATE " + tableName + " SET clientName = ? WHERE clientID = " + str(self.noxNum)
        self.executeCMD(cmd, windowName)  


    
        #self.sqlCursor.execute(cmd, data_tuple)
        #self.sqlConnection.commit()


    def getColName(self, tableName):
        check_exist_str = "SELECT * FROM " + tableName #+ " LIMIT 1;"
        self.sqlCursor.execute(check_exist_str)
        for a in self.sqlCursor.fetchall():
            print(a)

    def updateNameIfNeeded(self,cID):
        check_exist_str = "SELECT * FROM MAIN_CLI_TBL where " + columnName + "= ?"
        self.sqlCursor.execute(check_exist_str, (cID,))
        for value in self.sqlCursor.fetchall():
            if value[0] == cID and value[1] != self.windowName:
                self.updateStoredWindowName("MAIN_CLI_TBL", self.windowName)
        print("done")

    def initTables(self):
        self.sqlCursor.execute()                
    
    def insertCurrentTime(self, tableName, newValue, valueToChange):
        timeData = datetime.datetime.now(tz=pytz.timezone('America/Los_Angeles'))
        #updateCMD = "UPDATE " + tableName + " SET " + newValue + " = ?" + " WHERE " + valueToChange + " = ?"
        updateCMD = "UPDATE " + tableName + " SET " + newValue + " = ?" + " WHERE " + valueToChange + " = ?"
        self.executeCMD(updateCMD, (newValue, valueToChange))
        #self.sqlCursor.execute(updateCMD, (newValue, valueToChange))
        #self.sqlConnection.commit()

    
    def createClientCharTable(self, cID): #createTableIfDoesNot Exist
        createCMD = "CREATE TABLE IF NOT EXISTS charData_client" + str(cID) + " (charNumber INTEGER PRIMARY KEY, clientName TEXT NOT NULL, botLastOpened timestamp);"
        basic_dataTB_str = '''CREATE TABLE IF NOT EXISTS basic_data
                                      (clientID INTEGER PRIMARY KEY,
                                       clientName TEXT NOT NULL,
                                       botLastOpened timestamp);'''
    

    def WOO(self, i):
        #self.sqliteConnection = sqlite3.connect('autoTest.db')
        #self.sqlCursor = self.sqliteConnection.cursor()
        timeData = datetime.datetime.now(tz=pytz.timezone('America/Los_Angeles'))
        data_tuple = (self.noxNum, self.clientName, timeData)
        self.insertOrUpdateTable("A", "(clientID, clientName, botLastOpened)", data_tuple)
        print("mt insert ran")
        '''
        def insertOrUpdateTable(self, *args): #args[0] = tbl_name, args[1] = colVals, args[2] = valuestoinsert
        temp = '?'*(len(args[2]))
        s_tuple = eval(temp)

        cmd = "INSERT OR REPLACE INTO " + args[0] + " " + args[1] + " VALUES " + str(s_tuple) + ";"
        self.executeCMD(cmd, args[2])
    
    def MT_insertOrUpdate(self, tableName):
        cmd = "INSERT OR REPLACE INTO A (clientID, clientName, botLastOpened) VALUES (?, ?, ?);"
        timeData = datetime.datetime.now(tz=pytz.timezone('America/Los_Angeles'))
        data_tuple = (self.noxNum, self.clientName, timeData)
        self.executeCMD(cmd, data_tuple)

        if i == 0:
            sqlite_insert_with_param = """INSERT INTO 'MAIN_CLI_TBL'
                            ('clientID', 'clientName', 'botLastOpened') 
                            VALUES (?, ?, ?);"""
            data_tuple = (3, "weewoowooeoo", "NULL")
            self.sqlCursor.execute(sqlite_insert_with_param, data_tuple)
            self.sqliteConnection.commit()
            print(self.sqliteConnection)
            print("done with step 1")
        if i == 1:
            sqlite_insert_with_param = """INSERT INTO 'MAIN_CLI_TBL'
                            ('clientID', 'clientName', 'botLastOpened') 
                            VALUES (?, ?, ?);"""
            data_tuple = (2, "weew23oowooeoo", "NULL")
            self.sqlCursor.execute(sqlite_insert_with_param, data_tuple)
            self.sqliteConnection.commit()
            print("step 2")
            print(self.sqliteConnection)
        '''
                    

        #use 3 ''' or """" for multi-line quoted values.





def addDeveloper(clientID, clientName, botLastOpened):
    try:
        sqliteConnection = sqlite3.connect('autoTest.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
    
        basic_dataTB_str = '''CREATE TABLE IF NOT EXISTS basic_data
                                      (clientID INTEGER PRIMARY KEY,
                                       clientName TEXT NOT NULL,
                                       botLastOpened timestamp);'''

        cursor = sqliteConnection.cursor()
        cursor.execute(basic_dataTB_str)

        # insert developer detail   
        sqlite_insert_with_param = """INSERT INTO 'basic_data'
                          ('clientID', 'clientName', 'botLastOpened') 
                          VALUES (?, ?, ?);"""

        data_tuple = (clientID, clientName, botLastOpened)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Developer added successfully \n")

        # get developer detail
        sqlite_select_query = """SELECT clientName, botLastOpened from basic_data where clientID = ?"""
        cursor.execute(sqlite_select_query, (1,))
        records = cursor.fetchall()

        for row in records:
            developer= row[0]
            clName = row[1]
            print(developer, " client num info and timestamp: ", clName)
            print("timestamp dataType is ", type(botLastOpened))

        cursor.close()

    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")


import multiprocessing
import time
if __name__ == '__main__':   
    nprocs = multiprocessing.cpu_count()
    pList = {}

    sq0 = clientDB('autoTest.db', "name44", 0)
    sq1 = clientDB('autoTest.db', "name55", 3)
    sq2 = clientDB('autoTest.db', "name", 5)
    aList = []
    aList.append(sq0)
    aList.append(sq1)
    aList.append(sq2)
    while 1:
        for i in range(3):
            pList[i] = multiprocessing.Process(target=aList[i].WOO(i))
            print("GOT OBJ: " + str(i))
        
        for i in pList:
            pList[i].start()
        
        for i in pList:
            pList[i].join()
        
        print("done w/ 1 loop")
        time.sleep(2)
#addDeveloper(1, 'NoxPlayer0', datetime.datetime.now())
'''
sqliteConnection = sqlite3.connect('autoTest.db')
cursor = sqliteConnection.cursor()
print("Connected to SQLite")


#cursor.execute('PRAGMA table_info(basic_data)')
cursor.execute('SELECT * FROM basic_data')
data = cursor.fetchall()

for d in data:
    print(d[0], d[1], d[2])

print((data[0]))
print(len(data))

rows = cursor.fetchall()

timeData = datetime.datetime.now(tz=pytz.timezone('America/Los_Angeles'))
#timeData.month 
#timeData.day 

#timeData.hour <= int 
#timeData.minute <= int
#timeData.second <= int 
#print(type(timeData.))
'''