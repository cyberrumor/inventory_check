#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import sys
from newegg import newegg
from walmart import walmart
from bestbuy import bestbuy
import json




if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Usage: python3 search.py "rtx 3070"')
		exit()
	else:
		product = sys.argv[-1]


	exclusions = ['gaming pc', 'gaming desktop', 'aigo']



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
		valid = True
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
		user_choice = str(input('select items via index, separating ranges with "-" and singles with spaces: '))
		singles = user_choice.split()
		for i in singles:
			if len(i.split('-')) == 1:
				selection.append(int(i))
			else:
				through = i.split('-')
				start = int(through[0])
				end = int(through[1])
				selection = selection + [e for e in range(start, end + 1)]
		for i in selection:
			if i < len(drop_pages) and i >= 0:
				continue
			else:
				print('Please enter a valid selection, or ctrl + c to quit.')
				valid = False
		if valid:
			break

	desired_items = []
	print(f'selection: {selection}')
	for index in selection:
		desired_items.append(drop_pages[index])




