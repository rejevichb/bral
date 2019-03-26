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
        self.sock = None
        self.cookie = None
        self.seen = set()
        self.fringe = set()
        self.curr_page = None
        self.csrf = None
        self.session = None


    # need to have a socket for each one So make this service each request
    def request(self, msg):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("fring.ccs.neu.edu", 80))
        self.sock.send(msg.encode("utf-8"))
        return self.sock.recv(4096).rstrip().decode()


    def send_fb_get(self, page):
        if self.cookie is None:

            self.request("GET /{}/ HTTP/1.1\nHost: fring.ccs.neu.edu\r\n".format(page))
            #self.sock.send("GET /{}/ HTTP/1.1\nHost: fring.ccs.neu.edu\r\n".format(page).encode())
            self.curr_page = self.sock.recv(4096).decode("utf-8")
            self.get_cookie()
            #print("Curr Page: {}".format(self.curr_page))
        else:
            msg = str("GET /{}/ HTTP/1.1\r\n" +
                           "Host: fring.ccs.neu.edu\r\n" +
                           "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0\r\n" +
                           "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n" +
                           "Connection: keep-alive\r\n" +
                           "Cookie: {}\r\n\r\n").format(page, self.cookie)

            newmsg = str("GET /{}/ HTTP/1.1\r\n" +
                        "Host: fring.ccs.neu.edu\r\n" +
                        "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0\r\n" +
                        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n" +
                        "Accept-Language: en-US,en;q=0.5\r\n" +
                        "Accept-Encoding: gzip, deflate\r\n" +
                        "Referer: http://fring.ccs.neu.edu/accounts/login/?next=/fakebook/\r\n" +
                        "Upgrade-Insecure-Requests: 1\r\n" +
                        "Connection: keep-alive\r\n" +
                        "Cookie: {}\r\n\r\n").format(page, self.cookie)
            print(msg)
            self.sock.send(msg.encode())
            acc = ""
            for i in range(5):
                acc += self.sock.recv(4096).decode()

            #print(acc)

        return self.curr_page


    def get_links_to_visit(self):
        parsed = bs4.BeautifulSoup(self.curr_page, "html.parser")
        for link in parsed.find_all("a"):
            print("LINKS: " + str(link))
            if link not in self.seen:
                self.fringe.add(link['href'])
        print("FRINGE : {}".format(self.fringe))

    def login(self, username, pw):
        request = str("POST /accounts/login/ HTTP/1.1\n" +
                             "Host: fring.ccs.neu.edu\n" +
                             "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0\n" +
                             "Content-Length: 109\n" +
                             "Connection: Keep-Alive\n" +
                             "Cookie: " + self.cookie + "\n" +
                             "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\n" +
                             "Content-Type: application/x-www-form-urlencoded\n\n" +
                             "username={}&password={}&csrfmiddlewaretoken={}&next=%2Ffakebook%2F\r\n".format(USERNAME, PW, self.csrf))

        self.sock.send(request.encode())
        acc = ""
        for i in range(5):
            acc += str(self.sock.recv(1024).decode())

        self.get_cookie()
        self.curr_page = acc
        self.get_new_session()
        return acc

    def get_cookie(self):
        res = self.curr_page
        csrf = res[res.find("csrftoken="):]
        csrf = csrf[:csrf.find(";")]
        session = res[res.find("sessionid="):]
        session = session[:session.find(";")]
        self.cookie = "{}; {}".format(csrf, session)
        csrf = csrf[csrf.find("=") + 1:]
        self.csrf = csrf
        self.session = session[session.find("=") + 1:]

    def get_new_session(self):
        res = self.curr_page
        session = res[res.find("sessionid="):]
        session = session[:session.find(";")]
        self.cookie = "csrftoken={}; {}".format(self.csrf, session)


def main():
    #intiate crawler
    crawl = Crawler()
    #Get the page and intial cookie
    crawl.send_fb_get("accounts/login/?next=/fakebook")

    #login to the page given the user and pw and using initial cookie
    print("COOKIE: " + crawl.cookie)
    print(crawl.login(USERNAME, PW))
    print("COOKIE AFTER LOGIN: " + crawl.cookie)

    print("GETTTTTTTT" + crawl.send_fb_get("fakebook"))
    #crawl.get_links_to_visit()





    ########
    #subsequent GETS with new cookie from login


#    crawl.get_cookie(login)






    #crawl.send_fb_get("")
    #print("Response: {}".format(crawl.send_fb_get("fakebook")))
    # crawl.get_links_to_visit()
    # print("Current fringe: {}".format(crawl.fringe))
    #
    # counter = 0
    # while counter < 5:
    #     fringe_now = crawl.fringe.copy()  # get_links_to_visit adds to fringe
    #                                       # we cannot add to a set while iterating over it.
    #     for link in fringe_now:
    #         crawl.send_fb_get(link)
    #         crawl.get_links_to_visit()
    #         crawl.seen.add(link)
    #
    #         #counter+= 1
    # print("Current fringe: {}".format(crawl.fringe))


main()



