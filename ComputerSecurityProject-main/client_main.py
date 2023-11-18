import json
from time import sleep
import requests
import secrets
from server_main import ServerSide 

def start_client(client_data):
    server_url = f"{client_data['server']['ip']}:{client_data['server']['port']}"
    body = {}

    # Test connection
    resp_test = requests.get(server_url, json=body)
    print(resp_test.text)

    # Register user and get the session ID
    data = {'user_id': client_data['id'], 'password': client_data['password']}
    resp_register = requests.post(f"{server_url}/register", json=data).json()

    # Check if registration was successful
    if 'session_id' not in resp_register:
        print("Registration failed.")
        return

    session_id = resp_register['session_id']

    # Execute actions with delay
    action_delay = int(client_data['actions']['delay'])
    for action in client_data['actions']['steps']:
        print(action)
        [change, val] = action.split(':')
        if change == 'increase':
            data = {'session_id': session_id, 'by': val}
            resp_increase = requests.post(f"{server_url}/increase", json=data).json()
            print(resp_increase)
        elif change == 'decrease':
            data = {'session_id': session_id, 'by': val}
            resp_decrease = requests.post(f"{server_url}/decrease", json=data).json()
            print(resp_decrease)
        else:
            print('Action not recognized, check client json file.')

        sleep(action_delay)

    # Logout user
    data = {'session_id': session_id}
    resp_logout = requests.post(f"{server_url}/logout", json=data).json()
    print(resp_logout)

    # Check log file
    resp_check = requests.get(f"{server_url}/check").json()
    print(f'Complete log file: {resp_check["log"]}')

if __name__ == '__main__':
    with open('clients/client1.json') as client_file:
        cdata = json.load(client_file)

    print(cdata)
    start_client(cdata)