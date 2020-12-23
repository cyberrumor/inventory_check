#!/usr/bin/env python3
import requests
import time
from multiprocessing import Process
from products import *
from credentials import *

def notify(product_name, url):
	header = {'Content-type': 'application/x-www-form-urlencoded'}
	payload = {'token': api_token, 'user': user_key, 'message': product_name, 'url': url}
	response = requests.post('https://api.pushover.net/1/messages.json', headers = header, data = payload)
	return

def check_stock(product, header, thread):
	wait = 11
	while 1:
		print(f'THREAD {thread}: {product["site"]} \t {product["model"]} \t CHECKING')
		try:
			response = requests.get(product['url'], headers = header)
			if product['keyword'] not in response.text:
				if product['price'] in response.text:
					notify(product['model'], product['url'])
					print(f'THREAD {thread}: {product["site"]} \t {product["model"]} \t IN STOCK')
					just_notified = True
				else:
					print(f'THREAD {thread}: {product["site"]} \t {product["model"]} \t FAKE PRICE')
		except Exception as e:
			print(e)
			wait += 1
			print(f'THREAD {thread}: {product["site"]} \t {product["model"]} \t RATE LIMITED WAITING 10')
			time.sleep(10)
		print(f'THREAD {thread}: {product["site"]} \t {product["model"]} \t WAITING {wait}')
		time.sleep(wait)

if __name__ == '__main__':
	header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
	thread = 1
	for product in hardware:
		p = Process(target = check_stock, args = (product, header, thread))
		p.start()
		thread += 1
