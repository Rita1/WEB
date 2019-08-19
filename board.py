class Board():

    def __init__(self, x, y):
        self.sizeX = x
        self.sizeY = y
        new_board = Board.get_new_fields(x, y)
        self.fields = []

    def get_new_fields(x, y):
        fieldList = []

        return fieldList


    def toJson(self):

        myDict = {}
        myDict["cordX"] : self.sizeX
        myDict["cordY"] : self.sizeY

        fields = []
        myDict["fields"] : fields
        return myDict