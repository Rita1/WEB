# source env/bin/activate
# export FLASK_APP=run.py
# export FLASK_ENV=development
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
try:
    from . import board
except:
    import board
from flask import Response


# app = Flask(__name__,  template_folder='./static')
app = Flask(__name__, static_url_path='/static', template_folder='./static')

__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Server():

    game = ''
    active_users = 0
    HOURS_OLD = 1
    debug = False
    file1 = os.path.join(__location__, 'boards/board3')

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            data = request.get_json()
            if data['restart']:
                Server.restart_server()
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
        action = request.args.get('action')
        field_id = request.args.get('id')

        debug = False
        if request.args.get('debug'):
            debug = True

        logout = False
        if request.args.get('logout'):
            logout = True

        # If check status, return that game not started

        if checkStatus and Server.game == '':
            answ_not_started = {"gameStarted" : False}
            print("answer from server", answ_not_started)
            return Response(json.dumps(answ_not_started), mimetype='application/json')

        # Start game if needed
        Server.getGame(size, debug)
        print("Server game", Server.game)
        
        # Calculate users

        Server.calculate_users(user_name, user_cookie, logout)

        # Dig

        if action == 'dig':
            print("Diging")
            Server.game.dig(int (field_id))
        if action == 'flag':
            Server.game.flag(int (field_id))
        
        # Return answer
        answ = Server.toJson()
        print("Answer from server", answ)
        answ_json = json.dumps(answ)

        return Response(answ_json, mimetype='application/json')
    
    def getGame(size, debug):
        
        if not Server.game and debug:
            Server.restart_server()
            Server.game = board.Board(size, debug)
        if not Server.game:
            Server.game = board.Board(size)
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

    def restart_server():
        if os.path.exists('users.txt'):
            open("users.txt", 'w').close()
        Server.game = ''
        Server.active_users = 0

    def toJson():
        answ = {}
        # answ = {
        #     "userCount" : 2,
        #     "board" : {
        #         "cordX" : 9,
        #         "cordY" : 9,
        #         "fieldList" : {
        #             0 : {
        #                 "cordX" : 0,
        #                 "cordY" : 0,
        #                 "condition" : "Untouch",
        #                 "isBomb" : False,
        #                 "bombCount" : 0
        #             },
        #             1 : {
        #                 "cordX" : 1,
        #                 "cordY" : 0,
        #                 "condition" : "Untouch",
        #                 "isBomb" : False,
        #                 "bombCount" : 0
        #             }
        #         }
        #     },
        # }
        
        answ["gameStarted"] = True
        user_count = Server.active_users
        answ["userCount"] = user_count
        answ["board"] = Server.game.toJson()
        return answ


        
if __name__ == "__main__":
    app.run(host='0.0.0.0')
