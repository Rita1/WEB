# source env/bin/activate
# export FLASK_APP=run.py
# export FLASK_ENV=development
# flask run
# pip freeze > requirements.txt
# npm run watch
# npm install jquery --save
# python -m pytest
# npx cypress open
# pytest -k  "debug"
# gunicorn run:app --worker-class gevent --bind 0.0.0.0:8000
# https://github.com/Ulumanshu/SERVERD2/blob/master/Flask_Keras_Multi.py

import json
from datetime import datetime, timedelta
import time
import io
import os
from flask import Flask, render_template, request, Response
try:
    from . import board
    from . import user
except:
    import board
    import user


# app = Flask(__name__,  template_folder='./static')
app = Flask(__name__, static_url_path='/static', template_folder='./static')

__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Server():

# board'o desineje saugoma lentele su useriais ir ju taskais
# uz kiekviena atidaryta arba uzymeta veliavyte langeli gauni po taska
# laimi tas kuris zaidimo pabaigoje (gameWin) turi daugiausia tasku
# lentele isrikiuojama pagal daugiausiai turinti tasku zaideja

    game = ''
    active_users = 0
    HOURS_OLD = 1
    debug = False
    file1 = os.path.join(__location__, 'tests/boards/board3') # 3
    need_update = False
    users = []
    # users = [user_id, user_id, user_id]

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            # print("request, data, form", request, request.data, request.form)
            # data = json.loads(request.data.decode())
            restart = request.form.get('restart')
            if restart:
                Server.restart_server()
            debug = request.form.get('debug')
            if debug:
                Server.debug = True
        return render_template('index.html')
    


    @app.route('/stream')
    def stream():
        def push_answ():
            # while True:
            #     # time.sleep(1)
            #     if Server.need_update == True:
            #         yield 'data'+': '+ str(json.dumps(Server.toJson()))+'\n'+'\n'
            #         Server.need_update = False
            #         print("stream answ")
            if Server.need_update == True:
                yield 'data'+': '+ str(json.dumps(Server.toJson()))+'\n'+'\n'
                Server.need_update = False
                print("stream answ")
        return Response(response=push_answ(), status=200, mimetype="text/plain", content_type="text/event-stream")

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
        logout = request.args.get('logout') or False
        restart = request.args.get('restart') or False

        if logout:
            #  print("from logout", user_name)
            Server.calculate_users(user_name, user_cookie, logout)
            answ = Server.toJson()
            return Response(json.dumps(answ), mimetype='application/json')
       
        # If check status, return that game not started
        # print("Server.game", Server.game)
        if (checkStatus and Server.game == ''):
            # kartais neissivalo failiukas
            Server.restart_server()
            answ = Server.toJson()
            
            return Response(json.dumps(answ), mimetype='application/json')

        # Start game if needed
        Server.getGame(size)
        
        # Calculate users
        
        Server.calculate_users(user_name, user_cookie, logout)
        
        if field_id:
            field_id = int (field_id)
            f = Server.game.get_field(field_id)   
        # Dig
        boom = False
        
        if action == 'dig' and not f.get_condition() == "FLAG":
            digged_qty = 0
            if f.is_Bomb():
                Server.game.dig_bomb(field_id)
                boom = True
                Server.calculate_users(user_name, user_cookie, False)
            else:
                digged_qty = Server.game.dig(field_id)
            Server.update_users_info(user_cookie, action, digged_qty)    
        # Flag-unflag        
        if action == 'flag':
            Server.game.flag(field_id)
            Server.update_users_info(user_cookie, action, 1)
        # Restart server
        if restart:
            Server.restart_game()
        # Return answer
        answ = Server.toJson()
        if boom:
            answ["gameOver"] = True

        answ_json = json.dumps(answ)
        print("answ_json", answ_json)
        return Response(answ_json, mimetype='application/json')
    
    def getGame(size):
        
        print("Server.game, size, debug", Server.game, size, Server.debug)
        if not Server.game and Server.debug:
            Server.restart_server()
            Server.game = board.Board(size, Server.file1)
        if not Server.game:
            Server.game = board.Board(size)
        return Server.game

    # Takes user name and ID
    # saves with timestamp to file, if ID not present
    # saves active users from file to server
    # deletes very old users (>1h) from file
    # deletes user, when he logouts

    def calculate_users(user_name, user_cookie, logout=False):
        
        found = False
        count = 0
        if user_cookie and user_name and not logout:
            new_user = user.User(user_name, user_cookie)
            if not Server.users:
                Server.users.append(new_user)
            if user_cookie not in [u.return_cookie() for u in Server.users]:
                Server.users.append(new_user)
        if user_cookie and logout:
            for u in Server.users:
                if u.return_cookie() == user_cookie:
                    Server.users.remove(u)
        Server.active_users = len(Server.users)
  
    def update_users_info(user_cookie, action, qty):
        for u in Server.users:
            if u.return_cookie() == user_cookie:
                if action == "flag":
                    u.increase_flag(qty)
                    print("u increased flag", u.get_info())
                if action == "dig":
                    u.increase_digged(qty)
                    print("u increase_digged", u.get_info())

    def users_info():
        myDict = {}
        sorted_users = sorted(Server.users, key=lambda u: u.return_total_qty(), reverse=True)
        for u in sorted_users:
            myDict[u.return_cookie()] = u.get_info()
        return myDict
        
    def restart_server():
        print("Server restart!")
        # if os.path.exists('users.txt'):
        #     open("users.txt", 'w').close()
        Server.users = []  
        Server.game = ''
        Server.active_users = 0

    def restart_game():
        print("Game restart!")
        Server.game = '' 

    def toJson():
        answ = {}
        # answ = {
        #     "userCount" : 2,
        #     "users" : {
        #        cookie : {
        #          "username" : "Petras",
        #          "flaged_qty" : 0,
        #          "digged_qty " : 0,
        #          "total_qty" : 0,
        #        }
        #      }
        #     "gameOver" : True
        #     "board" : {
        #         "cordX" : 9,
        #         "cordY" : 9,
        #         "gameWin" : False
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
           
        answ["gameStarted"] = False
        answ["gameOver"] = False
        answ["ID"] = str(Server.game)
        user_count = Server.active_users
        answ["userCount"] = user_count
        answ["users"] = Server.users_info()
        if Server.game:
            answ["gameStarted"] = True
            answ["board"] = Server.game.toJson()

        # stream changes for all clients
        Server.need_update = True
        return answ


        
if __name__ == "__main__":
    #  app.run(host='0.0.0.0', threaded=True,)
    app.run(host='0.0.0.0', debug=True)
