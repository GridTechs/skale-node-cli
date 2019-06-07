import requests
import pickle
import json
from cli.config import URLS, TOKENS_FILEPATH
from cli.helper import safe_get_config, construct_url, clean_cookies, get_localhost_endpoint


def register_user(config, username, password, token):
    host = safe_get_config(config, 'host')
    if not host:
        host = get_localhost_endpoint()
    data = {
        'username': username,
        'password': password,
        'token': token
    }
    url = construct_url(host, URLS['register'])
    response = requests.post(url, json=data)

    if response.status_code == requests.codes.ok:
        cookies_text = pickle.dumps(response.cookies)
        config['cookies'] = cookies_text
        print(f'User created: {username}')
        print('Success, cookies saved.')
    else:
        print('Registration failed: ' + response.text)

def login_user(config, username, password):
    host = safe_get_config(config, 'host')
    if not host:
        return

    data = {
        'username': username,
        'password': password
    }
    url = construct_url(host, URLS['login'])
    response = requests.post(url, json=data)

    if response.status_code == requests.codes.ok:
        cookies_text = pickle.dumps(response.cookies)
        config['cookies'] = cookies_text
        print('Success, cookies saved.')
    else:
        print('Authorization failed: ' + response.text)


def logout_user(config):
    host = safe_get_config(config, 'host')
    url = construct_url(host, URLS['logout'])
    response = requests.get(url)

    if response.status_code == requests.codes.ok:
        clean_cookies(config)
        print('Cookies removed')
    else:
        print('Logout failed')
        print(response.text)


def show_registration_token():
    try:
        with open(TOKENS_FILEPATH, encoding='utf-8') as data_file:
            config = json.loads(data_file.read())
        print(f'User registration token: {config["token"]}')
    except FileNotFoundError as e:
        print("Couldn't find registration tokens file. Check that node inited on this machine.")
