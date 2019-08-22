import unittest
import pytest

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


class TestBoard(unittest.TestCase):

    def test_Field(self):

        f1 = field.Field(1, 4, False)
        self.assertEqual("UNTOUCH",f1.get_condition())

        f1Dict = f1.toJson()

        self.assertEqual(f1Dict["cordX"], 1)
        self.assertEqual(f1Dict["cordY"], 4)
        self.assertEqual(f1Dict["condition"], "UNTOUCH")
        f1.setBomb()
        self.assertTrue(f1.isBomb)

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

        b4 = board.Board("medium")
        f4 = b4.get_field(0)

        self.assertEqual(0, f4.getX())
        self.assertEqual(0, f4.getY())


#################

if __name__ == '__main__':
    unittest.main(verbosity=2)
