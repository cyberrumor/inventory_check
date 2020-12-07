# inventory_check

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/cyberrumor)

Checks inventory of configurable products with automatic rate limiting. Threaded. Notifies via Pushover.


Please be polite and don't spam retailers with excessive requests. Don't use this for reselling.

# Installation

Get your device set up with [Pushover](pushover.net) and create an application on their website. Copy your user ID and your application's API token into credentials.py. Configure products.py with your desired items and run via python3 bot.py. In the Pushover app, tell it to automatically open URLs when launched via notification. Set the URL handler to 'opener' if you want to use the retailer's app. 
