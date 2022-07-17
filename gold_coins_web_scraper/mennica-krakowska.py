import requests
import re
from bs4 import BeautifulSoup
import logging


urls_dict = {"Canadian Maple Leaf": "https://www.mennica.com.pl/produkty-inwestycyjne/produkt-inwestycyjny/lisc-klonowy-1oz-zlota-moneta-bulionowa-maple-leaf",
"Krugerrands":"https://www.mennica.com.pl/produkty-inwestycyjne/produkt-inwestycyjny/krugerrand-1-oz-zlota-moneta-bulionowa",
"Vienna Philharmonic": "https://www.mennica.com.pl/produkty-inwestycyjne/produkt-inwestycyjny/filharmonicy-wiedenscy-1oz-zlota-moneta-bulionowa",
"Australian Kangaroo": "https://www.mennica.com.pl/produkty-inwestycyjne/produkt-inwestycyjny/australijski-kangur-1oz-zlota-moneta-bulionowa"}

logging.basicConfig(level=logging.ERROR)


class GoldMarketNo2:
    """https://www.mennica.com.pl/"""
    def __init__(self, urls_dict) -> None:
        self.urls_dict = urls_dict

    def get_coin_prices(self):
        for coin in self.urls_dict:
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
                    #print(coin, price)
                    yield {coin: price}

                except Exception as e:
                    logging.critical(e, exc_info=True)
            else:
                logging.critical(f"Error while downloading coin price {r.status_code} - {url}", exc_info=True)

gmn2 = GoldMarketNo2(urls_dict)
data = gmn2.get_coin_prices()

print([x for x in data])

