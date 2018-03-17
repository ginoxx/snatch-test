import flask
from flask import jsonify, request
import sqlite3

app = flask.Flask(__name__)
# app.config["DEBUG"] = True


@app.route("/")
def hello():
    return "Hello Snatch!"


@app.route("/users/<string:user_name>")
def get_user(user_name):
    conn = sqlite3.connect("./data/users")
    cur = conn.cursor()
    sql = "SELECT username,email,phone,lat,lon FROM users WHERE username=?"
    cur.execute(sql, [user_name])
    user = cur.fetchone()
    map_link = "https://www.google.com/maps/search/?api=1&query=%s,%s" % (user[3], user[4])
    conn.close()

    if not user:
        return jsonify({'error': 'User does not exist'}), 404

    return jsonify({
        'username': user[0],
        'email': user[1],
        'phone': user[2],
        'map': map_link
    })


@app.route("/users", methods=["POST"])
def create_user():
    username = request.json.get('username')
    email = request.json.get('email')
    phone = request.json.get('phone')
    if not username or not email or not phone:
        return jsonify({'error': 'Please provide username, email and phone number '}), 400

    # check length
    if len(username) < 3 or len(username) > 12:
        return jsonify({
            'error': ' username must be between 3 and 12 characters '
        }), 400

    # validate username
    if check_name(username):
        conn = sqlite3.connect("./data/users")
        cur = conn.cursor()
        sql = "INSERT INTO users (username,email,phone) VALUES (?,?,?)"
        try:
            cur.execute(sql, [username, email, phone])
            conn.commit()
        except sqlite3.IntegrityError as e:
            if "username" in e.args[0]: field = "username"
            if "email" in e.args[0]: field = "email"
            if "phone" in e.args[0]: field = "phone"
            return jsonify({
                'error': ' %s already taken' % field
            }), 400

        finally:
            conn.close()

        if cur.lastrowid:
            return jsonify({
                'userId': cur.lastrowid,
                'username': username,
                'email': email,
                'phone': phone
            })

        else:
            return jsonify({
                'error': 'Database error'
            }), 400
    else:
        return jsonify({
            'error': 'Username %s not allowed' % username
        }), 400


@app.route("/location", methods=["POST"])
def update_location():
    # not clear is lat/lon need to be generated/fetched or provided via the API - Provided here
    username = request.json.get('username')
    lat = request.json.get('lat')
    lon = request.json.get('lon')
    if not username or not lat or not lon:
        return jsonify({'error': 'Please provide username, latitude and longitude'}), 400

    # db update
    conn = sqlite3.connect("./data/users")
    cur = conn.cursor()
    sql = "UPDATE users SET lat=?, lon=? WHERE username=?"
    cur.execute(sql, [lat, lon, username])
    conn.commit()
    conn.close()

    return jsonify({
        'username': username,
        'lat': lat,
        'lon': lon
    })


def check_name (user):
    user = user.lower()
    not_allowed = ['cat', 'dog', 'horse']
    exceptions = ['catfish', 'scatter', 'bulldog', 'seahorse']
    if any(user.find(s) >= 0 for s in not_allowed):
        if user in exceptions:
            return True
        else:
            return False
    else:
        return True


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')