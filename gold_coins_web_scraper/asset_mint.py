import requests
import re
from bs4 import BeautifulSoup
import logging


# consider bigger dict of url for each gold coin or scrape whole webside ?
urls_dict = {"Canadian Maple Leaf": "https://mennicakapitalowa.pl/product-pol-153-moneta-zlota-Kanadyjski-Lisc-Klonu-1oz-2022-najtaniej.html",
            "Krugerrands": "https://mennicakapitalowa.pl/product-pol-434-moneta-zlota-Krugerrand-1oz-2022-najtaniej.html",
            "Vienna Philharmonic": "https://mennicakapitalowa.pl/product-pol-148-moneta-zlota-Wiedenski-Filharmonik-1oz-2022-najtaniej.html",
            "Australian Kangaroo": "https://mennicakapitalowa.pl/product-pol-43-moneta-zlota-Australijski-Kangur-2022-1oz.html"}

logging.basicConfig(level=logging.ERROR)


class GoldMarketNo1:
    """https://mennicakapitalowa.pl"""
    def __init__(self, urls_dict) -> None:
        self.urls_dict = urls_dict

    def get_coin_prices(self):
        for coin in self.urls_dict:
            url = self.urls_dict[coin]
            r = requests.get(url)
            if r.status_code == 200:
                try:
                    doc = BeautifulSoup(r.text, "html.parser")
                    raw_price = doc.find_all("strong")[2]
                    raw_price = raw_price.text
                    raw_price = raw_price.replace(" ","").replace(",",".")
                    price = re.findall("\d+\.\d+", raw_price)
                    price = float(price[0])
                    print(coin, price)
                    # do some stuff with data 
                    # sql logging / yield
                    yield {coin: price}

                except Exception as e:
                    logging.critical(e, exc_info=True)
            else:
                logging.critical(f"Error while downloading coin price {r.status_code} - {url}", exc_info=True)

gmn1 = GoldMarketNo1(urls_dict)
data = gmn1.get_coin_prices()

# consider list comprehension to store data ?

print([x for x in data])