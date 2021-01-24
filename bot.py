#!/usr/bin/env python3
import requests
import time
from products import *
from credentials import *
from bs4 import BeautifulSoup

def notify(product_name, url):
    header = {'Content-type': 'application/x-www-form-urlencoded'}
    payload = {'token': api_token, 'user': user_key, 'message': product_name, 'url': url}
    response = requests.post('https://api.pushover.net/1/messages.json', headers = header, data = payload)
    return


# returns true or false. Did we get the name we expected?
def get_seller_name(soup, seller_name, selector, seller_id):
    seller = soup.find('a', attrs = {selector: seller_id}).string
    if seller == seller_name:
        return True
    else:
        return False

# returns price if price. Returns false if any error at all.
def get_price(soup, product):
    price = soup.find(attrs = product['price_selector'])
    if product['price_nested']:
        result = price[product['price_key']]
    else:
        result = price.string
    return result

# returns true if in stock, false otherwise.
def get_stock(soup, product):
    inventory = str(soup.find(attrs = {product['oos_selector']: product['oos_id']}))
    # print(inventory)
    if product['oos_keyword'] in inventory:
        return False
    else:
        return True

def check_stock(product, header):
    print(f'{product["site"]} \t {product["model"]} \t CHECKING')
    response = requests.get(product['url'], headers = header)
    soup = BeautifulSoup(response.text, 'lxml')

    if 'seller' in list(product.keys()):
        safe = get_seller_name(soup, product['seller'], product['seller_selector'], product['seller_id'])
    else:
        safe = True

    if safe:
        # check if in stock
        in_stock = get_stock(soup, product)
        if in_stock:
            # notify
            price = get_price(soup, product)
            print(f'{product["model"]} {product["url"]} {price}')

if __name__ == '__main__':
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    wait = 11
    while True:
        for product in hardware:
            check_stock(product, header)
        time.sleep(wait)
