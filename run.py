# source env/bin/activate
# export FLASK_APP=run.py
# flask run
# pip freeze > requirements.txt
# npm run watch
# npm install jquery --save
# python -m pytest
# npx cypress open
#  https://realpython.com/the-ultimate-flask-front-end/

import json
from datetime import datetime, timedelta
import io
import os
from flask import Flask, render_template, request
from . import board

# app = Flask(__name__,  template_folder='./static')
app = Flask(__name__, static_url_path='/static', template_folder='./static')



class Server():

    game = ''
    active_users = 0
    HOURS_OLD = 1

    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Board : sizeX, sizeY, listof Fields
    # Size: Small 9 x 9, Medium 16 x 16, Large 30 x 24
    # Field : cordX, cordY, condition (Flag, DUG, Untouch), isBomb, BombCount

    # HandleGame - main method to play multiPlayer Minsweeper
    # Check if game started:
    #	if started return game info
    #   else return new Game
    # Calculate active users
    # 

    @app.route('/board')
    def handleGame():

        # Parse info
        print("request.args", request.args)
        user_name = request.args.get('userName')
        user_cookie = request.args.get('userCookie')
        checkStatus = request.args.get("checkStart")
        size = request.args.get('size')

        logout = False
        if request.args.get('logout'):
            logout = True

        # If check status, return that game not started

        if checkStatus and Server.game == '':
            answ_not_started = {"gameStarted" : False}
            print("answer from server", answ_not_started)
            return json.dumps(answ_not_started)

        # Start game if needed
        Server.getGame(size, 0)
        print("Server game", Server.game)
        
        # Calculate users

        Server.calculate_users(user_name, user_cookie, logout)
        
        # Return answer
        answ = Server.toJson()
        print("Answer from server", answ)
        answ_json = json.dumps(answ)
        return answ_json
    
    def getGame(size, usercount):
        
        if not Server.game:
            Server.game = board.Board(size, usercount)
        return Server.game

    # Takes user name and ID
    # saves with timestamp to file, if ID not present
    # saves active users from file to server
    # deletes very old users (>1h) from file
    # deletes user, when he logouts

    def calculate_users(user_name, user_cookie, logout=False):
        
        buffer = io.StringIO()
        found = False
        count = 0
        d = datetime.now() - timedelta(hours=Server.HOURS_OLD)
        t1 = d.timestamp()

        if not os.path.exists('users.txt'):
            open("users.txt", 'a').close()

        with open('users.txt', 'r') as to_read:
            for line in to_read:
                li = line.split(";")
                line_cookie = li[0]
                line_timestamp = float(li[2])
                if line_cookie == user_cookie and logout:
                    found = True
                elif line_cookie == user_cookie:
                    found = True
                    if line_timestamp > t1:
                        buffer.write(line)
                        count += 1
                elif line_timestamp > t1:
                    buffer.write(line)
                    count += 1

        if not found:  
            if user_cookie and user_name:
                time = datetime.now().timestamp()
                str_to_write = user_cookie + ";" +  user_name + ";" + str(time) + "\n"
                buffer.write(str_to_write)
                count += 1
        with open('users.txt', 'w') as to_write:
            to_write.write(buffer.getvalue())
            buffer.flush()
        Server.active_users = count

    def toJson():
        answ = {
            "userCount" : 2,
            "board" : {
                "cordX" : 9,
                "cordY" : 9,
                "fieldList" : {
                    0 : {
                        "cordX" : 0,
                        "cordY" : 0,
                        "condition" : "Untouch",
                        "isBomb" : False,
                        "bombCount" : 0
                    },
                    1 : {
                        "cordX" : 1,
                        "cordY" : 0,
                        "condition" : "Untouch",
                        "isBomb" : False,
                        "bombCount" : 0
                    }
                }
            },
        }

        answ["gameStarted"] = True
        user_count = Server.active_users
        answ["userCount"] = user_count

        return answ


        
if __name__ == "__main__":
    app.run(host='0.0.0.0')
