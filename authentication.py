import logging
import pathlib


key_file = 'key.txt'

logging.basicConfig(level=logging.CRITICAL, format='%(message)s')


def watcher(function):
    def inner_eye(*args, **kwargs):
        try:
            rez = function(*args, **kwargs)

        except Exception as error:
            logging.critical(f'Something wrong!, system error:\n{error}')
            rez = f'{error}'    

        return rez
    
    return inner_eye


@watcher
def save_key(key: str, key_file: str = key_file) -> None:
    with open(key_file, "w") as fh:
        fh.write(key)


@watcher
def load_key(key_file: str = key_file) -> str:
    with open(key_file, "r") as fh:
        return fh.readline()


def get_password(key_file: str = key_file) -> str:
    """Return password from local file or user input in CLI."""
    if pathlib.Path(key_file).exists():
        print(f'Ok! Key-file ({key_file}) found.')
        key = load_key(key_file)

    else:
        print(f'Can`t find {pathlib.Path(key_file)}')
        key: str = input(f'Enter the KEY ({key_file}):\n')
        save_key(key, key_file) if key else None
    
    return key
