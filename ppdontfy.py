#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests, time
from pushover import init, Client


pushover_key = ""
pushover_token = ""
packtpage = "https://www.packtpub.com/packt/offers/free-learning"


def get_book():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'
    }
    page = requests.get(packtpage, headers=headers)
    page_data = page.text
    soup = BeautifulSoup(page_data, "html.parser")
    divs = soup.find("div", {"class":"dotd-title"})
    book = divs.find("h2")
    book = book.text.strip()
    return book

def send_notification(book):
    init(pushover_token)
    alert = "Packt Daily: %s" % book
    Client(pushover_key).send_message(title=alert, url=packtpage, message=book)


while True:
    date = time.strftime("%m/%d/%y")
    book = get_book()
    with open("books.txt", "a") as log:
        log.write("%s - %s\r\n" % (date, book))
    send_notification(book)
    time.sleep(86400)
