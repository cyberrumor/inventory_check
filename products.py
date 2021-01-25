hardware = [
	{
	'site': 'bestbuy',
        'url': 'https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161',
        'oos_keyword': 'Sold Out</button>',
        'oos_id': 'add-to-cart-button',
        'oos_selector': 'class',
        'price_selector': {'class': 'priceView-hero-price priceView-customer-price'},
        'price_nested': False,
	'model': 'PS5',
        'additional_headers': {'origin': 'https://www.bestbuy.com'},
        },
	{
	'site': 'walmart',
        'url': 'https://www.walmart.com/ip/Sony-PlayStation-5-Digital-Edition/493824815',
	'oos_keyword': '<b>out of stock</b>',
        'oos_id': 'prod-blitz-copy-message',
        'oos_selector': 'class',
	'model': 'PS5',
        'seller': 'Walmart',
        'seller_id': 'seller-name',
        'seller_selector': 'class',
        'price_selector': {'itemprop': 'price'},
        'price_nested': True,
        'price_key': 'content',
        'additional_headers': {},
        },
        {
        'site': 'newegg',
        'url': 'https://www.newegg.com/p/N82E16868110295?Description=playstation%205%20console&cm_re=playstation_5%20console-_-68-110-295-_-Product',
        'oos_keyword': 'OUT OF STOCK',
        'oos_selector': 'class',
        'oos_id': 'product-inventory',
        'model': 'PS5 Bundle',
        'seller': 'Newegg',
        'seller_selector': 'class',
        'seller_id': 'product-seller',
        'price_nested': False,
        'price_selector': {'class': 'price-current-label'},
        'additional_headers': {},
        },
]
