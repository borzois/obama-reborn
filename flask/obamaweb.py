from flask import Flask, render_template

app = Flask(__name__)

log_list = ['bla bla']


@app.route("/")
def index():
    return render_template('index.html', log_list=log_list)
