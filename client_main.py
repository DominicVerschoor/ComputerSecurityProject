import json
from password_strength import PasswordPolicy
from time import sleep

import bcrypt
import requests

policy = PasswordPolicy.from_names(
    length=10,
    uppercase=1,
    special=1,
    nonletters=1,
    entropybits=30
)


def start_client(client_data, client_salt):
    # Get server url
    url = client_data['server']['ip'] + ':' + client_data['server']['port']
    body = {}

    # Test connection
    resp_test = requests.get(url, json=body, verify=False)
    print(resp_test.text)

    # Register user
    if validate_password_input(client_data['password']):
        local_hashed_password = bcrypt.hashpw(client_data['password'].encode('utf-8'), client_salt)
        data = {'user_id': client_data['id'], 'password': str(local_hashed_password)}
        resp_register = requests.post(url + '/register', json=data, verify=False).json()
        print(resp_register)

    else:
        return None

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


def validate_password_input(unvalidate_input, max_length=50, min_length=10):
    # Type validation
    if type(unvalidate_input) is not str:
        return False

    # Length validation
    if (len(unvalidate_input) > max_length) & (len(unvalidate_input) <= min_length):
        return False

    # Character validation
    if not str(unvalidate_input).isascii():
        return False

    if str(unvalidate_input).isalnum():
        return False

    if len(policy.test(str(unvalidate_input))) > 0:
        return False

    return True


if __name__ == '__main__':
    with open('clients/client1.json') as client_file:
        cdata = json.load(client_file)

    password_salt = bcrypt.gensalt()
    start_client(cdata, password_salt)
