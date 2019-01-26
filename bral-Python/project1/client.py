#!/usr/bin/python3

import argparse
import socket
import sys


def connect_to_socket(hostname, port):
    """Connect to socket at given hostname and port then return socket
        :param hostname to connect to
        :param port to connect to
        :returns connected socket object
        :except """

    try:
        sock = socket.socket(family=socket.AF_INET)
        sock.settimeout(10)
        sock.connect((hostname, port))
        return sock

    except socket.error:
        raise ConnectionError("Unable to connect to socket at host {}, port {}".format(hostname, port))


def send_hello_msg(nu_id, sock):
    """Sends initial HELLO message to server
            :param nu_id to insert into message
            :param sock used to send message
            :returns None
            """

    hello_msg = "cs3700spring2019 HELLO {}\n".format(nu_id)
    sock.send(hello_msg.encode())


def send_count_msg(sock, ascii_sym, string_to_count):
    """Send COUNT msg to server
            :param sock used to send message
            :param ascii_sym character to count
            :param string_to_count chunk of text to search for ascii sym
            :returns None
            """

    count_msg = "cs3700spring2019 COUNT {}\n".format(string_to_count.count(ascii_sym))
    sock.send(count_msg.encode())


def recv_until_nl(sock):
    data = sock.recv(8192).decode('utf-8')

    while data[-1] != "\n":
        data += sock.recv(8192).decode('utf-8')

    return data


def valid_data(data_to_check):
    if data_to_check[1] == "FIND":
        return all([data_to_check[0] == "cs3700spring2019",
                    len(data_to_check[2]) == 1,
                    len(data_to_check[3]) <= 8192,
                    len(data_to_check[3]) > 0])

    elif data_to_check[1] == "BYE":
        return all([data_to_check[0] == "cs3700spring2019",
                    len(data_to_check[2]) == 64])

    else:
        return False


def main(port=27993, ssl=None, hostname=None, nu_id=None):
    if ssl is not None:
        pass

    else:
        sock = connect_to_socket(hostname, port)

        send_hello_msg(nu_id, sock)

        while True:
            split_data = recv_until_nl(sock).split()

            if valid_data(split_data):

                if split_data[1] == "BYE":
                    print(split_data[2])
                    break

                else:
                    send_count_msg(sock, split_data[2], split_data[3])

            else:
                raise ValueError("Incorrupt/Malformed output")


def main2(namespace):
    if namespace.s is not None:
        pass

    else:
        sock = connect_to_socket(namespace.hostname, namespace.p)

        send_hello_msg(namespace.NUID, sock)

        while True:
            split_data = recv_until_nl(sock).split()

            if valid_data(split_data):

                if split_data[1] == "BYE":
                    print(split_data[2])

                    break

                else:
                    send_count_msg(sock, split_data[2], split_data[3])

            else:
                raise ValueError("Incorrupt/Malformed output")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=27993, type=int, required=False)
    parser.add_argument('-s', default=None, required=False)
    parser.add_argument('hostname')
    parser.add_argument('NUID')

    return parser.parse_args(sys.argv[1:])


arguments = get_args()
main2(arguments)
# arguments = get_args()
# print(arguments)
# main(*arguments)
