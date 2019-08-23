from . import field
import random

class Board():
    
    # Size: Small 9 x 9, Medium 16 x 16, Large 30 x 24 or Any (for debug purposes)

    SMALL = (9,9)
    MEDIUM = (16,16)
    LARGE = (30,24)

    def __init__(self, size, file1=False):
        
        print("size", size)
        if not file1:
            if size == "small":
                self.sizeX = Board.SMALL[0]
                self.sizeY = Board.SMALL[1]
                print("small", self.sizeX, self.sizeY)
            elif size == "medium":
                self.sizeX = Board.MEDIUM[0]
                self.sizeY = Board.MEDIUM[1]
                print("medium", self.sizeX, self.sizeY)
            else:
                self.sizeX = Board.LARGE[0]
                self.sizeY = Board.LARGE[1]
                print("large", self.sizeX, self.sizeY)
            new_board_fields = Board.get_new_fields(self.sizeX, self.sizeY)
            new_board_with_bombs = Board.set_bombs(new_board_fields, self.sizeX, self.sizeY)
            self.fields = new_board_with_bombs
 
        else:
            new_board_fields = Board.parse_file(file1)
            self.fields = new_board_fields

            #TODO
            self.sizeX = 0
            self.sizeY = 0
            
            
    
    def parse_file(file1):
        
        fieldList = []
        # with open('file1', 'r') as to_read:
        #     for line in to_read:
        #         pass


        return fieldList

    def get_new_fields(x, y):
        fieldList = []
        for i in range(y):
            for n in range(x):
                f = field.Field(n, i, False)
                fieldList.append(f)
        # print("fieldList", fieldList)        
        return fieldList

    # random seeds bombs in given field list
    # 0.16 bomb one field

    def set_bombs(fields, x, y):
        
        bomb_count = round(x * y * 0.16)
        size = (x * y) - 1
        random_element = int(random.random() * size)
        field = fields[random_element]
        print("field", field, field.is_Bomb())
        
        while bomb_count > 0:
            
            random_element = int(random.random() * size)
        #     print("ran+elm, random()", random_element, random.random())
            field = fields[random_element]
            print("field", field, field.is_Bomb())
            if not field.is_Bomb():
                field.set_Bomb()
                bomb_count -= 1

        return fields

    # field index in board list, start from 0
    # return field by index

    def get_field(self, n):
        return self.fields[n]

    def getXandY(self):
        XandY = (self.sizeX, self.sizeY)
        return XandY

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