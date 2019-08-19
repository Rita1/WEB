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

        b1 = board.Board(1, 1)
        b1Dict = b1.toJson()
        print("b1Dict", b1Dict)
        #self.assertEqual(b1Dict)


#################

if __name__ == '__main__':
    unittest.main(verbosity=2)
