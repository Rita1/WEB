# source env/bin/activate
# export FLASK_APP=run.py
# flask run
# pip freeze > requirements.txt
# npm run watch
# npm install jquery --save
#  https://realpython.com/the-ultimate-flask-front-end/

import json
from flask import Flask, render_template, request

# app = Flask(__name__,  template_folder='./static')
app = Flask(__name__, static_url_path='/static', template_folder='./static')


class Server():

    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Board : sizeX, sizeY, listof Fields
    # Size: Small 9 x 9, Medium 16 x 16, Large 30 x 24
    # Field : cordX, cordY, condition (Flag, DUG, Untouch), isBomb, BombCount
    @app.route('/board')
    def getGame():

        my_dict = {
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
        username = request.args.get('userName')
        size = request.args.get('size')
        print("username", username, "size", size)
        json_dict = json.dumps(my_dict)
        print("json_dict", json_dict)
        return json_dict

        
if __name__ == "__main__":
    app.run(host='0.0.0.0')
