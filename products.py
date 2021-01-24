hardware = [
	{
	'site': 'bestbuy',
        'url': 'https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161',
        'oos_keyword': 'Sold Out</button>',
        'oos_id': 'add-to-cart-button',
        'oos_selector': 'class',
        'price_selector': {'class': 'priceView-hero-price priceView-customer-price'},
        'price_nested': False,
	'model': 'PS5'
	},
	{
	'site': 'walmart',
        'url': 'https://www.walmart.com/ip/Sony-PlayStation-5-Digital-Edition/493824815',
	'oos_keyword': '<b>out of stock</b>',
        'oos_id': 'prod-blitz-copy-message',
        'oos_selector': 'class',
	'model': 'PS5',
        'seller': 'Walmart',
        #'seller_id': 'ProductSellerInfo-SellerName',
        #'selector': 'id',
        'seller_id': 'seller-name',
        'seller_selector': 'class',
        'price_selector': {'itemprop': 'price'},
        'price_nested': True,
        'price_key': 'content',
        }
]
