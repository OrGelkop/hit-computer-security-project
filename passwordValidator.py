import configparser
import requests
from string import punctuation

config = configparser.RawConfigParser()
configFilePath = './config.ini'
config.read(configFilePath)

min_length = int(config.get('main', 'min_length'))
max_length = 16  # hard coded since database column for password is varchar(16)
require_digits = eval(config.get('main', 'require_digits'))
require_uppercase = eval(config.get('main', 'require_uppercase'))
require_lowercase = eval(config.get('main', 'require_lowercase'))
require_symbols = eval(config.get('main', 'require_symbols'))
passwords_history = int(config.get('main', 'passwords_history'))
common_passwords_link = config.get('main', 'common_passwords_link')


def check_common_passwords(password):
    resp = requests.get(common_passwords_link)
    common_passwords_list = resp.text.split('\n')

    for common_password in common_passwords_list:
        if password == common_password:
            return False

    return True


def validate_password(password):
    result = True
    info = ""

    if len(password) < min_length:
        info = info + 'Password length should be at least {}\n'.format(min_length)
        result = False

    if len(password) > max_length:
        info = info + 'Password length should be not be greater than {}\n'.format(max_length)
        result = False

    if require_digits and not any(char.isdigit() for char in password):
        info = info + 'Password should have at least one numeric character\n'
        result = False

    if require_uppercase and not any(char.isupper() for char in password):
        info = info + 'Password should have at least one uppercase letter\n'
        result = False

    if require_lowercase and not any(char.islower() for char in password):
        info = info + 'Password should have at least one lowercase letter\n'
        result = False

    if require_symbols and not any(char in punctuation for char in password):
        print("checking for symbols")
        info = info + 'Password should have at least one special character\n'
        result = False

    if not check_common_passwords(password):
        info = info + 'Please do not use common passwords, like 12345678...\n'
        result = False

    return {
        'status': result,
        'info': info.split('\n')
    }
