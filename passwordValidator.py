import configparser
from string import punctuation

config = configparser.RawConfigParser()
configFilePath = './config.ini'
config.read(configFilePath)

min_length = int(config.get('main', 'min_length'))
max_length = 16  # hard coded since database column for password is varchar(16)
passwords_history = int(config.get('main', 'passwords_history'))
knows_passwords_dictionary = config.get('main', 'dictionary')


def validate_password(passwd):
    val = True

    if len(passwd) < min_length:
        print('Password length should be at least {}'.format(min_length))
        val = False

    if len(passwd) > max_length:
        print('Password length should be not be greater than {}'.format(max()))
        val = False

    if not any(char.isdigit() for char in passwd):
        print('Password should have at least one numeric character')
        val = False

    if not any(char.isupper() for char in passwd):
        print('Password should have at least one uppercase letter')
        val = False

    if not any(char.islower() for char in passwd):
        print('Password should have at least one lowercase letter')
        val = False

    if not any(char in punctuation for char in passwd):
        print('Password should have at least one special character')
        val = False

    if passwd in knows_passwords_dictionary:
        print('Common passwords use is not permitted, please try to use another password')
        val = False

    return val

