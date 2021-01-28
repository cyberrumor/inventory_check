#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

file = __file__.split('/')[-1]
print(f'{file} successfully imported')


def item_is_in_stock(soup):
	inventory = str(soup.find(attrs = {'class': 'add-to-cart-button'}))
	if 'Sold Out</button>' in inventory:
		return False
	else:
		return True

def search(product):
	url = 'https://bestbuy.com'

	params = {
		'st': product,
		'_dyncharset': 'UTF-8',
		'_dynSessConf=': '',
		'id': 'pcat17071',
		'type': 'page',
		'sc': 'Global',
		'cp': 1,
		'nrp': '',
		'sp': '',
		'qp': '',
		'list': 'n',
		'af': 'true',
		'iht': 'y',
		'usc': 'All Categories',
		'ks': 960,
		'keys': 'keys'
	}
	header = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
		'origin': 'https://www.bestbuy.com',
		}

	r = requests.get(url + '/site/searchpage.jsp', headers = header, params = params)
	soup = BeautifulSoup(r.text, 'lxml')


	result = []
	items_list = soup.find('ol', attrs = {'class': 'sku-item-list'})
	for item in items_list.find_all('li', attrs = {'class': 'sku-item'}):
		valid = True
		header = item.find('h4', attrs = {'class': 'sku-header'})
		link_block = header.find('a')
		title = link_block.text
		link = link_block.get('href')
		for i in product.split():
			if i.lower() not in link.lower():
				valid = False
				break
		if not valid:
			continue
		if url not in link:
			href = url + link
		else:
			href = link

		price_block = item.find('div', attrs = {'class': 'price-block'})
		if price_block == None:
			price = '0.00'
		else:
			price_container = price_block.find('div', attrs = {'class': 'priceView-hero-price priceView-customer-price'})
			if price_container == None:
				price = '0.00'
			else:
				price = price_container.find('span', attrs = {'aria-hidden': 'true'}).text.strip('$')



		result.append({'site': 'bestbuy', 'url': href, 'price': price, 'title': title})

	return result
