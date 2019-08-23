import unittest
import pytest
import os
import sys

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
        self.assertEqual("UNTOUCH",f1.get_condition())

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
        f2 = b2.get_field(17)
        f3 = b2.get_field(19)
        f4 = b2.get_field(18)

        self.assertEqual(3, bomb_count)
        self.assertTrue(f1.is_Bomb())
        self.assertTrue(f2.is_Bomb())
        self.assertTrue(f3.is_Bomb())
        self.assertFalse(f4.is_Bomb())

    # def test_dug_board(self):

    #     file1 = os.path.join(__location__, 'boards/board4')
    #     self.assertTrue(os.path.exists(file1))

    #     b1 = board.Board("any", file1)
    #     self.assertEqual("a", b1)

    #     # TODO DUG

#################

if __name__ == '__main__':
    unittest.main(verbosity=2)
