#usr/bin/python3

import socket
import sys


def connect_to_socket(hostname, port):
    sock = socket.socket(family=socket.AF_INET)
    sock.connect((hostname, port))
    return sock


def send_hello_msg(nu_id, sock):
    hello_msg = f'cs3700spring2019 HELLO {nu_id}\n'
    sock.send(hello_msg.encode())


def send_count_msg(sock, ascii_sym, string_to_count):
    count_msg = f"cs3700spring2019 COUNT {string_to_count.count(ascii_sym)}\n"
    sock.send(count_msg.encode())


def recv_until_nl(sock):
    data = sock.recv(8192).decode('utf-8')

    while data[-1] != "\n":
        data += sock.recv(8192).decode('utf-8')

    return data


def main(port=27993, ssl=None, hostname="cbw.sh", nu_id="001655997"):
    if ssl is not None:
        pass

    else:
        sock = connect_to_socket(hostname, port)
        send_hello_msg(nu_id, sock)

        while True:
            split_data = recv_until_nl(sock).split()
            if split_data[1] == "BYE":
                print(split_data[2])
                break
            else:
                send_count_msg(sock, split_data[2], split_data[3])


if len(sys.argv) == 3:
    main(27993, None, sys.argv[1], sys.argv[2])

elif len(sys.argv) == 4:
    main(port=sys.argv[1], ssl=None, hostname=sys.argv[2], nu_id=sys.argv[3])
