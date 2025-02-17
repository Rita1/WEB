import unittest
import pytest
import os

from .. import field
from .. import board
from .. import run

# https://flask.palletsprojects.com/en/1.0.x/testing/
# try:
#     sys.path.append("..")
#     import field
#     import board
#     import run
# except:
#     from .. import field
#     from .. import board
#     from .. import run

__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

class TestBoard(unittest.TestCase):

    def test_Field(self):

        f1 = field.Field(1, 4, False)
        self.assertEqual("UNTOUCH", f1.get_condition())

        f1Dict = f1.toJson()

        self.assertEqual(f1Dict["cordX"], 1)
        self.assertEqual(f1Dict["cordY"], 4)
        self.assertEqual(f1Dict["condition"], "UNTOUCH")
        f1.set_Bomb()
        self.assertTrue(f1.is_Bomb())

        f1.flag()
        self.assertEqual("FLAG", f1.get_condition())

        f1.unFlag()
        self.assertEqual("UNTOUCH", f1.get_condition())

    def test_Field2(self):

        f1 = field.Field(2, 5, False)

        f1.dig()
        f1Dict = f1.toJson()

        self.assertEqual("DUG", f1.get_condition())
        self.assertEqual("DUG", f1Dict["condition"])

        f1.setBombCount(2)
        f1Dict2 = f1.toJson()
        self.assertEqual(2, f1Dict2["bomb_count"])

    def test_field_string(self):
        f1 = field.Field(2, 5, False)
        self.assertEqual("-", f1.toString())

        f1.flag()
        self.assertEqual("F", f1.toString())

        f1.dig()
        self.assertEqual(" ", f1.toString())

        f1.setBombCount(1)
        self.assertEqual("1", f1.toString())

    def test_create_board(self):

        b1 = board.Board("small")
        b1Dict = b1.toJson()

        self.assertEqual(b1Dict["cordX"], 9)
        self.assertEqual(b1Dict["cordY"], 9)
        fields_len = len(b1Dict["fieldList"])
        self.assertEqual(81, fields_len)

        b2 = board.Board("medium")
        b2Dict = b2.toJson()
        self.assertEqual(b2Dict["cordX"], 16)
        self.assertEqual(b2Dict["cordY"], 16)
        fields_len2 = len(b2Dict["fieldList"])
        self.assertEqual(256, fields_len2)

        b3 = board.Board("large")
        b3Dict = b3.toJson()
        self.assertEqual(b3Dict["cordX"], 30)
        self.assertEqual(b3Dict["cordY"], 24)
        fields_len3 = len(b3Dict["fieldList"])
        self.assertEqual(720, fields_len3)

    def test_create_board2(self):

        b4 = board.Board("small")

        f4 = b4.get_field(0)
        self.assertEqual(0, f4.getX())
        self.assertEqual(0, f4.getY())
        
        f5 = b4.get_field(9)
        self.assertEqual(0, f5.getX())
        self.assertEqual(1, f5.getY())

        f6 = b4.get_field(17)
        self.assertEqual(8, f6.getX())
        self.assertEqual(1, f6.getY())

    def test_count_bombs(self):

        # 0.16 bombos vienam laukeliui
        b1 = board.Board("small")
        bomb_count = 0
        for i in range(9*9):
            f = b1.get_field(i)
            if f.is_Bomb():
                bomb_count += 1

        self.assertEqual(13, bomb_count)

        # 0.16 bombos vienam laukeliui
        b2 = board.Board("medium")
        bomb_count2 = 0
        for i in range(16*16):
            f = b2.get_field(i)
            if f.is_Bomb():
                bomb_count2 += 1

        self.assertEqual(41, bomb_count2)    

    def test_parse_board(self):
        
        file1 = os.path.join(__location__, 'boards/board2')
        b2 = board.Board("any", file1)
        
        self.assertEqual(4, b2.getXandY()[0])
        self.assertEqual(5, b2.getXandY()[1])
        
        bomb_count = 0
        for i in range(4*5):
            f = b2.get_field(i)
            if f.is_Bomb():
                bomb_count += 1
        
        f1 = b2.get_field(0)
        f2 = b2.get_field(16)
        f3 = b2.get_field(19)
        f4 = b2.get_field(18)

        self.assertEqual(3, bomb_count)
        self.assertTrue(f1.is_Bomb())
        self.assertTrue(f2.is_Bomb())
        self.assertTrue(f3.is_Bomb())
        self.assertFalse(f4.is_Bomb())

    def test_return_index(self):

        i1 = board.Board.return_index(0, 0, 2, 3)
        self.assertEqual(0, i1)

        i5 = board.Board.return_index(1, 1, 3, 2)
        self.assertEqual(4, i5)
    
    # B 1 0
    # 1 1 0

    def test_count_right(self):

        file1 = os.path.join(__location__, 'boards/board4')
        b2 = board.Board("any", file1)

        answer_string = "0 1 0 1 1 0"
        answer = answer_string.split(" ")
        
        for i in range(2*3):
            f = b2.get_field(i)
            a = int(answer[i])
            self.assertEqual(a, f.getBombCount())
    
    # B 2 B 1 0 
    # 1 2 1 1 0
    # 1 1 1 0 0
    # 1 B 1 1 1
    # 2 3 2 3 B
    # B 2 B 3 B

    def test_count_full(self):

        file1 = os.path.join(__location__, 'boards/board3')
        b2 = board.Board("any", file1)

        answer_string = "0 2 0 1 0 " + "1 2 1 1 0 " + "1 1 1 0 0 " + "1 0 1 1 1 " + "2 3 2 3 1 " + "0 2 0 3 1"
        answer = answer_string.split(" ")
        
        for i in range(5*6):
            f = b2.get_field(i)
            a = int(answer[i])
            self.assertEqual(a, f.getBombCount())
    
    # 0 1
    # 2 3
    # 3 4

    def test_return_x_y(self):
        x = board.Board.return_x_y(0, 2, 3)[0]
        y = board.Board.return_x_y(0, 2, 3)[1]

        self.assertEqual(0, x)
        self.assertEqual(0, y)

        x = board.Board.return_x_y(1, 2, 3)[0]
        y = board.Board.return_x_y(1, 2, 3)[1]

        self.assertEqual(1, x)
        self.assertEqual(0, y)

    # 0 1
    # 2 3
    # 4 5
        x = board.Board.return_x_y(3, 2, 3)[0]
        y = board.Board.return_x_y(3, 2, 3)[1]

        self.assertEqual(1, x)
        self.assertEqual(1, y)
    # 0 1 2
    # 3 4 5
    # 6 7 8

        x = board.Board.return_x_y(8, 3, 3)[0]
        y = board.Board.return_x_y(8, 3, 3)[1]

        self.assertEqual(2, x)
        self.assertEqual(2, y)

    # 1 0 0
    # 0 0 0
    def test_dig_board(self):

        file1 = os.path.join(__location__, 'boards/board4')
        b1 = board.Board("any", file1)
        
        qty1 = b1.dig(5)
        b1Dict = b1.toJson()
        fl = b1Dict["fieldList"][5]["condition"]
        self.assertEqual("DUG", fl)
        self.assertEqual(4, qty1)

    # 0 0 0 0
    def test_dig_recursive(self):

        file1 = os.path.join(__location__, 'boards/board6')
        b1 = board.Board("any", file1)

        answ = "- - - -"
        self.assertEqual(answ, b1.toString())

        qty1 = b1.dig(0)
        fields = b1.toJson()["fieldList"]
      #   print("fields", fields)
        for f in fields:
            print("f", f)
            self.assertEqual("DUG", fields[f]["condition"])

        answ = "       "
        self.assertEqual(answ, b1.toString())
        self.assertEqual(4, qty1)

    # 5 6
    # 0 0 0 0 0 
    # 0 0 0 0 0
    # 0 0 0 0 0  # 2 2
    # 0 0 0 1 1
    # 1 2 1 2 B
    # B 2 B 2 1

    def test_dig_recursive_full(self):

        file1 = os.path.join(__location__, 'boards/board7_1')
        b1 = board.Board("any", file1)
        
        answ1 = "- - - - -\n" + "- - - - -\n" + "- - - - -\n" + "- - - - -\n"\
             + "- - - - -\n" + "- - - - -"
        self.assertEqual(answ1, b1.toString())

        qty1 = b1.dig(13)
        answ2 = "         \n" + "         \n" + "         \n" + "      1 1\n"\
            + "1 2 1 2 -\n" + "- - - - -"
        self.assertEqual(answ2, b1.toString())
        self.assertEqual(24, qty1)

    # 5 6
    # B 2 B 1 0 
    # 1 2 1 1 0
    # 1 1 1 0 0
    # 1 B 1 1 1 //<-
    # 2 3 2 3 B
    # B 2 B 3 B

    def test_dig_bomb1(self):
        file1 = os.path.join(__location__, 'boards/board3')
        b1 = board.Board("any", file1)

        qty1 = b1.dig(9)
        answ = "- - - 1  \n" + "- - 1 1  \n" + "- - 1    \n" \
            + "- - 1 1 1\n" + "- - - - -\n" + "- - - - -"

        self.assertEqual(answ, b1.toString())
        self.assertEqual(11, qty1)

        b1.dig_bomb(16)

        f1 = b1.get_field(16)
        self.assertFalse(f1.is_Bomb())
        self.assertEqual("DUG", f1.get_condition())
        self.assertEqual(0, f1.getBombCount())

    # 5 6
    # B 2 B 1 0 
    # 1 2 1 1 0
    # 0 0 0 0 0
    # 0 0 0 1 1 //<-
    # 1 2 1 3 B
    # B 2 B 3 B

        answ2 = "- - - 1  \n" + "1 2 1 1  \n" + "         \n" + \
            "      1 1\n" + "1 2 1 3 -\n" + "- - - - -"
        self.assertEqual(answ2, b1.toString())

        b1.dig_bomb(0)
        f2 = b1.get_field(0)
        self.assertFalse(f2.is_Bomb())
        self.assertEqual("DUG", f2.get_condition())
        self.assertEqual(0, f2.getBombCount())
    # 5 6
    # B 2 B 1 0 
    # 1 2 1 1 0
    # 0 0 0 0 0
    # 0 0 0 1 1 //<-
    # 1 2 1 3 B
    # B 2 B 3 B
    #   
        answ3 = "  1 - 1  \n" + "  1 1 1  \n" + "         \n" + \
            "      1 1\n" + "1 2 1 3 -\n" + "- - - - -"
        # print("b1.toString()", b1.toString())
        # print("b1.toJson()", b1.toJson())
        self.assertEqual(answ3, b1.toString())

