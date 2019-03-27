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
        self.links= {}      # Dict with each link as key and boolean as value denoting seen or not. Allows O(1) lookups
        self.curr_page = None
        self.csrf = None
        self.session = None
        self.referer = None

    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("fring.ccs.neu.edu", 80))

    def initial_get(self):
        self.create_socket()
        self.sock.send("GET /accounts/login/?next=/fakebook/ HTTP/1.1\nHost: fring.ccs.neu.edu\r\n\r\n".encode('utf-8'))
        self.curr_page = self.sock.recv(4096).decode("utf-8")
        self.get_cookie()

    def get(self, page):
        self.create_socket()
        self.referer = page
        msg = str("GET {} HTTP/1.1\n" +
                  "Host: fring.ccs.neu.edu\n" +
                  "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:52.0) Gecko/20100101 Firefox/52.0\n" +
                  "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\n" +
                  "Accept-Language: en-US,en;q=0.5\n" +
                  "Referer: http://fring.ccs.neu.edu{}\n".format(self.referer) +
                  "DNT: 1\n" +
                  "Connection: keep-alive\n" +
                  "Upgrade-Insecure-Requests: 1\n" +
                  "Cookie: {}\r\n\r\n").format(page, self.cookie)

        self.sock.send(msg.encode("utf-8"))
        acc = ""
        for i in range(5):
            acc += self.sock.recv(4096).decode()

        self.curr_page = acc
        return self.curr_page

    def get_links(self):
        parsed = bs4.BeautifulSoup(self.curr_page, "html.parser")
        for link in parsed.find_all("a"):
            if link in self.links:
                continue
            else:
                self.links[link] = False

    def login(self, username, pw):
        self.create_socket()

        request = str("POST /accounts/login/ HTTP/1.1\n" +
                             "Host: fring.ccs.neu.edu\n" +
                             "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0\n" +
                             "Content-Length: 109\n" +
                             "Connection: keep-alive\n" +
                             "Cookie: {}\n".format(self.cookie) +
                             "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\n" +
                             "Referer: http://fring.ccs.neu.edu/accounts/login/?next=/fakebook/\n" +
                             "DNT: 1\n" +
                             "Upgrade-Insecure-Requests: 1\n" +
                             "Content-Type: application/x-www-form-urlencoded\n\n" +
                             "username={}&password={}&csrfmiddlewaretoken={}&next=%2Ffakebook%2\r\n\r\n").format(USERNAME, PW, self.csrf)

        self.sock.send(request.encode("utf-8"))
        acc = "POST REQUEST: \n"
        for i in range(5):
            acc += str(self.sock.recv(1024).decode())

        self.get_cookie()
        self.curr_page = acc
        self.get_new_session()
        return acc

    def get_cookie(self):
        response = self.curr_page

        csrf = response[response.find("csrftoken="):]
        csrf = csrf[:csrf.find(";")]

        session = response[response.find("sessionid="):]
        session = session[:session.find(";")]

        self.cookie = "{}; {}".format(csrf, session)
        self.csrf = csrf[csrf.find("=") + 1:]
        self.session = session[session.find("=") + 1:]

    def get_new_session(self):
        response = self.curr_page

        session = response[response.find("sessionid="):]
        session = session[:session.find(";")]

        self.cookie = "csrftoken={}; {}".format(self.csrf, session)

    def find_flag(self):
        # Convert page to searchable bs4 object and look for h2 heading with class of "secret_flag"
        parsed = bs4.BeautifulSoup(self.curr_page, "html.parser")
        flag_search = parsed.find("h2", {"class" : "secret_flag"})
        print(flag_search)

        # if it is found, print the flag and return True so the main knows to increment counter
        if flag_search is not None:
            print(flag_search[0])
            return True

        return False



def main():
    #intiate crawler
    crawl = Crawler()

    #Get the page and intial cookie
    crawl.initial_get()

    #login to the page given the user and pw and using initial cookie
    crawl.login(USERNAME, PW)
    print("Logged in")
    crawl.get("/fakebook/")

    crawl.get_links()

    #TODO: Must set correct referer when navigating pages or will get 400
    #TODO: Some people will have multiple pages of friends, which are paginated as /PROFILE_ID/friends/PAGE_NUM

    #TODO: Handle 500 errors with retry

    #TODO: Handle non fring.ccs.neu.edu domains with simple skip

    flags_found = 0
    while flags_found < 5:
        # Copy fringe to prevent errors from modifying set during iteration
        fringe = crawl.links.copy()

        for link, hasSeen in fringe.items():
            if not hasSeen:
                print(crawl.get(link))
                return
                if crawl.find_flag():
                    flags_found += 1
                    print("FLAG FOUND!!!!")

                crawl.links[link] = True
                crawl.get_links()





main()



