#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import time

file = __file__.split('/')[-1]
print(f'{file} successfully imported')

def search(product):
	url = 'https://www.newegg.com'

	params = {
		'd': product,
		'N': '8000 4814', # this only shows results with newegg as the seller (8000) in new condition (4814)
	}
	header = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
		# possible captcha bypass?
		# 'referer': 'https://www.newegg.com/amd-ryzen-5-3600/p/N82E16819113569?Item=N82E16819113569&recaptcha=pass',
		}

	r = requests.get(url + '/p/pl', headers = header, params = params)
	if 'areyouahuman' in r.url:
		print(f'newegg redirected us to {r.url}, which has a captcha. Bailing.')
		return []
	soup = BeautifulSoup(r.text, 'lxml')

	result = []
	for item in soup.find_all('div', attrs = {'class': 'item-container'}):
		valid = True
		link = item.find('a')
		href = link.get('href')

		# make sure the product is relevant
		for i in product.split(' '):
			if i.lower() not in href.lower():
				valid = False
				break
		if not valid:
			continue


		# get price data. price_label == None if item on sale.
		price_label = item.find(attrs = {'class': 'price-current'})
		if price_label != None:
			# normal behavior, no sales
			dollar = price_label.find('strong')
			cent = price_label.find('sup')
			if cent != None and dollar != None:
				price = dollar.string + cent.string
			else:
				price = '0.00'
		else:
			# item is currently on sale. Info is loaded with js.
			price = '0.00'

		# get item title
		item_title = item.find(attrs = {'class': 'item-title'})
		if item_title != None:
			title = item_title.text
		else:
			title = href

		item = {'site': 'newegg', 'url': href, 'price': price, 'title': title}
		result.append(item)

	return result





