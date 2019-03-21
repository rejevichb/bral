import socket
import bs4
import sys
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

        self.sock.connect(("fring.ccs.neu.edu", 80))

    def send_fb_get(self, page):
        self.sock.send("GET /{}/ HTTP/1.1\nHost: fring.ccs.neu.edu\n\n".format(page).encode())
        self.curr_page = self.sock.recv(4096).decode("utf-8")
        self.get_cookie(self.curr_page)
        return self.curr_page#[9:12]

    def login(self, username, pw):
        request = str("POST /accounts/login/ HTTP/1.1\n" +
                       "Host: fring.ccs.neu.edu\n" +
                       "Connection: keep-alive\n" +
                       "Cache-Control: max-age=0\n" +
                       "Content-Type: application/x-www-form-urlencoded\n" +
                       "Cookie: " + self.cookie + "\n" +
                       "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\n" +
                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:52.0) Gecko/20100101 Firefox/52.0\n" +
                       "Accept-Encoding: gzip, deflate\n" +
                       "username={}&password={}\n\n".format(USERNAME, PW))
        self.sock.send(request.encode())


        for i in range(5):
            print(self.sock.recv(4096))
            time.sleep(3)

    def get_cookie(self, res):
        csrf = res[res.find("csrftoken="):]
        csrf = csrf[:csrf.find(";")]
        session = res[res.find("sessionid="):]
        session = session[:session.find(";")]
        self.cookie = "{};{}".format(csrf, session)




def main():
    crawl = Crawler()
    crawl.send_fb_get("accounts/login/?next=/fakebook")
    print(crawl.login(USERNAME, PW))



main()



