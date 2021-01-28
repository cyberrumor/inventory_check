#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import sys
from newegg import newegg
from walmart import walmart
from bestbuy import bestbuy
import time

def notify(item):
	print(f'IN STOCK: {item["site"]} {item["price"]} {item["url"]}')

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Usage: python3 search.py "rtx 3070"')
		exit()
	else:
		product = sys.argv[-1]

	# we don't care about bundles, sponsored items, laptops, and prebuilt computers. Avoid them here.
	exclusions = ['gaming pc', 'gaming desktop', 'aigo', 'gaming laptop']

	drop_pages = []
	for item in bestbuy.search(product):
		valid = True
		for i in exclusions:
			if i.lower() in item['title'].lower():
				valid = False
				break
		if valid:
			drop_pages.append(item)

	for item in walmart.search(product):
		valid = True
		for i in exclusions:
			if i.lower() in item['title'].lower():
				valid = False
				break
		if valid:
			drop_pages.append(item)

	for item in newegg.search(product):
		valid = True
		for i in exclusions:
			if i.lower() in item['title'].lower():
				valid = False
				break
		if valid:
			drop_pages.append(item)

	if len(drop_pages) == 0:
		print('no retailers were an official seller for this product, or the product can\'t be found.')
		exit()

	while 1:
		for index, item in zip(range(len(drop_pages)), drop_pages):
			if len(item["price"]) < 7:
				if len(item["title"]) < 100:
					print(f'[{index}]:\t{(item["site"])}\t${item["price"]}\t\t{item["title"]}')
				else:
					print(f'[{index}]:\t{(item["site"])}\t${item["price"]}\t\t{item["title"][0:100]}')
			else:
				if len(item["title"]) < 100:
					print(f'[{index}]:\t{(item["site"])}\t${item["price"]}\t{item["title"]}')
				else:
					print(f'[{index}]:\t{(item["site"])}\t${item["price"]}\t{item["title"][0:100]}')

		selection = []
		print('Please only pick one product per site to avoid banning. This system is not yet distributed.')
		user_choice = str(input('select items via index, separating ranges with "-" and singles with spaces: '))
		valid = True
		singles = user_choice.split()
		for i in singles:
			if len(i.split('-')) == 1:
				if int(i) < len(drop_pages):
					selection.append(int(i))
				else:
					valid = False
					break
			else:
				through = i.split('-')
				for n in through:
					if int(n) - 1 < len(drop_pages):
						continue
					else:
						valid = False
				if valid:
					start = int(through[0])
					end = int(through[1])
					selection = selection + [e for e in range(start, end + 1)]
				else:
					break
		if valid:
			break
		else:
			print('please enter a valid selection, or ctrl + c to quit.')
			continue

	desired_items = []
	print(f'selection: {selection}')
	for index in selection:
		desired_items.append(drop_pages[index])


	bestbuy_header = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
		'origin': 'https://www.bestbuy.com',
	}

	newegg_header = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
		# possible captcha bypass?
		# 'referer': 'https://www.newegg.com/amd-ryzen-5-3600/p/N82E16819113569?Item=N82E16819113569&recaptcha=pass',
	}

	walmart_header = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en-US,en;q=0.5',
		'cache-control': 'max-age=0',
		'connection': 'keep-alive',
	}

	wait = 10
	while 1:
		for item in desired_items:

			# print what we're looking for
			if len(item["site"]) < 7:
				if len(item["title"]) < 70:
					print(f'checking {item["site"]}\t\t{item["price"]}\t{item["title"]}.')
				else:
					print(f'checking {item["site"]}\t\t{item["price"]}\t{item["title"][0:69]}.')
			else:
				if len(item["title"]) < 70:
					print(f'checking {item["site"]}\t{item["price"]}\t{item["title"]}.')
				else:
					print(f'checking {item["site"]}\t{item["price"]}\t{item["title"][0:69]}.')


			if item['site'] == 'newegg':
				try:
					r = requests.get(item['url'], headers = newegg_header)
					r.raise_for_status()
				except Exception as e:
					print(f'Newegg raised error: {e}')
					wait += 1
					print(f'raising interval to {wait} seconds.')
					continue

				soup = BeautifulSoup(r.text, 'lxml')
				if newegg.item_is_in_stock(soup):
					notify(item)

			elif item['site'] == 'bestbuy':
				try:
					r = requests.get(item['url'], headers = bestbuy_header)
					r.raise_for_status()
				except Exception as e:
					print(f'bestbuy raised error: {e}')
					wait += 1
					print(f'raising interval to {wait}')
					continue

				soup = BeautifulSoup(r.text, 'lxml')
				if bestbuy.item_is_in_stock(soup):
					notify(item)

			elif item['site'] == 'walmart':
				try:
					r = requests.get(item['url'], headers = walmart_header)
					r.raise_for_status()
				except Exception as e:
					print(f'walmart raised error: {e}')
					wait += 1
					print(f'raising interval to {wait} seconds.')
					continue

				soup = BeautifulSoup(r.text, 'lxml')
				if walmart.item_is_in_stock(soup):
					notify(item)

			else:
				print(f'{item["site"]} is not yet a configured store front. Consider submitting a pull request to add support.')
				exit()

		print(f'waiting {wait} seconds to dodge rate limiting.')
		time.sleep(wait)
		continue

