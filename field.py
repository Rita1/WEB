class Field():

    def __init__(self, x, y, isBomb):
        self.x = x
        self.y = y
        self.condition = "UNTOUCH" # UNTOUCH, FLAG, DUG
        self.isBomb = isBomb
        self.countBomb = 0

    def get_condition(self):
        return self.condition

    def setBomb(self):
        self.isBomb = True

    def setNotBomb(self):
        self.isBomb = False

    def isBomb(self):
        bomb = self.isBomb
        return bomb

    def dig(self):
        self.condition = "DUG"

    def flag(self):
        self.condition = "FLAG"

    def unFlag(self):
        self.condition = "UNTOUCH"

    def getX(self):
        self.x

    def getY(self):
        self.y

    def getBombCount(self):
        return self.countBomb

    def setBombCount(self, bombCount):
        self.countBomb = bombCount

    def toJson(self):

        myDict = {}
        myDict["cordX"] = self.x
        myDict["cordY"] = self.y
        myDict["condition"] = self.get_condition()
        myDict["bomb_count"] = self.getBombCount()
        return myDict
