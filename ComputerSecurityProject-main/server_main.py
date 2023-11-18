import logging
import time
import uuid
from datetime import datetime
from passlib.hash import bcrypt
from werkzeug.middleware.proxy_fix import ProxyFix
import json
from flask import Flask, request, Response, session, jsonify
import secrets  

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Add HTTPS to SSL certificate and key files
ssl_certificate = 'your_cert.pem'  
ssl_key = 'your_key.pem'  

# Set a secure session key
app.secret_key = secrets.token_hex(16)

class ServerSide:

    def generate_session_id(self):
        return secrets.token_urlsafe(16)

    @app.route('/')
    def hello_world():
        return '<p>Hello world, server is live!</p>'

    @app.route('/register', methods=['POST', 'GET'])
    def register_user_api():
        if request.method == 'POST':
            post_data = request.get_json()
            user_id = post_data['user_id']
            # Generate a secure session ID
            session['session_id'] = ServerSide().generate_session_id()
            # Hash the password 
            hashed_password = bcrypt.using(rounds=12).hash(post_data['password'])
            # Log non-sensitive information
            app.logger.info(f"User registered: {user_id}")

            re_code, re_message, re_session_id = 200, 'User registered successfully', session['session_id']
            resp = Response(json.dumps({'message': re_message, 'session_id': re_session_id}), status=re_code,
                            mimetype='application/json')

            return resp
        else:
            return '<p>register_user called, use POST method with body={user_id, password}!</p>'


    @app.route('/logout', methods=['POST', 'GET'])
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
    def increase_value_api():
        if request.method == 'POST':
            post_data = request.get_json()
            re_code, re_message = server.increase_value(post_data['session_id'], post_data['by'])
            resp = Response(json.dumps({'message': re_message}), status=re_code, mimetype='application/json')
            return resp
        else:
            return '<p>increase_value called, use POST method with body={session_id, by}!</p>'

    @app.route('/decrease', methods=['POST', 'GET'])
    def decrease_value_api():
        if request.method == 'POST':
            post_data = request.get_json()
            re_code, re_message = server.decrease_value(post_data['session_id'], post_data['by'])
            resp = Response(json.dumps({'message': re_message}), status=re_code, mimetype='application/json')
            return resp
        else:
            return '<p>decrease_value called, use POST method with body={session_id, by}!</p>'

    @app.route('/check', methods=['GET'])
    def check_server_data():
        if request.method == 'GET':
            log_name = server.get_server_log()
            return Response(json.dumps({'log': log_name}), status='200', mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000, ssl_context=(ssl_certificate, ssl_key))
