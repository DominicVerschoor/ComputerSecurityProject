import json
from time import sleep

import bcrypt
import requests


def start_client(client_data, client_salt):
    # Get server url
    url = client_data['server']['ip'] + ':' + client_data['server']['port']
    body = {}

    # Test connection
    resp_test = requests.get(url, json=body, verify=False)
    print(resp_test.text)

    # Register user
    local_hashed_password = bcrypt.hashpw(client_data['password'].encode('utf-8'), client_salt)
    data = {'user_id': client_data['id'], 'password': str(local_hashed_password)}

    resp_register = requests.post(url + '/register', json=data, verify=False).json()
    print(resp_register)

    # Execute actions with delay
    action_delay = int(client_data['actions']['delay'])
    for action in client_data['actions']['steps']:
        print(action)
        [change, val] = action.split(':')
        if change == 'increase':
            data = {'session_id': resp_register['session_id'], 'by': val}
            resp_increase = requests.post(url + '/increase', json=data, verify=False).json()
            print(resp_increase)
        elif change == 'decrease':
            data = {'session_id': resp_register['session_id'], 'by': val}
            resp_decrease = requests.post(url + '/decrease', json=data, verify=False).json()
            print(resp_decrease)
        else:
            print('Action not recognized, check client json file.')

        sleep(action_delay)

    # Logout user
    data = {'session_id': resp_register['session_id']}
    resp_logout = requests.post(url + '/logout', json=data, verify=False).json()
    print(resp_logout)

    # Check log file
    resp_check = requests.get(url + '/check', verify=False).json()
    print(f'Complete log file: {resp_check["log"]}')


if __name__ == '__main__':
    with open('clients/client1.json') as client_file:
        cdata = json.load(client_file)

    password_salt = bcrypt.gensalt()
    start_client(cdata, password_salt)
