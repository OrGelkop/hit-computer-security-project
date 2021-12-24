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
    info = ""

    if len(passwd) < min_length:
        info = info + 'Password length should be at least {}\n'.format(min_length)
        val = False

    if len(passwd) > max_length:
        info = info + 'Password length should be not be greater than {}\n'.format(max_)
        val = False

    if not any(char.isdigit() for char in passwd):
        info = info + 'Password should have at least one numeric character\n'
        val = False

    if not any(char.isupper() for char in passwd):
        info = info + 'Password should have at least one uppercase letter\n'
        val = False

    if not any(char.islower() for char in passwd):
        info = info + 'Password should have at least one lowercase letter\n'
        val = False

    if not any(char in punctuation for char in passwd):
        info = info + 'Password should have at least one special character\n'
        val = False

    if passwd in knows_passwords_dictionary:
        info = info + 'Common passwords use is not permitted, please try to use another password\n'
        val = False

    return {
        'status': val,
        'info': info.split('\n')
    }
