from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    log_list = [row for row in list(open("../logs/obama.log"))]
    return render_template('index.html', log_list=log_list)
