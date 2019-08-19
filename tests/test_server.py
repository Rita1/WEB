import unittest
import pytest
import json
import os
import sys
from datetime import datetime, timedelta

from .. import field
from .. import board
from .. import run

# try:
#     #  sys.path.append("..")
#     from . import field
#     from . import board
#     from . import run
# except:
#     raise
#     # from .. import field
#     # from .. import board
#     # from .. import run

class TestServer(unittest.TestCase):

    def setUp(self):
        
        # print("os.getcwd()", os.getcwd())
        # print("os.path.dirname(path) ", os.path.dirname())
        open("users.txt", 'a').close()

        run.app.config["TESTING"] = True
        self.client = run.app.test_client()

    def tearDown(self):
        os.remove("users.txt")

    def test_calculate_users(self):
        
        # no users  
        answ0 = self.client.get("/board").data
        answ0 = json.loads(answ0.decode())
        self.assertEqual(0, answ0["userCount"])

        # 1 users
        answ1 = self.client.get("/board?userName=xsa&size=small&userCookie=9685").data
        answ1 = json.loads(answ1.decode())
        self.assertEqual(1, answ1["userCount"])

        # 2 users
        answ2 = self.client.get("/board?userName=xsa&size=small&userCookie=1005").data
        answ2 = json.loads(answ2.decode())
        self.assertEqual(2, answ2["userCount"])

        # same user
        answ3 = self.client.get("/board?userName=xsa&size=small&userCookie=9685").data
        answ3 = json.loads(answ3.decode())
        self.assertEqual(2, answ3["userCount"])

        # 1 user logs out
        answ4 = self.client.get("/board?userName=xsa&size=small&userCookie=9685&logout=True").data
        answ4 = json.loads(answ4.decode())
        self.assertEqual(1, answ4["userCount"])

        # new user logs in
        answ6 = self.client.get("/board?userName=xsa&size=small&userCookie=9905&logout=True").data
        answ6 = json.loads(answ6.decode())
        self.assertEqual(2, answ6["userCount"])

    # TODO - patikrinti ar teisingas user name

    def test_old_user(self):
        d = datetime.now() - timedelta(hours=1)
        time = d.timestamp()
        d1 = datetime.now() - timedelta(hours=48)
        time1 = d1.timestamp()

        d2 = datetime.now() + timedelta(hours=48)
        time2 = d2.timestamp()

        with open("users.txt", 'w') as f:
            f.write("1000;Jhon;" + str(time) + "\n" +
                    "2000;Jhon;" + str(time1) + "\n" +
                    "3000;Jhon;" + str(time2) + "\n")  
        
        answ0 = self.client.get("/board").data
        answ0 = json.loads(answ0.decode())
        self.assertEqual(1, answ0["userCount"])
        


if __name__ == '__main__':
    unittest.main(verbosity=2)        