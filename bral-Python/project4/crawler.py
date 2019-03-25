#!/usr/bin/env python

import socket

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
        self.to_visit = set()
        self.curr_page = None
        self.csrf = None

        self.sock.connect(("fring.ccs.neu.edu", 80))

    def send_fb_get(self, page):
        self.sock.send("GET /{}/ HTTP/1.1\r\nHost: fring.ccs.neu.edu\r\n\r\n".format(page).encode())
        self.curr_page = self.sock.recv(4096).decode("utf-8")
        self.get_cookie(self.curr_page)
        return self.curr_page

    def login(self, username, pw):
        request = str("POST /accounts/login HTTP/1.1\r\n" +
                       "Host: fring.ccs.neu.edu\r\n" +
                       "Connection: keep-alive\r\n" +
                       "Cache-Control: max-age=0\r\n" +
                       "Content-Type: application/x-www-form-urlencoded\r\n" +
                       "Cookie: " + self.cookie + "\r\n" +
                       "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n" +
                       "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:52.0) Gecko/20100101 Firefox/52.0\r\n" +
                       "Referer: http://fring.ccs.neu.edu/accounts/login/?next=/fakebook/ \r\n" +
                       #="Accept-Encoding: gzip, deflate\r\n" +
                       "username={}&password={}&csrfmiddlewaretoken={}\r\n\r\n".format(USERNAME, PW, self.csrf))





        jamesonRequest = str("POST /accounts/login/ HTTP/1.1\r\n" +
                     "Host: fring.ccs.neu.edu\r\n" +
                     "Content-Length: 92\r\n" +
                     "Connection: Keep-Alive\r\n" +
                     "Cookie: " + self.cookie + "\r\n" +
                     "Content-Type: text/html; charset=utf-8\r\n\r\n" +
                     "username={}&password={}&csrfmiddlewaretoken={}&next=%2Ffakebook%2F\r\n".format(USERNAME, PW, self.csrf))


        print("" + jamesonRequest)
        self.sock.send(jamesonRequest.encode())


        for i in range(5):
            print(self.sock.recv(4096))
            time.sleep(3)

    def get_cookie(self, res):
        csrf = res[res.find("csrftoken="):]
        csrf = csrf[:csrf.find(";")]
        session = res[res.find("sessionid="):]
        session = session[:session.find(";")]
        self.cookie = "{}; {}".format(csrf, session)
        csrf = csrf[csrf.find("=") + 1:]
        self.csrf = csrf




def main():
    crawl = Crawler()
    crawl.send_fb_get("accounts/login/?next=/fakebook")
    print(crawl.login(USERNAME, PW))



main()



