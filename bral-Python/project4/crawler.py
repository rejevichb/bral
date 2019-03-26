#!/usr/bin/env python

import socket
import bs4
import time


#FUTURE_USERNAME = sys.argv[1]
#FUTURE_PW = sys.argv[2]

USERNAME = "001655997"
PW = "ONO8WGDJ"


class Crawler:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cookie = None
        self.seen = set()
        self.fringe = set()
        self.curr_page = None
        self.csrf = None
        self.session = None

        self.sock.connect(("fring.ccs.neu.edu", 80))

    def send_fb_get(self, page):
        if self.cookie is None:
            self.sock.send("GET /{}/ HTTP/1.1\r\nHost: fring.ccs.neu.edu\r\n\r\n".format(page).encode())
            self.curr_page = self.sock.recv(4096).decode("utf-8")
            self.get_cookie(self.curr_page)

        else:
            self.sock.send(str("GET /fakebook/{}/ HTTP/1.1\r\n" +
                           "Host: fring.ccs.neu.edu\r\n"
                           "Connection: keep-alive\r\n"
                           "Cookie: {}\r\n\r\n".format(page, self.cookie)).encode())
            self.curr_page = self.sock.recv(4096).decode("utf-8")

        return self.curr_page

    def get_links_to_visit(self):
        parsed = bs4.BeautifulSoup(self.curr_page)

        for link in parsed.find_all("a"):
            if link not in self.seen:
                self.fringe.add(link)


    def login(self, username, pw):
        jamesonRequest = str("POST /accounts/login/ HTTP/1.1\r\n" +
                             "Host: fring.ccs.neu.edu\r\n" +
                             "Content-Length: 92\r\n" +
                             "Connection: Keep-Alive\r\n" +
                             "Cookie: " + self.cookie + "\r\n" +
                             "Content-Type: text/html; charset=utf-8\r\n\r\n" +
                             "username={}&password={}&csrfmiddlewaretoken={}&next=%2Ffakebook%2F\r\n".format(USERNAME, PW, self.csrf))

        self.sock.send(jamesonRequest.encode())
        acc = ""
        print(self.session)
        for i in range(5):
            print(self.sock.recv(1024))
            acc += str(self.sock.recv(1024).decode())
        return acc

    def get_cookie(self, res):
        csrf = res[res.find("csrftoken="):]
        csrf = csrf[:csrf.find(";")]
        session = res[res.find("sessionid="):]
        session = session[:session.find(";")]
        self.cookie = "{}; {}".format(csrf, session)
        csrf = csrf[csrf.find("=") + 1:]
        self.csrf = csrf
        self.session = session[session.find("=") + 1:]



def main():
    crawl = Crawler()
    crawl.send_fb_get("accounts/login/?next=/fakebook")
    login = crawl.login(USERNAME, PW)
    crawl.get_cookie(login)
    #print("Response: {}".format(crawl.send_fb_get("fakebook")))
    crawl.get_links_to_visit()
    print("Current fringe: {}".format(crawl.fringe))

    counter = 0
    while counter > 5:
        for link in crawl.fringe:
            crawl.send_fb_get(link)
            crawl.get_links_to_visit()
            crawl.seen.add(link)

            counter+= 1
    print("Current fringe: {}".format(crawl.fringe))





main()



