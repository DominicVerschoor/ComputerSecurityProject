import datetime
import logging
import time
import uuid
from time import strftime
from datetime import datetime

user_db = {}
session_map = {}


def set_up_log(filename=None):
    if filename is None:
        filename = 'server-log-' + str(round(time.time())) + '.log'

    logging.basicConfig(filename='log/' + filename, encoding='utf-8', level=logging.DEBUG)
    logging.info(f'Server setup time: {datetime.now()}')


def register_user(new_id, new_pass):
    new_id = str(new_id)
    new_pass = str(new_pass)

    if new_id in user_db.keys():

        if user_db[new_id]['password'] == new_pass:
            new_session_id = str(uuid.uuid4())
            session_map[new_session_id] = new_id
            user_db[new_id]['session'].append(new_session_id)
            
            logging.info(f'USER_ID: {new_id} SESSION_ID {new_session_id} VALUE: {user_db[new_id]["value"]} MESSAGE: New session created. {datetime.now()}')
            return 200, 'New session created.', new_session_id

        return 300, 'Incorrect password', None

    new_session_id = str(uuid.uuid4())
    session_map[new_session_id] = new_id
    user_db[new_id] = {'password': new_pass, 'value': 1, 'session': [new_session_id]}

    logging.info(f'USER_ID: {new_id} SESSION_ID {new_session_id} VALUE: {user_db[new_id]["value"]} MESSAGE: New user registered. {datetime.now()}')
    return 200, 'New user registered.', new_session_id


def logout_user(session_id):
    if session_id in session_map:
        user_id = session_map[session_id]

        if session_id in user_db[user_id]['session']:

            user_db[user_id]['session'].remove(session_id)
            session_map.pop(session_id)

            if len(user_db[user_id]['session']) <= 0:
                user_db.pop(user_id)

                logging.info(f'USER_ID: {user_id} SESSION_ID {session_id} MESSAGE: Session logout - user destroyed. {datetime.now()}')
                return 200, 'Session logout - user destroyed.'

            logging.info(f'USER_ID: {user_id} SESSION_ID {session_id} MESSAGE: Session logout - user still online. {datetime.now()}')
            return 200, 'Session logout - user still online.'

        return 300, 'Session do not exist 2.'

    return 300, 'Session do not exist.'


def increase_value(session_id, by):
    if session_id in session_map:
        user_id = session_map[session_id]

        if session_id in user_db[user_id]['session']:

            if str(by).isnumeric():
                user_db[user_id]['value'] += by

                logging.info(f'USER_ID: {user_id} SESSION_ID {session_id} VALUE: {user_db[user_id]["value"]} MESSAGE: Increase value by: {by}. {datetime.now()}')
                return 200, f'Set new value {user_db[user_id]["value"]}'

            print('Value provided not a number.')
            return 300, 'Value provided not a number.'
        print('Session do not exist 2.')
        return 300, 'Session do not exist 2.'
    print('Session do not exist.')
    return 300, 'Session do not exist.'


def decrease_value(session_id, by):
    if session_id in session_map:
        user_id = session_map[session_id]

        if session_id in user_db[user_id]['session']:

            if str(by).isnumeric():
                user_db[user_id]['value'] -= by

                logging.info(f'USER_ID: {user_id} SESSION_ID {session_id} VALUE: {user_db[user_id]["value"]} MESSAGE: Decrease value by: {by}. {datetime.now()}')
                return 200, f'Set new value {user_db[user_id]["value"]}'

            print('Value provided not a number.')
            return 300, 'Value provided not a number.'
        print('Session do not exist 2.')
        return 300, 'Session do not exist 2.'
    print('Session do not exist.')
    return 300, 'Session do not exist.'


if __name__ == '__main__':
    set_up_log()

    _, _, auth_1 = register_user(1, 'pass1')
    _, _, auth_2 = register_user(1, 'pass2')
    _, _, auth_3 = register_user(1, 'pass1')

    increase_value(auth_1, 56)
    decrease_value(auth_3, 96)

    logout_user(auth_1)
    logout_user(auth_1)
    logout_user(auth_3)
    logout_user(auth_3)

