#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

file = __file__.split('/')[-1]
print(f'{file} successfully imported')

# returns true if in stock, false otherwise.
def item_is_in_stock(soup):
	inventory = str(soup.find(attrs = {'class': 'prod-blitz-copy-message'}))
	if '<b>out of stock</b>' in inventory:
		return False
	else:
		return True

def search(product):
	url = 'https://www.amazon.com'
	params = {
		'k': product,
	}

	header = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en-US,en;q=0.5',
		'cache-control': 'max-age=0',
		'connection': 'keep-alive',
		'host': 'www.amazon.com',
		'TE': 'Trailers',
		'DNT': '1',
		'referer': 'https://www.amazon.com/',
	}

	s = requests.Session()
	r = s.get(url)
	r = s.get(url + '/s/', headers = header, params = params)
	r.raise_for_status()

	soup = BeautifulSoup(r.text, 'lxml')
	result = []
	item_block = soup.find(attrs = {'class': 's-main-slot s-result-list s-search-results sg-row'})
	item_list = soup.find_all(attrs = {'class': 's-result-item'})
	for item in item_list:
		link = item.find('a')
		if link == None:
			continue
		href = link.get('href')
		if 'adsystem' in href or 'picasso' in href:
			continue
		title_tag = item.find('span', attrs = {'class': 'a-size-medium a-color-base a-text-normal'})
		if title_tag == None:
			continue
		title = title_tag.text
		price_block = item.find('span', attrs = {'class': 'a-offscreen'})
		if price_block != None:
			price = price_block.text.strip('$')
		else:
			price = '0.00'

		result.append({'site': 'amazon', 'title': title, 'price': price, 'url': 'http://amazon.com' + href})


	return result
