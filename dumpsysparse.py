import re


class dumpsysparser:

    DEVICE_CONSTANT = "Android_Input"
    PATH_INDEX_OFFSET = 1
    PARSE_INDEX_OFFSET = 2



    def __init__(self, input):
        self.eventList = input.split("\n")
        self.len = len(self.eventList)

    def findIndex(self):
        for i in range(self.len):
            if self.DEVICE_CONSTANT in self.eventList[i]:
                return i + self.PARSE_INDEX_OFFSET
        
        return -1
    
    
    def findPathString(self):
        match = self.findIndex()
        pathString = self.eventList[match]
        list = pathString.split()

        return list[self.PATH_INDEX_OFFSET]

