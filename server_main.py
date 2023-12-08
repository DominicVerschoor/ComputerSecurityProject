import datetime
import logging
import time
import uuid
from datetime import datetime

import bcrypt


class ServerSide:

    def __init__(self, logfile=None):
        self.user_db = {}
        self.session_map = {}

        if logfile is None:
            logfile = 'server-log-' + str(round(time.time())) + '.log'

        self.logfile = logfile

        logging.basicConfig(filename='log/' + logfile, encoding='utf-8', level=logging.DEBUG)
        logging.info(f'Server setup time: {datetime.now()}')

    def validate_id_input(self, unvalidate_input, max_length=24):
        # Type validation
        if type(unvalidate_input) is not str:
            return False

        # Length validation
        if len(unvalidate_input) > max_length:
            return False

        # Character validation
        if not str(unvalidate_input).isalnum():
            return False

        return True

    def register_user(self, new_id, new_pass):
        if self.validate_id_input(new_id):
            new_id = str(new_id)
        else:
            return 300, 'Incorrect password or ID', None

        if not isinstance(new_pass, (bytes, bytearray)):
            new_pass = new_pass.encode('utf-8')

        hash_new_pass = bcrypt.hashpw(new_pass,
                                      bcrypt.gensalt())

        if new_id in self.user_db.keys():

            if bcrypt.checkpw(new_pass, self.user_db[new_id]['password']):
                new_session_id = str(uuid.uuid4())
                # hash_session_id = new_session_id
                hash_session_id = str(bcrypt.hashpw(new_session_id.encode('utf-8'), bcrypt.gensalt()))

                self.session_map[hash_session_id] = new_id
                self.user_db[new_id]['session'].append(hash_session_id)

                logging.info(
                    f'USER_ID: {new_id} SESSION_ID {list(self.session_map.keys()).index(hash_session_id)} VALUE: {self.user_db[new_id]["value"]} MESSAGE: New session created. {datetime.now()}')
                return 200, 'New session created.', hash_session_id

            return 300, 'Incorrect password or ID', None

        new_session_id = str(uuid.uuid4())
        # hash_session_id = new_session_id
        hash_session_id = str(bcrypt.hashpw(new_session_id.encode('utf-8'), bcrypt.gensalt()))

        self.session_map[hash_session_id] = new_id
        self.user_db[new_id] = {'password': hash_new_pass, 'value': 1, 'session': [hash_session_id]}

        logging.info(
            f'USER_ID: {new_id} SESSION_ID {list(self.session_map.keys()).index(hash_session_id)} VALUE: {self.user_db[new_id]["value"]} MESSAGE: New user registered. {datetime.now()}')
        return 200, 'New user registered.', hash_session_id

    def logout_user(self, session_id):
        if session_id in self.session_map.keys():
            user_id = self.session_map[session_id]

            if session_id in self.user_db[user_id]['session']:

                self.user_db[user_id]['session'].remove(session_id)
                self.session_map.pop(session_id)

                if len(self.user_db[user_id]['session']) <= 0:
                    self.user_db.pop(user_id)

                    logging.info(
                        f'USER_ID: {user_id} SESSION_ID {session_id} MESSAGE: Session logout - user destroyed. {datetime.now()}')
                    return 200, 'Session logout - user destroyed.'

                logging.info(
                    f'USER_ID: {user_id} SESSION_ID {session_id} MESSAGE: Session logout - user still online. {datetime.now()}')
                return 200, 'Session logout - user still online.'

            return 300, 'Session do not exist 2.'

        return 300, 'Session do not exist.'

    def increase_value(self, session_id, by):  # TODO: Input validation 1. length, 2. characters, 3. type
        if session_id in self.session_map.keys():
            user_id = self.session_map[session_id]

            if session_id in self.user_db[user_id]['session']:

                if str(by).isnumeric():
                    self.user_db[user_id]['value'] += float(by)

                    logging.info(
                        f'USER_ID: {user_id} SESSION_ID {session_id} VALUE: {self.user_db[user_id]["value"]} MESSAGE: Increase value by: {by}. {datetime.now()}')
                    return 200, f'Set new value {self.user_db[user_id]["value"]}'

                print('Value provided not a number.')
                return 300, 'Value provided not a number.'
            print('Session do not exist 2.')
            return 300, 'Session do not exist 2.'
        print('Session do not exist.')
        return 300, 'Session do not exist.'

    def decrease_value(self, session_id, by):  # TODO: Input validation 1. length, 2. characters, 3. type
        if session_id in self.session_map.keys():
            user_id = self.session_map[session_id]

            if session_id in self.user_db[user_id]['session']:

                if str(by).isnumeric():
                    self.user_db[user_id]['value'] -= float(by)

                    logging.info(
                        f'USER_ID: {user_id} VALUE: {self.user_db[user_id]["value"]} MESSAGE: Decrease value by: {by}. {datetime.now()}')
                    return 200, f'Set new value {self.user_db[user_id]["value"]}'

                print('Value provided not a number.')
                return 300, 'Value provided not a number.'
            print('Session do not exist 2.')
            return 300, 'Session do not exist 2.'
        print('Session do not exist.')
        return 300, 'Session do not exist.'

    def get_server_log(self):
        return self.logfile


if __name__ == '__main__':
    server = ServerSide()

    _, _, auth_1 = server.register_user(1, 'pass1')
    _, _, auth_2 = server.register_user(1, 'pass2')
    _, _, auth_3 = server.register_user(1, 'pass1')

    server.increase_value(auth_1, 56)
    server.decrease_value(auth_3, 96)

    server.logout_user(auth_1)
    server.logout_user(auth_1)
    server.logout_user(auth_3)
    server.logout_user(auth_3)
