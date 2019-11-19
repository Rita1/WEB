import time
from datetime import datetime, timedelta

class User():

    # name - prisiregistravusio zaidejo vardas
    # cookie
    # timestamp - kada useris prisiregistravo, senus ismetam lauk
    # flaged_qty - Veliavele pazymeta tasku
    # digged_qty -  Atidengta lauku su taskais
    # total_qty - Bendras tasku kiekis

    def __init__(self, name, cookie):
        self.name = name
        self.cookie = cookie
        self.timestamp = datetime.now().timestamp()
        self.flaged_qty = 0
        self.digged_qty = 0
        self.total_qty = 0

    def increase_flag(self, qty):
        self.flaged_qty += qty
        self.total_qty += qty

    def increase_digged(self, qty):
        self.digged_qty += qty
        self.total_qty += qty

    def return_cookie(self):
        return self.cookie

    def return_total_qty(self):
        return self.total_qty

    def return_timestamp(self):
        return self.timestamp

    def make_zero(self):
        self.flaged_qty = 0
        self.digged_qty = 0
        self.total_qty = 0  
    
    # returns dict about user:
        #        {
        #          "username" : "Petras",
        #          "flaged_qty" : 0,
        #          "digged_qty " : 0,
        #          "total_qty" : 0,
        #        }
    def get_info(self):
        user = {}
        user["username"] = self.name
        user["cookie"] = self.cookie
        user["flaged_qty"] = self.flaged_qty
        user["digged_qty"] = self.digged_qty
        user["total_qty"] = self.total_qty

        return user
