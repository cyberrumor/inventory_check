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
	header = [
		{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
	]
	wait = 6
	just_notified = False
	while True:
		if just_notified:
			just_notified = False
			logging.warning('waiting 30 seconds after sending notification...')
			time.sleep(30)
		for product in hardware:
			try:
				logging.warning('checking {} at {}'.format(product['model'], product['site']))
				response = requests.get(product['url'], headers = random.choice(header))
				if product['keyword'] not in response.text:
					if product['price'] in response.text:
						notify(product['url'])
						logging.warning('IN STOCK: ' + product['model'] + ' at ' + product['site'])
						logging.warning(product['url'])
						logging.warning('notification sent')
						just_notified = True
					else:
						logging.warning('we are being fed a fake price from ' + product['site'])
			except Exception as e:
				logging.warning(e)
				wait += 1
				logging.warning('Possible rate limiting. Increasing wait by 1')
				logging.warning('briefly pausing to reset their limiter...')
				time.sleep(10)
		jitter = random.randint(3, 9) + wait
		logging.warning('waiting {} seconds'.format(jitter))
		time.sleep(jitter)
