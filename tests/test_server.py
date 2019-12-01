import unittest
import pytest
import json
import os
import sys
from datetime import datetime, timedelta

from .. import field
from .. import board
from .. import run
from .. import user

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
        
        # OLD
        open("users.txt", 'a').close()

        run.app.config["TESTING"] = True
        self.client = run.app.test_client()
        data = {"restart": True}
        self.client.post("/", data=data)

    def tearDown(self):
        # OLD
        os.remove("users.txt")

        data = {"restart": True}
        self.client.post("/", data=data)

    def test_calculate_users(self):
        
        # no users  
        answ0 = self.client.get("/board").data
        answ0 = json.loads(answ0.decode())
        self.assertEqual(0, answ0["userCount"])
        self.assertFalse(answ0["users"])

        # 1 users
        answ1 = self.client.get("/board?userName=xsa&size=small&userCookie=9685").data
        answ1 = json.loads(answ1.decode())
        self.assertEqual(1, answ1["userCount"])
        self.assertEqual("xsa", answ1["users"]["9685"]["username"])

        # 2 users
        answ2 = self.client.get("/board?userName=xsa&size=small&userCookie=1005").data
        answ2 = json.loads(answ2.decode())
        self.assertEqual(2, answ2["userCount"])
        self.assertEqual("xsa", answ2["users"]["1005"]["username"])

        # # same user
        answ3 = self.client.get("/board?userName=xsa&size=small&userCookie=9685").data
        answ3 = json.loads(answ3.decode())
        self.assertEqual(2, answ3["userCount"])

        # # 1 user logs out
        answ4 = self.client.get("/board?userName=xsa&size=small&userCookie=9685&logout=True").data
        answ4 = json.loads(answ4.decode())
        self.assertEqual(1, answ4["userCount"])

        # new user logs in
        answ6 = self.client.get("/board?userName=xsa&size=small&userCookie=9905").data
        answ6 = json.loads(answ6.decode())
        self.assertEqual(2, answ6["userCount"])

    # TODO - patikrinti ar teisingas user name

    # def test_old_user(self):
    #     d = datetime.now() - timedelta(hours=1)
    #     time = d.timestamp()
    #     d1 = datetime.now() - timedelta(hours=48)
    #     time1 = d1.timestamp()

    #     d2 = datetime.now() + timedelta(hours=48)
    #     time2 = d2.timestamp()

    #     with open("users.txt", 'w') as f:
    #         f.write("1000;Jhon;" + str(time) + "\n" +
    #                 "2000;Jhon;" + str(time1) + "\n" +
    #                 "3000;Jhon;" + str(time2) + "\n")
        
    #     answ0 = self.client.get("/board").data
    #     answ0 = json.loads(answ0.decode())
    #     self.assertEqual(1, answ0["userCount"])
    
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
        self.assertEqual("1000", answ1["gameOver"])
        self.assertFalse(answ1["board"]["gameWin"])
        
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

    def test_flag_unflag(self):
        
        data = {"restart": True, "debug": True}
        self.client.post("/", data=data)
        
        # Flag
        answ1 = self.client.get("/board?userName=Ali&userCookie=1000&action=flag&id=0").data
        answ1 = json.loads(answ1.decode())

        f1 = answ1["board"]["fieldList"]["0"]
        self.assertEqual("FLAG", f1["condition"])
        
        # CLICK
        answ10 = self.client.get("/board?userName=Ali&userCookie=1000&action=dig&id=0").data
        answ10 = json.loads(answ10.decode())
        f1 = answ1["board"]["fieldList"]["0"]
        self.assertEqual("FLAG", f1["condition"])

        # UNFLAG
        answ2 = self.client.get("/board?userName=Ali&userCookie=1000&action=flag&id=0").data
        answ2 = json.loads(answ2.decode())

        f1 = answ2["board"]["fieldList"]["0"]
        self.assertEqual("UNTOUCH", f1["condition"])

    def test_restart_server(self):

        #Restart
        answ1 = self.client.get("/board?userName=Ali&userCookie=1000&restart=True").data
        answ1 = json.loads(answ1.decode())
        # print("answ1", answ1)
        self.assertFalse(answ1["gameStarted"])
        self.assertTrue("board" not in answ1)
        # # Push button and restart
        # Register
        answ2 = self.client.get("/board?userName=xsa&size=small&userCookie=9685").data
        answ2 = json.loads(answ2.decode())

        self.assertTrue(answ2["gameStarted"])
        self.assertTrue(answ2["board"])
        # Push button
        self.client.get("/board?userName=Ali&userCookie=1000&action=dig&id=0")
        # Restart
        answ3 = self.client.get("/board?userName=Ali&userCookie=1000&restart=True").data
        answ3 = json.loads(answ3.decode())

        self.assertFalse(answ3["gameStarted"])
        self.assertTrue("board" not in answ3)

    def test_update_user_info(self):

        data = {"restart": True, "debug": True}
        self.client.post("/", data=data)

        answ1 = self.client.get("/board?userName=Ali&userCookie=1000&action=flag&id=0").data
        answ1 = json.loads(answ1.decode())

        u1 = answ1["users"]["1000"]
        self.assertEqual(0, u1["flaged_qty"])
        self.assertEqual(0, u1["digged_qty"])
        self.assertEqual(0, u1["total_qty"])

        answ1 = self.client.get("/board?userName=Jhon&userCookie=2000&action=dig&id=1").data
        answ1 = json.loads(answ1.decode())

        u1 = answ1["users"]["2000"]
        self.assertEqual(0, u1["flaged_qty"])
        self.assertEqual(1, u1["digged_qty"])
        self.assertEqual(1, u1["total_qty"])

        answ1 = self.client.get("/board?userName=Ali&userCookie=1000&action=dig&id=9").data
        answ1 = json.loads(answ1.decode())
        u1 = answ1["users"]["1000"]
        self.assertEqual(0, u1["flaged_qty"])
        self.assertEqual(11, u1["digged_qty"])
        self.assertEqual(11, u1["total_qty"])

    def test_dig_bomb_unflag(self):
        #  viena karta susprogus ir nuimant veliavele vel sprogsti
        data = {"restart": True, "debug": True}
        self.client.post("/", data=data)

        # zymim veliava
        answ1 = self.client.get("/board?userName=Ali&userCookie=1000&action=flag&id=1").data
        answ1 = json.loads(answ1.decode())
        self.assertEqual(False, answ1["gameOver"])
        
        # sprogdinam bomba
        answ1 = self.client.get("/board?userName=Ali&userCookie=1000&action=dig&id=0").data
        answ1 = json.loads(answ1.decode())

        u1 = answ1["users"]["1000"]
        self.assertEqual(0, u1["total_qty"])
        self.assertEqual("1000", answ1["gameOver"])
        
        # nuimam veliava
        answ1 = self.client.get("/board?userName=Ali&userCookie=1000&action=flag&id=1").data
        answ1 = json.loads(answ1.decode())

        u1 = answ1["users"]["1000"]
        self.assertEqual(0, u1["total_qty"])
        self.assertEqual(False, answ1["gameOver"])

if __name__ == '__main__':
    unittest.main(verbosity=2)