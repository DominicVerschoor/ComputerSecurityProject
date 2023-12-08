import json

from flask import Flask, request, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from server_main import ServerSide

# instance of flask application
app = Flask(__name__)
server = ServerSide()

limiter = Limiter(get_remote_address, app=app)



@app.route('/')
@limiter.limit("10/minute")
def hello_world():
    return '<p>Hello world, serve is live!</p>'


@app.route('/register', methods=['POST', 'GET'])
@limiter.limit("10/minute")
def register_user_api():
    if request.method == 'POST':
        post_data = request.get_json()
        re_code, re_message, re_session_id = server.register_user(post_data['user_id'], post_data['password'])
        resp = Response(json.dumps({'message': re_message,
                                    'session_id': re_session_id}), status=re_code, mimetype='application/json')
        return resp
    else:
        return '<p>register_user called, use POST method with body={user_id, password}!</p>'


@app.route('/logout', methods=['POST', 'GET'])
@limiter.limit("10/minute")
def logout_user_api():
    if request.method == 'POST':
        post_data = request.get_json()
        re_code, re_message = server.logout_user(post_data['session_id'])
        resp = Response(json.dumps({'message': re_message, 'session_id': post_data['session_id']}), status=re_code,
                        mimetype='application/json')
        return resp
    else:
        return '<p>logout_user called, use POST method with body={session_id}!</p>'


@app.route('/increase', methods=['POST', 'GET'])
@limiter.limit("20/minute")
def increase_value_api():
    if request.method == 'POST':
        post_data = request.get_json()
        re_code, re_message = server.increase_value(post_data['session_id'], post_data['by'])
        resp = Response(json.dumps({'message': re_message}), status=re_code, mimetype='application/json')
        return resp
    else:
        return '<p>increase_value called, use POST method with body={session_id, by}!</p>'


@app.route('/decrease', methods=['POST', 'GET'])
@limiter.limit("20/minute")
def decrease_value_api():
    if request.method == 'POST':
        post_data = request.get_json()
        re_code, re_message = server.decrease_value(post_data['session_id'], post_data['by'])
        resp = Response(json.dumps({'message': re_message}), status=re_code, mimetype='application/json')
        return resp
    else:
        return '<p>decrease_value called, use POST method with body={session_id, by}!</p>'


@app.route('/check', methods=['GET'])
@limiter.limit("10/minute")
def check_server_data():
    if request.method == 'GET':
        log_name = server.get_server_log()
        return Response(json.dumps({'log': log_name}), status='200', mimetype='application/json')


if __name__ == '__main__':
    app.run(ssl_context=('server_main.crt', 'server_main.key'), debug=False)
