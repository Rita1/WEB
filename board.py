from . import field

class Board():
    
    # Size: Small 9 x 9, Medium 16 x 16, Large 30 x 24

    SMALL = (9,9)
    MEDIUM = (16,16)
    LARGE = (30,24)

    def __init__(self, size, debug=False):
        
        print("size", size)
        if size == "small":
            self.sizeX = Board.SMALL[0]
            self.sizeY = Board.SMALL[1]
        elif size == "medium":
            self.sizeX = Board.MEDIUM[0]
            self.sizeY = Board.MEDIUM[1]    
        else:
            self.sizeX = Board.LARGE[0]
            self.sizeY = Board.LARGE[1]
        if debug:
            self.fields = []
        else:    
            new_board_fields = Board.get_new_fields(self.sizeX, self.sizeY)
            self.fields = new_board_fields

    def get_new_fields(x, y):
        fieldList = []
        for i in range(y):
            for n in range(x):
                f = field.Field(n, i, False)
                fieldList.append(f)
        print("fieldList", fieldList)        
        return fieldList

    # field index in board list, start from 0
    # return field by index

    def get_field(self, n):
        return self.fields[n]

    def toJson(self):

        myDict = {}
        myDict["cordX"] = self.sizeX
        myDict["cordY"] = self.sizeY
        
        count = 0
        fields_dict = {}
        for f in self.fields:
            fields_dict[count] = f.toJson()
            count += 1
        myDict["fieldList"] = fields_dict
        return myDict