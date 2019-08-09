# source env/bin/activate
# export FLASK_APP=run.py
# flask run
# pip freeze > requirements.txt
# npm run watch
# npm install jquery --save
#  https://realpython.com/the-ultimate-flask-front-end/

import json
from flask import Flask, render_template

# app = Flask(__name__,  template_folder='./static')
app = Flask(__name__, static_url_path='/static', template_folder='./static')


class Server():

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/board')
    def getGame():
        my_dict = {
            1 : "A",
            2 : "B",
            3 : "C",
        }

        json_dict = json.dumps(my_dict)
        return json_dict

        
if __name__ == "__main__":
    app.run(host='0.0.0.0')
