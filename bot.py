#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
import json
import requests
import time
from multiprocessing import Process
from products import *
from credentials import *

def notify(product_name, url):
	header = {'Content-type': 'application/x-www-form-urlencoded'}
	payload = {'token': api_token, 'user': user_key, 'message': product_name, 'url': url}
	response = requests.post('https://api.pushover.net/1/messages.json', headers = header, data = payload)
	return response.status

def check_stock(product, header, thread):
	wait = 11
	while 1:
		print('THREAD {}: checking for {} at {}.'.format(thread, product['model'], product['site']))
		try:
			response = requests.get(product['url'], headers = header)
			if product['keyword'] in response.text:
				if product['price'] in response.text:
					notify(product['model'], product['url'])
					print('THREAD {}: IN STOCK: {} at {}'.format(thread, product['model'], product['site']))
					just_notified = True
				else:
					print('THREAD {}: we are being fed a fake price from {}.'.format(thread, product['site']))
		except Exception as e:
			print(e)
			wait += 1
			print('THREAD {}: Possible rate limiting. Increasing wait by 1'.format(thread))
			print('THREAD {}: briefly pausing to reset their limiter...'.format(thread))
			time.sleep(10)
		print('THREAD {}: waiting {} seconds for {}'.format(thread, wait, product['site']))
		time.sleep(wait)

if __name__ == '__main__':
	header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
	thread = 1
	for product in hardware:
		p = Process(target = check_stock, args = (product, header, thread))
		p.start()
		thread += 1
