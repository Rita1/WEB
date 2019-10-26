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

import json
from datetime import datetime, timedelta
import time
import io
import os
from flask import Flask, render_template, request, Response, stream_with_context
try:
    from . import board
except:
    import board


# app = Flask(__name__,  template_folder='./static')
app = Flask(__name__, static_url_path='/static', template_folder='./static')

__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Server():

    game = ''
    active_users = 0
    HOURS_OLD = 1
    debug = False
    file1 = os.path.join(__location__, 'tests/boards/board3') # 3
    answ = 0
    need_update = False

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            print("request, data, form", request, request.data, request.form)
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
            while True:
                if Server.need_update == True:
                    yield 'data'+': '+ str(Server.toJson())+'\n'+'\n'
                    Server.answ += 1
                    Server.need_update = False
                Server.answ += 1
                print("stream", Server.answ)

        return Response(response=push_answ(), status=200, mimetype="text/plain", content_type="text/event-stream")

# https://www.edureka.co/community/30828/how-do-you-add-a-background-thread-to-flask-in-python

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

        logout = False
        if request.args.get('logout'):
            logout = True
            print("from logout", user_name)
            Server.calculate_users(user_name, user_cookie, logout)
            answ = Server.toJson()
            return Response(json.dumps(answ), mimetype='application/json')

        # If check status, return that game not started
        print("Server.game", Server.game)
        if checkStatus and Server.game == '':
            print("from checkStatus")
            answ_not_started = {"gameStarted": False}
            # kartais neissivalo failiukas
            Server.restart_server()
            return Response(json.dumps(answ_not_started), mimetype='application/json')

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
            if f.is_Bomb():
                Server.game.dig_bomb(field_id)
                boom = True
                Server.calculate_users(user_name, user_cookie, True)
            else:
                Server.game.dig(field_id)
        # Flag-unflag        
        if action == 'flag':
            Server.game.flag(field_id)
        
        # Return answer
        answ = Server.toJson()
        if boom:
            answ["gameOver"] = True

        # print("Answer from server", answ)
        answ_json = json.dumps(answ)
    
        return Response(answ_json, mimetype='application/json')
    
    def getGame(size):
        
        # print("Server.game, size, debug", Server.game, size, debug)
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
        
        # print("user_name, cookie, logout", user_name, user_cookie, logout)
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
            if user_cookie and user_name and not logout:
                time = datetime.now().timestamp()
                str_to_write = user_cookie + ";" +  user_name + ";" + str(time) + "\n"
                buffer.write(str_to_write)
                count += 1
        with open('users.txt', 'w') as to_write:
            to_write.write(buffer.getvalue())
            buffer.flush()
        Server.active_users = count
        # print("calculating users", Server.active_users)

    def restart_server():
        print("Server restart!")
        if os.path.exists('users.txt'):
            open("users.txt", 'w').close()
        Server.game = ''
        Server.active_users = 0

    def toJson():
        answ = {}
        # answ = {
        #     "userCount" : 2,
        #     "gameOver" : True
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
        answ["ID"] = str( Server.game )
        user_count = Server.active_users
        answ["userCount"] = user_count
        if Server.game:
            answ["board"] = Server.game.toJson()

        # stream changes for all clients
        print("Stream from handle game")
        Server.need_update = True
        return answ


        
if __name__ == "__main__":
    #  app.run(host='0.0.0.0', threaded=True,)
    app.run(host='0.0.0.0', debug=True)
