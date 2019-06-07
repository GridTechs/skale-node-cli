import pickle
import yaml
from functools import wraps
import urllib.parse

from readsettings import ReadSettings
from cli.config import CONFIG_FILEPATH, TEXT_FILE, SKALE_NODE_UI_LOCALHOST, SKALE_NODE_UI_PORT

config = ReadSettings(CONFIG_FILEPATH)


def safe_get_config(config, key):
    try:
        return config[key]
    except KeyError as e:
        #print(f'No such key in config: {key}')
        return None


def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        cookies_text = safe_get_config(config, 'cookies')
        if not cookies_text:
            TEXTS = safe_load_texts()
            print(TEXTS['service']['unauthorized'])
        else:
            return f(*args, **kwargs)

    return inner


def safe_load_texts():
    with open(TEXT_FILE, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def get_node_creds(config):
    TEXTS = safe_load_texts()
    host = safe_get_config(config, 'host')
    if not host:
        host = get_localhost_endpoint()
    cookies_text = safe_get_config(config, 'cookies')
    if not host or not cookies_text:
        raise Exception(TEXTS['service']['no_node_host'])
    cookies = pickle.loads(cookies_text)
    return host, cookies


def construct_url(host, url):
    return urllib.parse.urljoin(host, url)


def get_response_data(response):
    json = response.json()
    return json['data']


def clean_cookies(config):
    if safe_get_config(config, 'cookies'):
        del config["cookies"]


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


def server_only(f):
    @wraps(f)
    def inner(*args, **kwargs):
        # todo: implement check that local node exists
        return f(*args, **kwargs)
    return inner


def get_localhost_endpoint():
    return f'{SKALE_NODE_UI_LOCALHOST}:{SKALE_NODE_UI_PORT}'