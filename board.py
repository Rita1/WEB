
try:
    from . import field
except:
    import field
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
            with_bombs_count = Board.count_bombs(new_board_with_bombs, self.sizeX, self.sizeY)
            self.fields = with_bombs_count
 
        else:
            self.parse_file(file1)

    def parse_file(self, file1):
        
        fieldList = []
        first_line = True
        index = 0
        with open(file1, 'r') as to_read:
            for line in to_read:
                if first_line:
                    parts = line.split(" ")
                    x = int(parts[0])
                    y = int(parts[1])
                    first_line = False

                    fieldList = Board.get_new_fields(x, y)
                    
                else:
                    parts = line.split(" ")
                    for part in parts:
                        print("part", part)
                        if int(part) == 1:
                            field = fieldList[index]
                            field.set_Bomb()
                        index += 1
        with_bombs_count = Board.count_bombs(fieldList, x, y)

        self.sizeX = x
        self.sizeY = y
        self.fields = with_bombs_count

    def get_new_fields(x, y):
        fieldList = []
        for i in range(y):
            for n in range(x):
                f = field.Field(n, i, False)
                fieldList.append(f)     
        return fieldList

    # random seeds bombs in given field list
    # 0.16 bomb one field

    def set_bombs(fields, x, y):
        
        bomb_count = round(x * y * 0.16)
        size = (x * y) - 1
        random_element = int(random.random() * size)
        field = fields[random_element]
        
        while bomb_count > 0:
            
            random_element = int(random.random() * size)
            field = fields[random_element]
            if not field.is_Bomb():
                field.set_Bomb()
                bomb_count -= 1

        return fields
    
    # Helper method to count bombs. COUNT neighbors that have a bomb
    # newly created board
    # board with bombs count

    def count_bombs(fields, x, y):
        countedBombs = []

        # Create Counter
        for i in range(x*y):
            countedBombs.append(0)

        # Update by found bomb
        for f in fields:
            if f.is_Bomb():
                countedBombs = Board.update_count(countedBombs, f, x, y)

        # Update fields
        for n in range(y*x):
            field = fields[n]
            c = countedBombs[n]
            field.setBombCount(c)

        return fields

   # Update related fields (Right, Left, Up, Down and 4 diag. by bomb counts
    # counter - already counted bombs
    # bomb - field, where bomb is found
    # board X size
    # board Y size
    # return updated list of integers
    def update_count(counter, bomb, CordX, CordY):

        x = bomb.getX()
        y = bomb.getY()
        
        # Right
        if (x + 1) < CordX:
            indexR = Board.return_index(x+1, y, CordX, CordY)
            bombCount = counter[indexR]
            counter[indexR] = bombCount + 1
           # print("IndexR, Counter R", indexR, counter)
        # Left
        if (x - 1) >= 0:
            indexL = Board.return_index(x-1, y, CordX, CordY)
            bombCount = counter[indexL]
            counter[indexL] = bombCount + 1
          #  print("IndexL, Counter L", indexL, counter)
        # Up
        if (y - 1) >= 0:
            indexU = Board.return_index(x, y-1, CordX, CordY)
            bombCount = counter[indexU]
            counter[indexU] = bombCount + 1
          #  print("IndexU, Counter U", indexU, counter)
        # Down
        if (y + 1) < CordY:
            indexD = Board.return_index(x, y+1, CordX, CordY)
            bombCount = counter[indexD]
            counter[indexD] = bombCount + 1
        # right-down
        if ((y + 1) < CordY) and ((x + 1) < CordX):
            indexRD = Board.return_index(x + 1, y + 1, CordX, CordY)
            bombCount = counter[indexRD]
            counter[indexRD] = bombCount + 1
        # left-down
        if ((y + 1) < CordY) and ((x - 1) >= 0):
            indexLD = Board.return_index(x-1, y+1, CordX, CordY)
            bombCount = counter[indexLD]
            counter[indexLD] = bombCount + 1
        # right-up
        if (y - 1) >= 0 and (x + 1) < CordX:
            indexRU = Board.return_index(x + 1, y - 1, CordX, CordY)
            bombCount = counter[indexRU]
            counter[indexRU] = bombCount + 1
        # left-up
        if (y - 1) >= 0 and (x - 1) >= 0:
            indexLU = Board.return_index(x-1, y-1, CordX, CordY)
            bombCount = counter[indexLU]
            counter[indexLU] = bombCount + 1
        return counter


    # field index in board list, start from 0
    # return field by index

    def get_field(self, n):
        return self.fields[n]

    def getXandY(self):
        XandY = (self.sizeX, self.sizeY)
        return XandY
    
    # Helper method calculate index from x and y
    # x coordinate
    # y coordinate
    # return calculated index started from 0

    def return_index(x, y, CordX, CordY):
        index = (y * CordX) + x
        return index

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