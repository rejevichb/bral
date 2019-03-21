import socket
import bs4
import sys



FUTURE_USERNAME = sys.argv[1]
FUTURE_PW = sys.argv[2]



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
        return self.curr_page[8:12]

    def login():




def main():
    crawl = Crawler()
    print(crawl.send_fb_get("accounts/login/?next=/fakebook"))



main()



