from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Jack, Michael and Sharjeel are very cool (not Tipu)</p>"