import random

class cCoords:

    def __init__(self, coordX, coordY):
        self.setPoints(coordX, coordY)

    #matchTemplate will set pts. 
    def setPoints(self, coordX, coordY):
        self.xyLoc = (coordX, coordY)
    
    # sending touch/tap will reset tuple after pressing loc. from matchTemplate
    def reset(self):
        self.setPoints(0,0)

    # randomize touch to bypass standard (recorded) macro detection system <= recorded macro sends input at the exact same x,y every time aka impossible
    def randomizeCoords(self, maxX, maxY):
        randX = round(random.uniform(self.xyLoc[0], maxX), 1)
        randY = round(random.uniform(self.xyLoc[1], maxY), 1)
        
        return (randX, randY)

def randTime(minTime, maxTime):
    waitTime = random.uniform(minTime, maxTime)
    return waitTime

def randPoint(xStart, xEnd, yStart, yEnd):
    randX = round(random.uniform(xStart, xEnd))
    randY = round(random.uniform(yStart, yEnd))

    return (randX, randY)

        
    