#export FLASK_APP=run.py
#https://realpython.com/the-ultimate-flask-front-end/

from flask import Flask
from flask import render_template

app = Flask(__name__)

class Run:
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/more')
    def more():
        return render_template('more.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')