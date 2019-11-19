

class Users_list():

    # list of users object

    def __init__(self):
        self.users = []

    def increase_flag(self, qty):
        self.flaged_qty += qty

    def increase_digged(self, qty):
        self.digged_qty += qty

    def return_cookie(self):
        return self.cookie

    def return_timestamp(self):
        return self.timestamp
    
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

        return user
