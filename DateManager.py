import datetime
import pytz
from pytz import timezone

timeData = datetime.datetime.now(tz=pytz.timezone('America/Los_Angeles'))


def getCurrDay():
    return int(timeData.day)

def getCurrHour():
    return int(timeData.hour)

def getCurrMinute():
    return int(timeData.minute)


'''
time when botLastOpened: 
    if DNE, skip b/c first time running 
    else:
        store botLastOpened in tempvar.
        get curret time info and store in tempvar2
        if currTime.day == botLastOpened.day
            daily reset hasnt occurred so... do nothing 
            pass
        else: NOT equal so.. there exists at least one entry; curr client has been registered already


        if currTime.day != botLastOpened.day []
'''