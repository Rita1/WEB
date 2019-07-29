#export FLASK_APP=run.py
#ccs
#klase
#responsive
#.body {
#    display: flex;
#    flex-wrap: wrap;
#}

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/more')
def more():
    return render_template('more.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')