class Field():

    def __init__(self, x, y, isBomb):
        self.x = x
        self.y = y
        #self.condition = condition #Todo
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