# 0 0 0 0
# 0 0 1 1
# 0 1 2 B
# 0 1 B 2
# 0 1 1 1

    def test_dig_bomb3(self):
        file1 = os.path.join(__location__, 'boards/board8')
        b1 = board.Board("any", file1)

        b1.dig(0)

        answ = "       \n" + "    1 1\n" + "  1 2 -\n" + "  1 - -\n" + "  1 - -"
        # print("from board", b1.toString())
        self.assertEqual(answ, b1.toString())
        # print("START DIG")
        b1.dig_bomb(14)
        # print("DIG 14!", b1.toString())
        answ1 = "       \n" + "    1 1\n" + "    1 -\n" + "    1 1\n" + "       "
        self.assertEqual(answ1, b1.toString())

    # B 1 0
    # 1 1 0
    def test_win_board(self):

        file1 = os.path.join(__location__, 'boards/board4')
        b1 = board.Board("any", file1)

        gameWin = b1.toJson()["gameWin"]
        self.assertFalse(gameWin)
        
        b1.dig(2)
        gameWin1 = b1.toJson()["gameWin"]
        self.assertFalse(gameWin1)
        b1.dig(3)
        b1.dig(4)
        b1.dig(5)
        gameWin2 = b1.toJson()["gameWin"]
        self.assertFalse(gameWin2)
        b1.flag(0)
        gameWin3 = b1.toJson()["gameWin"]
        self.assertTrue(gameWin3)
        
    # B 1 0
    # 1 1 0
    def test_win_board2(self):

        file1 = os.path.join(__location__, 'boards/board4')
        b1 = board.Board("any", file1)
        
        gameWin = b1.toJson()["gameWin"]
        self.assertFalse(gameWin)
        
        b1.dig(5)
        b1.dig_bomb(0)
        gameWin1 = b1.toJson()["gameWin"]
        print("b1.toJson, gameWin", gameWin, b1.toJson())
        self.assertTrue(gameWin1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
