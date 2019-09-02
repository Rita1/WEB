class Field():

    def __init__(self, x, y, isBomb):
        self.x = x
        self.y = y
        self.condition = "UNTOUCH" # UNTOUCH, FLAG, DUG
        self.isBomb = isBomb
        self.countBomb = 0

    def get_condition(self):
        return self.condition

    def set_Bomb(self):
        self.isBomb = True

    def setNotBomb(self):
        self.isBomb = False
        # self.countBomb = 0

    def is_Bomb(self):
        bomb = self.isBomb
        return bomb

    def dig(self):
        self.condition = "DUG"

    def flag(self):
        print("flaging from field")
        self.condition = "FLAG"

    def unFlag(self):
        self.condition = "UNTOUCH"

    def getX(self):
        return self.x

    def getY(self):
        return self.y

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

    def toString(self):

        msg = ''
        if self.get_condition() == "FLAG":
            msg = "F"
            return msg
        if self.get_condition() == 'DUG':
            if self.getBombCount() == 0:
                msg = " "
                return msg
            else:
                msg = str(self.getBombCount())
                return msg
        else:
            msg = "-"
            return msg
