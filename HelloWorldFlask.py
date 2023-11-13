# import flask module
from flask import Flask, request, jsonify, render_template, redirect, url_for
import server_main as server

user_db = {}
session_map = {}

# instance of flask application
app = Flask(__name__)

# home route that returns below text when root url is accessed
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    client_id = data.get('client_id')
    password = data.get('password')

    status, message, session_id = server.register_user(client_id, password)

    if status == 200:
        return jsonify({'status': status, 'message': message, 'session_id': session_id})
    else:
        return jsonify({'status': status, 'error': message})

if __name__ == '__main__':
      app.run(debug=True)
      # server.set_up_log()

# if __name__ == '__main__':
#     set_up_log()

#     _, _, auth_1 = register_user(1, 'pass1')
#     _, _, auth_2 = register_user(1, 'pass2')
#     _, _, auth_3 = register_user(1, 'pass1')

#     increase_value(auth_1, 56)
#     decrease_value(auth_3, 96)

#     logout_user(auth_1)
#     logout_user(auth_1)
#     logout_user(auth_3)
#     logout_user(auth_3)