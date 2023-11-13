import datetime
import logging
import time
import uuid
from datetime import datetime


class ServerSide:

    def __init__(self, logfile=None):
        self.user_db = {}
        self.session_map = {}

        if logfile is None:
            logfile = 'server-log-' + str(round(time.time())) + '.log'

        self.logfile = logfile

        logging.basicConfig(filename='log/' + logfile, encoding='utf-8', level=logging.DEBUG)
        logging.info(f'Server setup time: {datetime.now()}')

    def register_user(self, new_id, new_pass):
        new_id = str(new_id)
        new_pass = str(new_pass)

        if new_id in self.user_db.keys():

            if self.user_db[new_id]['password'] == new_pass:
                new_session_id = str(uuid.uuid4())
                self.session_map[new_session_id] = new_id
                self.user_db[new_id]['session'].append(new_session_id)

                logging.info(
                    f'USER_ID: {new_id} SESSION_ID {new_session_id} VALUE: {self.user_db[new_id]["value"]} MESSAGE: New session created. {datetime.now()}')
                return 200, 'New session created.', new_session_id

            return 300, 'Incorrect password', None

        new_session_id = str(uuid.uuid4())
        self.session_map[new_session_id] = new_id
        self.user_db[new_id] = {'password': new_pass, 'value': 1, 'session': [new_session_id]}

        logging.info(
            f'USER_ID: {new_id} SESSION_ID {new_session_id} VALUE: {self.user_db[new_id]["value"]} MESSAGE: New user registered. {datetime.now()}')
        return 200, 'New user registered.', new_session_id

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

    def increase_value(self, session_id, by):
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

    def decrease_value(self, session_id, by):
        if session_id in self.session_map.keys():
            user_id = self.session_map[session_id]

            if session_id in self.user_db[user_id]['session']:

                if str(by).isnumeric():
                    self.user_db[user_id]['value'] -= float(by)

                    logging.info(
                        f'USER_ID: {user_id} SESSION_ID {session_id} VALUE: {self.user_db[user_id]["value"]} MESSAGE: Decrease value by: {by}. {datetime.now()}')
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
    print(server.get_server_data())

    _, _, auth_1 = server.register_user(1, 'pass1')
    _, _, auth_2 = server.register_user(1, 'pass2')
    _, _, auth_3 = server.register_user(1, 'pass1')

    server.increase_value(auth_1, 56)
    server.decrease_value(auth_3, 96)

    server.logout_user(auth_1)
    server.logout_user(auth_1)
    server.logout_user(auth_3)
    server.logout_user(auth_3)
