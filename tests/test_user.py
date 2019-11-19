import unittest
import pytest

from .. import field
from .. import board
from .. import run
from .. import user


class TestUser(unittest.TestCase):

    def test_User(self):

        u1 = user.User("Jhon", 1000)
        u1Dict = u1.get_info()
        self.assertEqual(u1Dict["username"], "Jhon")
        self.assertEqual(u1Dict["cookie"], 1000)
        self.assertEqual(u1Dict["flaged_qty"], 0)
        self.assertEqual(u1Dict["digged_qty"], 0)
        self.assertEqual(u1Dict["total_qty"], 0)

        u1.increase_digged(2)
        u1.increase_flag(5)
        u1Dict = u1.get_info()
        self.assertEqual(u1Dict["flaged_qty"], 5)
        self.assertEqual(u1Dict["digged_qty"], 2)
        self.assertEqual(u1.return_cookie(), 1000)
        self.assertEqual(u1Dict["total_qty"], 7)

        u1.make_zero()
        u1Dict = u1.get_info()
        self.assertEqual(u1Dict["flaged_qty"], 0)
        self.assertEqual(u1Dict["digged_qty"], 0)
        self.assertEqual(u1Dict["total_qty"], 0)

