from bs4 import BeautifulSoup
import requests
import re
import sys
import os


def check_game_request(url):
    s = requests.session()
    page = s.get(url)
    page_html = BeautifulSoup(page.text, 'html.parser')
    try:
        price_full_tag = page_html.find("h3", class_="price-display__price").text
        price = re.sub('[^0-9\.]', '', str(price_full_tag))
        currency = price_full_tag.replace(price, '').strip()
        print("price - {}, currency - {}".format(price, currency))
        if '$' in currency:
            currency = 'USD'
        if price and currency:
            print("Given URL found valid, will insert details to DB")
            return currency
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
        print("Given URL not valid, ignoring")
        return ""
