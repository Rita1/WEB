import unittest
# import sys
# sys.path.append("..")

from minesweeper import field



class TestBoard(unittest.TestCase):

    def test_test_Field(self):

        f1 = field.Field(1, 4, False)

        f1.setBomb()
        self.assertTrue(f1.isBomb)

if __name__ == '__main__':
    unittest.main(verbosity=2)
