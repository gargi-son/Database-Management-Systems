import sys
import cx_Oracle
import os


def connect(username, password):
    if username == '':
        raise ValueError(f'Please fill the username in the credentials file!!')

    if password == '':
        raise ValueError(f'Please fill the password in the credentials file!!')

    try:
        if sys.platform.startswith("darwin"):
            lib_dir = os.path.join(os.environ.get("HOME"), "Downloads","instantclient_10_1")
            cx_Oracle.init_oracle_client(lib_dir=lib_dir)

    except Exception as err:
        print("Whoops!")
        print(err)

    login = f'{username}/{password}@artemis.vsnet.gmu.edu:1521/vse18c.vsnet.gmu.edu'

    print('Connecting...')
    conn = cx_Oracle.connect(login)
    print('Connection complete\n')

    return conn

