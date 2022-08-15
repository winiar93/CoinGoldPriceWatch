import requests
import re
from bs4 import BeautifulSoup
import logging
import time
from rejson import Client, Path

# for local testing
#rejson_client = Client(host='rejson', port=6379, decode_responses=True)
rejson_client = Client(host='redis-master.default.svc.cluster.local', port=6379, decode_responses=True)

logging.basicConfig(level=logging.ERROR)


class GoldMarketNo1:
    """https://mennicakapitalowa.pl"""
    def __init__(self) -> None:
        self.urls_dict = {"Canadian Maple Leaf": "https://mennicakapitalowa.pl/product-pol-153-moneta-zlota-Kanadyjski-Lisc-Klonu-1oz-2022-najtaniej.html",
            "Krugerrands": "https://mennicakapitalowa.pl/product-pol-434-moneta-zlota-Krugerrand-1oz-2022-najtaniej.html",
            "Vienna Philharmonic": "https://mennicakapitalowa.pl/product-pol-148-moneta-zlota-Wiedenski-Filharmonik-1oz-2022-najtaniej.html",
            "Australian Kangaroo": "https://mennicakapitalowa.pl/product-pol-43-moneta-zlota-Australijski-Kangur-2022-1oz.html"}
        self.output_data = {'Mint':'mennicakapitalowa.pl'}

    def get_coin_prices(self):
        for cnt, coin in enumerate(self.urls_dict):
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
                    tmp_data = {'Coin': f'{coin}', 'Price': f'{price}', "Link": url}
                    self.output_data.update(tmp_data)
                    rejson_client.jsonset(f'mennicakapitalowa:{cnt}', Path.rootPath(), self.output_data)
                    print(coin, price)


                except Exception as e:
                    logging.critical(e, exc_info=True)
            else:
                logging.critical(f"Error while downloading coin price {r.status_code} - {url}", exc_info=True)


class GoldMarketNo2:
    """https://www.mennica.com.pl/"""
    def __init__(self) -> None:
        self.urls_dict = {"Canadian Maple Leaf": "https://www.mennica.com.pl/produkty-inwestycyjne/produkt-inwestycyjny/lisc-klonowy-1oz-zlota-moneta-bulionowa-maple-leaf",
            "Krugerrands":"https://www.mennica.com.pl/produkty-inwestycyjne/produkt-inwestycyjny/krugerrand-1-oz-zlota-moneta-bulionowa",
            "Vienna Philharmonic": "https://www.mennica.com.pl/produkty-inwestycyjne/produkt-inwestycyjny/filharmonicy-wiedenscy-1oz-zlota-moneta-bulionowa",
            "Australian Kangaroo": "https://www.mennica.com.pl/produkty-inwestycyjne/produkt-inwestycyjny/australijski-kangur-1oz-zlota-moneta-bulionowa"}
        self.output_data = {'Mint':'mmennica.com.pl'}
    def get_coin_prices(self):
        for cnt, coin in enumerate(self.urls_dict):
            url = self.urls_dict[coin]
            r = requests.get(url)
            if r.status_code == 200:
                try:
                    doc = BeautifulSoup(r.text, "html.parser")
                    raw_price = doc.find_all("span", {"class": "product_price_value_current"})[0]
                    raw_price = raw_price.text.strip()
                    raw_price = re.sub(r"\s+", "", raw_price)
                    raw_price = raw_price.replace(",",".")
                    price = re.findall("\d+\.\d+", raw_price)
                    price = float(price[0])
                    tmp_data = {'Coin': f'{coin}', 'Price': f'{price}', "Link": url}
                    self.output_data.update(tmp_data)
                    rejson_client.jsonset(f'www.mennica.com.pl:{cnt}', Path.rootPath(), self.output_data)
                    print(coin, price)

                except Exception as e:
                    logging.critical(e, exc_info=True)
            else:
                logging.critical(f"Error while downloading coin price {r.status_code} - {url}", exc_info=True)

gmn2 = GoldMarketNo2()
gmn1 = GoldMarketNo1()

while True:
    gmn1.get_coin_prices()
    gmn2.get_coin_prices()
    time.sleep(30)
