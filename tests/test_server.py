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
    
    def test_debug_mode(self):
        data = {"restart": True, "debug": True}
        self.client.post("/", data=data)
        
        # debug mode
        answ1 = self.client.get("/board?userName=xsa&size=small&userCookie=9685").data
        answ1 = json.loads(answ1.decode())

        self.assertEqual(True, answ1["gameStarted"])
        self.assertEqual(1, answ1["userCount"])
        self.assertEqual(5, answ1["board"]["cordX"])
        self.assertEqual(6, answ1["board"]["cordY"])

        fieldList = answ1["board"]["fieldList"]
        count = 0
        for k in fieldList:
            count += 1
        self.assertEqual(30, count)

        answ1 = self.client.get("/board?userName=xsa&action=dig&id=13").data
        answ1 = json.loads(answ1.decode())

        f = answ1["board"]["fieldList"]["13"]
        self.assertEqual(0, f["bomb_count"])
        self.assertEqual("DUG", f["condition"])

    def test_dig_bomb2(self):
        
    # 5 6
    # B 2 B 1 0 
    # 1 2 1 1 0
    # 1 1 1 0 0
    # 1 B 1 1 1 //<-
    # 2 3 2 3 B
    # B 2 B 3 B

    # 5 6
    # 0 1 B 1 0 
    # 0 1 1 1 0
    # 1 1 1 0 0
    # 1 B 1 1 1 //<-
    # 2 3 2 3 B
    # B 2 B 3 B

        data = {"restart": True, "debug": True}
        self.client.post("/", data=data)

        self.client.get("/board?userName=Ali&size=small&userCookie=1000")
        
        answ1 = self.client.get("/board?userName=Ali&userCookie=1000&action=dig&id=0").data
        answ1 = json.loads(answ1.decode())
        self.assertEqual(True, answ1["gameOver"])
        
        f1 = answ1["board"]["fieldList"]["0"]
        self.assertEqual(0, f1["bomb_count"])
        self.assertEqual("DUG", f1["condition"])

        f2 = answ1["board"]["fieldList"]["1"]
        self.assertEqual(1, f2["bomb_count"])
        self.assertEqual("DUG", f2["condition"])

        f3 = answ1["board"]["fieldList"]["5"]
        self.assertEqual(0, f3["bomb_count"])
        self.assertEqual("DUG", f3["condition"])

        f4 = answ1["board"]["fieldList"]["6"]
        self.assertEqual(1, f4["bomb_count"])
        self.assertEqual("DUG", f4["condition"])

        f5 = answ1["board"]["fieldList"]["7"]
        self.assertEqual(1, f5["bomb_count"])
        self.assertEqual("UNTOUCH", f5["condition"])



if __name__ == '__main__':
    unittest.main(verbosity=2)