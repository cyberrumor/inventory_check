#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
import requests
import time
from twilio.rest import Client
import random
import logging
from products import *
from credentials import *

client = Client(first_cred, second_cred)
def notify(url):
	client.messages.create(to = notification_recipient,
				from_ = notification_sender,
				body = url)

if __name__ == '__main__':
	logging.basicConfig(format="%(asctime)s %(levelname)s:%(module)s: %(message)s", level=logging.WARNING)
	s = requests.Session()
	header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:83.0) Gecko/20100101 Firefox/83.0'}
	wait = 6
	while True:
		for product in hardware:
			try:
				logging.warning('checking {} at {}'.format(product['model'], product['site']))
				response = s.get(product['url'], headers = header)
				if product['keyword'] not in response.text:
					notify(product['url'])
					logging.warning('IN STOCK: ' + product['model'] + ' at ' + product['site'])
					logging.warning(product['url'])
					logging.warning('notification sent')
			except Exception as e:
				logging.warning(e)
				wait += 1
				logging.warning('Possible rate limiting. Increasing wait by 1')
				logging.warning('briefly pausing to reset their limiter...')
				time.sleep(10)
		jitter = random.randint(3, 9) + wait
		logging.warning('waiting {} seconds'.format(jitter))
		time.sleep(jitter)
