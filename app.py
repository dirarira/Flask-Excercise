from flask import Flask, jsonify, request
from flask.json import JSONEncoder

app = Flask(__name__)
app.users = {}
app.tweets = []
app.id_count = 1


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)

        return JSONEncoder.default(o)


app.json_encoder = CustomJSONEncoder


@app.route("/ping", methods=['GET'])
def ping():
    return "pong"


@app.route("/sign-up", methods=['POST'])
def sign_up():
    new_user = request.json
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count += 1

    return jsonify(new_user)


@app.route("/tweet", methods=['POST'])
def tweet():
    payload = request.json
    user_id = int(payload['id'])
    tweet = payload['tweet']

    if user_id not in app.users:
        return '사용자가 존재하지 않습니다', 400

    if len(tweet) > 300:
        return '300자를 초과했습니다', 300

    app.tweets.append({
        'user_id': user_id,
        'tweet': tweet
    })

    return 'Success!!', 200


@app.route('/follow', methods=['POST'])
def follow():
    paylod = request.json
    id = int(paylod['id'])
    follow = int(paylod['follow'])

    if id not in app.users or follow not in app.users:
        return '사용자가 존재하지 않습니다', 400

    user: dict = app.users[id]
    user.setdefault('follow', set()).add(follow)

    return jsonify(user)


@app.route('/unfollow', methods=['POST'])
def unfollow():
    payload = request.json
    user_id = payload['id']
    unfollow = payload['unfollow']

    if user_id not in app.users or follow not in app.users:
        return '사용자가 존재하지 않습니다', 400

    user: dict = app.users[user_id]
    user.setdefault('follow', set()).discard(unfollow)


@app.route('/timeline/<int:user_id>', methods=['GET'])
def timeline(user_id):
    if user_id not in app.users:
        return '사용자가 존재하지 않습니다', 400

    follow_list: set = app.users[user_id].get('follow', set())
    follow_list.add(user_id)
    timeline = [tweet for tweet in app.tweets if tweet['user_id'] in follow_list]

    return jsonify({
        'user_id': user_id,
        'timeline': timeline
    })

