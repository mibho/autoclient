#--------------------------------------
# system/native imports 
#--------------------------------------
import psutil
#--------------------------------------
# public/3rd-party imports 
#--------------------------------------
import win32gui, win32ui, win32api, win32con, win32process
#--------------------------------------
# project specific imports  
#--------------------------------------

#--------------------------------------

def getPortFromSockAddress(sock_addr):
    filtered = sock_addr.split(":", 1)
    
    return int(filtered[1])





#Callback func. used w/ EnumWindows() [Win32 func]
def pEnumWindowsProc(hwnd, lParam):
    if (lParam is None) or ((lParam is not None) and (win32process.GetWindowThreadProcessId(hwnd)[1] == lParam[0])):
        wName = win32gui.GetWindowText(hwnd)

        if wName:
            wStyle = win32api.GetWindowLong(hwnd, win32con.GWL_STYLE)
            wEXStyle = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)

            if (wStyle & win32con.WS_VISIBLE) and (wStyle & win32con.WS_GROUP) and not (wEXStyle & win32con.WS_EX_TOOLWINDOW):
                wMatch = win32gui.FindWindow(None, wName)
                
                if wMatch:
                    lParam[1].append(wName)
                    print(str(hwnd) + " " + wName)


def getWindowNameFromPID(processID):
    nameList = []
    callbackObj = (processID, nameList)
    win32gui.EnumWindows(pEnumWindowsProc, callbackObj)
    return callbackObj[1]


def getHWNDFromTitle(windowName):
    hwnd = win32gui.FindWindow(None, windowName)
    return hwnd