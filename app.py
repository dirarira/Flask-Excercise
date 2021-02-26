from flask import Flask, jsonify, request

app = Flask(__name__)
app.users = {}
app.id_count = 1


@app.route("/ping", methods=['GET'])
def ping():
    return "pong"

@app.route("/sign-up", methods=['POST'])
def sign_up():
    new_user = request.json
    new_user["id"] = app.id_count