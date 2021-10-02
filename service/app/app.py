from flask import Flask


app = Flask(__name__)


@app.route("/user_management/login", methods=["POST"])
def login():
    # need to return jwt sort of things
    return "you are logged in"