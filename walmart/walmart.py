#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import time

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
	url = 'https://www.walmart.com'

	params = {
		'cat_id': 0,
		'facet': 'retailer:Walmart.com',
		'query': product,
	}



    #Cookie: com.wm.reflector="reflectorid:0@lastupd:0@firstcreate:0"; next-day=0; location-data=0



	header = {
        'Host': 'www.walmart.com',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate, br',
		'Referer': 'https://www.walmart.com/',
		'DNT': '1',
		'Connection': 'keep-alive',
        'Cookie': 'com.wm.reflector="reflectorid:0@lastupd:0@firstcreate:0"; next-day=0; location-data=0',
        'TE': 'Trailers',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
	}

	s = requests.Session()
	r = s.get(url)
	time.sleep(4)
	r = s.get(url + '/search/', headers = header, params = params)
	r.raise_for_status()

	if 'blocked' in r.url:
		print('walmart hit us with a captcha. Bailing.')
		return []

	if 'Sorry, no products matched' in r.text:
		return []

	soup = BeautifulSoup(r.text, 'lxml')

	result = []
	item_list = soup.find(attrs = {'class': 'search-result-listview-items'})
	for div in item_list.children:
		valid = True
		# this is for CPUs
		link_block = div.find('a', attrs = {'class': 'product-title-link line-clamp line-clamp-2 truncate-title'})
		# for GPUs we need a different search for the link.
		if link_block != None:
			link = link_block.get('href')
		else:
			continue
		if url in link:
			href = link
		else:
			href = url + link
		for i in product.split(' '):
			if i.lower() not in href.lower():
				valid = False
				break
		if not valid:
			continue

		price_block = div.find('span', attrs = {'class': 'price display-inline-block arrange-fit price price-main'})
		if price_block == None:
			price = '0.00'
		else:
			price_semi = price_block.find('span', attrs = {'class': 'visuallyhidden'})
			if price_semi == None:
				price = '0.00'
			else:
				price = price_semi.string.strip('$')
		title = link_block.find('span').text
		result.append({'site': 'walmart', 'url': href, 'price': price, 'title': title})

	return result
