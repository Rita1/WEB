import unittest

import sys
try:
    sys.path.append("..")
    import field
except:
    from .. import field


class TestBoard(unittest.TestCase):

    def test_test_Field(self):

        f1 = field.Field(1, 4, False)

        f1.setBomb()
        self.assertTrue(f1.isBomb)
        #self.assertTrue(True)

if __name__ == '__main__':
    unittest.main(verbosity=2)
